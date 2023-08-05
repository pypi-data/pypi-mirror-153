# OSEF library

Library containing utilities to read and parse a stream, live or recorded, retrieved from an
**ALB** (**A**ugmented **L**iDAR **B**ox).

The stream is in the **OSEF** format (**O**pen **SE**rialization **F**ormat):
it's an Outsight-defined serialisation binary format used to encode data streaming out of the ALB. 
It is based on *TLV-encoding*.

For the full documentation, contact us @ https://support.outsight.ai

## Installation
Install from PyPi using pip:
```bash
pip install osef
``` 
## Usage
Open and parse an osef file or stream: 

```python
import osef

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

frame_iterator = osef.parser.parse(osef_path)
for frame_dict in frame_iterator:
    tracked_objects = frame_dict["timestamped_data"]["scan_frame"]["tracked_objects"]
```

By default, the parser processes the recorded data as quickly as your computer allows it,
so potentially faster than in real conditions. 
To process recorded data at the same pace as real time OSEF stream coming from an ALB,
set the parameter real_frequency = True
```python
frame_iterator = osef.parser.parse(osef_path, True)
```

or
```python
import osef

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

with osef.parser.OsefStream(osef_path) as osef_stream:
    tlv_iterator = osef.parser.get_tlv_iterator(osef_stream)
    for index, tlv in tlv_iterator:
        tree = osef.parser.build_tree(tlv)
        frame_dict = osef.parser.parse_to_dict(tree)
        tracked_objects = frame_dict["timestamped_data"]["scan_frame"]["tracked_objects"]
```

To find more code samples, see Outsight Code Samples repository:
https://gitlab.com/outsight-public/outsight-code-samples/-/tree/master