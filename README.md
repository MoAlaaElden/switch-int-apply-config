# Cisco Apply config to interfaces in particular VLAN
> A simple script to apply interface-level configuration to all interface in particular VLAN.
> You specify the IP address of switch or list of switches, commands that need to be pushed and vlan

Files:
* ise-switch-int-apply-config.py - main script
* connect_to_device.py - includes functions: ping and connect SSH/Telnet to the device
* devices.csv - list of IP addresses
* local.py - credentials
* config_intf_ise.txt - configuration commands that need to be applied
* device-result.json - stores results of running script

## Technologies
* Python3
* Cisco IOS switches

## Setup
python ise-switch-int-apply-config.py <IP_address> <vlan_id>

python ise-switch-int-apply-config.py device.csv <vlan_id>

Examples:
* python ise-switch-int-apply-config.py devices.csv 10
* python ise-switch-int-apply-config.py 10.10.10.10 10

How it works
* Breakdown post [here](https://dmitrygolovach.com/python-apply-config-to-multiple-interfaces/)
* How it works [youtube](https://youtu.be/DfhimzoWDJA)

## Contact
* Created by Dmitry Golovach
* Web: [https://dagolovachgolovach.com](https://dmitrygolovach.com) 
* Twitter: [@dagolovach](https://twitter.com/dagolovach)
* LinkedIn: [@dmitrygolovach](https://www.linkedin.com/in/dmitrygolovach/)

- feel free to contact me!