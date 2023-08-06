# Local MQTT Example Configuration
## Folder Structure
A generic folder structure is shown below that details the path each config file should be found in. Starting at the 
AWAREPATH i.e. `/etc/AWARE` (on Linux).
```console
.
└── config
    ├── connection.yaml
    ├── gateway.yaml
    └── test_dev.yaml
```
### Config
The "config" folder contains "gateway.yaml" (device and pyaware configuration), connection.yaml (mqtt configuration) 
and "test_dev.yaml" (device parameter configuration). 

"connection.yaml" in this example contains the following information:
* The minimum configuration to establish connection to a local mqtt instance. This includes, device_id.

"gateway.yaml" in this example contains,
* The configuration for a simple modbus device
* Path linking to a test modbus device

"test_dev.yaml" in this example contains,
* The parameter configuration for a simple modbus device with holding and input registers. 
  
For more information about how to construct these config files, please see the main README.md file.
