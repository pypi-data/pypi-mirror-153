import datetime
import logging.handlers
import asyncio
import time
import uuid
import typing
from dataclasses import dataclass, field
from collections import defaultdict
import hbmqtt.client
from hbmqtt.client import ClientException, ConnectException
from hbmqtt.mqtt.constants import QOS_1
import pydantic
from pyaware import events, StopException
from pyaware.mqtt import models, transformations, factories, log_to_file
from pyaware import store
import pyaware.config
import ifaddr

try:
    import rapidjson as json
except ImportError:
    import json

log = logging.getLogger(__file__)


@dataclass(order=True)
class MsgItem:
    priority: int
    topic: str
    topic_type: str
    payload: str
    uid: str
    qos: int
    client: str
    fut: asyncio.Future = field(compare=False)
    from_backlog: bool = False


# Patch the client to handle reconnect logic
class MQTTClient(hbmqtt.client.MQTTClient):
    def __init__(self, client_id=None, config=None, loop=None):
        self._on_connect = None
        self.uri_gen = None
        self.disconnect_after = 0
        self._disconnect_after_task: typing.Optional[asyncio.Future] = None
        self._on_connect_task = None
        self._on_disconnect_task = None
        self.connect_params = {}
        super().__init__(client_id, config, loop)
        self.client_tasks = set()

    @property
    def on_connect(self):
        """If implemented, called when the broker responds to our connection
        request."""
        return self._on_connect

    @on_connect.setter
    def on_connect(self, func):
        """Define the connect callback implementation.

        Expected signature is:
            connect_callback()
        """
        self._on_connect = func

    @property
    def on_disconnect(self):
        """If implemented, called when the broker responds to our connection
        request."""
        return self._on_disconnect

    @on_disconnect.setter
    def on_disconnect(self, func):
        """Define the connect callback implementation.

        Expected signature is:
            connect_callback()
        """
        self._on_disconnect = func

    async def connect(
        self,
        uri=None,
        cleansession=None,
        cafile=None,
        capath=None,
        cadata=None,
        extra_headers=None,
    ):
        if extra_headers is None:
            extra_headers = {}
        self.extra_headers = extra_headers
        self.connect_params = {
            "uri": uri,
            "cleansession": cleansession,
            "cafile": cafile,
            "capath": capath,
            "cadata": cadata,
        }
        try:
            return await self._do_connect()
        except BaseException as be:
            self.logger.warning("Connection failed: %r" % be)
            auto_reconnect = self.config.get("auto_reconnect", False)
            if not auto_reconnect:
                raise
            else:
                return await self.reconnect()

    async def _do_connect(self):
        if self.uri_gen:
            uri = self.uri_gen()
        else:
            uri = self.connect_params["uri"]
        cleansession = self.connect_params["cleansession"]
        cafile = self.connect_params["cafile"]
        capath = self.connect_params["capath"]
        cadata = self.connect_params["cadata"]
        self.session = self._initsession(uri, cleansession, cafile, capath, cadata)
        return_code = await self._connect_coro()
        self._disconnect_task = asyncio.create_task(self.handle_connection_close())
        if self.disconnect_after:

            async def disconnect_later():
                """
                Starts the disconnect procedure after a set number of seconds
                Keeps the handle_connection_close intact so that the reconnect logic still
                works
                :return:
                """
                await asyncio.sleep(self.disconnect_after)
                log.warning("Scheduled mqtt disconnect")
                if self.session.transitions.is_connected():
                    await self._handler.mqtt_disconnect()
                else:
                    self.logger.warning(
                        "Client session is not currently connected, ignoring scheduled disconnect"
                    )

            self._disconnect_after_task = asyncio.create_task(disconnect_later())
        if return_code == 0 and self.on_connect:
            self._on_connect_task = asyncio.create_task(self.on_connect())
        return return_code

    async def handle_connection_close(self):
        def cancel_tasks():
            self._no_more_connections.set()
            while self.client_tasks:
                task = self.client_tasks.pop()
                if not task.done():
                    task.set_exception(ClientException("Connection lost"))

        self.logger.debug("Watch broker disconnection")
        # Wait for disconnection from broker (like connection lost)
        await self._handler.wait_disconnect()
        self.logger.warning("Disconnected from broker")
        if self._disconnect_after_task:
            if not self._disconnect_after_task.done():
                self._disconnect_after_task.cancel()
        if self.on_disconnect:
            self._on_disconnect_task = asyncio.create_task(self.on_disconnect())

        # Block client API
        self._connected_state.clear()

        # stop an clean handler
        self._handler.detach()
        self.session.transitions.disconnect()

        if self.config.get("auto_reconnect", False):
            # Try reconnection
            self.logger.debug("Auto-reconnecting")
            try:
                await self.reconnect()
            except ConnectException:
                # Cancel client pending tasks
                cancel_tasks()
        else:
            # Cancel client pending tasks
            cancel_tasks()

    async def deliver_message(self, timeout=None):
        """
        Deliver next received message.

        Deliver next message received from the broker. If no message is available, this methods waits until next message arrives or ``timeout`` occurs.

        This method is a *coroutine*.

        :param timeout: maximum number of seconds to wait before returning. If timeout is not specified or None, there is no limit to the wait time until next message arrives.
        :return: instance of :class:`hbmqtt.session.ApplicationMessage` containing received message information flow.
        :raises: :class:`asyncio.TimeoutError` if timeout occurs before a message is delivered
        """
        deliver_task = asyncio.create_task(self._handler.mqtt_deliver_next_message())
        self.client_tasks.add(deliver_task)
        self.logger.debug("Waiting message delivery")
        try:
            done, pending = await asyncio.wait(
                [deliver_task],
                loop=self._loop,
                return_when=asyncio.FIRST_EXCEPTION,
                timeout=timeout,
            )
        finally:
            self.client_tasks.discard(deliver_task)
        if deliver_task in done:
            if deliver_task.exception() is not None:
                # deliver_task raised an exception, pass it on to our caller
                raise deliver_task.exception()
            return deliver_task.result()
        else:
            # timeout occurred before message received
            deliver_task.cancel()
            raise asyncio.TimeoutError


