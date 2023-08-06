from __future__ import annotations
import asyncio
import logging
import inspect
from functools import wraps
from dataclasses import dataclass, field
import typing
import time
import pyaware

log = logging.getLogger(__file__)


class AggregatedEvent(asyncio.Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.evts: typing.List[asyncio.Event] = []

    def clear(self):
        pass

    def set(self):
        pass

    async def wait(self):
        raise NotImplementedError


class AggregateEventAny(AggregatedEvent):
    def is_set(self) -> bool:
        return any(evt.is_set() for evt in self.evts)


class AggregateEventAll(AggregatedEvent):
    def is_set(self) -> bool:
        return all(evt.is_set() for evt in self.evts)


_watchdogs = {}


@dataclass
class WatchDog:
    """
    A watchdog class that will wait for the feedback_time before checking if it is fed. If fed it will call success_cbf
    otherwise it will call failure_cbf

    Watchdog that will call a function
    """

    heartbeat_time: typing.Union[int, float]
    success_cbf: typing.Callable = field(
        default_factory=lambda: lambda: None
    )  # Default return callable that no ops
    failure_cbf: typing.Callable = field(
        default_factory=lambda: lambda: None
    )  # Default return callable that no ops
    task: typing.Optional[asyncio.Task] = None

    def __post_init__(self):
        self._last_fed: float = time.time()
        self._fed: asyncio.Event = asyncio.Event()
        self._fed_bool: bool = False
        self._starved: asyncio.Event = asyncio.Event()
        self._waiter = None

    @property
    def waiter(self):
        return self._waiter

    @waiter.setter
    def waiter(self, value: asyncio.Event):
        self._waiter = value

    @property
    def fed(self):
        return self._fed_bool

    @property
    def time_to_starve(self):
        tm = self.heartbeat_time + self._last_fed - time.time()
        if tm < 0:
            tm = self.heartbeat_time
        return tm

    def feed(self):
        # print(f"Feeding {self.__class__.__name__}:{self.heartbeat_time}")
        self._last_fed = time.time()
        self._starved.clear()
        self._fed_bool = True
        self._fed.set()
        self.waiter = self._starved

    def starve(self):
        # print(f"Starving {self.__class__.__name__}:{self.heartbeat_time}")
        self._fed.clear()
        self._fed_bool = False
        self.waiter = self._fed
        self._starved.set()

    def start(self, start_fed: bool = False):
        if self.task is not None and not self.task.cancelled() and not self.task.done():
            return
        if start_fed:
            self.waiter = self._starved
            self.feed()
        else:
            self.waiter = self._fed
            self._starved.set()
        if self.task:
            self.task.cancel()
        self.task = asyncio.create_task(self._start())

    async def wait(self):
        return await self.waiter.wait()

    async def _start(self):
        while True:
            try:
                if self.fed:
                    self._fed_bool = True
                    self._fed.clear()
                    self._starved.clear()
                    self.waiter = self._starved
                    await pyaware.async_wrap(self.success_cbf())
                    first_sleep = self.time_to_starve
                    second_sleep = self.heartbeat_time - first_sleep
                    try:
                        # print(f"First sleep {self.__class__.__name__}:{self.heartbeat_time}")
                        await asyncio.wait_for(self.wait(), first_sleep)
                    except asyncio.TimeoutError:
                        if not self._fed.is_set():
                            self._fed_bool = False
                            continue
                    # print(f"Second sleep {self.__class__.__name__}:{self.heartbeat_time}")
                    await asyncio.wait_for(self.wait(), second_sleep)
                else:
                    self._fed_bool = False
                    self._starved.set()
                    self._fed.clear()
                    await pyaware.async_wrap(self.failure_cbf())
                    self.waiter = self._fed
                    # print(f"Starved wait {self.__class__.__name__}:{self.heartbeat_time}")
                    await asyncio.wait_for(self.wait(), self.heartbeat_time)
            except (asyncio.CancelledError, pyaware.StopException):
                return
            except asyncio.TimeoutError:
                pass
            except BaseException as e:
                log.error(repr(e))

    def stop(self) -> typing.Union[None, asyncio.Task]:
        if self.task:
            self.task.cancel()
        return self.task


@dataclass
class WatchDogAll(WatchDog):
    """
    Watchdog that will watch multiple watchdogs to call an aggregated call back checking that all the
    """

    def __post_init__(self):
        self._last_fed: float = time.time()
        self._waiter = None
        self._fed = AggregateEventAll()
        self._starved = AggregateEventAny()
        self.watchdogs: list = []

    def add_watchdogs(self, watchdogs: typing.Sequence[WatchDog]):
        self._fed.evts.extend(dog._fed for dog in watchdogs)
        self._starved.evts.extend(dog._starved for dog in watchdogs)
        self.watchdogs.extend(watchdogs)

    async def wait(self):
        return await asyncio.wait(
            [dog.wait() for dog in self.watchdogs], return_when=asyncio.FIRST_COMPLETED
        )

    @property
    def waiter(self):
        return None

    @waiter.setter
    def waiter(self, value: asyncio.Event):
        pass

    @property
    def fed(self):
        return all(watchdog._fed_bool for watchdog in self.watchdogs)


@dataclass
class WatchDogAny(WatchDog):
    """
    Watchdog that will watch multiple watchdogs to call an aggregated call back
    """

    def __post_init__(self):
        self._last_fed: float = time.time()
        self._waiter = None
        self._fed = AggregateEventAny()
        self._starved = AggregateEventAll()
        self.watchdogs: list = []

    def add_watchdogs(self, watchdogs: typing.Sequence[WatchDog]):
        self._fed.evts.extend(dog._fed for dog in watchdogs)
        self._starved.evts.extend(dog._starved for dog in watchdogs)
        self.watchdogs.extend(watchdogs)

    @property
    def fed(self):
        return any(watchdog.fed for watchdog in self.watchdogs)


@dataclass
class WatchdogManager:
    watchdogs: dict = field(default_factory=dict)

    def add(self, name: str, watchdog: WatchDog):
        self.watchdogs[name] = watchdog

    def get(self, name: str) -> WatchDog:
        try:
            return self.watchdogs[name]
        except KeyError:
            raise ValueError(f"No valid watchdog by name {name}")

    async def stop(self, timeout: float = 1):
        await asyncio.wait(
            [watch.stop() for watch in self.watchdogs.values()],
            timeout=timeout,
            return_when=asyncio.ALL_COMPLETED,
        )


manager = WatchdogManager()


def watch(
    name: str,
    starve_on_exception: typing.Optional[int] = None,
    feed_on_entry: bool = False,
):
    """
    Watch a function call and feed the watchdog every successful call to the function.
    If no watchdog is created, then the function call will ignore the watchdog and continue executing as a normal
    function

    :param f: Function to monitor
    :param name: Unique name of the watchdog as set in add_watchdog
    :param starve_on_exception: Optionally explicitly force the watchdog to starve when the function call causes an
    exception
    :param feed_on_entry: Feed the watchdog before calling the function.
    :return:
    """
    if starve_on_exception and feed_on_entry:
        raise ValueError(
            "Cannot define both starve_on_exception and always_feed as they are mutually exclusive"
        )

    def outer(f):
        cls_based = "self" in inspect.signature(f).parameters
        bound_method = inspect.ismethod(f)
        exc_cnt = 0
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            async def inner(*args, **kwargs):
                nonlocal exc_cnt
                if cls_based:
                    watch_name = name.format(self=args[0])
                elif bound_method:
                    watch_name = name.format(self=f.__self__)
                else:
                    watch_name = name
                try:
                    watchdog = manager.get(watch_name)
                except ValueError:
                    return await f(*args, **kwargs)
                try:
                    if feed_on_entry:
                        watchdog.feed()
                    ret_val = await f(*args, **kwargs)
                    exc_cnt = 0
                    watchdog.feed()
                    return ret_val
                except Exception:
                    if starve_on_exception is not None:
                        exc_cnt += 1
                        if exc_cnt >= starve_on_exception:
                            watchdog.starve()
                    raise

        else:

            @wraps(f)
            def inner(*args, **kwargs):
                nonlocal exc_cnt
                if cls_based:
                    watch_name = name.format(self=args[0])
                elif bound_method:
                    watch_name = name.format(self=f.__self__)
                else:
                    watch_name = name
                try:
                    watchdog = manager.get(watch_name)
                except ValueError:
                    return f(*args, **kwargs)
                try:
                    if feed_on_entry:
                        watchdog.feed()
                    ret_val = f(*args, **kwargs)
                    exc_cnt = 0
                    watchdog.feed()
                    return ret_val
                except Exception:
                    if starve_on_exception is not None:
                        exc_cnt += 1
                        if exc_cnt >= starve_on_exception:
                            watchdog.starve()
                    raise

        return inner

    return outer


def watch_starve(name: str):
    """
    Watch a function call and starve the watchdog immediately on a call to the function.
    If no watchdog is created, then the function call will ignore the watchdog and continue executing as a normal
    function

    :param f: Function to monitor
    :param name: Unique name of the watchdog as set in add_watchdog
    :param starve_on_exception: Optionally explictly force the watchdog to starve when the function call causes an
    exception
    :return:
    """

    def outer(f):
        cls_based = "self" in inspect.signature(f).parameters
        bound_method = inspect.ismethod(f)
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            async def inner(*args, **kwargs):
                if cls_based:
                    watch_name = name.format(self=args[0])
                elif bound_method:
                    watch_name = name.format(self=f.__self__)
                else:
                    watch_name = name
                try:
                    watchdog = manager.get(watch_name)
                except ValueError:
                    return await f(*args, **kwargs)
                watchdog.starve()
                return await f(*args, **kwargs)

        else:

            @wraps(f)
            def inner(*args, **kwargs):
                if cls_based:
                    watch_name = name.format(self=args[0])
                elif bound_method:
                    watch_name = name.format(self=f.__self__)
                else:
                    watch_name = name
                try:
                    watchdog = manager.get(watch_name)
                except ValueError:
                    return f(*args, **kwargs)
                watchdog.starve()
                return f(*args, **kwargs)

        return inner

    return outer


if __name__ == "__main__":

    class TestThing:
        name_thing = "Blah"

        async def do_the_thing(self):
            print("DOING IT")

    test = TestThing()
    test.do_the_thing = watch("test_dog/{self.name_thing}")(test.do_the_thing)

    async def main():
        dog = WatchDog(1, lambda: print("Fed"), lambda: print("Starved"))
        manager.add("test_dog/Blah", dog)
        dog.start(start_fed=False)
        while True:
            await asyncio.sleep(0.1)
            # dog.feed()
            await test.do_the_thing()

    asyncio.run(main())
