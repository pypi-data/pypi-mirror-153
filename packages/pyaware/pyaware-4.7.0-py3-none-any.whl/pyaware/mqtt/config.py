import dataclasses
import datetime
import os
import uuid
from dataclasses import dataclass, field
import logging
import jwt

import pyaware.config
import pyaware.mqtt

log = logging.getLogger(__name__)


class MQTTConfigBase:
    """
    Used to store the cloud configuration information as well as keep jwt tokens fresh
    """

    device_id: str
    authentication_required: bool
    client_id: str
    host: str
    port: str
    keepalive: int
    bind_address: str
    clean_session: bool
    private_key_path: str
    ca_certs_path: str
    ssl_algorithm: str
    _private_key: str
    _token: str
    token_exp: datetime.datetime
    parsers: dict
    subscribe_qos: int
    publish_qos: int
    token_life: int
    serial_number: str = ""
    batch: bool = False
    batch_hold_off: float = 0.0
    batch_soft_limit_characters: int = 20000000
    batch_max_size: int = 268435455
    max_message_queue_size: int = 0
    max_in_flight_messages: int = 0
    backlog_enable: bool = False
    remote_configuration_timeout: int = 20

    @property
    def private_key(self):
        if not self._private_key:
            try:
                with open(self.private_key_path, "r") as f:
                    self._private_key = f.read()
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    "Could not find the ssl private key file as specified in the cloud config"
                ) from e
        return self._private_key

    @property
    def jwt_token(self):
        if datetime.datetime.utcnow() > self.token_exp - datetime.timedelta(minutes=1):
            self._create_jwt()
        return self._token

    def _create_jwt(self):
        pass

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        return {
            key for key in self.__dataclass_fields__ if self.__dict__.get(key) != ""
        }


def credential_factory(cred):
    def _tmp():
        return os.path.join(pyaware.config.aware_path, "credentials", cred)

    return _tmp


def default_gcp_parsers():
    return {
        "telemetry": {
            "factory": {"name": "telemetry_v1"},
            "model": {"name": "TelemetryV1"},
            "topic": "/devices/{device_id}/events/telemetry",
        },
        "config": {"topic": "/devices/{device_id}/config"},
        "errors": {"topic": "/devices/{device_id}/errors"},
        "commands": {
            "topic": "/devices/{device_id}/commands/#",
            "model": {"name": "CommandRequestV2"},
        },
        "command_response": {
            "model": {"name": "CommandResponse"},
            "topic": "/devices/{device_id}/events/command-response",
        },
        "attach": {"topic": "/devices/{device_id}/attach"},
        "state": {
            "model": {"name": "State"},
            "topic": "/devices/{device_id}/state",
            "device_message": False,
            "cache": False,
        },
    }


def default_local_parsers():
    return {
        "telemetry": {
            "factory": {"name": "telemetry_v2"},
            "model": {"name": "TelemetryV2"},
            "topic": "devices/{gateway_id}/{device_id}/events/telemetry",
            "batchable_backlog": True,
        },
        "telemetry_serial": {
            "factory": {"name": "telemetry_v2"},
            "transforms": [
                {"name": "remove_keys", "keys": {"raw_values"}},
            ],
            "model": {"name": "TelemetryV2"},
            "topic": "devices/{gateway_id}/{device_id}/{serial_number}/events/telemetry",
            "batchable_backlog": True,
        },
        "config": {"topic": "devices/{gateway_id}/config"},
        "errors": {"topic": "devices/{gateway_id}/errors"},
        "commands": {
            "topic": "devices/{device_id}/{serial_number}/commands",
            "model": {"name": "CommandRequestV1"},
        },
        "command_response": {
            "model": {"name": "CommandResponse"},
            "topic": "devices/{gateway_id}/{device_id}/events/telemetry/commands",
        },
        "topology": {
            "model": {"name": "Topology"},
            "topic": "devices/{gateway_id}/{device_id}/topology",
        },
        "topology_serial": {
            "model": {"name": "Topology"},
            "topic": "devices/{gateway_id}/{device_id}/{serial_number}/topology",
        },
        "gateway": {
            "model": {"name": "Heartbeat"},
            "topic": "gateways/{gateway_id}/heartbeat",
            "cache": False,
            "device_message": False,
        },
        "device_heartbeat_source": {
            "model": {"name": "EmptyPayload"},
            "topic": "devices/{gateway_id}/{device_id}/heartbeat/{source}",
            "cache": False,
        },
        "device_heartbeat_serial_source": {
            "model": {"name": "EmptyPayload"},
            "topic": "devices/{gateway_id}/{device_id}/{serial_number}/heartbeat/{source}",
            "cache": False,
        },
        "state": {
            "model": {"name": "State"},
            "topic": "gateways/{gateway_id}/state",
            "retain": False,
            "device_message": False,
            "cache": False,
        },
        "state_serial": {
            "model": {"name": "State"},
            "topic": "gateways/{gateway_id}/{serial_number}/state",
            "retain": False,
        },
    }


