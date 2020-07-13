import pprint
import pandas as pd
import numpy as np
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
#from meraki_sdk.exceptions.api_exception import APIException

# x_cisco_meraki_api_key = '1f7c1eab553c0e70ca80c7d3c6168c643131d258'
# api_key = input("Provide the API key associated with your account: ")

api_key = input("Provide the API key associated with your account: ")
meraki = MerakiSdkClient(api_key)


def getorgs():
    # Get organizations - Return list of organizations and IDs
    orgs = meraki.organizations.get_organizations()
    print('The organizations associated to this API KEY are: ')
    pp = pprint.PrettyPrinter(indent=5, )
    pp.pprint(orgs)


def getnetworks():
    organization = input("Which organization's networks would you like to see?\n  " +
                         "Results will be formatted in alphabetic order: ")
    params = {"organization_id": organization}
    nets = meraki.networks.get_organization_networks(params)
    #    print(type(nets))
    sorted_nets = sorted(nets, key=lambda x: x['name'])
    pprint.pprint(sorted_nets)


def getdevices():
    net_id: str = input("Provide network ID for network whose devices you would like to see:\n " +
                        "Results will be formatted in alphabetic order: ")
    devices = meraki.devices.get_network_devices(net_id)
    pprint.pprint(devices)
    print('Devices will be grouped by name')
    net_dv = pd.DataFrame(devices, columns=['name', 'firmware', 'serial'])
    print(net_dv.to_string())


def getswitchports():
    selected_serial: str = input('Input the serial number of the device which switchports you would like to see\n')
    switch_ports = meraki.switch_ports.get_device_switch_ports(selected_serial)
    sorted_ports = pd.DataFrame(switch_ports, columns=['name', 'number', 'type', 'vlan'])
    print(sorted_ports.to_string())


def testloopcondition(condition):
    answer: str = input('Would you like to check a different network/device? Press Y/N')
    if answer in ['y', 'Y']:
        condition = True
    elif answer in ['n', 'N']:
        condition = False


getorgs()
getnetworks()
getdevices()

condition = True
while condition:
    selection = int(input('Would you like to see switchports on a particular device? Press 1\n'))
    if selection == 1:
        print('Getting switchports\n')
        getswitchports()