@events.enable
class Mqtt:
    """
    Class for setting up google mqtt protocol.
    Assumes that Key Certificates are already generated and the device is created with the associated public key
    """

    def __init__(
        self, config: dataclass, gateway_config: dict = None, _async: bool = False
    ):
        """
        :param config: Config dictionary. Must have at least the device_id specified
        """
        self.config = config
        self.device_topics_setup: asyncio.Event = asyncio.Event()
        self.gateway_config: dict = gateway_config or {}
        self.gateway_config_raw: bytes = b""
        self.gateway_config_received: asyncio.Event = asyncio.Event()
        self.gateway_setup_evt: asyncio.Event = asyncio.Event()
        self.gateway_parse_complete: asyncio.Event = asyncio.Event()
        self.mqtt_promises = {}
        self.cmds_active = set([])
        client_config = {
            "default_qos": self.config.publish_qos,
            "auto_reconnect": True,
            "reconnect_max_interval": 60,
            "reconnect_retries": -1,
            "keep_alive": self.config.keepalive,
        }
        if self.config.serial_number:
            self.status_postfix = "_serial"
        else:
            self.status_postfix = ""
        self.client = MQTTClient(
            self.config.client_id,
            config=client_config,
        )
        self.evt_connected: asyncio.Event = self.client._connected_state
        self.client.uri_gen = self.gen_uri
        if self.config.token_life > 1:
            self.client.disconnect_after = self.config.token_life * 60 - 60
        else:
            self.client.disconnect_after = 0
        self.client.on_connect = self.setup
        self.client.on_disconnect = self.clean_up
        self.topic_loggers = {}
        self.log_messages = True
        self.state_sent = False
        self.sub_handles = {}
        self.sub_topics: typing.List[typing.Tuple[str, int]] = []
        self.gateway_sub_topics: typing.List[typing.Tuple[str, int]] = []
        # Note: Sub topics are divided up into groups of 3 as GCP seems to only take the first 4 subscriptions per message
        self.device_sub_topics: typing.List[typing.List[typing.Tuple[str, int]]] = []
        self.setup_tasks: typing.List[asyncio.Task] = []
        self.active_uids = set([])
        self.message_queues = defaultdict(
            lambda: asyncio.PriorityQueue(self.config.max_message_queue_size)
        )
        self.setup_gateway_topics()

    def start(self):
        asyncio.create_task(self.connect())
        asyncio.create_task(self.loop())

    def start_managers(self):
        if self.config.batch:
            self.message_manager = MessageManagerBatch(
                self.publish,
                self.config.parsers,
                self.evt_connected,
                self.config.max_message_queue_size,
                self.config.batch_hold_off,
            )
        else:
            self.message_manager = MessageManagerSingle(
                self.publish,
                self.config.parsers,
                self.evt_connected,
                self.config.max_message_queue_size,
            )
        asyncio.create_task(self.message_manager.start())
        asyncio.create_task(self.gateway_heartbeat())
        if self.config.backlog_enable:
            self.backlog_manager = BacklogManager(
                self.message_manager.evt_device_setup, self.config.client_id
            )
            asyncio.create_task(self.backlog_manager.start(self.message_manager.add))

    def setup_gateway_topics(self):
        self.gateway_sub_topics = []
        self.sub_handles = [
            (f"config", self.handle_config),
            (f"errors", self.handle_errors),
            (f"commands/system/stop", self.handle_stop),
            (f"commands", self.handle_commands),
        ]
        sub_topics = [
            (
                self.config.parsers["config"]["topic"].format(**self.config),
                1,
            ),
            (
                self.config.parsers["errors"]["topic"].format(**self.config),
                0,
            ),
        ]
        try:
            commands_topic = (
                (
                    self.config.parsers["commands"]["topic"].format(**self.config),
                    0,
                ),
            )
            sub_topics.extend(commands_topic)
        except KeyError as e:
            if self.gateway_parse_complete.is_set():
                message = (
                    "The following parameters are not in connection.yaml: " + e.args[0]
                )
                commands_topic = (
                    (
                        self.config.parsers["commands"]["topic"].format_map(
                            defaultdict(str)
                        ),
                        0,
                    ),
                )
                sub_topics.extend(commands_topic)
                log.warning(
                    f"{message}. Commands topic has not been fully established. Subscribed to {commands_topic}."
                )
        self.gateway_sub_topics.extend(sub_topics)

    def update_gateway_command_topic(self, params: typing.Dict):
        """
        Complete gateway setup if all parameters were not parsed during initial setup.
        """
        self.config.update(**params)
        try:
            commands_topic = (
                (
                    self.config.parsers["commands"]["topic"].format(**self.config),
                    0,
                ),
            )
        except KeyError as e:
            message = (
                "The following parameters are not in connection.yaml: " + e.args[0]
            )
            commands_topic = (
                (
                    self.config.parsers["commands"]["topic"].format_map(
                        defaultdict(str)
                    ),
                    0,
                ),
            )
            log.warning(
                f"{message}. Commands topic has not been fully established. Subscribed to {commands_topic}."
            )
        self.gateway_sub_topics.extend(commands_topic)
        self.gateway_parse_complete.set()

    def setup_device_topics(self):
        self.device_sub_topics = []
        # Note: Sub topics are divided up into groups of 3 as GCP seems to only take the first 4 subscriptions per message
        for dev_id in self.gateway_config.get("devices", []):
            dev_config = {**self.config, **{"device_id": dev_id}}
            sub_topics = [
                (
                    self.config.parsers["config"]["topic"].format(**dev_config),
                    1,
                ),
                (
                    self.config.parsers["errors"]["topic"].format(**dev_config),
                    0,
                ),
                (
                    self.config.parsers["commands"]["topic"].format(**dev_config),
                    0,
                ),
            ]
            self.device_sub_topics.append(sub_topics)
        self.device_topics_setup.set()

    async def setup(self):
        self.gateway_setup_evt.clear()
        while True:
            if pyaware.evt_stop.is_set():
                raise StopException("Pyaware is stopped")
            try:
                # Begins setting up mqtt subscriptions and publishes
                await self.gateway_setup()
                log.info(f"Setup gateway mqtt {self.config.device_id}")
                break
            except (asyncio.CancelledError, StopException, GeneratorExit):
                raise
            except BaseException as e:
                log.exception(e)
            await self.clean_up_setup_tasks()
            await asyncio.sleep(1)

    async def gateway_setup(self):
        """
        Get config if it exists. Then set up attached devices from the config
        Note: Sub topics are divided up into groups of 3 as GCP seems to only take the first 4 subscriptions per message
        :return:
        """
        # Setup gateway heartbeat independent of gateway.yaml
        await self.gateway_parse_complete.wait()
        await self.client.subscribe(self.gateway_sub_topics)
        log.info(f"Listening to mqtt topics {self.gateway_sub_topics}")
        self.sub_topics.extend(self.gateway_sub_topics)
        self.gateway_setup_evt.set()
        self.setup_tasks.append(asyncio.create_task(self.device_setup()))

    async def device_setup(self):
        await self.device_topics_setup.wait()
        log.info("Setting up mqtt devices")
        try:
            device_attaches = [
                self.publish(
                    self.config.parsers["attach"]["topic"].format(device_id=device_id),
                    json.dumps({"authorization": ""}),
                    qos=QOS_1,
                )
                for device_id in self.gateway_config.get("devices", [])
            ]
            await asyncio.gather(*device_attaches)
        except KeyError:
            pass

        for device_topic_group in self.device_sub_topics:
            await self.client.subscribe(device_topic_group)
            log.info(f"Listening to device mqtt topics {device_topic_group}")
        self.message_manager.evt_device_setup.set()

    async def gateway_heartbeat(self):
        log.info("Starting Gateway Heartbeat")
        connections_save_state = []
        # Get all adapter static info and setup array
        adapter_info = [
            {
                "macAddress": await pyaware.config.get_mac_address(adapter.name),
                "adapter": adapter.name,
            }
            for adapter in ifaddr.get_adapters()
        ]
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing gateway heartbeat")
                return
            try:
                connections = []
                # Collects network adapters, ip addresses and mac addresses
                for adapter in ifaddr.get_adapters():
                    for ip_address in adapter.ips:
                        if ip_address.is_IPv4:
                            connections = connections + [
                                {
                                    "adapter": ip_address.nice_name,
                                    "macAddress": info.get("macAddress"),
                                    "ipAddress": ip_address.ip,
                                }
                                for info in adapter_info
                                if adapter.name == info.get("adapter")
                            ]
                timestamp = datetime.datetime.now()
                data = {"network": connections, "timestamp": timestamp}
                # Send gateway heartbeat to mqtt
                events.publish(
                    f"trigger_send",
                    data=data,
                    timestamp=timestamp,
                    topic_type="gateway",
                )
                if connections != connections_save_state or not self.state_sent:
                    # Update the state of the gateway
                    asyncio.create_task(self.update_gateway_state(data))
                    connections_save_state = connections
                    self.state_sent = True
            except Exception as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)
            try:
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("Gateway heartbeat cancelled without stop signal")
                    break

    async def update_gateway_state(self, data: dict):
        log.info("Gateway state change detected. Sending new state.")
        timestamp = datetime.datetime.now()
        state = {"network": data.get("network", {}), "timestamp": timestamp}
        events.publish(
            f"trigger_send",
            topic_type="state",
            data=state,
            timestamp=datetime.datetime.utcnow(),
        )
        # Update the gateway network topology
        await self.gateway_parse_complete.wait()
        events.publish(f"update_gateway_network/{id(self)}", data=data["network"])

    async def clean_up_setup_tasks(self):
        # Cancels all possible running setup tasks
        log.info("Cleaning up MQTT setup tasks")
        cancelled_tasks = []
        self.state_sent = False
        while self.setup_tasks:
            task = self.setup_tasks.pop()
            if not task.done():
                cancelled_tasks.append(task)
                task.cancel()
        # Ensures all running setup tasks are completed before starting new ones
        # Returns the cancelled exceptions so they are suppressed
        results = await asyncio.gather(*cancelled_tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, BaseException):
                log.error("Error cancelling MQTT setup tasks", exc_info=result)

    async def clean_up(self):
        await self.clean_up_setup_tasks()
        self.message_manager.clear()

    async def connect(self):
        if self.config.authentication_required:
            await self.client.connect(
                uri=None,
                cleansession=self.config.clean_session,
                cafile=self.config.ca_certs_path,
            )
        else:
            await self.client.connect(
                uri=f"mqtt://{self.config.host}:{self.config.port}",
                cleansession=self.config.clean_session,
            )

    def gen_uri(self):
        if self.config.authentication_required:
            return f"mqtts://unused:{self.config.jwt_token.decode('utf-8')}@{self.config.host}:{self.config.port}"
        else:
            return f"mqtt://{self.config.host}:{self.config.port}"

    async def loop(self):
        while True:
            if pyaware.evt_stop.is_set():
                log.info(
                    f"Stopping event loop for hbmqtt client {self.config.device_id}"
                )
                break
            try:
                msg = await self.client.deliver_message(timeout=1)
            except asyncio.TimeoutError:
                continue
            except (AttributeError, IndexError):
                await asyncio.sleep(1)
                continue
            except asyncio.CancelledError:
                raise
            except Exception as e:
                log.exception(e)
                continue
            log.info("Message Received")
            asyncio.create_task(self.sub_handler(msg))

    async def sub_handler(self, msg):
        for handle_str, handle in self.sub_handles:
            if handle_str in msg.topic:
                try:
                    if handle is not None:
                        await pyaware.async_wrap(handle(msg))
                        break
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    log.exception(e)

    @events.subscribe(topic=f"trigger_send")
    async def send(self, *, data: dict, topic_type: str, **kwargs):
        if topic_type not in self.config.parsers:
            return
        uid = str(uuid.uuid4())
        delay = 2 + self.config.batch_hold_off
        params = {**self.config, **kwargs}
        try:
            payload, topic = self.form_message(
                data=data, topic_type=topic_type, **params
            )
        except Exception as e:
            log.exception(e)
            log.warning(
                f"Failed to form message for data: {data}, topic_type: {topic_type}, params: {params}"
            )
            return
        if self.config.parsers.get(topic_type, {}).get("cache", True):
            # Wait for database to be initialised before attempting to cache
            await store.disk_storage_setup_evt.wait()
            fut = store.disk_storage.mqtt.insert_delayed(
                topic=topic,
                payload=payload,
                qos=self.config.publish_qos,
                uid=uid,
                delay=delay,
                client=self.config.client_id,
                topic_type=topic_type,
            )
        else:
            fut = asyncio.Future()
            fut.set_result(None)
        try:
            await asyncio.wait_for(
                self.message_manager.add(
                    topic=topic,
                    topic_type=topic_type,
                    payload=payload,
                    uid=uid,
                    qos=self.config.publish_qos,
                    fut=fut,
                    priority=0,
                    client=self.config.client_id,
                ),
                20,
            )
        except asyncio.TimeoutError:
            fut.cancel()
            return

    async def publish(self, topic, payload, qos, retain: bool = False):
        """
        Publish a message to the mqtt broker
        This will first queue up a store the message cache on a delay of 2 seconds. If the message isn't acknowledged
        within 2 seconds, then the message will be stored in cache.
        If the message is finally acknowledged then the cache will have the message marked as ack'd.
        :param topic:
        :param payload:
        :param qos:
        :return:
        """
        try:
            payload = payload.encode()
        except AttributeError:
            pass
        await self.client.publish(topic, payload, qos, retain=retain)

    def form_message(
        self, data: dict, topic_type: str, **kwargs
    ) -> typing.Tuple[str, str]:
        parsers = self.config.parsers.get(topic_type, {})
        factory = factories.get_factory(parsers.get("factory"))
        msg = factory(data=data, **kwargs)
        for transform in parsers.get("transforms", []):
            msg = transformations.get_transform(**transform)(msg)
        msg = models.model_to_json(parsers.get("model", {}), msg)
        topic = parsers.get("topic", "")
        topic = topic.format(**kwargs)
        if "{" in topic:
            raise ValueError(f"Missing parameters in topic string {topic}")
        return msg, topic

    def mqtt_log(self, topic, payload, mid, resolved=False):
        if log_to_file:
            try:
                mqtt_log = self.topic_loggers[topic]
            except KeyError:
                mqtt_log = logging.getLogger(topic)
                mqtt_log.setLevel(logging.INFO)
                log_dir = pyaware.config.aware_path / "mqtt_log"
                log_dir.mkdir(parents=True, exist_ok=True)
                formatter = logging.Formatter("%(asctime)-15s %(message)s")
                handler = logging.handlers.TimedRotatingFileHandler(
                    log_dir / f"{topic.replace('/', '_')}.log", "h", backupCount=2
                )
                handler.setFormatter(formatter)
                mqtt_log.addHandler(handler)
                mqtt_log.propagate = False
                self.topic_loggers[topic] = mqtt_log
            if resolved:
                mqtt_log.info(f"Resolved {self.config.host} {mid}")
                return
            mqtt_log.info(f"Publishing {self.config.host} {mid}:\n{payload}")

    async def subscribe(self, topic, callback, qos):
        await self.client.subscribe([(topic, qos)])
        self.sub_handles[topic] = callback

    async def unsubscribe(self, topic):
        if self.client._connected_state.is_set():
            await self.client.unsubscribe([topic])
            self.sub_handles.pop(topic, None)

    def handle_config(self, msg):
        """
        Callback when a new configuration is sent via mqtt.
        If the
        If the gateway handle config to update devices and set up remaining pyaware config
        :return:
        """
        # Ensures the devices configuration received is the gateway not a child device
        gateway_config_topic = self.config.parsers["config"]["topic"].format(
            **self.config
        )
        if msg.topic == gateway_config_topic:
            """
            Check if new config is different to the old config
            If so, override config cache present
            """
            log.info("Gateway config received: {}".format(msg.data))
            if msg.data:
                try:
                    old_config = pyaware.config.load_file_raw(
                        pyaware.config.config_main_path
                    )
                except OSError:
                    old_config = b""
                if msg.data != old_config:
                    log.info(
                        "New gateway configuration detected. Replacing existing gateway.yaml."
                    )
                    pyaware.config.save_config_raw(
                        pyaware.config.config_main_path, msg.data
                    )
                    if self.gateway_config_received.is_set():
                        log.warning(
                            "New gateway configuration detected. Stopping process"
                        )
                        pyaware.stop()
                if not self.gateway_config_received.is_set():
                    self.gateway_config_raw = msg.data
                    self.gateway_config = pyaware.config.yaml_load(msg.data)
                    self.gateway_config_received.set()
            else:
                log.info("Gateway configuration received was empty")
                self.gateway_config_received.set()
        else:
            log.info(f"Device config {msg.topic} received: {msg.data}")

    def load_config_from_disk(self):
        try:
            self.gateway_config_raw = pyaware.config.load_file_raw(
                pyaware.config.config_main_path
            )
            self.gateway_config = pyaware.config.yaml_load(self.gateway_config_raw)
            self.gateway_config_received.set()
        except FileNotFoundError:
            log.warning("No valid gateway configuration detected. Stopping process")
            pyaware.stop()

    def handle_errors(self, mid):
        try:
            log.warning(f"Error received from gcp\n{mid.data.decode('utf-8')}")
        except:
            log.warning(f"Error received from gcp\n{mid.data}")

    def handle_commands(self, mid):
        # TODO any error should send back a CommandResponse Object with undefined error

        parsers = self.config.parsers.get("commands", {})
        try:
            dev_id_index = parsers["topic"].split("/").index("{device_id}")
        except ValueError:
            log.info(f"Command topic {parsers['topic']} did not have device_id preset")
            raise
        try:
            dev_id = mid.topic.split("/")[dev_id_index]
        except IndexError:
            log.info(
                f"Command topic received did not have a valid device_id {mid.topic}, forwarding to gateway"
            )
            dev_id = self.config.device_id
        try:
            msg = models.model_to_dict(parsers.get("model", {}), mid.data)
        except AttributeError:
            # Ignore commands with no payload
            return
        except json.JSONDecodeError as e:
            log.error(repr(e))
            return
        except pydantic.ValidationError as e:
            log.error(repr(e))
            invalid_message = json.loads(mid.data)
            resp = {
                "id": invalid_message["id"],
                "type": 3,
                "timestamp": datetime.datetime.utcnow(),
                "message": e.json(),
            }
            events.publish(
                "mqtt_command_response",
                data=resp,
                timestamp=datetime.datetime.utcnow(),
                device_id=dev_id,
            )
            return

        self.cmds_active.add(msg["id"])
        pyaware.events.publish(
            f"mqtt_command/{dev_id}",
            data=msg,
            timestamp=datetime.datetime.utcnow(),
        )

    def handle_stop(self, mid):
        pyaware.stop()

    # TODO this needs to have a instance ID as any more than one MQTT device will break here (eg. 2 imacs)
    @events.subscribe(topic=f"mqtt_command_response")
    async def publish_command_response(
        self, data: dict, timestamp: datetime.datetime, device_id: str
    ):
        await self.send(
            data=data,
            topic_type="command_response",
            topic=f"trigger_send",
            timestamp=timestamp,
            device_id=device_id,
        )
        if data["type"] > 1:
            self.cmds_active.discard(data["id"])


