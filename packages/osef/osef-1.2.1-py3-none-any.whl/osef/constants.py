"""Constants used throughout project and that can be used by user"""
from collections import namedtuple
from enum import Enum


class PerceptIds(Enum):
    """Ids of the elements classified by the percept algorithm"""

    DEFAULT = 0
    ROAD = 1
    VEGETATION = 2
    GROUND = 3
    SIGN = 4
    BUILDING = 5
    FLAT_GND = 6
    UNKNOWN = 7
    MARKING = 8
    OBJECT = 9
    WALL = 10


class TrackedObjectClassIds(Enum):
    """Ids of the objects classified by the tracking algorithm"""

    UNKNOWN = 0
    PERSON = 1
    LUGGAGE = 2
    TROLLEY = 3
    TRUCK = 4
    BUS = 5
    CAR = 6
    VAN = 7
    TWO_WHEELER = 8
    MASK = 9
    NO_MASK = 10
    LANDMARK = 11


class LidarModelIds(Enum):
    """LiDAR models enum"""

    UNKNOWN = 0
    VELODYNE_VLP16 = 1
    VELODYNE_VLP32 = 2
    VELODYNE_VLS128 = 3
    VELODYNE_HDL32 = 4
    ROBOSENSE_BPEARL_V1 = 5
    ROBOSENSE_BPEARL_V2 = 6
    ROBOSENSE_RS32 = 7
    ROBOSENSE_HELIOS = 8
    LIVOX_HORIZON = 9
    LIVOX_AVIA = 10
    LIVOX_MID70 = 11
    OUSTER = 12
    OUTSIGHT_SA01 = 13
    HESAI_PANDAR_XT = 14
    HESAI_PANDAR_QT = 15
    RANDOM = 16


LidarModel = namedtuple("LidarModel", ("id", "name"))


# TLV constant
_Tlv = namedtuple("TLV", "type length value")
_TreeNode = namedtuple("TreeNode", "type children leaf_value")
# Structure Format definition (see https://docs.python.org/3/library/struct.html#format-strings):
# Meant to be used as: _STRUCT_FORMAT % length
_STRUCT_FORMAT = "<"  # little endian
_STRUCT_FORMAT += "L"  # unsigned long        (field 'T' ie. 'Type')
_STRUCT_FORMAT += "L"  # unsigned long        (field 'L' ie. 'Length')
_STRUCT_FORMAT += "%ds"  # buffer of fixed size (field 'V' ie. 'Value')
