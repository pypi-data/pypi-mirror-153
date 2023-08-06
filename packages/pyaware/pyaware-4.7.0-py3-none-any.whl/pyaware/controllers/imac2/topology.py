from __future__ import annotations
import asyncio
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from pyaware import events
import pyaware


log = logging.getLogger(__file__)


@events.enable
@dataclass
class Topology:
    device_id: str = ""
    serial_number: str = ""
    include_serial: bool = False
    network: dict = None
    update_interval: Optional[int] = None

    def __post_init__(self):
        self.topologies = {}
        self.identify()
        if self.include_serial:
            self.topic_types = {
                "topology": "topology_serial",
            }
        else:
            self.topic_types = {
                "topology": "topology",
            }
        events.publish("request_topology")
        self.update_topology(log_update=True)
        if self.update_interval is not None:
            asyncio.create_task(self.trigger_interval())

    @events.subscribe(topic="update_gateway_network/#")
    def update_network(self, data):
        self.network = data
        self.update_topology()

    def identify(self):
        data = {}
        if self.network:
            data["network"] = self.network
        return {
            "values": data,
            "timestamp": datetime.utcnow(),
            "children": list(self.topologies.values()),
        }

    def update_topology(self, log_update=True):
        """
        Updates the topology for a given device and resends all the currently connected devices
        :param data: Device topology payload derived from identify method
        :param timestamp: Timestamp of the topology
        :param topic: device_topology/{device_id}
        :return:
        """
        payload = self.identify()
        if log_update:
            log.info(f"New topology:  {payload}")
        events.publish(
            f"trigger_send",
            data=payload,
            timestamp=datetime.utcnow(),
            topic_type=self.topic_types["topology"],
            device_id=self.device_id,
            serial_number=self.serial_number,
        )

    @events.subscribe(topic="device_topology/#", parse_topic=True)
    def build_topology(self, data, timestamp, topic):
        """
        Updates the topology for a given device and resends all the currently connected devices
        :param data: Device topology payload derived from identify method
        :param timestamp: Timestamp of the topology
        :param topic: device_topology/{device_id}
        :return:
        """
        device_id = topic.split("/")[-1]
        self.topologies[device_id] = data
        self.update_topology(log_update=True)

    async def trigger_interval(self):
        log.info(f"Starting topology at interval: {self.update_interval}")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing topology interval")
                return
            try:
                self.update_topology(log_update=False)
            except BaseException as e:
                if pyaware.evt_stop.is_set():
                    continue
                log.error(repr(e))
            await asyncio.sleep(self.update_interval)
