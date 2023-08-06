__version__ = "4.7.0"

import functools
import inspect
import logging
import argparse
import signal
import platform
import os
import sys
import asyncio
from pathlib import Path
from pyaware.maintenance import do_updates, scheduled_restart
from pyaware import events
from pyaware.exceptions import StopException
from pyaware.store.disk import init_db
import pyaware.config

try:
    import rapidjson as json
except ImportError:
    import json

parser = argparse.ArgumentParser(
    description="Sets up a minimal pyaware slave for imac to respond to mqtt commands"
)
parser.add_argument(
    "path", help="Path to the pyaware path that houses config and credentials"
)
parser.add_argument(
    "--profile", help="Runs the profiler and outputs to 'path'", type=int
)
parser.add_argument(
    "--mem_profile", help="Runs the profiler and outputs to 'path'", type=int
)

log = logging.getLogger()
_parent_process = os.getpid()
evt_stop = events.evt_stop


async def stop_in(timeout: int):
    """Stops pyAWARE in the timeout specified in seconds."""
    await asyncio.sleep(timeout)
    pyaware.stop()


def stop():
    if evt_stop.is_set():
        raise StopException("Pyaware is stopped")
    evt_stop.set()
    os.kill(_parent_process, signal.SIGINT)
    raise StopException("Pyaware is stopped")


async def shutdown(signal, comms, loop):
    """Cleanup tasks tied to the service's shutdown."""
    global _stopping
    try:
        log.info(f"Received exit signal {signal.name}...")
        log.info(f"Stopping internal events")
        events.stop()
        log.info("Closing comms connections")
        for name, instance in comms.items():
            if name == "local_broker":
                log.info("Disconnecting MQTT local broker")
                try:
                    instance.disconnect()
                except BaseException as e:
                    log.exception(e)
            if name == "serial":
                log.info("Disconnecting Master Serial Modbus")
                try:
                    instance.disconnect()
                except BaseException as e:
                    log.exception(e)
            if name == "ethernet":
                log.info("Disconnecting Master Ethernet Modbus")
                try:
                    instance.disconnect()
                except BaseException as e:
                    log.exception(e)

        try:
            log.info("Closing database connection")
            await asyncio.wait_for(pyaware.store.disk_storage.close(), 3)
        except AttributeError:
            pass
        except BaseException as e:
            log.exception(e)
        log.info("Cancelling outstanding tasks")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

        [task.cancel() for task in tasks]

        log.info(f"Cancelling {len(tasks)} outstanding tasks")
        if tasks:
            done, pending = await asyncio.wait(
                tasks, timeout=5, return_when=asyncio.ALL_COMPLETED
            )
            if pending:
                log.info(f"Force stopping event loop but tasks still remain {tasks}")
            else:
                log.info(f"All tasks stopped. Stopping event loop")
        loop.stop()
    finally:
        _stopping = False


async def _main(comms):
    events.start()
    try:
        import pyaware.config

        # Establish logging
        logging_config()

        # Attempt to establish MQTT comms
        connection_config = pyaware.config.load_connection_config()
        # If the connection config is empty raise this so that the user provides a valid connection config
        if connection_config is None:
            raise TypeError(
                "Connection config file is empty. Please provide a connection config with valid configuration."
            )
        connection_feature_flags = connection_config.pop("feature_flags", {})
        if connection_feature_flags and not connection_feature_flags.pop(
            "feature_mqtt", True
        ):
            log.warning(
                "MQTT disabled for this instance of PyAWARE ... aborting MQTT setup"
            )
            mqtt_client = None
            deferred_params = None
        else:
            # Establish MQTT client
            params, deferred_params = await pyaware.config.parse_comm_params(
                {"params": connection_config}, {}
            )
            is_deferred_params = bool(deferred_params)
            mqtt_client = await pyaware.config.parse_mqtt(params, is_deferred_params)
        try:
            do_updates()
        except StopException:
            raise
        except Exception as e:
            log.exception(e)
            log.info("Failed to do pyaware updates. Proceeding to start pyaware")

        config = pyaware.config.load_yaml_config(pyaware.config.config_main_path)
        try:
            restart_hour = config["scheduled_restart"]

            scheduled_restart(**restart_hour)
        except KeyError:
            pass
        except asyncio.CancelledError:
            raise
        except Exception as e:
            log.exception(e)

        await init_db(**config.get("database", {"max_size": "500MB", "memory": True}))
        comms.update(
            await pyaware.config.parse_communication(
                communication=config["communication"]
            )
        )
        for comm in comms.values():
            try:
                init = comm.init
            except AttributeError:
                continue
            init()
        if mqtt_client and deferred_params:
            params, invalid_params = await pyaware.config.parse_comm_params(
                {"params": deferred_params}, comms
            )
            # If the gateway parsing is not complete for the mqtt client then complete the parsing here with
            # information from gateway.yaml
            mqtt_client.update_gateway_command_topic(params)
            if invalid_params:
                log.error(f"Unable to evaluate connection params {invalid_params}")
        if mqtt_client:
            mqtt_client.setup_device_topics()
    except StopException as e:
        pass
    except BaseException as e:
        log.exception(e)
        pyaware.stop()


