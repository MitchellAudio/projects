# Home VPN — Personal WireGuard on a Raspberry Pi


This document describes a practical, secure setup for running a personal VPN that your iOS devices can use to connect back to a Raspberry Pi you control remotely. It covers architecture choices, a step-by-step WireGuard server and iOS client setup, packet-capture advice (Wireshark/tcpdump), security and maintenance, NAT/CGNAT options, and useful scripts.

**Short answer**

- A personal VPN from iOS to a Raspberry Pi is effective for secure remote access, routing traffic, and accessing home resources. Use WireGuard for simplicity, performance, and battery friendliness on iOS.
- A Raspberry Pi 3 can run WireGuard for a few devices for general browsing and SSH, but a Raspberry Pi 4 (or newer) is strongly recommended for higher throughput, reliability, and longevity.

**Recommended stack**

- Primary: WireGuard server on Raspberry Pi + official WireGuard iOS app.
- Alternative (recommended if you want NAT traversal and minimal router changes): Tailscale (runs WireGuard under the hood, handles coordination and NAT traversal automatically).
- Avoid OpenVPN/IPsec unless you need compatibility with legacy systems — they are heavier and harder to maintain on Pi3.

Hardware notes

- Raspberry Pi 3: usable for light workloads. Expect CPU-bound encryption throughput and USB2-limited Ethernet.
- Raspberry Pi 4+: preferred — better CPU, USB3/GbE path, improved thermal behaviour.
- Power: use a quality power supply and consider a small UPS or remote power-restart option for an offsite Pi.

Network prerequisites

- You need a publicly reachable endpoint for your Pi:
	- Public IPv4 + router port forwarding of a UDP port (51820 default) to the Pi, or
	- Dynamic DNS (DuckDNS/No-IP) pointing to a public IP — update it when IP changes, or
	- If ISP provides CGNAT (no public IPv4), use Tailscale/ZeroTier or a small VPS as a relay.

WireGuard server setup (Raspberry Pi)

These steps assume Raspberry Pi OS (Debian-based) and a user with sudo.

1) Update the system

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y qrencode iptables-persistent
```

2) Install WireGuard

```bash
sudo apt install -y wireguard
```

3) Enable IPv4 forwarding (temporary + persistent)

```bash
sudo sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
```

4) Generate server + client keys (example single-client)

```bash
mkdir -p ~/wireguard-keys && cd ~/wireguard-keys
umask 077
wg genkey | tee server_private.key | wg pubkey > server_public.key
wg genkey | tee client_private.key | wg pubkey > client_public.key
```

5) Create server config `/etc/wireguard/wg0.conf`

Replace `<server_private_key>` with the contents of `server_private.key` and adjust `eth0` if your Pi uses another uplink interface.

```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server_private_key>
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Client peer(s)
[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32
```

6) Create client config for iOS `wg-client.conf` (import into WireGuard app via QR or file)

```ini
[Interface]
PrivateKey = <client_private_key>
Address = 10.0.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = <server_public_key>
Endpoint = your.dyndns.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

- Notes:
	- `AllowedIPs = 0.0.0.0/0` routes all traffic through the VPN (full tunnel). To only access home LAN resources, use `AllowedIPs = 10.0.0.0/24` (or appropriate subnet).
	- `PersistentKeepalive` helps maintain NAT mappings on mobile networks.

7) Start and enable the interface

```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
sudo wg show
```

8) Router: forward UDP port `51820` to the Pi's LAN IP.

Creating QR code for iOS

On your Pi or any machine with `qrencode`:

```bash
qrencode -t png -o client-qr.png < client.conf
# or to show in terminal
cat client.conf | qrencode -t ansiutf8
```

Packet capture strategy (Wireshark/tcpdump)

- Recommended: capture on the Pi itself after WireGuard decrypts packets (interface `wg0`). Captures on `wg0` contain decrypted IP traffic destined for the server/Internet.

```bash
sudo tcpdump -i wg0 -w /tmp/vpn-capture.pcap
# stop with Ctrl+C, then copy to your workstation for Wireshark analysis
scp pi@yourpi:/tmp/vpn-capture.pcap ~/Downloads/
```

- Capturing on the uplink interface (eth0) will show encrypted WireGuard UDP packets — not human-readable without additional complex workstation-side decryption.
- iOS: native Wireshark capture on-device is impractical. Alternatives:
	- Capture on the Pi (recommended)
	- Use a Mac as a gateway or tether and capture on the Mac
	- Use app-level HTTP/HTTPS debugging proxies for app-specific inspection

Security & maintenance checklist

- Store keys securely and never commit them to git.
- Use `unattended-upgrades` for automatic security updates.
- Harden SSH: use SSH keys, disable password auth, consider `fail2ban`.
- Only open necessary ports; restrict firewall rules to expected sources where possible.
- Keep backups of `wg0.conf` and private keys in an offline/secure location.
- Periodically rotate keys and remove revoked peers by deleting their `[Peer]` entries on the server and restarting `wg-quick`.

Performance tuning and expectations

- WireGuard is efficient; expect reasonable latency and low CPU overhead. A Pi 3 will handle normal browsing and light streaming, but high-bitrate multi-stream use will push CPU and USB/Ethernet limits.
- If you see fragmentation, try setting `MTU = 1420` (client-side) or tune MTU on both ends.

Dealing with CGNAT / No public IPv4

- If your ISP uses CGNAT and you cannot get a public IPv4/port forward:
	- Use Tailscale/ZeroTier (no port forwarding required), or
	- Run a small VPS as a relay/rendezvous server (peer both the Pi and iOS through the VPS), or
	- Use reverse SSH tunnels to a VPS and forward traffic through it (more complex).

Alternative: Tailscale (recommended for NAT traversal)

- Tailscale uses WireGuard under the hood, automatically handles NAT traversal, and provides easy device access with identity-based login. Good choice if you don't want to manage port forwarding or dynamic DNS.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Scripts and helpers (examples)

1) Generate keys and print a client QR (local script): save as `~/wireguard-keys/make-client.sh`

```bash
#!/bin/bash
set -e
cd ~/wireguard-keys
umask 077
CLIENT_NAME=${1:-client1}
wg genkey | tee ${CLIENT_NAME}_private.key | wg pubkey > ${CLIENT_NAME}_public.key
SERVER_PUB=$(cat server_public.key)
CLIENT_PRIV=$(cat ${CLIENT_NAME}_private.key)
CLIENT_PUB=$(cat ${CLIENT_NAME}_public.key)
cat > ${CLIENT_NAME}.conf <<EOF
[Interface]
PrivateKey = ${CLIENT_PRIV}
Address = 10.0.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = ${SERVER_PUB}
Endpoint = your.dyndns.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF

qrencode -o ${CLIENT_NAME}-qr.png < ${CLIENT_NAME}.conf
echo "Client config and QR generated: ${CLIENT_NAME}.conf, ${CLIENT_NAME}-qr.png"
```

2) Add a peer to server config (manual safe method):

- Append a `[Peer]` block with the `PublicKey` and `AllowedIPs` to `/etc/wireguard/wg0.conf`, then run `sudo wg set wg0 peer <client_public_key> allowed-ips 10.0.0.2/32` and `sudo systemctl restart wg-quick@wg0`.

Tips

- Monitor connectivity with `sudo wg` and check `journalctl -u wg-quick@wg0` for errors.
- Consider using `ufw` or explicit `iptables` rules to lock down access.
- If you need IPv6, add appropriate `Address` ranges and ensure ISP/gateway supports IPv6 routing.

