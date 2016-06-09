This python script is intended to automate the extraction of embedded certificates and keys from OpenVPN config files.

Unfortunately the GNOME Network-Manager is not able to automatically import OpenVPN config files with embedded certificates and keys. A workaround is to manually extract these and store them in separate files (e.g. see https://naveensnayak.wordpress.com/2013/03/04/ubuntu-openvpn-with-ovpn-file/).

Instructions:

* Make shure all the required packages are installed. For example on Ubuntu and Debian run:

    >$ sudo apt-get install python3 network-manager-openvpn-gnome

* Extract the certs and keys using the python script

    >$ python3 extract_ovpn_cert.py path/to/VPNCONFIG.ovpn

* Import the created file `path/to/VPNCONFIG_nocert.ovpn` with the GNOME network config tool

-----------------------------------------

References:

* Manual extraction HOWTO https://naveensnayak.wordpress.com/2013/03/04/ubuntu-openvpn-with-ovpn-file/
* Ubuntu bug report https://bugs.launchpad.net/ubuntu/+source/network-manager-openvpn/+bug/606365