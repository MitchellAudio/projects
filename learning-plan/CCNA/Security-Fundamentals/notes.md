# Security Fundamentals — Starter Notes

## Key topics

- Device hardening: secure passwords, enable secret, local user accounts, AAA basics
- Secure management: SSH instead of Telnet, disable unused services (HTTP/TFTP if not used)
- ACLs: standard vs extended, order of statements, use cases for filtering
- Port security on switches: limit MAC addresses per port
- Basic VPN and firewall concepts (high-level)
- Simple threat awareness: common attacks (DoS, spoofing) and mitigation basics

## Common Cisco commands

- `line vty 0 4\n transport input ssh` (enable SSH only)
- `ip access-list extended BLOCK\n deny tcp any any eq 23` (example deny Telnet)
- `username admin privilege 15 secret <password>`
- `switchport port-security\n switchport port-security maximum 2` (port-security)

## Practical notes

- Use key-based SSH and strong passwords; rotate credentials in production environments.
- Apply ACLs close to the source for filtering unwanted traffic and limit the rule count on core devices.
- Use out-of-band management networks where possible.

## Practice tasks

1. Enable SSH on a router and test remote access using an SSH client.
2. Create a simple ACL to block a specific network and verify with `show access-lists` and `ping` tests.
3. Configure port-security on an access switch port and demonstrate violation modes.
