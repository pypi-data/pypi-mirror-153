from pyaware.store.memory import MemoryStore
from pyaware.store.disk import DiskStorage
import typing
import asyncio


memory_storage = MemoryStore()
disk_storage: typing.Optional[DiskStorage] = None
disk_storage_setup_evt: asyncio.Event = asyncio.Event()
