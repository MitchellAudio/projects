#!/bin/bash
# setup.sh — install WireGuard and helpers on a Debian-based Raspberry Pi
# Run as root or with sudo: sudo bash setup.sh
set -euo pipefail

# Update and install packages
apt update
apt upgrade -y
apt install -y wireguard qrencode iptables-persistent

# Enable IP forwarding now and persistently
sysctl -w net.ipv4.ip_forward=1
if ! grep -q '^net.ipv4.ip_forward=1' /etc/sysctl.conf 2>/dev/null; then
  echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf
fi

# Create keys directory
mkdir -p /root/wireguard-keys
chmod 700 /root/wireguard-keys

cat <<'EOF'

Setup complete. Next steps (manual):

1) Generate server and client keys (example):
   cd /root/wireguard-keys
   umask 077
   wg genkey | tee server_private.key | wg pubkey > server_public.key
   wg genkey | tee client_private.key | wg pubkey > client_public.key

2) Edit 'wg0.conf.template' in this project, replace placeholders with your keys and verify the uplink interface (eth0 or wlan0).
   Then copy the file to /etc/wireguard/wg0.conf:

   sudo cp /path/to/this/repo/side-projects/home-vpn/wg0.conf.template /etc/wireguard/wg0.conf

3) Start WireGuard:
   sudo systemctl enable wg-quick@wg0
   sudo systemctl start wg-quick@wg0
   sudo wg show

4) Use 'make-client.sh' to generate client config and QR:
   sudo bash /path/to/this/repo/side-projects/home-vpn/make-client.sh client1 10.0.0.2

5) Forward the UDP port you choose (51820 default) from your router to the Pi's LAN IP.

EOF
