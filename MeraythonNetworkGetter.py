import pprint
import pandas as pd
import numpy as np
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
import requests
from meraki_sdk.exceptions.api_exception import APIException
import getpass
import time
import json

api_key = input('Provide the API key associated with your account: ')
# key = json(api_key)
meraki = MerakiSdkClient(api_key)


def mainmenu():
    answer = True
    while True:

        condition = True

        while True:
            purpose = int(input('\nTo view organizations, their networks & devices, press 1\n'
                                'Would you like to manage/update switches, firewalls, or access points?\n' +
                                'For switches, press 2 & hit enter\n' + 'For firewalls, press 3 & hit enter\n' +
                                'For MX vlans, press 4 & hit enter \n'))
            if purpose == 1:
                networkmenu()
            elif purpose == 2:
                switchportmenu()
            elif purpose == 3:
                firewallmenu()
            elif purpose == 4:
                vlanmenu()


def networkmenu():
    getorgs()

    answer = int(input('To view all networks within an organization, press 1\n'
                        + 'To view all devices within a network, press 2\n If you are unsure of'
                          ' your devices network ID, press 1 first\n' + 'For main menu, press 3\n'))
    if answer == 1:
        getnetworks()
    elif answer == 2:
        getdevices()
    elif answer == 3:
        mainmenu()


def getorgs():
    # Get organizations - Return list of organizations and IDs
    orgs = meraki.organizations.get_organizations()
    organizations = pd.DataFrame(orgs, columns=['name', 'id'])
    print('The organizations associated to this API KEY are: ')
    # pp = pprint.PrettyPrinter(indent=5, )
    # pp.pprint(orgs)
    print(organizations.to_string())

    time.sleep(2)
    print('\n')
    for row in organizations.itertuples(index=True, name='Pandas'):
        try:
            params = {'organization_id': getattr(row, 'id')}
            print(params)
            nets = meraki.networks.get_organization_networks(params)
            org_nets = pd.DataFrame(nets, columns=['name', 'id', 'type'])
            print('Networks within ' + getattr(row, 'name') + ' organization:\n')
            print(org_nets.to_string())

        except:
            pass


def getnetworks():
    organization = input("Which organization's networks would you like to see?\n  " +
                         "Results will be formatted in alphabetic order: ")
    params = {"organization_id": organization}
    nets = meraki.networks.get_organization_networks(params)
    org_nets = pd.DataFrame(nets, columns=['name', 'id', 'type'])
    # sorted_nets = sorted(org_nets, key=lambda x: x['name'])
    # pprint.pprint(sorted_nets)

    print(org_nets.to_string())


def getdevices():
    net_id: str = input('\nProvide network ID for network whose devices you would like to see:\n')
    devices = meraki.devices.get_network_devices(net_id)
    # pprint.pprint(devices)
    print('\nDevices will be grouped by firmware\n')
    net_dv = pd.DataFrame(
        devices)  # columns=['name', 'firmware', 'serial', 'networkID', 'lanIp', 'mac', 'model', 'notes'])
    print(net_dv.to_string())


def switchportmenu():
    selection = int(input('Would you like to see switchports on a particular device? Press 1\n' +
                          'Press 2 to update switchport settings\n' + '\nIf you want to update '
                                                                      'and are unsure of serial/portId, '
                                                                      'press 1 to view switchports first\n'
                                                                      'or Press 3 to exit to main menu\n'))
    if selection == 1:
        print('Getting switchports\n')
        getswitchports()
    elif selection == 2:
        print('Updating switchport...')
        selection = int(input('1 to update the name\n' +
                              '2 to update the vlan\n'))
        if selection == 1:
            print('Updating switchport name...')
            updateswitchportname()
        elif selection == 2:
            print('Updating switchport vlan...')
            updateswitchportvlan()
    elif selection == 3:
        mainmenu()


