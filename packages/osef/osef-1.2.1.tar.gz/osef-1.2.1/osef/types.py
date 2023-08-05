"""Types of the objects contained in the OSEF stream."""
import uuid
from collections import namedtuple

import numpy as np

# OSEF imports
import osef._unpackers as _unpackers
import osef._packers as _packers
from osef.osef_types import OsefTypes
from osef.osef_types import OsefKeys


LeafInfo = namedtuple("Leaf", "unpack_function pack_function")
InternalNodeInfo = namedtuple("InternalNode", "type")
TypeInfo = namedtuple("Type", "name node_info")


outsight_types = {
    OsefTypes.AUGMENTED_CLOUD.value: TypeInfo(
        OsefKeys.AUGMENTED_CLOUD.value, InternalNodeInfo(dict)
    ),
    OsefTypes.NUMBER_OF_POINTS.value: TypeInfo(
        OsefKeys.NUMBER_OF_POINTS.value,
        LeafInfo(
            _unpackers._get_value_unpacker("<L"), _packers._get_value_packer("<L")
        ),
    ),
    OsefTypes.SPHERICAL_COORDINATES.value: TypeInfo(
        OsefKeys.SPHERICAL_COORDINATES.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    (
                        [
                            ("azimuth", np.float32),
                            ("elevation", np.float32),
                            ("distance", np.float32),
                        ]
                    ),
                )
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.REFLECTIVITIES.value: TypeInfo(
        OsefKeys.REFLECTIVITIES.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.uint8)), _packers._array_packer
        ),
    ),
    OsefTypes.BACKGROUND_FLAGS.value: TypeInfo(
        OsefKeys.BACKGROUND_FLAGS.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(bool)), _packers._array_packer
        ),
    ),
    OsefTypes.CARTESIAN_COORDINATES.value: TypeInfo(
        OsefKeys.CARTESIAN_COORDINATES.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    ([("x", np.float32), ("y", np.float32), ("z", np.float32)]),
                )
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes._BGR_COLORS.value: TypeInfo(
        OsefKeys._BGR_COLORS.value,
        LeafInfo(_unpackers._bytes_unpacker, _packers._bytes_packer),
    ),
    OsefTypes._OBJECT_DETECTION_FRAME.value: TypeInfo(
        OsefKeys._OBJECT_DETECTION_FRAME.value, InternalNodeInfo(dict)
    ),
    OsefTypes._IMAGE_DIMENSION.value: TypeInfo(
        OsefKeys._IMAGE_DIMENSION.value,
        LeafInfo(
            _unpackers._get_dict_unpacker("<LL", ["image_width", "image_height"]),
            _packers._get_dict_packer("<LL", ["image_width", "image_height"]),
        ),
    ),
    OsefTypes.NUMBER_OF_OBJECTS.value: TypeInfo(
        OsefKeys.NUMBER_OF_OBJECTS.value,
        LeafInfo(
            _unpackers._get_value_unpacker("<L"), _packers._get_value_packer("<L")
        ),
    ),
    OsefTypes._CLOUD_FRAME.value: TypeInfo(
        OsefKeys._CLOUD_FRAME.value, InternalNodeInfo(dict)
    ),
    OsefTypes.TIMESTAMP_MICROSECOND.value: TypeInfo(
        OsefKeys.TIMESTAMP_MICROSECOND.value,
        LeafInfo(_unpackers._parse_timestamp, _packers._timestamp_packer),
    ),
    OsefTypes._AZIMUTHS_COLUMN.value: TypeInfo(
        OsefKeys._AZIMUTHS_COLUMN.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.float32)), _packers._array_packer
        ),
    ),
    OsefTypes.NUMBER_OF_LAYERS.value: TypeInfo(
        OsefKeys.NUMBER_OF_LAYERS.value,
        LeafInfo(
            _unpackers._get_value_unpacker("<L"), _packers._get_value_packer("<L")
        ),
    ),
    OsefTypes._CLOUD_PROCESSING.value: TypeInfo(
        OsefKeys._CLOUD_PROCESSING.value,
        LeafInfo(
            _unpackers._processing_bitfield_unpacker,
            _packers._processing_bitfield_packer,
        ),
    ),
    OsefTypes._RANGE_AZIMUTH.value: TypeInfo(
        OsefKeys._RANGE_AZIMUTH.value,
        LeafInfo(
            _unpackers._get_dict_unpacker(
                "<ff", ["azimuth_begin_deg", "azimuth_end_deg"]
            ),
            _packers._get_dict_packer("<ff", ["azimuth_begin_deg", "azimuth_end_deg"]),
        ),
    ),
    OsefTypes._BOUNDING_BOXES_ARRAY.value: TypeInfo(
        OsefKeys._BOUNDING_BOXES_ARRAY.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    (
                        [
                            ("x_min", np.float32),
                            ("y_min", np.float32),
                            ("x_max", np.float32),
                            ("y_max", np.float32),
                        ]
                    ),
                )
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.CLASS_ID_ARRAY.value: TypeInfo(
        OsefKeys.CLASS_ID_ARRAY.value,
        LeafInfo(_unpackers._class_array_unpacker, _packers._class_array_packer),
    ),
    OsefTypes._CONFIDENCE_ARRAY.value: TypeInfo(
        OsefKeys._CONFIDENCE_ARRAY.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.float32)), _packers._array_packer
        ),
    ),
    OsefTypes.TIMESTAMPED_DATA.value: TypeInfo(
        OsefKeys.TIMESTAMPED_DATA.value, InternalNodeInfo(dict)
    ),
    OsefTypes._PERCEPT.value: TypeInfo(
        OsefKeys._PERCEPT.value,
        LeafInfo(_unpackers._percept_class_unpacker, _packers._percept_class_packer),
    ),
    OsefTypes._BGR_IMAGE_FRAME.value: TypeInfo(
        OsefKeys._BGR_IMAGE_FRAME.value, InternalNodeInfo(dict)
    ),
    OsefTypes.POSE.value: TypeInfo(
        OsefKeys.POSE.value, LeafInfo(_unpackers._pose_unpacker, _packers._pose_packer)
    ),
    OsefTypes.SCAN_FRAME.value: TypeInfo(
        OsefKeys.SCAN_FRAME.value, InternalNodeInfo(dict)
    ),
    OsefTypes.TRACKED_OBJECTS.value: TypeInfo(
        OsefKeys.TRACKED_OBJECTS.value, InternalNodeInfo(dict)
    ),
    OsefTypes.BBOX_SIZES.value: TypeInfo(
        OsefKeys.BBOX_SIZES.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    (
                        [
                            ("bbox_x", np.float32),
                            ("bbox_y", np.float32),
                            ("bbox_z", np.float32),
                        ]
                    ),
                ),
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.SPEED_VECTORS.value: TypeInfo(
        OsefKeys.SPEED_VECTORS.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    ([("Vx", np.float32), ("Vy", np.float32), ("Vz", np.float32)]),
                ),
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.POSE_ARRAY.value: TypeInfo(
        OsefKeys.POSE_ARRAY.value,
        LeafInfo(_unpackers._pose_array_unpacker, _packers._pose_array_packer),
    ),
    OsefTypes.OBJECT_ID.value: TypeInfo(
        OsefKeys.OBJECT_ID.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.ulonglong)),
            _packers._array_packer,
        ),
    ),
    OsefTypes.CARTESIAN_COORDINATES_4F.value: TypeInfo(
        OsefKeys.CARTESIAN_COORDINATES_4F.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    (
                        [
                            ("x", np.float32),
                            ("y", np.float32),
                            ("z", np.float32),
                            ("__todrop", np.float32),
                        ]
                    ),
                )
            ),
            _packers._structured_array_packer,
        ),
    ),
    # __todrop are unused columns that are here to
    # have 4 floats in the TLV which is more cpu efficient.
    OsefTypes.SPHERICAL_COORDINATES_4F.value: TypeInfo(
        OsefKeys.SPHERICAL_COORDINATES_4F.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    (
                        [
                            ("azimuth", np.float32),
                            ("elevation", np.float32),
                            ("distance", np.float32),
                            ("__todrop", np.float32),
                        ]
                    ),
                )
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.ZONES_DEF.value: TypeInfo(
        OsefKeys.ZONES_DEF.value, InternalNodeInfo(list)
    ),
    OsefTypes.ZONE.value: TypeInfo(OsefKeys.ZONE.value, InternalNodeInfo(dict)),
    OsefTypes.ZONE_VERTICES.value: TypeInfo(
        OsefKeys.ZONE_VERTICES.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(([("x", np.float32), ("y", np.float32)])),
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.ZONE_NAME.value: TypeInfo(
        OsefKeys.ZONE_NAME.value,
        LeafInfo(_unpackers._get_string_unpacker(), _packers._get_string_packer()),
    ),
    OsefTypes._ZONE_UUID.value: TypeInfo(
        OsefKeys._ZONE_UUID.value,
        LeafInfo(lambda v: uuid.UUID(bytes=v), lambda v: v.bytes),
    ),
    OsefTypes.ZONES_OBJECTS_BINDING.value: TypeInfo(
        OsefKeys.ZONES_OBJECTS_BINDING.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    ([("object_id", np.uint64), ("zone_idx", np.uint32)]),
                ),
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.OBJECT_PROPERTIES.value: TypeInfo(
        OsefKeys.OBJECT_PROPERTIES.value,
        LeafInfo(
            _unpackers._object_properties_unpacker, _packers._object_properties_packer
        ),
    ),
    OsefTypes._IMU_PACKET.value: TypeInfo(
        OsefKeys._IMU_PACKET.value,
        LeafInfo(_unpackers._imu_unpacker, _packers._imu_packer),
    ),
    OsefTypes._TIMESTAMP_LIDAR_VELODYNE.value: TypeInfo(
        OsefKeys._TIMESTAMP_LIDAR_VELODYNE.value,
        LeafInfo(
            _unpackers._get_dict_unpacker("<LL", ["unix_s", "remaining_us"]),
            _packers._get_dict_packer("<LL", ["unix_s", "remaining_us"]),
        ),
    ),
    OsefTypes.POSE_RELATIVE.value: TypeInfo(
        OsefKeys.POSE_RELATIVE.value,
        LeafInfo(_unpackers._pose_unpacker, _packers._pose_packer),
    ),
    OsefTypes._GRAVITY.value: TypeInfo(
        OsefKeys._GRAVITY.value,
        LeafInfo(
            _unpackers._get_dict_unpacker("<fff", ["x", "y", "z"]),
            _packers._get_dict_packer("<fff", ["x", "y", "z"]),
        ),
    ),
    OsefTypes.EGO_MOTION.value: TypeInfo(
        OsefKeys.EGO_MOTION.value, InternalNodeInfo(dict)
    ),
    OsefTypes._PREDICTED_POSITION.value: TypeInfo(
        OsefKeys._PREDICTED_POSITION.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    ([("x", np.float32), ("y", np.float32), ("z", np.float32)]),
                ),
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.GEOGRAPHIC_POSE.value: TypeInfo(
        OsefKeys.GEOGRAPHIC_POSE.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    (
                        [
                            ("lat", np.float32),
                            ("long", np.float32),
                            ("heading", np.float32),
                        ]
                    )
                )
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes.OBJECT_ID_32_BITS.value: TypeInfo(
        OsefKeys.OBJECT_ID_32_BITS.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.uint32)), _packers._array_packer
        ),
    ),
    OsefTypes.ZONES_OBJECTS_BINDING_32_BITS.value: TypeInfo(
        OsefKeys.ZONES_OBJECTS_BINDING_32_BITS.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    ([("object_id", np.uint32), ("zone_idx", np.uint32)]),
                ),
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes._BACKGROUND_BITS.value: TypeInfo(
        OsefKeys._BACKGROUND_BITS.value,
        LeafInfo(_unpackers._bool_bitfield_unpacker, _packers._bool_bitfield_packer),
    ),
    OsefTypes._GROUND_PLANE_BITS.value: TypeInfo(
        OsefKeys._GROUND_PLANE_BITS.value,
        LeafInfo(_unpackers._bool_bitfield_unpacker, _packers._bool_bitfield_packer),
    ),
    OsefTypes._AZIMUTHS.value: TypeInfo(
        OsefKeys._AZIMUTHS.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.float32)), _packers._array_packer
        ),
    ),
    OsefTypes._ELEVATIONS.value: TypeInfo(
        OsefKeys._ELEVATIONS.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.float32)), _packers._array_packer
        ),
    ),
    OsefTypes._DISTANCES.value: TypeInfo(
        OsefKeys._DISTANCES.value,
        LeafInfo(
            _unpackers._get_array_unpacker(np.dtype(np.float32)), _packers._array_packer
        ),
    ),
    OsefTypes._LIDAR_MODEL.value: TypeInfo(
        OsefKeys._LIDAR_MODEL.value,
        LeafInfo(_unpackers._lidar_model_unpacker, _packers._lidar_model_packer),
    ),
    OsefTypes.SLAM_POSE_ARRAY.value: TypeInfo(
        OsefKeys.SLAM_POSE_ARRAY.value,
        LeafInfo(_unpackers._pose_array_unpacker, _packers._pose_array_packer),
    ),
    OsefTypes.ZONE_VERTICAL_LIMITS.value: TypeInfo(
        OsefKeys.ZONE_VERTICAL_LIMITS.value,
        LeafInfo(
            _unpackers._get_array_unpacker(
                np.dtype(np.float32),
            ),
            _packers._array_packer,
        ),
    ),
    OsefTypes.GEOGRAPHIC_POSE_PRECISE.value: TypeInfo(
        OsefKeys.GEOGRAPHIC_POSE_PRECISE.value,
        LeafInfo(
            _unpackers._get_structured_array_unpacker(
                np.dtype(
                    (
                        [
                            ("lat", np.float64),
                            ("long", np.float64),
                            ("heading", np.float32),
                        ]
                    )
                )
            ),
            _packers._structured_array_packer,
        ),
    ),
    OsefTypes._ROAD_MARKINGS_BITS.value: TypeInfo(
        OsefKeys._ROAD_MARKINGS_BITS.value,
        LeafInfo(_unpackers._bool_bitfield_unpacker, _packers._bool_bitfield_packer),
    ),
    OsefTypes.FILTERED_POSE.value: TypeInfo(
        OsefKeys.FILTERED_POSE.value,
        LeafInfo(_unpackers._pose_array_unpacker, _packers._pose_array_packer),
    ),
}


def get_type_info_by_id(type_code):
    """Get TypeInfo for a given type code.

    :param type_code: Int value in OsefTypes
    :return:
    """
    if type_code in outsight_types:
        return outsight_types[type_code]

    return TypeInfo(f"Unknown type ({type_code})", LeafInfo(None, None))


def get_type_info_by_key(type_name: str) -> TypeInfo:
    """Get TypeInfo for a given key/name.

    :param type_name: Int value in OsefTypes
    :return:
    """
    for value in outsight_types.values():
        if value.name == type_name:
            return value
    return TypeInfo(f"Unknown type ({type_name})", LeafInfo(None, None))


def get_type_by_key(type_name: str) -> OsefTypes:
    """Get type index for a given key/name.

    :param type_name: Int value in OsefTypes
    :return:
    """
    for key, value in outsight_types.items():
        if value.name == type_name:
            return OsefTypes(key)
    raise ValueError(f"No type found for type_name={type_name}")
