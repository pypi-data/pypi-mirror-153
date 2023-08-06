import asyncio
import yappi
import tracemalloc
import datetime
import threading
import pyaware.config
import logging
import os

profile_lock = threading.Lock()
log = logging.getLogger(__name__)
profile_path = pyaware.config.aware_path / "profiling"
try:
    profile_path.mkdir()
except FileExistsError:
    pass


def start():
    yappi.start()


def profile_dump():
    with profile_lock:
        yappi.stop()
        stats = yappi.get_func_stats()
        pstats = yappi.convert2pstats(stats)
        dump = pstats.dump_stats(
            profile_path
            / f"profiler_{datetime.datetime.utcnow().isoformat().replace('-', '_').replace(':', '_')}.pstat"
        )
        yappi.clear_stats()
        logging.info(f"Dumped profile data")
        yappi.start()


async def profile_loop(interval):
    while True:
        await asyncio.sleep(interval)
        try:
            await asyncio.get_event_loop().run_in_executor(None, profile_dump)
        except asyncio.CancelledError:
            raise
        except BaseException as e:
            logging.exception(e)


class MemProfile:
    def __init__(self):
        self.last_snapshot = None

    def start(self):
        tracemalloc.start()

    async def loop(self, interval):
        while True:
            await asyncio.sleep(interval)
            try:
                await asyncio.get_event_loop().run_in_executor(None, self.dump)
            except asyncio.CancelledError:
                raise
            except BaseException as e:
                logging.exception(e)

    def dump(self):
        snapshot = tracemalloc.take_snapshot()
        snapshot = snapshot.filter_traces(
            (
                tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
                tracemalloc.Filter(False, "<unknown>"),
            )
        )
        log.info("memory profile snapshotted")
        stats = snapshot.statistics("lineno")
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        with open(profile_path / f"{now}-mem.log", "w") as f:
            f.write(os.linesep.join([str(x) for x in stats[:50]]))
        if self.last_snapshot is not None:
            stats = snapshot.compare_to(self.last_snapshot, "lineno")
            with open(profile_path / f"{now}-mem-diff.log", "w") as f:
                f.write(os.linesep.join([str(x) for x in stats[:50]]))
            stats = snapshot.compare_to(self.last_snapshot, "traceback")
            with open(profile_path / f"{now}-mem-tb.log", "w") as f:
                for stat in stats[:50]:
                    f.write(
                        "\n%s memory blocks: %.1f KiB\n"
                        % (stat.count, stat.size / 1024)
                    )
                    f.write(os.linesep.join([x for x in stat.traceback.format()]))
        self.last_snapshot = snapshot