class MessageManager:
    def __init__(
        self,
        publish_cbf: typing.Callable,
        topic_parser: dict,
        evt_connected: asyncio.Event,
        max_queue_size: int = 0,
        max_in_flight_messages: int = 50,
    ):
        self.evt_device_setup = asyncio.Event()
        self.evt_connected = evt_connected
        self.publish = publish_cbf
        self.parser = topic_parser
        self.max_queue_size = max_queue_size
        self.in_flight: dict = {}
        self.sem_in_flight = asyncio.BoundedSemaphore(max_in_flight_messages)
        self.max_in_flight_messages = max_in_flight_messages

    async def handle_publish_flow(
        self,
        topic,
        topic_type,
        payload,
        qos: int,
        futs: typing.List[typing.Tuple[str, asyncio.Future]],
    ):
        """
        Handles the publish flow for storing the
        :param topic:
        :param payload:
        :param qos:
        :param futs: Contains the uid, future pairing to mark a message as complete.
        The fut is an asyncio.Future which is the task that commits the mqtt message to disk after a set time.
        As messages can be batches, they can contain multiple uids for a single message send.
        The database commit futures are cancelled if the message is successfully received by the broker before being
        committed to the database
        :param sem: A semaphore that needs to be released when the message has finished processing either by success or
        error
        :return:
        """
        try:
            await self.evt_connected.wait()
            # If the message can be sent without device topics then send immediately. Else wait for 60s.
            # This is as a result of gateway config parsing.
            if self.parser.get(topic_type, {}).get("device_message", True):
                await asyncio.wait_for(self.evt_device_setup.wait(), 60)
            retain = self.parser.get(topic_type, {}).get("retain", False)
            await asyncio.wait_for(
                self.publish(topic, payload, qos=qos, retain=retain),
                10,
            )
            for uid, fut in futs:
                if fut.done():
                    await store.disk_storage_setup_evt.wait()
                    asyncio.create_task(store.disk_storage.mqtt.ack(uid))
                else:
                    fut.cancel()
        except (asyncio.TimeoutError, asyncio.CancelledError):
            pass
        finally:
            for uid, fut in futs:
                self.in_flight.pop(uid, None)
            self.sem_in_flight.release()

    def clear(self):
        log.info("Cleaning up in flight messages")
        self.evt_device_setup.clear()
        for task in set(self.in_flight.values()):
            try:
                task.cancel()
            except AttributeError:
                continue

    async def add(
        self,
        topic: str,
        topic_type: str,
        payload: str,
        uid: str,
        qos: int,
        fut: asyncio.Future,
        client: str,
        priority: int = 0,
    ):
        raise NotImplementedError

    async def start(self):
        raise NotImplementedError


