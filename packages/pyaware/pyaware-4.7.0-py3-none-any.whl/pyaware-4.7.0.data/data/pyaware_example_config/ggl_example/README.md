# GGL Example Configuration
## Folder Structure
A generic folder structure is shown below that details the path each config file should be found in. Starting at the 
AWAREPATH i.e. `/etc/AWARE` (on Linux).
```console
.
└── config
    ├── connection.yaml
    └── gateway.yaml
```
### Config
The "config" folder contains "gateway.yaml" (device and pyaware configuration) and connection.yaml (mqtt configuration). 

"connection.yaml" in this example contains the following information:
* The minimum configuration to establish connection to a local mqtt instance. This includes, device_id.
* Change in host IP Address
* Additional serial number identifier
* Updated MQTT parser example to either edit or add new mqtt topics to pyaware.

"gateway.yaml" contains the configuration required to interface to an [iMAC2](https://www.ampcontrolgroup.com/wp-content/uploads/2017/05/iMAC2-System-User-Manual.pdf),
* Pinned AWARE version
* Modbus TCP interface
* Modbus RTU interface
* iMAC2 auto detect device configuration 
  
For more information about how to construct these config files, please see the main README.md file.
