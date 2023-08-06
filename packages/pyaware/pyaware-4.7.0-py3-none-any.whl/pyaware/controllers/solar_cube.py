from __future__ import annotations
import asyncio
import logging
import time
from datetime import datetime
from dataclasses import dataclass
from pyaware.mqtt.client import Mqtt
from pyaware import watchdog

from pyaware import events

log = logging.getLogger(__file__)


@events.enable
@dataclass
class SolarCube:
    device_id: str
    cloud_broker: Mqtt = None

    def init(self):
        asyncio.create_task(self.heartbeat())
        self.setup_watchdogs()

    def setup_watchdogs(self):
        try:
            self.cloud_broker.client.on_connect = watchdog.watch(
                f"ipc_cloud_comms_status_{id(self)}"
            )(self.cloud_broker.client.on_connect)
        except AttributeError:
            pass
        try:
            self.cloud_broker.client.publish = watchdog.watch(
                f"ipc_cloud_comms_status_{id(self)}"
            )(self.cloud_broker.client.publish)
        except AttributeError:
            pass
        try:
            self.cloud_broker.client.on_disconnect = watchdog.watch_starve(
                f"ipc_cloud_comms_status_{id(self)}"
            )(self.cloud_broker.client.on_disconnect)
        except AttributeError:
            pass
        dog_eth = watchdog.WatchDog(
            heartbeat_time=60,
            success_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"cloud-comms-status": True},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
            failure_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"cloud-comms-status": False},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
        )
        watchdog.manager.add(f"ipc_cloud_comms_status_{id(self)}", dog_eth)
        dog_eth.start(start_fed=False)

    async def heartbeat(self):
        while True:
            events.publish(
                f"process_data/{id(self)}",
                data={"heartbeat": time.time()},
                timestamp=datetime.now(),
                device_id=self.device_id,
            )
            await asyncio.sleep(30)
