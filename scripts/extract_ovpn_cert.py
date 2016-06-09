#!/usr/bin/python3
#
# Extract certificates and keys from an OpenVPN config file (*.ovpn)
# The config file is rewritten to use the extracted certificates.
#
# Usage: >$ extract_ovpn_cert.py VPNCONFIG.ovpn
#

import os
import re
import sys

outputLocation = '.'
if len(sys.argv) > 2:
    outputLocation = sys.argv[2]
outputLocation = os.path.abspath(outputLocation)
# open input ovpn config file
ovpn_file_path =  os.path.dirname(os.path.abspath(sys.argv[1]))
print 'Opening {!s}'.format(os.path.abspath(sys.argv[1]))
ovpn_file = open(sys.argv[1], 'r')
ovpn_config = ovpn_file.read()
ovpn_file.close()

# open output config file
ovpn_nocert = os.path.join(outputLocation, "vpngate_nocert.ovpn")
print 'Creating {!s}'.format(ovpn_nocert)
ovpn_file = open(ovpn_nocert, 'w')

# prepare regex
regex_tls = re.compile("<tls-auth>(.*)</tls-auth>", re.IGNORECASE|re.DOTALL)
regex_ca = re.compile("<ca>(.*)</ca>", re.IGNORECASE|re.DOTALL)
regex_cert = re.compile("<cert>(.*)</cert>", re.IGNORECASE|re.DOTALL)
regex_key = re.compile("<key>(.*)</key>", re.IGNORECASE|re.DOTALL)

# extract keys
match_string = regex_tls.search(ovpn_config)
if match_string is not None:
    tls_auth_key = os.path.join(outputLocation, 'tls-auth.key')
    print 'Creating {!s}'.format(tls_auth_key)
    cert_file = open(tls_auth_key, 'w')
    cert_file.write(match_string.group(1))
    cert_file.close()
    ovpn_config = regex_tls.sub("",ovpn_config)
    # get key direction setting
    regex_tls = re.compile("key-direction ([01])", re.IGNORECASE)
    match_string = regex_tls.search(ovpn_config)
    if match_string is not None:
        key_direction = match_string.group(1)
    else:
        key_direction = ""
    ovpn_file.write("tls-auth tls-auth.key " + key_direction + "\n")

match_string = regex_ca.search(ovpn_config)
if match_string is not None:
    ca_cert = os.path.join(outputLocation, 'ca.crt')
    print 'Creating {!s}'.format(ca_cert)
    cert_file = open(ca_cert, 'w')
    cert_file.write(match_string.group(1))
    cert_file.close()
    ovpn_config = regex_ca.sub("",ovpn_config)
    ovpn_file.write("ca ca.crt\n")

match_string = regex_cert.search(ovpn_config)
if match_string is not None:
    client_cert = os.path.join(outputLocation, 'client.crt')
    print 'Creating {!s}'.format(client_cert)
    cert_file = open(client_cert, 'w')
    cert_file.write(match_string.group(1))
    cert_file.close()
    ovpn_config = regex_cert.sub("",ovpn_config)
    ovpn_file.write("cert client.crt\n")

match_string = regex_key.search(ovpn_config)
if match_string is not None:
    client_key = os.path.join(outputLocation, 'client.key')
    print 'Creating {!s}'.format(client_key)
    cert_file = open(client_key, 'w')
    cert_file.write(match_string.group(1))
    cert_file.close()
    ovpn_config = regex_key.sub("",ovpn_config)
    ovpn_file.write("key client.key\n")

# copy and append previous config
ovpn_file.write(ovpn_config)

# update configuration file to have automatic DNS (see https://wiki.archlinux.org/index.php/OpenVPN#DNS)
ovpn_file.write('''
###############################################################################
# Automatic DNS resolve configuration.
# 

script-security 2
up /etc/openvpn/update-resolv-conf
down /etc/openvpn/update-resolv-conf
''')
ovpn_file.close()
