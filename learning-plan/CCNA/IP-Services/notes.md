# IP Services — Starter Notes

## Key topics

- DHCP: server vs client, DHCP pools, options (gateway, DNS)
- NAT / PAT: inside vs outside, overload (PAT) for IPv4 address conservation
- DNS basics and troubleshooting
- NTP: importance for timestamps and logs
- SNMP and syslog basics for monitoring
- Basic QoS concepts: classification, marking (DSCP), queueing (LLQ, CBWFQ) — overview only

## Common Cisco commands

- DHCP pool example:
```
ip dhcp pool OFFICE
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
```
- NAT example (PAT):
```
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface Gig0/0 overload
```
- `show ip nat translations`, `show ip dhcp binding`, `show ntp status`

## Practical notes

- For labs, use NAT to simulate Internet access for private addressing.
- Keep NTP synchronized across devices for coherent logs and troubleshooting.
- Use SNMPv3 where possible for secure monitoring.

## Practice tasks

1. Configure a DHCP server on a router and verify a host obtains IP and gateway.
2. Configure PAT to allow internal hosts to reach the Internet through a single public IP (simulate on a router).
3. Set up basic NTP and check logs for timestamped events.
