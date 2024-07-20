# Gossip-based-human-tracking

This is a project for the university of basel. In this project, we created an easy to use face-recognition program that uses a gossip-protocol to reliably transmit the information across a network. In addition, we provide a short guide for a wireless adhoc network. All this runs on Raspberry Pi's. The original plan was to create an additional mesh-network that is one level below the application layer. This might come in the near future. Currently each Pi makes use of the broadcast function local networks provide and the codebase is heavily focused on the gossip protocol. 

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements

For hardware we used: 
- 3 Raspberry pi 5 with 8 gb of ram (Any Pi should work, although a pi zero 2 w took over 48h to compile dlib in our case)
- 2 NoiR camera for Raspberry pi (A camera with an Infrared filter works fine, but in darker settings, the camera without a filter works better)
- 1 or 3 USB wifi dongles (TP-Link AC600 HIGH GAIN WI-FI USB AD is our recommendation because it works out of the box on raspberry pi OS. At least one is needed for an adhoc network. Equip the others with one too for better range)
- The 3D-files we used for this project can be found here:

## Installation

You will need your raspberry pi's loaded up with 'Raspberry Pi OS with desktop' (since the lite version comes without all networking libraries).

Following these steps, should allow you to recreate the project:

```bash
sudo apt update
```
```bash
sudo apt install build-essential cmake
sudo apt install libgtk-3-dev
sudo apt install libboost-all-dev
```
```
pip3 install dlib
pip3 install skipy
pip3 install scikit-image
pip3 install face-recognition
```
It is recommended to work in a pyvenv, but if you prefer to work without one, add ``` --break-system-packages ``` at the end of the above pip commands
The installation needs to be done on all raspberry pi's that are supposed to be on the network.

Optionally, if you intend to use a raspberry pi without face-tracking, the default libraries that come with the 'Raspberry Pi Os with desktop' the standard libraries that come with the OS are enough.

## Usage

To add a person/face to the project, put a JPG of the person into the directory 'faces'. The name of the JPG is how the Person will be seen by the network. 
Example: A picture of Obama should be named "Obama.jpg".

To start the face-recognition with the gossip in your local network, run gossip.py with ```python3 gossip.py```
Note: Depending on your network and your submask, you might have to set your IP address and your subnet mask seperately (default is 192.168.2.x and 255.255.255.0)

To start the gossip without face-recognition, run gossip_no_facerec.py with ```python3 gossip_no_facerec.py```. This will broadcast the latest gossip in your network.
Additionally, if you wish for a nice representation of the latest gossip being sent around in your network, you can run display.py with ```python3 display.py```. 
There you can also assign different display colors to your pi's.

This project is designed such that it can be used with an Ad-hoc network, or your existing wifi-network at home. It should also work in a mesh-wifi network, but this has not been tested yet. 

### Ad-hoc network
To set up an Ad-hoc network, you need to follow these steps:
```bash
cd /etc/network
sudo cp interfaces wifi-interface
sudo nano adhoc-interface
```
Now copy the following and paste it into the file:
```bash
  auto lo
  iface lo inet loopback
  iface eth0 inet dhcp

  auto wlan0
  iface wlan0 inet static
  address 192.168.2.1
  netmask 255.255.255.0
  wireless-channel 4
  wireless-essid PiEyeNet
  wireless-mode ad-hoc
```
To enable the pi hosting the Ad-hoc network to assign an IP to the other raspberry pi's, execute following command
```bash
sudo apt-get install isc-dhcp-server
```
To configure the dhcp-server use:
```bash
sudo nano /etc/dhcp/dhcpd.conf
```
and change the contents to:
```bash
  ddns-update-style interim;
  default-lease-time 600;
  max-lease-time 7200;
  authoritative;
  log-facility local7;
  subnet 192.168.2.0 netmask 255.255.255.0 {
   range 192.168.2.5 192.168.2.150;

  }
```
With the ad-hoc network ready to go, switch to the network directory with
```bash
cd /etc/network
```
and enable it with:
```bash
sudo cp /etc/network/wifi-interface interfaces
```

Now you can connect all raspberry pi's to the network 'PiEyeNet' and start the gossip.py program.