def getswitchports():
    selected_serial: str = input('Input the serial number of the device which switchports you would like to see\n')
    switch_ports = meraki.switch_ports.get_device_switch_ports(selected_serial)
    sorted_ports = pd.DataFrame(switch_ports, columns=['name', 'number', 'type', 'vlan'])
    print(sorted_ports.to_string())


def updateswitchportname():
    selected_serial: str = input('Input the serial number of the device which switchport vlan '
                                 'you would like to change\n')
    selected_number: str = input('Input the port ID of the port which name you want to change\n')
    name: str = input('Input the name you would like to assign to this switchport\n')
    api = api_key
    # api: str = input('Input your API key\n')
    url = f"https://api.meraki.com/api/v0/devices/{selected_serial}/switchPorts/{selected_number}"

    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}
    # headers = {'X-Cisco-Meraki-API-Key': ''}
    # {"Content-Type: application/json"}

    r = requests.put(url, data={"name": f"{name}"}, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated port settings: \n')
    pprint.pprint(r.content)


def updateswitchportvlan():
    selected_serial: str = input('Input the serial number of the device which switchport vlan '
                                 'you would like to change\n')
    selected_number: str = input('Input the port ID of the port which VLAN you want to change \n')
    new_vlan_id: str = input('Input the vlan ID you would like to assign to this switchport\n')
    api = api_key
    url = f"https://api.meraki.com/api/v0/devices/{selected_serial}/switchPorts/{selected_number}"

    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.put(url, data={"vlan": f"{new_vlan_id}"}, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated port settings: \n')
    pprint.pprint(r.content)


def firewallmenu():
    selection = int(input('Would you like to see VLAN settings on all MX ports? Press 1\n' +
                          'Press 2 to update MX VLAN port settings\n' + '\nIf you want to update '
                                                                        'and are unsure of portId, '
                                                                        'press 1 to view ports first\n'
                                                                        'or Press 3 to exit to main menu\n'))
    if selection == 1:
        print('Getting MX ports\n')
        getmxports()
    elif selection == 2:
        print('Updating MX VLAN port...')
        selection = int(input('1 to update the assigned vlan on a port\n' +
                              '2 to update allowed vlans on a port\n'))
        if selection == 1:
            print('Updating port vlan...')
            updateMXvlanport()
        elif selection == 2:
            print('Updating allowed vlans on port...')
            updateMXallowedvlans()
    elif selection == 3:
        mainmenu()


def getmxports():
    selected_netid: str = input('\nInput the network ID to see MX vlan port settings\n')
    api = api_key
    url = f"https://api.meraki.com/api/v0/networks/{selected_netid}/appliancePorts"
    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.get(url, headers=headers)
    port_settings = pd.DataFrame(r)  # columns=['number', 'enabled', 'type',
    # 'dropUntaggedTraffic', 'vlan', 'allowedVlans'])
    print(port_settings.to_string())


def updateMXvlanport():
    selected_net: str = input('\nInput the network ID to update MX vlan port\n')
    selected_port: str = input('\nInput the port ID which port vlan you want to update\n')
    new_vlanid: str = input('\nInput new vlan to be assigned to selected port\n')
    api = api_key
    url = f'https://api.meraki.com/api/v0/networks/{selected_net}/appliancePorts/{selected_port}'
    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.put(url, data={"vlan": f"{new_vlanid}"}, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated port settings: \n')
    pprint.pprint(r.content)


def updateMXallowedvlans():
    selected_net: str = input('\nInput the network ID to update MX vlan port\n')
    selected_port: str = input('\nInput the port ID to update allowed vlans\n')
    new_allowedvlans: str = input('\nInput the allowed vlans for this port. If using multiple vlans,\n'
                                  + 'please input as commma-delimited list. To allow all vlans, type all\n')
    api = api_key
    url = f'https://api.meraki.com/api/v0/networks/{selected_net}/appliancePorts/{selected_port}'
    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.put(url, data={"allowedVlans": f"{new_allowedvlans}"}, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated port settings: \n')
    pprint.pprint(r.content)


def vlanmenu():
    selection = int(input('Would you like to list all vlans in a MX network? Press 1 & hit enter\n'
                          + 'To update an existing vlan, press 2 & hit enter\n' + 'To add a new vlan'
                                                                                  'press 3 & hit enter\n'
                          + 'Press 4 to exit to main menu\n'))
    if selection == 1:
        print('Getting all vlans in the network...\n')
        getMXvlans()
    elif selection == 2:
        choice = int(input('Update name? press 1 & enter\n' + 'Update subnet? press 2 & hit enter\n'
                           + 'Update appliance IP? press 3 & hit enter\n'))
        if choice == 1:
            updateMXvlanname()
        if choice == 2:
            updateMXvlansubnet()
        elif choice == 3:
            updateMXvlanIP()

    elif selection == 3:
        print('Adding new vlan...\n')
        addMXvlan()
    elif selection == 4:
        mainmenu()



def getMXvlans():
    selected_netid: str = input('\nInput the network ID to see all vlans on MX network\n')
    api = api_key
    url = f"https://api.meraki.com/api/v0/networks/{selected_netid}/vlans"
    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.get(url, headers=headers)
    port_settings = pd.DataFrame(r)  # columns=['number', 'enabled', 'type',
    # 'dropUntaggedTraffic', 'vlan', 'allowedVlans'])
    print(port_settings.to_string())


def updateMXvlanname():
    selected_network: str = input('Input the MX network containing the vlan you would like to update\n')
    selected_vlan: str = input('Input the vlan ID of the vlan which you want to update\n')
    new_vlan_name: str = input('Input the name you would like to assign to this vlan\n')

    api = api_key
    url = f"https://api.meraki.com/api/v0/networks/{selected_network}/vlans/{selected_vlan}"

    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.put(url, data={"name": f"{new_vlan_name}"}, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated port settings: \n')
    pprint.pprint(r.content)


def updateMXvlansubnet():
    selected_network: str = input('Input the MX network containing the vlan you would like to update\n')
    selected_vlan: str = input('Input the vlan ID of the vlan which you want to update\n')
    new_vlan_subnet: str = input('Input the subnet you would like to assign to this vlan\n')

    api = api_key
    url = f"https://api.meraki.com/api/v0/networks/{selected_network}/vlans/{selected_vlan}"

    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.put(url, data={"subnet": f"{new_vlan_subnet}"}, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated port settings: \n')
    pprint.pprint(r.content)


def updateMXvlanIP():
    selected_network: str = input('Input the MX network containing the vlan you would like to update\n')
    selected_vlan: str = input('Input the vlan ID of the vlan which you want to update\n')
    new_vlan_ip: str = input('Input the IP you would like to assign to this vlan\n')

    api = api_key
    url = f"https://api.meraki.com/api/v0/networks/{selected_network}/vlans/{selected_vlan}"

    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.put(url, data={"applianceIP": f"{new_vlan_ip}"}, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated port settings: \n')
    pprint.pprint(r.content)


def addMXvlan():
    selected_network: str = input('Input the MX network to add vlan to\n')
    vlanid: str = input('vlan ID: ')
    vlanname: str = input('vlan name: ')
    vlansubnet: str = input('vlan subnet: ')
    vlanapplianceip: str = input('vlan appliance ip: ')

    api = api_key
    url = f"https://api.meraki.com/api/v0/networks/{selected_network}/vlans"

    data = {"id": f"{vlanid}", "name": f"{vlanname}", "subnet": f"{vlansubnet}",
            "applianceIp": f"{vlanapplianceip}", "groupPolicyId": None}

    headers = {'X-Cisco-Meraki-API-Key': f'{api}'}

    r = requests.post(url, data=data, headers=headers)

    with open('content.txt', 'w') as fd:
        fd.write(r.text)
    print('Updated MX vlan: \n')
    pprint.pprint(r.content)

    # getMXvlans()


mainmenu()