PARSERS = {"gcp": default_gcp_parsers, "local": default_local_parsers}


@dataclass
class LocalConfig(MQTTConfigBase):
    device_id: str = ""
    client_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    gateway_id: str = ""
    serial_number: str = ""
    authentication_required: bool = False
    host: str = "127.0.0.1"
    port: str = 1883
    keepalive: int = 60
    bind_address: str = ""
    clean_session: bool = False
    disable_parsers: list = field(default_factory=list)
    parsers: dict = field(default_factory=dict)
    subscribe_qos: int = 1
    publish_qos: int = 1
    token_life = 0
    batch: bool = True
    batch_hold_off: float = 5.0
    batch_max_size: int = 268435455
    max_message_queue_size: int = 100
    max_in_flight_messages: int = 100
    backlog_enable: bool = False
    remote_configuration_timeout: int = 2
    parsers_default: str = "local"

    def __post_init__(self):
        mqtt_parsers = PARSERS[self.parsers_default]()
        # Add/Update parsers defined in config
        mqtt_parsers.update(self.parsers)
        # Remove parsers defined in config
        topics_disabled = [
            mqtt_parsers.pop(k).get("topic")
            for k in self.disable_parsers
            if k in mqtt_parsers
        ]
        if topics_disabled:
            log.info(
                f"The following MQTT topics have been disabled by config: {topics_disabled}"
            )
        self.parsers = mqtt_parsers

    def update(self, **kwargs: dict):
        config = dataclasses.asdict(self)
        # Get intersection of two dictionaries to find matching keys
        matching_keys = set(config.keys()) & set(kwargs.keys())
        # Update the import to only include the existing fields of the class
        kwargs = {k: kwargs[k] for k in matching_keys if k in kwargs}
        # Update the config and set it to the class.__dict__ method
        config.update(kwargs)
        self.__dict__ = config


@dataclass
class GCPCloudConfig(MQTTConfigBase):
    """
    Used to store the cloud configuration information as well as keep jwt tokens fresh
    """

    device_id: str
    serial_number: str = ""
    gateway_id: str = ""
    project_id: str = "aware-iot"
    registry_id: str = "aware-iot"
    cloud_region: str = "asia-east1"
    host: str = "mqtt.googleapis.com"
    port: str = 8883
    keepalive: int = 60
    bind_address: str = ""
    clean_session: bool = True
    private_key_path: str = field(default_factory=credential_factory("rsa_private.pem"))
    ca_certs_path: str = field(default_factory=credential_factory("google_roots.pem"))
    ssl_algorithm: str = "RS256"
    token_life: int = 60  # In Minutes
    _private_key: str = ""
    _token: str = ""
    authentication_required: bool = True
    token_exp: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.utcnow()
        + datetime.timedelta(minutes=10)
    )
    disable_parsers: list = field(default_factory=list)
    parsers: dict = field(default_factory=default_gcp_parsers)
    subscribe_qos: int = 1
    publish_qos: int = 1
    max_in_flight_messages: int = 100
    batch: bool = True
    batch_hold_off: float = 3.0
    batch_max_size: int = 268435455
    max_message_queue_size: int = 100
    backlog_enable: bool = False
    remote_configuration_timeout: int = 20
    parsers_default: str = "gcp"

    def __post_init__(self):
        mqtt_parsers = PARSERS[self.parsers_default]()
        # Add/Update parsers defined in config
        mqtt_parsers.update(self.parsers)
        # Remove parsers defined in config
        topics_disabled = [
            mqtt_parsers.pop(k).get("topic")
            for k in self.disable_parsers
            if k in mqtt_parsers
        ]
        if topics_disabled:
            log.info(
                f"The following MQTT topics have been disabled by config: {topics_disabled}"
            )
        self.parsers = mqtt_parsers

    @property
    def client_id(self):
        if any(
            len(x) == 1
            for x in [
                self.project_id,
                self.cloud_region,
                self.registry_id,
                self.device_id,
            ]
        ):
            raise ValueError("Cannot return client id if not all parameters are set")
        return f"projects/{self.project_id}/locations/{self.cloud_region}/registries/{self.registry_id}/devices/{self.device_id}"

    @property
    def private_key(self):
        if not self._private_key:
            try:
                with open(self.private_key_path, "r") as f:
                    self._private_key = f.read()
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    "Could not find the ssl private key file as specified in the cloud config"
                ) from e
        return self._private_key

    @property
    def jwt_token(self):
        self._create_jwt()
        return self._token

    def _create_jwt(self):
        log.info("Creating new jwt token")
        token_exp = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=self.token_life
        )
        token = {
            # The time that the token was issued at
            "iat": datetime.datetime.utcnow(),
            # The time the token expires.
            "exp": token_exp,
            # The audience field should always be set to the GCP project id.
            "aud": self.project_id,
        }
        self._token = jwt.encode(token, self.private_key, algorithm=self.ssl_algorithm)
        self.token_exp = token_exp
