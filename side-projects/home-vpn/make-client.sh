#!/bin/bash
# make-client.sh — generate WireGuard client keys, config, and QR
# Usage: ./make-client.sh <client-name> <client-ip>  (e.g. ./make-client.sh phone 10.0.0.2)
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <client-name> <client-ip>"
  exit 2
fi

CLIENT_NAME="$1"
CLIENT_IP="$2"
KEYDIR="/root/wireguard-keys"
mkdir -p "$KEYDIR"
cd "$KEYDIR"

umask 077
wg genkey | tee ${CLIENT_NAME}_private.key | wg pubkey > ${CLIENT_NAME}_public.key
SERVER_PUB_FILE=server_public.key
SERVER_PRIV_FILE=server_private.key

if [ ! -f "$SERVER_PUB_FILE" ] || [ ! -f "$SERVER_PRIV_FILE" ]; then
  echo "Server keys not found in $KEYDIR. Create server_private.key and server_public.key first."
  exit 1
fi

SERVER_PUB=$(cat $SERVER_PUB_FILE)
CLIENT_PRIV=$(cat ${CLIENT_NAME}_private.key)
CLIENT_PUB=$(cat ${CLIENT_NAME}_public.key)

# create client config
CLIENT_CONF=${CLIENT_NAME}.conf
cat > "$CLIENT_CONF" <<EOF
[Interface]
PrivateKey = ${CLIENT_PRIV}
Address = ${CLIENT_IP}/32
DNS = 1.1.1.1

[Peer]
PublicKey = ${SERVER_PUB}
Endpoint = your.dyndns.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF

# create QR
if command -v qrencode >/dev/null 2>&1; then
  qrencode -o ${CLIENT_NAME}-qr.png < ${CLIENT_CONF}
  echo "Generated ${CLIENT_CONF} and ${CLIENT_NAME}-qr.png in ${KEYDIR}"
else
  echo "qrencode not installed; client conf written to ${KEYDIR}/${CLIENT_CONF}"
fi

echo "Client public key: ${CLIENT_PUB}"

echo "To add the client to the server, append a [Peer] block to /etc/wireguard/wg0.conf like this (replace PUBLICKEY and IP):\n\n[Peer]\nPublicKey = ${CLIENT_PUB}\nAllowedIPs = ${CLIENT_IP}/32\n"

echo "Then run: sudo wg set wg0 peer ${CLIENT_PUB} allowed-ips ${CLIENT_IP}/32 && sudo systemctl restart wg-quick@wg0"
