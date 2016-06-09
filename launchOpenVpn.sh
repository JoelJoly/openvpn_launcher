# launch VPN
#sudo 

rm -R -f key_extract
mkdir key_extract
pushd key_extract
python ../scripts/extract_ovpn_cert.py ../servers/vpngate_vpn536492275.opengw.net_udp_1394.ovpn
#iptables -L -n -v –line-numbers
sudo openvpn --config vpngate_nocert.ovpn
popd
