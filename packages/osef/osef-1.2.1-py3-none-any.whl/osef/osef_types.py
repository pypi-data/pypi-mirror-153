"""OSEF private types definition."""
__version__ = "1.2.1"

# Standard imports
from enum import Enum, IntEnum

# !!! Warning !!!
# !!! This file has been auto generated, do not attempt to edit it !!!
# Important: all words use little-endian representation, unless specified otherwise


class OsefTypes(IntEnum):
    """OSEF types."""

    AUGMENTED_CLOUD = 1
    NUMBER_OF_POINTS = 2
    SPHERICAL_COORDINATES = 3
    REFLECTIVITIES = 4
    BACKGROUND_FLAGS = 5
    CARTESIAN_COORDINATES = 6
    _BGR_COLORS = 7
    _OBJECT_DETECTION_FRAME = 8
    _IMAGE_DIMENSION = 9
    NUMBER_OF_OBJECTS = 10
    _CLOUD_FRAME = 11
    TIMESTAMP_MICROSECOND = 12
    _AZIMUTHS_COLUMN = 13
    NUMBER_OF_LAYERS = 14
    _CLOUD_PROCESSING = 15
    _RANGE_AZIMUTH = 16
    _BOUNDING_BOXES_ARRAY = 17
    CLASS_ID_ARRAY = 18
    _CONFIDENCE_ARRAY = 19
    TIMESTAMPED_DATA = 20
    _PERCEPT = 21
    _BGR_IMAGE_FRAME = 23
    POSE = 24
    SCAN_FRAME = 25
    TRACKED_OBJECTS = 26
    BBOX_SIZES = 27
    SPEED_VECTORS = 28
    POSE_ARRAY = 29
    OBJECT_ID = 30
    CARTESIAN_COORDINATES_4F = 31
    SPHERICAL_COORDINATES_4F = 32
    ZONES_DEF = 33
    ZONE = 34
    ZONE_VERTICES = 35
    ZONE_NAME = 36
    _ZONE_UUID = 37
    ZONES_OBJECTS_BINDING = 38
    OBJECT_PROPERTIES = 39
    _IMU_PACKET = 40
    _TIMESTAMP_LIDAR_VELODYNE = 41
    POSE_RELATIVE = 42
    _GRAVITY = 43
    EGO_MOTION = 44
    _PREDICTED_POSITION = 45
    GEOGRAPHIC_POSE = 46
    OBJECT_ID_32_BITS = 47
    ZONES_OBJECTS_BINDING_32_BITS = 48
    _BACKGROUND_BITS = 49
    _GROUND_PLANE_BITS = 50
    _AZIMUTHS = 51
    _ELEVATIONS = 52
    _DISTANCES = 53
    _LIDAR_MODEL = 54
    SLAM_POSE_ARRAY = 55
    ZONE_VERTICAL_LIMITS = 56
    GEOGRAPHIC_POSE_PRECISE = 57
    _ROAD_MARKINGS_BITS = 58
    FILTERED_POSE = 59
    _INTERACTIVE_REQUEST = 60
    _INTERACTIVE_RESPONSE = 61
    _INTERACTIVE_REQUEST_ID = 62
    _INTERACTIVE_REQUEST_BACKGROUND_HEADER = 63
    _INTERACTIVE_RESPONSE_BACKGROUND_HEADER = 64
    _INTERACTIVE_REQUEST_BACKGROUND_DATA = 65
    _INTERACTIVE_RESPONSE_BACKGROUND_DATA = 66
    _INTERACTIVE_REQUEST_PINGPONG = 67
    _INTERACTIVE_RESPONSE_PINGPONG = 68


