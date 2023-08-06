# Protocol Buffer structure for Speos
Python package containing protocol buffer structure for Speos APIs.
## Directory structure
    - ansys
        |---- api
        |       |---- speos
        |       |       |-- api-example1
        |       |       |       |-- v1
        |       |       |       |   |-- service1_pb2.py
        |       |       |       |   |-- service1_pb2_grpc.py
        |       |       |       |   |-- service2_pb2.py
        |       |       |       |   |-- service2_pb2_grpc.py
        |       |       |       |-- v2
        |       |       |       |   |-- service2_pb2.py
        |       |       |       |   |-- service2_pb2_grpc.py

## What's new
### 2.0.1

### 1.0.0
`LTF API v1` available in *ansys/api/speos/LTF/v1*

With the following service:
* `LTF` - service to create, open, modify and save *.OPTDistortion files


`lpf API v1` available in *ansys/api/speos/lpf/v1*

With the following service:
 * `lpf_file_reader` - service to read lpf file and get all its RayPath


`xmp API v1` available in *ansys/api/speos/xmp/v1*

With the following service:
 * `xmp_file` - service to manage xmp file


`bsdf API v1` available in *ansys/api/speos/bsdf/v1*

With the following services:
 * `anisotropic_bsdf` - service to create, open, modify and save *.anisotropicbsdf files
 * `bsdf_creation` - service to create, open, modify and save *.brdf files
 * `spectral_bsdf` - service to assemble *.anisotropicbsdf or *.brdf files into .bsdf180 files<br/>
   or isotropic *.anisotropicbsdf to anisotropic *.anisotropicbsdf files<br/>
   or isotropic *.anisotropicbsdf to spectral *.brdf files

