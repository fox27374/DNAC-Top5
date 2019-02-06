#!/usr/bin/env python
from __future__ import print_function
import sys
import json
from argparse import ArgumentParser
from util import get_url

def list_single_device(ip):
    return get_url("network-device/ip-address/%s" % ip)

def list_network_devices():
    return get_url("network-device")

def create_filtered_list(response):
    f_list=[]
    for device in response['response']:
        if args.hostname and args.hostname in device['hostname']:
            f_list.append(device)
        if args.ip and args.ip in device['managementIpAddress']:
            f_list.append(device)
        if args.serial and args.serial in device['serialNumber']:
            f_list.append(device)
        if args.platform and args.platform in device['platformId']:
            f_list.append(device)
        if args.version and args.version in device['softwareVersion']:
            f_list.append(device)
    return f_list

if __name__ == "__main__":
    parser = ArgumentParser(description='Filter results based on the device attributes containing the supplied string. Multiple filters behave in an OR manner.')
    parser.add_argument('-H', '--hostname', type=str, help="Hostname")
    parser.add_argument('-i', '--ip', type=str, help="IP Address")
    parser.add_argument('-s', '--serial', type=str, help="Serial")
    parser.add_argument('-p', '--platform', type=str, help="Platform")
    parser.add_argument('-v', '--version', type=str, help="Software Version")
    args = parser.parse_args()
    
    # Get device list
    response = list_network_devices()
    print("\n"
            )
    # Print header
    print("{0:32}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format("Hostname", "IP Address", "Serial", "Platform", "SW Version", "Role", "Uptime"))

    # Check if filters are applied
    if len(sys.argv) <= 1:
        filtered_list = response['response']
    else:
        filtered_list = create_filtered_list(response)

    for device in filtered_list:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if  device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        for (serialNumber,platformId) in serialPlatformList:
            # Print list
            print("{0:32}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(device['hostname'],
                         device['managementIpAddress'],
                         serialNumber,
                         platformId,
                         device['softwareVersion'],
                         device['role'],
                         uptime))
