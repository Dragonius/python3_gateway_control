import argparse
import miniupnpc
import natpmp

def list_upnp_port_mappings():
    """Discovers UPnP devices and lists open ports."""
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 200
    num_devices = upnp.discover()

    if num_devices == 0:
        print("No UPnP devices found. Ensure your router supports UPnP and it is enabled.")
        return
    
    upnp.selectigd()
    print(f"Discovered UPnP device. External IP: {upnp.externalipaddress()}")

    i = 0
    while True:
        mapping = upnp.getgenericportmapping(i)
        if mapping is None:
            break
        print(f"Mapping {i}: {mapping}")
        i += 1

def upnp_port_forward(protocol, external_port, internal_port, internal_ip, description):
    """Adds a UPnP port mapping."""
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 200
    upnp.discover()
    upnp.selectigd()
    
    print(f"External IP: {upnp.externalipaddress()}")
    print(f"Adding port forwarding: {protocol} {external_port} -> {internal_ip}:{internal_port}")
    
    upnp.addportmapping(
        external_port, protocol, internal_ip, internal_port, description, ''
    )
    print("Port mapping added successfully!")

def remove_upnp_mapping(protocol, external_port):
    """Removes a UPnP port mapping."""
    upnp = miniupnpc.UPnP()
    upnp.discover()
    upnp.selectigd()
    
    print(f"Removing port mapping: {protocol} {external_port}")
    upnp.deleteportmapping(external_port, protocol)
    print("Port mapping removed successfully!")

def list_nat_pmp_port_mappings():
    """Lists NAT-PMP port mappings (limited information)."""
    client = NATPMPClient()
    public_ip = client.get_public_address().public_ip
    print(f"NAT-PMP Gateway Public IP: {public_ip}")
    print("NAT-PMP does not support full port listing; you must manually manage mappings.")

def nat_pmp_forward(protocol, private_port, public_port, lifetime):
    """Adds a NAT-PMP port mapping."""
    client = NATPMPClient()
    proto_code = 1 if protocol == "UDP" else 0
    response = client.addportmapping(proto_code, private_port, public_port, lifetime)
    print(f"NAT-PMP: Mapped port {public_port} -> {private_port}")
    print(f"External IP: {client.publicaddress().publicip}")

def nat_pmp_remove(protocol, private_port, public_port):
    """Removes a NAT-PMP port mapping."""
    client = NATPMPClient()
    proto_code = 1 if protocol == "UDP" else 0
    client.addportmapping(proto_code, private_port, public_port, 0)
    print(f"NAT-PMP: Removed mapping for port {public_port}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control UPnP and NAT-PMP gateway port forwarding.")
    parser.add_argument("--protocol", choices=["TCP", "UDP"], default="TCP", help="Protocol to use.")
    parser.add_argument("--external-port", type=int, help="External port for mapping.")
    parser.add_argument("--internal-port", type=int, help="Internal port for mapping.")
    parser.add_argument("--internal-ip", type=str, help="Internal IP address (UPnP only).")
    parser.add_argument("--description", type=str, default="Python Port Mapping", help="Description for the mapping.")
    parser.add_argument("--lifetime", type=int, default=3600, help="Lifetime for NAT-PMP mappings.")
    parser.add_argument("--action", choices=["add", "remove", "list"], help="Action: add, remove, or list mappings.")
    parser.add_argument("--method", choices=["upnp", "natpmp"], help="Method: UPnP or NAT-PMP.")

    args = parser.parse_args()

    if not args.method:
        print("No method specified. Defaulting to UPnP discovery and listing.")
        list_upnp_port_mappings()
    elif args.method == "upnp":
        if args.action == "list":
            list_upnp_port_mappings()
        elif args.action == "add":
            if not (args.external_port and args.internal_port and args.internal_ip):
                print("Missing parameters for adding a UPnP port mapping. Use --external-port, --internal-port, and --internal-ip.")
            else:
                upnp_port_forward(args.protocol, args.external_port, args.internal_port, args.internal_ip, args.description)
        elif args.action == "remove":
            if not args.external_port:
                print("Missing external port for UPnP removal.")
            else:
                remove_upnp_mapping(args.protocol, args.external_port)
    elif args.method == "natpmp":
        if args.action == "list":
            list_nat_pmp_port_mappings()
        elif args.action == "add":
            if not (args.external_port and args.internal_port):
                print("Missing parameters for adding a NAT-PMP mapping. Use --external-port and --internal-port.")
            else:
                nat_pmp_forward(args.protocol, args.internal_port, args.external_port, args.lifetime)
        elif args.action == "remove":
            if not args.external_port:
                print("Missing external port for NAT-PMP removal.")
            else:
                nat_pmp_remove(args.protocol, args.internal_port, args.external_port)