def logging_config(level=logging.INFO, to_stdout=True, to_file=True, mqtt_log=True):
    import logging.handlers
    import pyaware.config

    log = logging.getLogger()
    logname = os.path.join(pyaware.config.aware_path, "AWARE.log")
    formatter = logging.Formatter(
        "%(asctime)-15s %(threadName)-15s "
        "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
    )
    if to_file:
        handler = logging.handlers.TimedRotatingFileHandler(
            logname, when="midnight", backupCount=7
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)

    if to_stdout:
        screen_handler = logging.StreamHandler(sys.stdout)
        screen_handler.setFormatter(formatter)
        log.addHandler(screen_handler)
    log.setLevel(level=level)
    import pyaware.mqtt

    pyaware.mqtt.log_to_file = mqtt_log


def main():
    import pyaware.config

    args = parser.parse_args()
    comms = {}
    loop = asyncio.get_event_loop()
    pyaware.config.aware_path = Path(args.path)
    pyaware.config.config_main_path = (
        pyaware.config.aware_path / "config" / "gateway.yaml"
    )
    if platform.system() == "Windows":
        signals = (signal.SIGTERM, signal.SIGINT)
        for sig in signals:
            signal.signal(
                sig, lambda s=sig: asyncio.create_task(pyaware.shutdown(s, comms, loop))
            )
        loop.set_exception_handler(
            lambda: asyncio.create_task(pyaware.shutdown(signal.SIGINT, comms, loop))
        )
    else:
        # May want to catch other signals too
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for sig in signals:
            loop.add_signal_handler(
                sig, lambda s=sig: asyncio.create_task(pyaware.shutdown(s, comms, loop))
            )
    if args.profile:
        import pyaware.profiler

        pyaware.profiler.start()
        loop.create_task(pyaware.profiler.profile_loop(args.profile))
    if args.mem_profile:
        import pyaware.profiler

        mem = pyaware.profiler.MemProfile()
        mem.start()
        loop.create_task(mem.loop(args.mem_profile))
    try:
        loop.create_task(_main(comms))
        loop.run_forever()
    finally:
        loop.close()
        log.info("Successfully shutdown")


def async_threaded(f):
    """
    Wraps a function so that when it is called from an asyncio event loop, it runs in a threadpool executor instead
    :param f:
    :return:
    """

    @functools.wraps(f)
    def _wrapped(*args, **kwargs):
        func = functools.partial(f, *args, **kwargs)
        if from_coroutine():
            return asyncio.get_running_loop().run_in_executor(None, func)
        else:
            return func()

    return _wrapped


async def async_wrap(resp):
    if inspect.isawaitable(resp):
        return await resp
    return resp


async def async_call(handle, *args, **kwargs):
    return await async_wrap(handle(*args, **kwargs))


def from_coroutine():
    """
    Checks if function is in an event loop. If so, then blocking code should not be used
    :return:
    """
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False
