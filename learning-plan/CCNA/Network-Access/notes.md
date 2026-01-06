# Network Access — Starter Notes

## Key topics

- VLANs: purpose, access ports vs trunk ports, native VLANs
- 802.1Q trunking: encapsulation, negotiation (DTP) — prefer static in production
- Inter-VLAN routing: SVI (switch virtual interface) vs router-on-a-stick
- Spanning Tree Protocol (STP): basic purpose, root bridge, common variants (RSTP)
- Switchport security: port-security, MAC address limiting
- Wireless basics: SSID, WPA2/WPA3, basic RF considerations

## Common Cisco commands

- `show vlan brief`
- `show interface trunk`
- `show mac address-table`
- `show spanning-tree`
- `switchport mode access` / `switchport mode trunk`
- `interface Vlan10\n ip address 192.168.10.1 255.255.255.0` (SVI example)
- `switchport port-security` and related `mac-address` commands

## Practical notes

- Use consistent naming and VLAN numbering across switches; document native VLAN choices.
- Avoid DTP in production; configure trunking explicitly.
- For voice VLANs, configure QoS trust and correct tagging.

## Practice tasks

1. Configure two switches with VLANs 10 and 20 and a trunk between them; verify inter-VLAN routing using a router-on-a-stick.
2. Demonstrate port-security by limiting a port to one MAC address and test violation actions.
3. Simulate STP: change root bridge priority and observe topology changes.

## Expanded topics and configuration examples

### VLANs — concepts and behavior

- Purpose: Logical segmentation of a Layer‑2 network to create separate broadcast domains and isolate traffic.
- Types: data VLAN, voice VLAN (for IP phones), management VLAN (for device management), native VLAN (untagged frames on 802.1Q trunk).
- Best practice: use a dedicated management VLAN (not VLAN 1) and avoid using the native VLAN for user traffic.

### Configure VLANs and access ports (example)

Example: create VLAN 10 and assign a port to access VLAN 10:

```
configure terminal
 vlan 10
	name STUDENT
 exit
 interface GigabitEthernet0/3
	switchport mode access
	switchport access vlan 10
	description "Student workstation"
```

Verification:

```
show vlan brief
show mac address-table interface Gi0/3
```

### Trunks and 802.1Q

- Trunks carry multiple VLANs between switches or between a switch and router (router-on-a-stick). 802.1Q tags frames with VLAN ID; one VLAN can be left untagged as the native VLAN.
- Avoid dynamic trunking protocol (DTP) in production — configure trunking statically.

Example: configure trunk on two switches

```
interface GigabitEthernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999    ! management/native (optional)
 switchport trunk allowed vlan 10,20,99
```

Verification:

```
show interfaces trunk
show interface GigabitEthernet0/1 switchport
```

### Native VLAN cautions

- The native VLAN carries untagged frames; mismatched native VLANs cause traffic leaks and security issues. Use the same native VLAN on both ends or set native to an unused VLAN.

### Inter-VLAN routing: SVI vs Router-on-a-Stick

- SVI (Switch Virtual Interface): used on L3 switches — create an interface vlanX and assign IP. Best for high-performance inter-VLAN routing.

Example SVI (on a multilayer switch):

```
interface Vlan10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface Vlan20
 ip address 192.168.20.1 255.255.255.0
```

- Router-on-a-stick: a router subinterface per VLAN on a physical interface (used with access switches without L3 capability).

Example router-on-a-stick (on Cisco IOS router):

```
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.254 255.255.255.0
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.254 255.255.255.0
```

### EtherChannel (port-channel) basics

- EtherChannel bundles multiple physical links into a single logical link for resiliency and increased bandwidth. LACP (802.3ad) is recommended.

Example LACP config (switch side):

```
interface range Gi0/1 - 2
 channel-group 1 mode active
!
interface Port-channel1
 switchport mode trunk
```

Verification:

```
show etherchannel summary
show interfaces port-channel 1
```

### Spanning Tree Protocol (STP)

- Purpose: prevent Layer‑2 loops in networks with redundant links by creating a loop‑free tree. Key concepts: root bridge, path cost, port roles (root, designated, blocking), BPDU.
- Variants: PVST+ (Cisco per-VLAN STP), RSTP (802.1w) faster convergence.
- Useful features: `spanning-tree portfast` (for access ports to speed up port forwarding), `spanning-tree bpduguard` (disable ports receiving BPDUs), `spanning-tree root primary/secondary` to influence root election.

Common commands:

```
show spanning-tree
show spanning-tree vlan 10
```

Examples:

```
interface GigabitEthernet0/3
 switchport mode access
 spanning-tree portfast

interface GigabitEthernet0/4
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
```

### VTP (VLAN Trunking Protocol) — note

- VTP is a Cisco protocol for distributing VLAN config; it can be useful but is also risky in some labs/production (accidental VLAN deletions). Consider using VTP in transparent mode or avoid it unless you understand the domain/trust model.

### Port Security

- Limits the number of MAC addresses on an access port and can take actions on violation (protect, restrict, shutdown).

Example:

```
interface GigabitEthernet0/10
 switchport mode access
 switchport access vlan 10
 switchport port-security
 switchport port-security maximum 1
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
```

Verification:

```
show port-security interface Gi0/10
show port-security address
```

### Voice VLAN and QoS basics

- When supporting IP phones, configure a voice VLAN so phones tag voice traffic while PCs remain untagged on the access VLAN. Trust DSCP/CoS on uplink ports to preserve QoS marking from phones.

Example voice VLAN config:

```
interface Gi0/5
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
```

### Troubleshooting commands & tips

- `show interface status` — link up/down, speed/duplex
- `show interfaces trunk` — trunk status and allowed VLANs
- `show mac address-table` — where MACs learned
- `show cdp neighbors` / `show lldp neighbors` — neighbor discovery
- If VLANs don't pass traffic, check trunk allowed VLAN list and native VLAN mismatch.
- If STP blocks a port you expected up, examine `show spanning-tree` to see root path and port roles.

### Security and hardening checklist (Network Access layer)

- Move management services off VLAN 1; use a dedicated management VLAN.
- Disable unused ports and place them in an inactive VLAN, enable `portfast` only on end-user ports.
- Enable `bpduguard` on access ports and `root guard` on uplinks where appropriate.
- Use port-security with sticky MACs for access ports when appropriate.

### Practice labs (detailed)

1) Full inter-VLAN lab (SVI):
 - Topology: one L3 switch, two access switches, hosts in VLAN 10 and VLAN 20.
 - Tasks: configure VLANs, SVIs, default gateway on hosts, verify routing between VLANs, test `show ip route`, `show ip interface brief`.

2) Router-on-a-stick lab:
 - Topology: switch - trunk - router (router subinterfaces).
 - Tasks: configure trunk, configure router subinterfaces with dot1q, assign host IPs, verify connectivity and traceroute path through router.

3) STP behavior lab:
 - Topology: 3 switches in triangular topology (redundant links).
 - Tasks: observe root election, change bridge priority to force a different root, enable `portfast` and `bpduguard` on access ports, test link failure and observe convergence.

4) EtherChannel lab:
 - Topology: two switches with two parallel links.
 - Tasks: configure LACP `channel-group` on both sides, verify `show etherchannel summary`, test failover when a member link fails.

---

If you'd like, I can also generate step-by-step Packet Tracer configs or a ready-to-import GNS3 topology for any of the above labs. Which lab should I create first? 
