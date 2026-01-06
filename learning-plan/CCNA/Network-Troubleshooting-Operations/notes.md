# Network Troubleshooting & Operations — Starter Notes

## Key topics

- Troubleshooting methodology: identify, isolate, fix, verify, document
- Useful `show` commands: `show interfaces`, `show ip route`, `show ip ospf neighbor`, `show logging`, `show interface status`
- Ping and traceroute usage and interpretation
- Basic packet capture with Wireshark: filter usage and common signs (retransmits, ICMP unreachable)
- Device backup/restore and image management

## Practical tips

- Reproduce the problem reliably before changing configurations.
- Change one thing at a time and document each step.
- Use logging and time-synced timestamps (NTP) to correlate events across devices.

## Common scenarios & quick checks

- No connectivity: check interface status, IP addressing, and routes.
- Intermittent connectivity: check errors, CRC, duplex/MTU mismatches, and physical layer first.
- High latency / packet loss: run `ping` with large packet size and `traceroute` to find the hop introducing delay.

## Practice tasks

1. Simulate a link failure and practice rerouting/verification. Document steps to restore service.
2. Capture a failing TCP session in Wireshark and identify retransmits and the root cause (e.g., MTU or congestion).
3. Create a scheduled backup script for device configurations and test a restore.