class MessageManagerBatch(MessageManager):
    def __init__(
        self,
        publish_cbf: typing.Callable,
        topic_parser: dict,
        evt_connected: asyncio.Event,
        max_queue_size: int = 0,
        batch_hold_off: float = 0,
        max_in_flight_messages: int = 50,
    ):
        super().__init__(
            publish_cbf,
            topic_parser,
            evt_connected,
            max_queue_size,
            max_in_flight_messages,
        )
        self.batch_hold_off = batch_hold_off
        self.queues = {}

    def start_new_topic(self, topic: str, topic_type: str):
        self.queues[topic] = asyncio.PriorityQueue(self.max_queue_size)
        batchable = self.parser.get(topic_type, {}).get("batchable", False)
        batchable_backlog = self.parser.get(topic_type, {}).get(
            "batchable_backlog", batchable
        )
        if batchable:
            asyncio.create_task(self._start(self.queues[topic]))
        else:
            asyncio.create_task(self._start_non_batch(self.queues[topic]))
        if batchable_backlog and not batchable:
            self.queues[f"{topic}_backlog"] = asyncio.PriorityQueue(self.max_queue_size)
            asyncio.create_task(self._start(self.queues[f"{topic}_backlog"]))
        else:
            self.queues[f"{topic}_backlog"] = self.queues[topic]

    async def add(
        self,
        topic: str,
        topic_type: str,
        payload: str,
        uid: str,
        qos: int,
        fut: asyncio.Future,
        client: str,
        priority: int = 0,
        from_backlog: bool = False,
    ):
        if uid in self.in_flight:
            return
        self.in_flight[uid] = None
        if topic not in self.queues:
            self.start_new_topic(topic, topic_type)

        if from_backlog:
            new_topic = f"{topic}_backlog"
        else:
            new_topic = topic
        await self.queues[new_topic].put(
            MsgItem(
                priority=priority,
                topic=topic,
                topic_type=topic_type,
                payload=payload,
                uid=uid,
                qos=qos,
                fut=fut,
                client=client,
                from_backlog=from_backlog,
            )
        )

    async def start(self):
        """
        This function doesn't need to be called because there is a task for each queue created on a new topic addition
        in the add method
        :return:
        """

    async def _start_non_batch(self, q):
        while True:
            msg = await q.get()
            await self.sem_in_flight.acquire()
            self.in_flight[msg.uid] = asyncio.create_task(
                self.handle_publish_flow(
                    msg.topic,
                    msg.topic_type,
                    msg.payload,
                    msg.qos,
                    [(msg.uid, msg.fut)],
                )
            )
            q.task_done()

    async def _start(self, q):
        """
        Group messages by topic
        Uses the publish qos by default
        :return:
        """
        start = time.time()
        while True:
            msg = await self._pull_from_queue(q)
            if msg:
                await self.sem_in_flight.acquire()
                task = asyncio.create_task(self.handle_publish_flow(**msg))
                for uid, fut in msg["futs"]:
                    self.in_flight[uid] = task
                    q.task_done()
                sleep_time = 0.1
                start = time.time()
            else:
                sleep_time = time.time() - start + self.batch_hold_off
                start = time.time()
                if sleep_time < 0.1:
                    sleep_time = 0.1
            await asyncio.sleep(sleep_time)

    async def _pull_from_queue(self, q) -> dict:
        payloads = []
        futs = []
        max_qos = 0
        msg = None
        while True:
            try:
                msg = q.get_nowait()
                payloads.append(msg.payload)
                futs.append((msg.uid, msg.fut))
                max_qos = max(max_qos, msg.qos)
            except asyncio.QueueEmpty:
                break
        if not msg:
            return {}
        return {
            "topic": msg.topic,
            "topic_type": msg.topic_type,
            "payload": f"[{','.join(payloads)}]",
            "qos": max_qos,
            "futs": futs,
        }


