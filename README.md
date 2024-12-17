# Gateway Control Script

This Python script provides a command-line tool for managing port forwarding on network gateways via UPnP and NAT-PMP protocols. It allows users to discover devices, list existing port mappings, and add or remove port forwarding rules with ease.

## Features
Supports both UPnP (Universal Plug and Play) and NAT-PMP (NAT Port Mapping Protocol).<br/>
Discover UPnP and NAT-PMP-enabled devices on the network.<br/>
List all existing UPnP port mappings and NAT-PMP public IP.<br/>
Add and remove port forwarding rules for both protocols.<br/>
Configurable options for protocol, port numbers, description, and lifetime.<br/>

## Requirements
Python 3.7 or later

The following Python libraries:<br/>
miniupnpc for UPnP<br/>
natpmp for NAT-PMP

You can install the required libraries with:<br/>
pip install -r requirements.txt

## Usage
### 1. General Syntax
python gateway_control.py [--method METHOD] [--action ACTION] [options]

### 2. Available Options
--method: Specify the protocol to use (upnp or natpmp).<br/>
--action: Choose the action (list, add, or remove).<br/>
--protocol: Specify the protocol for the mapping (TCP or UDP). Default: TCP.<br/>
--external-port: External port number for the gateway.<br/>
--internal-port: Internal port number for your device.<br/>
--internal-ip: Local IP address of your device (UPnP only).<br/>
--description: Description for the mapping. Default: "Python Port Mapping".<br/>
--lifetime: Duration of the mapping in seconds (NAT-PMP only). Default: 3600 seconds.<br/>

### 3. Examples
Discover Devices and List Mappings<br/>

**List existing UPnP port mappings:<br/>**
python gateway_control.py --method upnp --action list

**Show the public IP of the NAT-PMP gateway:<br/>**
python gateway_control.py --method natpmp --action list

### 4. Add a Port Mapping
**Add a UPnP port mapping:<br/>**
python gateway_control.py --method upnp --action add --protocol TCP --external-port 8080 --internal-port 8080 --internal-ip 192.168.1.100 --description "Game Server"<br/>

**Add a NAT-PMP port mapping:<br/>**
python gateway_control.py --method natpmp --action add --protocol UDP --external-port 8080 --internal-port 8080 --lifetime 7200<br/>

### 5. Remove a Port Mapping
**Remove a UPnP port mapping:<br/>**
python gateway_control.py --method upnp --action remove --protocol TCP --external-port 8080<br/>

**Remove a NAT-PMP port mapping:<br/>**
python gateway_control.py --method natpmp --action remove --protocol UDP --external-port 8080<br/>

### 6. Default Behavior
If no arguments are provided, the script defaults to discovering UPnP devices and listing existing mappings.<br/>

### 7. Contributing
Contributions, bug reports and feature requests are welcome! Feel free to fork this repository and submit a pull request.<br/>

### 8. License
This project is licensed under the MIT License. See the LICENSE file for details.
