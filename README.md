# MeraythonNetworkGetter

 Meraki Interactive CLI Tool - Securely Retrieves secrets from secret server and allows for CLI query of big Meraki networks with several 100s of appliances 



## Features

1. Securely retrieves dashboard password from Secret Server with OTP and access token
2. Interactive menu that will display devices and/or networks based on organization or device type (firewall, switches, access points)
3. Devices will be output with their associated network and type and serial
4. Options to update/change switch port names, switch port VLAN, MX VLAN ports, MX allowed VLANS, MX VLAN names, MX VLAN subnets, MX VLAN IPs, and to add MX VLANS to a network
5. Any changes or updates create an output of the updates/changes made and the new device/network settings




## Libraries Used - Python

- pprint
- pandas
- numpy
- MerakiSdkClient
- requests
- getpass
- time
- json
