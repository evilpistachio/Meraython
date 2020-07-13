import pprint
import pandas as pd
import numpy as np
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
from meraki_sdk.exceptions.api_exception import APIException

# x_cisco_meraki_api_key = ''
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
    sorted_nets = pd.DataFrame(nets, columns=['name', 'id', 'productTypes', 'type'])
    # sorted_nets = sorted(nets, key=lambda x: x['name'])
    # pprint.pprint(sorted_nets)
    # sorted_nets.sort_values('name')
    print(sorted_nets.sort_values('name').to_string())


def getdevices():
    net_id: str = input("Provide network ID for network whose devices you would like to see:\n " +
                        "Results will be formatted in alphabetic order: ")
    devices = meraki.devices.get_network_devices(net_id)

    print('Devices will be grouped by name')
    net_dv = pd.DataFrame(devices, columns=['name', 'firmware', 'serial', 'networkId'])
    print(net_dv.to_string())


def getswitchports():
    selected_serial: str = input('Input the serial number of the device which switchports you would like to see\n')
    switch_ports = meraki.switch_ports.get_device_switch_ports(selected_serial)
    sorted_ports = pd.DataFrame(switch_ports)#, columns=['name', 'number', 'type', 'cdp/lldp', 'vlan'])
    print(sorted_ports.to_string())


def get_network_vlans():
    network_id: str = input("Provide network ID for network device which vlans you'd like to see")
    vlans_controller = meraki.vlans
    result = vlans_controller.get_network_vlans(network_id)
    pprint.pprint(result)


def testloopcondition(condition):
    answer: str = input('Would you like to check a different network/device? Press Y/N')
    if answer in ['y', 'Y']:
        condition = True
    elif answer in ['n', 'N']:
        condition = False

    # condition = True


getorgs()
getnetworks()
getdevices()

condition = True
while condition:
    selection = int(input('Would you like to see switchports on a particular device? Press 1\n' +
                          'Or see all vlans within this network? Press 2\n'))
    if selection == 1:
        print('Getting switchports\n')
        getswitchports()
    elif selection == 2:
        print('Getting vlans\n')
    get_network_vlans()
        #get_network_vlans(self,network_id=input("Provide network ID for network device which vlans you'd like to see"))
testloopcondition(condition)