class MessageManagerSingle(MessageManager):
    def __init__(
        self,
        publish_cbf: typing.Callable,
        topic_parser: dict,
        evt_connected: asyncio.Event,
        max_queue_size: int = 0,
        max_in_flight_messages: int = 50,
    ):
        super().__init__(
            publish_cbf,
            topic_parser,
            evt_connected,
            max_queue_size,
            max_in_flight_messages,
        )
        self.q = asyncio.PriorityQueue(max_queue_size)

    async def add(
        self,
        topic: str,
        topic_type: str,
        payload: str,
        uid: str,
        qos: int,
        fut,
        client: str,
        priority: int = 0,
        from_backlog: bool = False,
    ):
        if uid in self.in_flight:
            return
        self.in_flight[uid] = None
        await self.q.put(
            MsgItem(
                priority=priority,
                topic=topic,
                topic_type=topic_type,
                payload=payload,
                uid=uid,
                qos=qos,
                fut=fut,
                client=client,
                from_backlog=from_backlog,
            )
        )

    async def start(self):
        while True:
            msg = await self.q.get()
            await self.sem_in_flight.acquire()
            self.in_flight[msg.uid] = asyncio.create_task(
                self.handle_publish_flow(
                    msg.topic,
                    msg.topic_type,
                    msg.payload,
                    msg.qos,
                    [(msg.uid, msg.fut)],
                )
            )
            self.q.task_done()


