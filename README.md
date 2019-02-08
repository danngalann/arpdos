# arpDoS
A python script to DoS every device on the network (except yourself ;))

## How it works _(roughly)_
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
usage: arpDoS.py [-h] [-i INTERFACE] [-n NETWORK] [-g GATEWAY] [-f FILE] [-m]

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
  -m, --mitm            Use MITM instead
```

## An explanation on -m
This script works by telling all devices that the gateway is at a random MAC. It's programmed like a MITM only there's nothing at that address to process the data so the requests never get to the gateway.

The -m option will use _your_ MAC address instead, and will enable IP forwarding in your computer so the data _does_ get to the gateway, through you.

You're basically MITM-ing the entire network. _(Make sure your computer can handle it though)_

## Installing Scapy
To install scapy open a terminal and type
```
pip3 install scapy
```
## Disclaimer
This project is a proof of concept for testing and educational purposes.
It's meant to be used against networks you have permission to tamper with.

I don't take any responsibility for what you do with this program.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE) for details

## Additional notes
This script **only works on Linux** and **must be executed with root privileges**