class OsefKeys(Enum):
    """OSEF type keys."""

    """
    Augmented Cloud
    **Output when**: Augmented Cloud is enabled.
    **Purpose**: An augmented cloud represents a cloud of points. Each point can have attributes, all of which are
    optional, which describe its position, physical property, movement, etc...
    Contains following sub-TLVs:
    - exactly one:     Number of Points               (NUMBER_OF_POINTS)
    - exactly one:     Number of layers               (NUMBER_OF_LAYERS)
    - none or one:     Spherical Coordinates          (SPHERICAL_COORDINATES) [DEPRECATED USAGE]
    - none or one:     Reflectivities                 (REFLECTIVITIES)
    - none or one:     Background Flags               (BACKGROUND_FLAGS) [DEPRECATED USAGE]
    - none or one:     Cartesian coordinates          (CARTESIAN_COORDINATES)
    - none or one:     BGR Colors                     (BGR_COLORS)
    - none or one:     Azimuths Column                (AZIMUTHS_COLUMN)
    - none or one:     Cloud Processing               (CLOUD_PROCESSING)
    - none or one:     Percept                        (PERCEPT)
    - none or one:     Object Id 32 bits              (OBJECT_ID_32_BITS)
    - none or one:     Cartesian Coordinates 4F       (CARTESIAN_COORDINATES_4F) [DEPRECATED USAGE]
    - none or one:     Background bits                (BACKGROUND_BITS)
    - none or one:     Ground plane bits              (GROUND_PLANE_BITS)
    - none or one:     Azimuths                       (AZIMUTHS)
    - none or one:     Elevations                     (ELEVATIONS)
    - none or one:     Distances                      (DISTANCES)
    - none or one:     Road Markings bits             (ROAD_MARKINGS_BITS)
    """
    AUGMENTED_CLOUD = "augmented_cloud"

    """
    Number of Points
    **Output when**: Augmented Cloud is enabled.
    **Format**: Contains 32 bits unsigned int value.
    **Purpose**: Represents the number of points in the point cloud.
    """
    NUMBER_OF_POINTS = "number_of_points"

    """
    Spherical Coordinates
    Contains list of spherical single-precision float coordinates, three per point:
    * azimuth : degrees, range [ 0.0 .. 360.0 ]
    * elevation : degrees, range [ -90.0 .. +90.0 ]
    * distance : meters, range [ 0.0 ..  +inf ]
    """
    SPHERICAL_COORDINATES = "spherical_coordinates"

    """
    Reflectivities
    **Output when**: Augmented Cloud is enabled.
    **Format**: list of unsigned 8-bits integers.
    **Purpose**: Contains list of reflectivity values.
    Diffuse reflectors report values from 0 to 100 for reflectivities from 0% to 100%.
    Retroreflectors report values from 101 to 255, where 255 represents an ideal reflection.
    """
    REFLECTIVITIES = "reflectivities"

    """
    Background Flags
    **Instead, use**: "Background bits" (Type 49)
    Contains a list of boolean values encoded on an unsigned 8-bits integer:
    * 0 means the point is not part of the background
    * all other values mean the point is part of the background
    The background is defined as the objects which were frequently detected in the past.
    On the contrary the foreground is composed of objects that were not seen before (i.e. they appeared recently and/or
    they are moving).
    """
    BACKGROUND_FLAGS = "background_flags"

    """
    Cartesian coordinates
    **Output when**: Augmented Cloud is enabled.
    Contains list of Cartesian single-precision float coordinates, three per point:
    * x : meters, range [ -inf .. +inf ]
    * y : meters, range [ -inf .. +inf ]
    * z : meters, range [ -inf .. +inf ]
    **Coordinate Frame**:
    - Passthrough & Mobile: Relative to LiDAR Coordinate Frame.
    - Static: in Absolute/World Frame, witch is:
        - Single-LiDAR: On-Ground LiDAR Coordinate Frame.
        - Multi-LiDARs: Map Coordinate Frame.
    """
    CARTESIAN_COORDINATES = "cartesian_coordinates"

    """
    BGR Colors
    Contain list of BGR colors, encoded as three consecutive unsigned 8-bits integers:
    * blue  : range [ 0 .. 255 ]
    * green : range [ 0 .. 255 ]
    * red   : range [ 0 .. 255 ]
    """
    _BGR_COLORS = "bgr_colors"

    """
    Object Detection Frame
    Group all classification results relative to an image.
    Contains following sub-TLVs:
    - exactly one:     Number of Objects              (NUMBER_OF_OBJECTS)
    - none or one:     Timestamp Microsecond          (TIMESTAMP_MICROSECOND)
    - exactly one:     Bounding Boxes Array           (BOUNDING_BOXES_ARRAY)
    - exactly one:     Class ID Array                 (CLASS_ID_ARRAY)
    - none or one:     Confidence Array               (CONFIDENCE_ARRAY)
    """
    _OBJECT_DETECTION_FRAME = "object_detection_frame"

    """
    Image Dimension
    Contain following concatenated data:
    * image_width   : in pixel, unsigned 32-bits integer, range [ 0 .. 2^32 [
    * image_height  : in pixel, unsigned 32-bits integer, range [ 0 .. 2^32 [
    """
    _IMAGE_DIMENSION = "image_dimension"

    """
    Number of Objects
    **Output when**: Tracking is enabled.
    **Purpose**: Number of tracked objects.
    **Format**: unsigned 32-bits integer, range [ 0 .. 2^32 [
    """
    NUMBER_OF_OBJECTS = "number_of_objects"

    """
    Cloud Frame
    Contains following sub-TLVs:
    - exactly one:     Augmented Cloud                (AUGMENTED_CLOUD)
    - exactly one:     Range Azimuth                  (RANGE_AZIMUTH)
    - none or one:     Timestamp Lidar Velodyne       (TIMESTAMP_LIDAR_VELODYNE)
    """
    _CLOUD_FRAME = "cloud_frame"

    """
    Timestamp Microsecond
    **Output when**: Always.
    **Purpose**: Describes a unix timestamp with microsecond precision, same as struct timeval of UNIX <sys/time.h>.
    **Format**: Contains concatenation of:
    * UNIX time in seconds,   unsigned 32-bits integer, range [ 0 .. 2^32 [
    * remaining microseconds, unsigned 32-bits integer, range [ 0 .. 1000000 [
    """
    TIMESTAMP_MICROSECOND = "timestamp_microsecond"

    """
    Azimuths Column
    Contains list of azimuth values in degrees expressed as single-precision floats.
    This azimuth value is computed before corrections due to:
      * The time between each laser firing
      * The correction when lasers of the same firing sequence are not aligned
    The range is [ 0.0 .. 360.0 [.
    """
    _AZIMUTHS_COLUMN = "azimuths_column"

    """
    Number of layers
    **Output when**: Augmented Cloud is enabled.
    **Format**: Contains 32 bits unsigned int value.
    **Purpose**: Represents the number of layers of the point cloud.
    0 indicates that this cloud does not have a 2D structure.
    """
    NUMBER_OF_LAYERS = "number_of_layers"

    """
    Cloud Processing
    Contains a 64 bits bitfield, representing the processing that have been applied.
    If no bit are set this means that no processing have been done on this cloud.
    * Bit 0 : The background points have been removed
    """
    _CLOUD_PROCESSING = "cloud_processing"

    """
    Range Azimuth
    Range of azimuth values for the points contained in a given lidar packet.
    Contains exactly two 32 bits floats. The first one marks the beginning of the range, the second the end.
      The range is [ 0.0 .. 360.0 [.
    """
    _RANGE_AZIMUTH = "range_azimuth"

    """
    Bounding Boxes Array
    Contains list of bounding boxes dimensions, four per box:
    * x_min : percentage of the image size, 32-bits floating-point, range [ 0 .. 1 ]
    * y_min : percentage of the image size, 32-bits floating-point, range [ 0 .. 1 ]
    * x_max : percentage of the image size, 32-bits floating-point, range [ 0 .. 1 ]
    * y_max : percentage of the image size, 32-bits floating-point, range [ 0 .. 1 ]
    """
    _BOUNDING_BOXES_ARRAY = "bounding_boxes_array"

    """
    Class ID Array
    **Output when**: Tracking is enabled.
    **Format**: list of signed 32 bits integers.
    **Purpose**: Contains list of class IDs.
    Mapping between ID and class is given below:
    * 0: UNKNOWN (class cannot yet be determined with confidence)
    * 1: PERSON
    * 2: LUGGAGE
    * 3: TROLLEY
    * 4: TRUCK
    * 5: BUS
    * 6: CAR
    * 7: VAN
    * 8: TWO_WHEELER
    * 9: MASK
    * 10: NO_MASK
    * 11: LANDMARK
    Note that this is an extended list, covering all possible class IDs.
    The effective list of detected classes is always a subset, adapted to the use cases of the version.
    """
    CLASS_ID_ARRAY = "class_id_array"

    """
    Confidence Array
    Contains list of confidences, one per element:
    32-bits floating-point, range [ 0.0 .. 1.0 ]
    """
    _CONFIDENCE_ARRAY = "confidence_array"

    """
    Timestamped data
    **Output when**: Always.
    Contains following sub-TLVs:
    - exactly one:     Timestamp Microsecond          (TIMESTAMP_MICROSECOND)
    - none or one:     Object Detection Frame         (OBJECT_DETECTION_FRAME)
    - none or one:     Cloud Frame                    (CLOUD_FRAME)
    - none or one:     Scan Frame                     (SCAN_FRAME)
    """
    TIMESTAMPED_DATA = "timestamped_data"

    """
    Percept
    Contains list of percept classes represented as unsigned 16-bits integer.
    * 0: DEFAULT
    * 1: ROAD
    * 2: VEGETATION
    * 3: GROUND
    * 4: SIGN
    * 5: BUILDING
    * 6: FLAT_GND
    * 7: UNKNOWN
    * 8: MARKING
    * 9: OBJECT
    * 10: WALL
    """
    _PERCEPT = "percept"

    """
    BGR Image Frame
    Contains following sub-TLVs:
    - exactly one:     BGR Colors                     (BGR_COLORS)
    - exactly one:     Image Dimension                (IMAGE_DIMENSION)
    """
    _BGR_IMAGE_FRAME = "bgr_image_frame"

    """
    Pose
    **Output when**: Ego-Motion is enabled.
    **Purpose**: Pose of the LiDAR.
    **Format**: Concatenation of 12 floats of 32-bits each, in this order:
    - Tx, Ty and Tz, representing the translation vector T to get the position coordinates in meters
    - Rxx, Ryx, Rzx, Rxy, Ryy, Rzy, Rxz, Ryz and Rzz represent the rotation matrix R (given column-wise) defining the
    orientation
    As a consequence, considering a device in a pose defined by T and R, you can compute the coordinates Xabs in the
    absolute referential from the coordinates Xrel in device referential using the vectorial formula:
    ```
    Xabs = R * Xrel + T
    ```
    with:
    ```
        [Rxx Rxy Rxz]
    R = [Ryx Ryy Ryz]
        [Rzx Rzy Rzz]
        [Tx]
    T = [Ty]
        [Tz]
    ```
    **Coordinate Frame**:
    Absolute/World Frame, witch is:
    - Ego-Motion: Initial pose of the LiDAR.
    - Relocalisation: Map Coordinate Frame.
    """
    POSE = "pose"

    """
    Scan Frame
    **Output when**: Always.
    Contains following sub-TLVs:
    - none or one:     Augmented Cloud                (AUGMENTED_CLOUD)
    - none or one:     Pose                           (POSE)
    - none or one:     Geographic pose                (GEOGRAPHIC_POSE)
    - none or one:     Geographic pose precise        (GEOGRAPHIC_POSE_PRECISE)
    - none or one:     Ego Motion                     (EGO_MOTION)
    - none or one:     Tracked Objects                (TRACKED_OBJECTS)
    - none or one:     Zones Def                      (ZONES_DEF)
    - none or one:     Zones Objects Binding          (ZONES_OBJECTS_BINDING) [DEPRECATED USAGE]
    - none or one:     Zones Objects Binding 32 bits  (ZONES_OBJECTS_BINDING_32_BITS)
    - none or one:     Filtered Pose                  (FILTERED_POSE)
    """
    SCAN_FRAME = "scan_frame"

    """
    Tracked Objects
    **Output when**: Tracking is enabled.
    **Purpose**: Properties of tracked objects, which includes centroid, bbox, speed...
    Contains following sub-TLVs:
    - exactly one:     Number of Objects              (NUMBER_OF_OBJECTS)
    - exactly one:     Object Id 32 bits              (OBJECT_ID_32_BITS)
    - none or one:     Class ID Array                 (CLASS_ID_ARRAY)
    - none or one:     Bbox Sizes                     (BBOX_SIZES)
    - none or one:     Speed Vectors                  (SPEED_VECTORS)
    - none or one:     Pose Array                     (POSE_ARRAY)
    - none or one:     Slam Pose Array                (SLAM_POSE_ARRAY)
    - none or one:     Object Properties              (OBJECT_PROPERTIES)
    """
    TRACKED_OBJECTS = "tracked_objects"

    """
    Bbox Sizes
    **Output when**: Tracking is enabled.
    Contains list of bbox sizes for tracked objects, three per object:
    * x : meters, range [ -inf .. +inf ]
    * y : meters, range [ -inf .. +inf ]
    * z : meters, range [ -inf .. +inf ]
    The coordinate system is not specified.
    """
    BBOX_SIZES = "bbox_sizes"

    """
    Speed Vectors
    **Output when**: Tracking is enabled.
    Contains list of speed vectors for tracked objects, three per object:
    * x : meters, range [ -inf .. +inf ]
    * y : meters, range [ -inf .. +inf ]
    * z : meters, range [ -inf .. +inf ]
    The coordinate system is not specified.
    """
    SPEED_VECTORS = "speed_vectors"

    """
    Pose Array
    **Output when**: Tracking is enabled.
    **Purpose**: Contains the poses defining the bounding box of a tracked object.
    **Format**: 12 floats of 32-bits per object:
    * Tx, Ty and Tz represent the translation vector T to get the position coordinates in meters.
    * Rxx, Rxy, Rxz, Ryx, Ryy, Ryz, Rzx, Rzy and Rzz represent the rotation matrix R defining the orientation.
    As a consequence, considering a device in a pose defined by T and R, you can compute the coordinates Xabs in the
    absolute referential from the coordinates Xrel in device referential using the vectorial formula:
    Xabs = R * Xrel + T
    **Coordinate Frame**:
    Absolute/World Frame, witch is:
    - Single-LiDAR configuration: On-Ground LiDAR Coordinate Frame.
    - Multi-LiDARs configuration: Map Coordinate Frame.
    """
    POSE_ARRAY = "pose_array"

    """
    Object Id
    **Instead, use**: "Object Id 32 bits" (Type 47)
    """
    OBJECT_ID = "object_id"

    """
    Cartesian Coordinates 4F
    Alternative way to represent coordinates, where a fourth float is added.
    It can be more efficient to construct if an application aligns the points to use SIMD on 128 bits words.
    Contains list of cartesian single-precision float coordinates, four per point:
    * x : meters, range [ -inf .. +inf ]
    * y : meters, range [ -inf .. +inf ]
    * z : meters, range [ -inf .. +inf ]
    * w : unused, for 128 bits alignment only
    """
    CARTESIAN_COORDINATES_4F = "cartesian_coordinates_4f"

    """
    Spherical Coordinates 4F
    Alternative way to represent coordinates, where a fourth float is added.
    It can be more efficient to construct if an application aligns the points to use SIMD on 128 bits words.
    Contains list of spherical single-precision float coordinates, four per point:
    * azimuth   : degrees, range [ 0.0 .. 360.0 ]
    * elevation : degrees, range [ -90.0 .. +90.0 ]
    * distance  : meters,  range [ 0.0 ..  +inf ]
    * w         : unused, for 128 bits alignment only
    """
    SPHERICAL_COORDINATES_4F = "spherical_coordinates_4f"

    """
    Zones Def
    **Output when**: Tracking is enabled, and at least a zone is defined.
    **Purpose**: Definition of the event zones. They represent spatial areas of interest.
    Their order is important, since the index is used to identify a zone in type 48.
    Contains following sub-TLVs:
    - zero to many:    Zone                           (ZONE)
    """
    ZONES_DEF = "zones_def"

    """
    Zone
    **Output when**: Tracking is enabled, and at least a zone is defined.
    **Purpose**: Defines one zone.
    Contains following sub-TLVs:
    - exactly one:     Zone Vertices                  (ZONE_VERTICES)
    - exactly one:     Zone Name                      (ZONE_NAME)
    - none or one:     Zone UUID                      (ZONE_UUID)
    - none or one:     Zone Vertical Limits           (ZONE_VERTICAL_LIMITS)
    """
    ZONE = "zone"

    """
    Zone Vertices
    **Output when**: Tracking is enabled, and a zone has been defined.
    **Purpose**: Vertices of the polygon defining the zone.
    They are defined on the ground, so the z coordinate is absent.
    **Format**: Contains list of cartesian single-precision float coordinates, two per point.
    * x : meters, range [ -inf .. +inf ]
    * y : meters, range [ -inf .. +inf ]
    There must be at least 3 vertices, so at least 6 floats.
    """
    ZONE_VERTICES = "zone_vertices"

    """
    Zone Name
    **Output when**: Tracking is enabled, and at least a zone is defined.
    **Purpose**: User-defined name to the zone, do not use as unique identifier.
    **Format**: It is UTF-8 encoded and null-terminated.
    """
    ZONE_NAME = "zone_name"

    """
    Zone UUID
    128 bits UUID of the zone in BIG-endian representation.
    UUID 00112233-4455-6677-8899-aabbccddeeff is encoded as the bytes 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff.
    It enables to keep the identity of a zone across renaming or resizing.
    """
    _ZONE_UUID = "zone_uuid"

    """
    Zones Objects Binding
    **Instead, use**: "Zones Objects Binding 32 bits" (Type 48)
    Concatenation of 0 to N couples of:
    * an unsigned 64-bits integer, representing the ID of an object (see type 30)
    * an unsigned 32-bits integer, representing the index of the zone (the n-th type 34 of type 33)
    Each object-zone couple means that the object is considered by the algorithm to be in the zone.
    """
    ZONES_OBJECTS_BINDING = "zones_objects_binding"

    """
    Object Properties
    **Output when**: Tracking is enabled.
    **Purpose**: Properties of the object.
    **Format**: One byte per object, each bit of this can represent different properties.
    * 1st bit: 1 if the object has a proper orientation (like a cuboid), 0 otherwise (like a cylinder).
    * 2nd bit: 1 if the object has been seen in the last scan, 0 if it was not seen.
    * 3rd bit: 1 if the object has a valid slam pose, 0 otherwise. See type 55 (Slam Pose Array) for more information.
    * 4th bit: 1 if the object is static (e.g. traffic signs, poles...), 0 otherwise
    * 5th bit: reserved for later use
    * 6th bit: reserved for later use
    * 7th bit: reserved for later use
    * 8th bit: reserved for later use
    """
    OBJECT_PROPERTIES = "object_properties"

    """
    IMU Packet
    Contains the following data:
    * Time when the IMU packet was received
    * Byte [0,3]: UNIX time in seconds,   unsigned 32-bits integer, range [ 0 .. 2^32 [
    * Byte [4,7]: remaining microseconds, unsigned 32-bits integer, range [ 0 .. 1000000 [
    * Acceleration vector
    * Byte [8,11] x : meters / second^2, 32 bits float, range [ -inf .. +inf ]
    * Byte [12,15] y : meters / second^2, 32 bits float, range [ -inf .. +inf ]
    * Byte [16,19] z : meters / second^2, 32 bits float, range [ -inf .. +inf ]
    * Angular velocity vector
    * Byte [20,23] x : degrees / second, 32 bits float, range [ -inf .. +inf ]
    * Byte [24,27] x : degrees / second, 32 bits float, range [ -inf .. +inf ]
    * Byte [28,31] x : degrees / second, 32 bits float, range [ -inf .. +inf ]
    """
    _IMU_PACKET = "imu_packet"

    """
    Timestamp Lidar Velodyne
    Describes a timestamp with microsecond precision. This timestamp is in the lidar reference system, and uses the
    Velodyne format. This means that this timestamp is the time spent since the beginning of the hour.
    Contains concatenation of:
    * UNIX time in seconds,   unsigned 32-bits integer, range [ 0 .. 2^32 [
    * remaining microseconds, unsigned 32-bits integer, range [ 0 .. 1000000 [
    """
    _TIMESTAMP_LIDAR_VELODYNE = "timestamp_lidar_velodyne"

    """
    Pose Relative
    **Output when**: Ego-motion is enabled.
    **Purpose**: This pose represents the movement of the device between two scans.
    So the position of the current scan can be computed from the one of the previous scan using the following vectorial
    formula:
    ```
    Xcurrent = R * Xprevious + T
    ```
    with:
    ```
        [Rxx Rxy Rxz]
    R = [Ryx Ryy Ryz]
        [Rzx Rzy Rzz]
        [Tx]
    T = [Ty]
        [Tz]
    ```
    **Format**: Concatenation of 12 floats of 32-bits each, in this order:
    - Tx, Ty and Tz, representing the translation vector T to get the position coordinates in meters
    - Rxx, Ryx, Rzx, Rxy, Ryy, Rzy, Rxz, Ryz and Rzz, representing the rotation matrix R (given column-wise) defining
    the orientation
    **Coordinate Frame**: relative to the pose of the previous scan.
    """
    POSE_RELATIVE = "pose_relative"

    """
    Gravity
    Concatenation of 3 floats of 32-bits each [x, y, z], this is the direction of the gravity in the acquisition sensor
    reference frame.
    The vector is either normalised if valid, or [0, 0, 0] if invalid.
    """
    _GRAVITY = "gravity"

    """
    Ego Motion
    **Output when**: Ego-motion is enabled.
    Contains following sub-TLVs:
    - exactly one:     Pose Relative                  (POSE_RELATIVE)
    - none or one:     Predicted Position             (PREDICTED_POSITION)
    """
    EGO_MOTION = "ego_motion"

    """
    Predicted Position
    **Output when**: Ego-motion is enabled.
    **Purpose**: Cartesian coordinates of the predicted position in slam.
    The time of prediction is set at startup, and defaults to 1 second.
    **Format**: Contains 3 floats.
    **Coordinate Frame**: relative to the LiDAR Coordinate Frame.
    """
    _PREDICTED_POSITION = "predicted_position"

    """
    Geographic pose
    **Deprecated since**: 5.3
    **Instead, use**: "Geographic pose precise" (Type 57)
    **Purpose**: Represents the geographic pose, output from the relocation processing, expressed in decimal degrees
    notation (latitude, longitude & heading).
    **Format**: Concatenation of 3 single precision (32 bits) floats [lat, long, heading].
    * Single-precision floating-point (float32) : latitude in decimal degrees, range [ -90.0 .. 90.0 ]
    * Single-precision floating-point (float32) : longitude in decimal degrees, range [ -180.0 .. 180.0 ]
    * Single-precision floating-point (float32) : heading in decimal degrees, range [ 0.0 .. 360.0 [
    """
    GEOGRAPHIC_POSE = "geographic_pose"

    """
    Object Id 32 bits
    **Output when**: Tracking is enabled.
    **Format**: List of unsigned 32-bits integer.
    **Purpose**: Contains list of object IDs found by tracking.
    Each ID represents a distinct tracked object.
    The affectation of an ID to an object is arbitrary.
    The special value 0 is used to mean 'no object'.
    For instance, if the object ID of a point is 0, it means that this point does not belong to any object.
    """
    OBJECT_ID_32_BITS = "object_id_32_bits"

    """
    Zones Objects Binding 32 bits
    **Output when**: Tracking is enabled, and at least one zone has been defined.
    **Purpose**: This type is used to know with tracked objects are in which event zones.
    The binary payload is the concatenation of 0 to N couples of:
    * an unsigned 32-bits integer, representing the ID of an object (see 47)
    * an unsigned 32-bits integer, representing the index of the event zone (the n-th type 34 of type 33)
    Each object-zone couple means that the object is considered by the algorithm to be in the zone.
    """
    ZONES_OBJECTS_BINDING_32_BITS = "zones_objects_binding_32_bits"

    """
    Background bits
    Contains a padded list of bits, 1 bit per point of the cloud. If the bit is set, the point is a background point.
    The background is defined as the objects which were frequently detected in the past.
    On the contrary the foreground is composed of objects that were not seen before (i.e. they appeared recently and/or
    they are moving).
    """
    _BACKGROUND_BITS = "background_bits"

    """
    Ground plane bits
    Contains a padded list of bits, 1 bit per point of the cloud. If the bit is set, the point belongs to the ground.
    """
    _GROUND_PLANE_BITS = "ground_plane_bits"

    """
    Azimuths
    Contains list of azimuth coordinates.
    The definition of this angle can be found
    [here](https://docs.outsight.ai/software/coordinate-conventions#lidar-reference-frame).
    The azimuths are in degrees and expressed as single-precision floats. Several values are concatenated so the
    information of n points are given at once.
    The range of each value is [ 0.0 .. 360.0 [. 360.0 [.
    """
    _AZIMUTHS = "azimuths"

    """
    Elevations
    Contains list of elevation values in degrees expressed as single-precision floats.
    The definition of the elevation can be found
    [here](https://docs.outsight.ai/software/coordinate-conventions#lidar-reference-frame).
    The range is [ -90.0 .. +90.0 [.
    """
    _ELEVATIONS = "elevations"

    """
    Distances
    Contains list of distance values in meters expressed as single-precision floats.
    The definition of the distance can be found
    [here](https://docs.outsight.ai/software/coordinate-conventions#lidar-reference-frame).
    The range is [ 0.0 .. +inf [.
    """
    _DISTANCES = "distances"

    """
    LiDAR Model
    One unsigned 8-bits integer representing a model of LiDAR.
    * 0: Unknown
    * 1: Velodyne VLP16
    * 2: Velodyne VLP32
    * 3: Velodyne VLS128
    * 4: Velodyne HDL32
    * 5: Robosense BPearl v1
    * 6: Robosense BPearl v2
    * 7: Robosense RS32
    * 8: Robosense Helios
    * 9: Livox Horizon
    * 10: Livox Avia
    * 11: Livox Mid70
    * 12: Ouster
    * 13: Outsight SA01
    * 14: Hesai PandarXT32
    * 15: Hesai PandarQT64
    * 16: Random (fake LiDAR for testing)
    * 17: Hesai PandarXT32M2X
    * 18: Robosense M1
    """
    _LIDAR_MODEL = "lidar_model"

    """
    Slam Pose Array
    **Output when**: Tracking/objects_super_resolution is enabled.
    **Purpose**: Pose of tracked objects. It is similar to type 29 "Pose Array", but it is more accurate since
    it uses a SLAM algorithm and not just a box fitting algorithm.
    The position part follows an arbitrary point on the object, which is not necessarily its center.
    The orientation part is arbitrary for the first predicted pose, then follows the rotation of the object.
    The SLAM algorithm may not run on all tracked objects. When the SLAM does not run on an object,
    let say on object number 5, all floats of the related pose in this array, e.g. the fifth, are equal to zero.
    Moreover, the related element of type 39 "Object properties", e.g. the fifth, has its third bit equal to zero.
    **Format**: The binary payload is a repetition of the following content, one per tracked object:
    * single-precision floats Tx, Ty and Tz represent the translation vector T to get the position coordinates in
    meters.
    * single-precision floats Rxx, Rxy, Rxz, Ryx, Ryy, Ryz, Rzx, Rzy and Rzz represent the rotation matrix R defining
    the orientation.
    **Coordinate Frame**:
    Absolute/world, witch is:
    - Single-LiDAR: On-Ground LiDAR Coordinate Frame.
    - Multi-LiDARs: Map Coordinate Frame.
    """
    SLAM_POSE_ARRAY = "slam_pose_array"

    """
    Zone Vertical Limits
    **Output when**: Tracking is enabled, and at least a zone has been defined with Vertical Limits.
    **Format**: The binary value is the concatenation of:
    * one single-precision float, elevation, in meters
    * one single-precision float, height, in meters
    **Purpose**: Optional zone configuration which adds a filtering depending on the vertical position of objects.
    It is part of the definition of the zone.
    Only objects whose altitude is between elevation and elevation + height will be considered in the zone.
    """
    ZONE_VERTICAL_LIMITS = "zone_vertical_limits"

    """
    Geographic pose precise
    **Output when**: georeferencing is enabled.
    **Purpose**: Represents the geographic pose, output from the relocation processing, expressed in decimal degrees
    notation (latitude, longitude & heading).
    **Format**: Concatenation of 2 double precision (64 bits) and a single precision (32 bits) floats [lat, long,
    heading].
    * Double-precision floating-point (float64) : latitude in decimal degrees, range [ -90.0 .. 90.0 ]
    * Double-precision floating-point (float64) : longitude in decimal degrees, range [ -180.0 .. 180.0 ]
    * Single-precision floating-point (float32) : heading in decimal degrees, range [ 0.0 .. 360.0 [
    """
    GEOGRAPHIC_POSE_PRECISE = "geographic_pose_precise"

    """
    Road Markings bits
    Contains a padded (up to a byte) list of bits, 1 bit per point of the cloud. If the bit is set, the point belongs
    to a road marking.
    """
    _ROAD_MARKINGS_BITS = "road_markings_bits"

    """
    Filtered Pose
    **Output when**: Ego-motion is enabled.
    **Purpose**: Filtered pose of the LiDAR, in order to smooth out the discrepancies.
    **Format**: Concatenation of 12 floats of 32-bits each, see type Pose for more details.
    """
    FILTERED_POSE = "filtered_pose"

    """
    Interactive Request
    A Request to a device, where a Timestamp and a Request ID are mandatory.
    """
    _INTERACTIVE_REQUEST = "interactive_request"

    """
    Interactive Response
    A Response made by a device.
    """
    _INTERACTIVE_RESPONSE = "interactive_response"

    """
    Interactive Request ID
    An ID to identify to which request is associated the response.
    **Format**: unsigned 32-bits integer.
    """
    _INTERACTIVE_REQUEST_ID = "interactive_request_id"

    """
    Interactive Request Background Header
    Request background header.
    """
    _INTERACTIVE_REQUEST_BACKGROUND_HEADER = "interactive_request_background_header"

    """
    Interactive Response Background Header
    Response background header.
    """
    _INTERACTIVE_RESPONSE_BACKGROUND_HEADER = "interactive_response_background_header"

    """
    Interactive Request Background Data
    Request background data.
    """
    _INTERACTIVE_REQUEST_BACKGROUND_DATA = "interactive_request_background_data"

    """
    Interactive Response Background Data
    Response background data.
    """
    _INTERACTIVE_RESPONSE_BACKGROUND_DATA = "interactive_response_background_data"

    """
    Interactive Request PingPong
    Request pingpong.
    **Format**: binary payload
    """
    _INTERACTIVE_REQUEST_PINGPONG = "interactive_request_pingpong"

    """
    Interactive Response PingPong
    Response pingpong.
    **Format**: The same binary payload as in the request
    """
    _INTERACTIVE_RESPONSE_PINGPONG = "interactive_response_pingpong"