class BacklogManager:
    def __init__(self, evt_device_setup: asyncio.Event, client: str):
        self.evt_device_setup = evt_device_setup
        self.client = client

    async def start(
        self,
        a_callback: typing.Union[MessageManagerBatch.add, MessageManagerSingle.add],
    ):
        """
        Continually add messages the the queue from the disk storage if they are not currently in flight
        :param a_callback: Callback to the message manager.
        Will block adding messages if the manager queue is full
        :return:
        """
        await store.disk_storage_setup_evt.wait()
        log.info(f"Starting mqtt backlog")
        while True:
            start = None
            if pyaware.evt_stop.is_set():
                log.info("Shutting down mqtt backlog manager")
                return
            msg_cnt = 0
            try:
                async for row in store.disk_storage.mqtt.get_all_unsent(
                    self.client, 1000
                ):
                    if start is None:
                        start = time.time()
                    await self.evt_device_setup.wait()
                    fut = asyncio.Future()
                    # Indicate that the data is already committed to disk
                    fut.set_result(None)
                    await a_callback(**row, fut=fut, priority=1, from_backlog=True)
                    msg_cnt += 1
                if msg_cnt > 0:
                    log.info(
                        f"Finished adding mqtt backlog for {msg_cnt} in {time.time() - start}s"
                    )
            except asyncio.CancelledError:
                if pyaware.evt_stop.is_set():
                    log.info("Shutting down mqtt backlog manager")
                    return
            except asyncio.InvalidStateError:
                log.info(
                    "aiosqlite race condition error see https://github.com/omnilib/aiosqlite/issues/80"
                )
            except BaseException as e:
                log.error(repr(e))
            await asyncio.sleep(60)
