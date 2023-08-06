# TopgreenerApi
## _Control Topgreener devices from the cloud_

TopgreenerApi allows control of devices added to the Topgreener mobile app from Python. The library implements the "new" Tuya cloud mobile API. Currently, support is limited to dimmer switches, though other devices can be added relatively easily by adding new service calls to the "Device" module. 

## Features

- Login to Tuya's cloud API using Topgreener's account
- Get all configured locations
- Get all configured devices
- Set device power state
- Set device brightness level

## Installation

TopgreenerApi can be installed using pip as follows:
```sh
pip install topgreenerapi
```
Once installed, you can create a new instance of TopgreenerCloud as follows:
```python
 api = TopgreenerCloud(client_id, app_secret, super_secret, app_certhash)
```
To find the correct values for these secret keys, take a look at this repository:  
[https://github.com/nalajcie/tuya-sign-hacking][PlDb]

## License

MIT
