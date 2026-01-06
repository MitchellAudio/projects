Home VPN — quick start

This folder contains helper scripts and templates to set up a WireGuard VPN server on a Raspberry Pi and generate client configs for iOS.

Files here

- `setup.sh` — installs packages (WireGuard, qrencode, iptables-persistent), enables forwarding, and prints next steps. Run on the Pi.
- `make-client.sh` — generates client keypair and a client config file and QR image. Run on the Pi (in `~/wireguard-keys`) or any secure machine.
- `wg0.conf.template` — server config template with placeholders you must replace with real keys and interface names.
- `client.conf.template` — client config template to import into the WireGuard iOS app.

Quick start (recommended)

1) Copy this repo to your Pi and open a shell on the Pi.

2) Make scripts executable:

```bash
chmod +x side-projects/home-vpn/setup.sh
chmod +x side-projects/home-vpn/make-client.sh
```

3) Run the setup script (installs packages and prepares environment):

```bash
sudo bash side-projects/home-vpn/setup.sh
```

4) Generate server and client keys (the `setup.sh` helps create `~/wireguard-keys`). Edit `wg0.conf.template` and replace placeholders, then move it to `/etc/wireguard/wg0.conf`.

5) Use `make-client.sh` to generate the client config and a QR code, then import the QR code into the WireGuard iOS app.

6) Enable the interface:

```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
sudo wg show
```

Notes and safety

- Never commit private keys to git. Keep `~/wireguard-keys` restricted (umask 077 recommended).
- If your ISP uses CGNAT and you cannot port-forward, consider Tailscale or a small VPS relay.
- The templates use `51820` UDP by default; change it if you prefer another port.

If you want I can:
- Create an example `wg0.conf` populated with placeholder keys in this folder (you will still replace keys with your actual values), or
- Walk through running `setup.sh` and `make-client.sh` step-by-step on your Pi.
