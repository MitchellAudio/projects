# Network Fundamentals — Expanded Notes

These notes cover core concepts used throughout the CCNA: models, layer behaviors, addressing, basic protocols, and practical troubleshooting.

## Models: OSI vs TCP/IP

- OSI (7 layers): Application, Presentation, Session, Transport, Network, Data Link, Physical. Useful for conceptual separation.
- TCP/IP (4 layers): Application, Transport, Internet, Link — pragmatic mapping used in most real networks.
- Use the models to localize problems: e.g., ARP/LLDP problems are Link layer; route problems are Network layer; TCP retransmits are Transport layer.

## Ethernet & Layer 2 fundamentals

- Ethernet frames carry destination MAC, source MAC, EtherType, payload, and FCS (CRC). Standard MAC is 48-bit.
- Switching: switches learn MAC→port mappings by inspecting source MACs, then forward frames to the learned port for destination MACs or flood if unknown.
- Collision domains vs broadcast domains: each switch port is its own collision domain (in modern full-duplex), VLANs create separate broadcast domains.
- Duplex and speed: mismatched duplex causes late collisions and errors — prefer auto-negotiation but verify when problems occur.

Common facts:
- MTU default: 1500 bytes (Ethernet). Jumbo frames may be used in some networks (e.g., ~9000), but require end-to-end support.

## ARP (Address Resolution Protocol)

- Purpose: resolve IPv4 addresses to MAC addresses on the local link.
- Operation: ARP request is broadcast; the owner replies with ARP reply (unicast). ARP entries cached in ARP table.
- Troubleshooting: `arp -a` (host), `show ip arp` (Cisco). Duplicate IPs or stale ARP entries cause reachability issues.

## ICMP (Internet Control Message Protocol)

- Tools: `ping` (ICMP echo), `traceroute` (ICMP/UDP/TCP-based depending on OS)
- ICMP messages include unreachable, time-exceeded, redirect; useful for path and reachability debugging.

## IPv4 addressing and subnetting (practical)

Subnet mask in binary:
- Subnet bits are all 1's (network portion), host bits are all 0's (usable host portion)
- Example: /24 = 255.255.255.0 = first 24 bits are 1's, last 8 bits are 0's (usable for hosts)
- /26 = 255.255.255.192 = first 26 bits are network, last 6 bits are hosts
  - 2^6 = 64 addresses per subnet
  - 64 addresses = 4 subnets per /24 (256/64 = 4)

- Address classes are historical — modern networks use CIDR (prefix length). Notation: `192.0.2.0/24`.
- Three main address types: unicast (single host), broadcast (all hosts in subnet), multicast (group delivery).
- Private ranges commonly used in labs:
   - 10.0.0.0/8
   - 172.16.0.0/12
   - 192.168.0.0/16

Subnetting steps (systematic method):
1. Decide required hosts per subnet → pick mask with enough host bits (hosts = 2^n - 2).
2. Convert mask to dotted decimal and determine increment for the octet where the mask changes (increment = 256 - mask_octet).
3. List subnets by adding increments from 0.

Example: 192.168.10.0/26
- Mask: 255.255.255.192
- Increment: 64 (in 4th octet)
- Subnets: .0/26 (.0–.63), .64/26 (.64–.127), .128/26 (.128–.191), .192/26 (.192–.255)

Practice problems:
- Convert these into network, broadcast, and usable host range:
   - 10.1.5.130/25
   - 172.16.20.10/28
   - Given a /24, split into 8 subnets and list ranges.

## IPv6 basics (concise)

- IPv6 address: 128 bits, written hex colon notation (e.g., `2001:db8::1`).
- Types: link‑local (`fe80::/10`), global unicast (public), multicast, anycast.
- No ARP — neighbor discovery (NDP) uses ICMPv6.
- Prefix allocation uses CIDR-like prefixes (`/64` common for LANs).

## Transport layer: TCP vs UDP

- TCP: reliable, connection-oriented, flow control, retransmission, 3-way handshake (SYN, SYN-ACK, ACK).
- UDP: connectionless, lower overhead, used for real-time or query protocols (DNS, RTP).
- Well-known ports: HTTP 80, HTTPS 443, DNS 53, SSH 22, etc. Keep a short list in flashcards.

## Common protocols and where they live

- Ethernet/MAC: Link layer — `show mac address-table`, `tcpdump -e` shows MAC addresses.
- IPv4/IPv6: Network layer — `show ip route`, `ip -4 addr`.
- ARP/ND: Link/Network helpers — `show ip arp`, `ip neigh`.
- TCP/UDP: Transport layer — `netstat -tulpn`, `ss`.

## Useful CLI / tools (Cisco IOS / Linux / Windows)

- Cisco IOS (device):
   - `show ip interface brief`
   - `show interfaces` (counters, errors)
   - `show ip route`
   - `show ip arp`
   - `show mac address-table`
   - `show running-config`
- Linux / macOS:
   - `ip addr`, `ip route`, `ip neigh`
   - `arp -n`
   - `ping`, `traceroute` (or `traceroute -I` for ICMP)
   - `tcpdump -i <iface>` and `tcpdump -nn -s0 -w capture.pcap`
- Windows:
   - `ipconfig /all`, `arp -a`, `ping`, `tracert`

## Wireshark basics & common filters

- Capture filters (libpcap) reduce data at capture time: `host 192.168.1.10`, `port 80`.
- Display filters for analysis:
   - `ip.addr == 192.168.10.1`
   - `arp` (ARP traffic)
   - `icmp` (ping)
   - `tcp.port == 22`
- Use color rules, follow TCP stream, and examine packet details pane (headers per layer).

## Troubleshooting checklist (step-by-step)

1. Physical / Layer 1: cable, link lights, SFP/copper, duplex/speed mismatches. Use `show interfaces`.
2. Link/Layer 2: correct VLANs, MAC learning (`show mac address-table`), trunk allowed VLANs (`show interfaces trunk`).
3. Network/Layer 3: IP addressing, subnet masks, default gateway, `show ip route`.
4. Transport/Layer 4: port reachability, `telnet <ip> <port>` or `nc` to test TCP ports, check firewall/ACLs.
5. Capture: use `tcpdump` or Wireshark to confirm packets flow and where they stop.

## Labs & practice exercises

1) Subnetting drill (repeated practice): create 10 practice questions per session and time yourself. Include VLSM exercises.

2) ARP/ICMP capture lab:
   - Topology: 2 hosts on same VLAN + switch. Use Wireshark on one host.
   - Task: Clear ARP cache, ping the other host, capture ARP request/reply and ICMP echo.

3) Small network build (Packet Tracer/GNS3):
   - Topology: 2 switches, 2 routers, 4 hosts in two subnets.
   - Tasks: assign IPs, configure routing (static on routers), verify `ping` and `traceroute`, capture packets.

4) IPv6 starter lab:
   - Configure link-local and global addresses, ping using IPv6, and inspect NDP entries.

## Notes & next steps

- After mastering fundamentals, proceed to Network Access (VLANs, STP), then IP Connectivity (routing/OSPF).
- Add your lab configs and Wireshark captures into `learning-plan/CCNA/Network-Fundamentals/labs/` as you practice.

