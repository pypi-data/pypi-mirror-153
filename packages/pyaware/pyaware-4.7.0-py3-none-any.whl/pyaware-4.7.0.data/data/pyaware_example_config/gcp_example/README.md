# Google Cloud Platform (GCP) Example Configuration
## Folder Structure
A generic folder structure is shown below that details the path each config file should be found in. Starting at the 
AWAREPATH i.e. `/etc/AWARE` (on Linux).
```console
.
├── config
|   ├── connection.yaml
|   ├── gateway.yaml
|   └── test_dev.yaml
└── credentials
    ├── google_roots.pem
    └── rsa_private.pem
```
### Config
The "config" folder contains "gateway.yaml" (device and pyaware configuration), "connection.yaml" (mqtt configuration)
and "test_dev.yaml" (device parameter configuration). 

"connection.yaml" in this example contains,
* The minimum information to establish an mqtt connection with GCP. This includes, defaults, cloud_id, project_id and
registry_id.

"gateway.yaml" in this example contains,
* The configuration for a simple modbus device
* Path linking to a test modbus device

"test_dev.yaml" in this example contains,
* The parameter configuration for a simple modbus device with holding and input registers.

For more information about how to construct these config files, please see the main README.md file.

### Credentials
The "credentials" folder contains the information for authentication to the GCP. It contains a copy of "google_roots.pem"
 (the Google Root Certificate found [here](https://pki.google.com/roots.pem)), and a copy of a private key(details on how
to do this are found [here](https://cloud.google.com/iot/docs/how-tos/credentials/keys)). For example purposes only the
files found in the path are empty.
