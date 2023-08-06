from enum import IntEnum


class ModuleStatus(IntEnum):
    ONLINE = 0
    SYSTEM = 1
    OFFLINE = 2
    CLASH = 3
    NEVER_ONLINE = 4
    SYSTEM_ONLINE = 5
    L1_OWNED = 6
    L2_OWNED = 7
    UNKNOWN = 10
