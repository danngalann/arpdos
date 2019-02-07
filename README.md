# arpDoS
A python script to DoS every device on the network (except yourself ;))

## How it works
* Use ARP to scan the whole network searching for devices
* Store all those devices in a list
* Erase some devices from that list (you and those on the exceptions file)
* Go through every device and tell it that the gateway is at a random MAC


## Requirements
This script will require
* Scapy for Python (see [installing Scapy](#installing-scapy))
* Root privileges

## Usage
```
usage: arpDoS.py [-h] [-i INTERFACE] [-n NETWORK] [-g GATEWAY] [-f FILE]

a command line tool to DoS all devices on a network (except yourself :D)

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        Interface to use
  -n NETWORK, --network NETWORK
                        Network to DoS
  -g GATEWAY, --gateway GATEWAY
                        Gateway IP
  -f FILE, --file FILE  List of IPs to exclude from the attack (one per line)
```

## Installing Scapy
To install scapy open a terminal and type
```
pip3 install scapy
```

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE) for details

## Additional notes
This script **only works on Linux** and **must be executed with root privileges**
