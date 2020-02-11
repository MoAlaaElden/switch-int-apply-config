#!/usr/bin/env python3

"""
A simple script to apply interface-level configuration to all interface in particular VLAN

Files:
ise-switch-int-apply-config.py - main script
connect_to_device.py - includes functions: ping and connect SSH/Telnet to the device
devices.csv - list of IP addresses
local.py - credentials
config_intf_ise.txt - configuration commands that need to be applied

(C) 2019 Dmitry Golovach
email: dmitry.golovach@outlook.com
"""

# Imports
from ciscoconfparse import CiscoConfParse
import ipaddress
import pandas as pd
import sys
import time
import threading
import json

# Imports custom created modules
import connect_to_device


# Module Functions and Classes

class Device:
    """Creating the class with:

        self.current_ip_address - IP address
        self.current_index - index from devices.csv
        self.vlan_id - VLAN number to apply config at

        Methods:
            def collect_interfaces - method to collect all interfaces in particular VLAN (vlan_id)
            def init_connection - initiate SSH connection to the device
            def close_connection - close SSH connection to the device
            def apply_intf_config - apply configuration to port in vlan_id
    """

    def __init__(self, current_ip_address, current_index, vlan_id):
        self.current_ip_address = current_ip_address
        self.current_index = current_index
        self.vlan_id = vlan_id

    def collect_interfaces(self):
        self.connection.send_command("term len 0")
        run_config = self.connection.send_command("show startup-config")
        cisco_cfg = CiscoConfParse(run_config.splitlines())
        pattern = r'^\sswitchport\saccess\svlan\s' + str(self.vlan_id)
        intf_name = [obj.text for obj in cisco_cfg.find_objects(r"^interf") if obj.re_search_children(pattern)]
        return intf_name

    def apply_intf_config(self, intf_name):
        with open('config_intf_ise.txt') as f:
            commands_lines = f.read()
        intf_config = commands_lines.split('\n')
        for intf in intf_name:
            intf_config.insert(0, intf)
            self.connection.send_config_set(intf_config)
            del intf_config[0]
        self.connection.send_command("write mem")


    def init_connection_ssh(self):
        self.connection = connect_to_device.try_to_connect_ssh(self.current_ip_address)

    def close_connection(self):
        self.connection.disconnect()

    @staticmethod
    def write_result(current_ip_address):
        dict_result = {
            'ip': current_ip_address,
            'comment': 'Comment OK'
        }
        with open('device-result.json', 'a') as f_obj:
            f_obj.write(json.dumps(dict_result, indent=4))
        return


def main(current_ip_address, current_index, vlan_id):
    ping_result = connect_to_device.ping_device(current_ip_address)
    if not ping_result:
        return
    else:
        device = Device(current_ip_address, current_index, vlan_id)
        device.init_connection_ssh()
        intf_name = device.collect_interfaces()
        device.apply_intf_config(intf_name)
        device.write_result(current_ip_address)
        device.close_connection()

    return

# Check to see if this file is the "__main__" script being executed
if __name__ == "__main__":
    start_time = time.time()

    threads = []
    if len(sys.argv) == 3:
        try:
            ipaddress.ip_address(sys.argv[1])
            # pass only IP address of the device
            current_index = 0
            main(sys.argv[1], current_index, sys.argv[2])
        except ValueError:
            df = pd.read_csv(sys.argv[1])
            for current_index in df.index:
                thread = threading.Thread(target=main, args=(df['ip'][current_index], current_index, sys.argv[2]))
                threads.append(thread)
                thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join()


    else:
        raise SyntaxError("Insufficient arguments.")

    print(time.time() - start_time)
