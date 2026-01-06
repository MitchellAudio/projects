# Cisco Packet Tracer - CCNA Study Guide

Complete guide to using Cisco Packet Tracer to prepare for the CCNA exam.

## Download & Installation

1. **Create Cisco Networking Academy account** (free): https://www.netacad.com/
2. **Download Packet Tracer** from Networking Academy portal
3. Install and login with your Networking Academy credentials

## Interface Overview

### Main Components

- **Logical Workspace**: Where you build topologies
- **Physical Workspace**: Physical device view (click a device to enter)
- **Device Selection Panel** (bottom): Categories of devices to add
  - **Network Devices**: Routers, switches, wireless
  - **End Devices**: PCs, servers, phones, tablets
  - **Connections**: Cables (Copper Straight, Copper Cross, Fiber, Console, etc.)
  - **Components**: Can add modules (NICs, WICs) to devices

### Key Toolbar Functions

- **Select Tool**: Move and select devices
- **Delete Tool**: Remove devices
- **Inspect Tool**: Quick view device info
- **Simple PDU**: Test connectivity (ping-like)
- **Complex PDU**: Create custom traffic patterns
- **Simulation Mode**: Step through packet flow (critical for learning!)
- **Realtime Mode**: Normal operation

---

## First Lab: Basic Network Connectivity

### Lab 1: Two PCs and a Switch

**Objective**: Connect two PCs through a switch and verify connectivity

**Topology**:
```
PC0 ---- Switch0 ---- PC1
```

**Steps**:

1. **Add devices**:
   - Click "End Devices" → drag "PC" to workspace (PC0)
   - Repeat for PC1
   - Click "Network Devices" → "Switches" → drag "2960" switch to workspace

2. **Connect devices**:
   - Click "Connections" → select "Copper Straight-Through"
   - Click PC0 → select FastEthernet0
   - Click Switch0 → select any FastEthernet port (e.g., Fa0/1)
   - Repeat to connect PC1 to Switch0 (e.g., Fa0/2)
   - Wait for green triangles (ports up)

3. **Configure PC IP addresses**:
   
   **PC0**:
   - Click PC0 → Desktop tab → IP Configuration
   - Static: IP Address: `192.168.1.10`, Subnet Mask: `255.255.255.0`
   
   **PC1**:
   - Click PC1 → Desktop tab → IP Configuration
   - Static: IP Address: `192.168.1.11`, Subnet Mask: `255.255.255.0`

4. **Test connectivity**:
   - Click PC0 → Desktop → Command Prompt
   - Type: `ping 192.168.1.11`
   - Should see replies!

5. **Use Simulation Mode (KEY LEARNING TOOL)**:
   - Click "Simulation" button (bottom right)
   - Click "Add Simple PDU" (envelope icon)
   - Click PC0 as source, PC1 as destination
   - Click "Capture/Forward" button to step through packet flow
   - Observe: ARP request (broadcast), ARP reply, ICMP echo request/reply
   - Check "Event List" and "Device List" panels

**What you learned**:
- Basic topology building
- IP configuration on end devices
- Layer 2 switching (MAC learning)
- ARP process
- ICMP (ping) operation

---

## Lab 2: Router Between Two Networks

**Objective**: Route traffic between two different subnets

**Topology**:
```
PC0 (192.168.1.10/24) --- Switch0 --- Router0 --- Switch1 --- PC1 (192.168.2.10/24)
                                   Gi0/0     Gi0/1
                              (192.168.1.1) (192.168.2.1)
```

**Steps**:

1. **Build topology**:
   - Add 2 PCs, 2 switches (2960), 1 router (1941 or 2911)
   - Connect: PC0 → Switch0, PC1 → Switch1
   - Connect: Switch0 Fa0/24 → Router Gi0/0
   - Connect: Switch1 Fa0/24 → Router Gi0/1

2. **Configure Router**:
   - Click Router0 → CLI tab
   - Wait for prompt, press Enter
   - Type:

```
enable
configure terminal
hostname R1

interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown
 exit

end
```

3. **Configure PCs**:
   
   **PC0** (Subnet 1):
   - IP: `192.168.1.10`
   - Mask: `255.255.255.0`
   - Gateway: `192.168.1.1` ← Router interface!
   
   **PC1** (Subnet 2):
   - IP: `192.168.2.10`
   - Mask: `255.255.255.0`
   - Gateway: `192.168.2.1`

4. **Verify routing**:
   - PC0 → Command Prompt: `ping 192.168.2.10`
   - Router CLI: `show ip interface brief` (verify IPs and status)
   - Router CLI: `show ip route` (see directly connected networks)

5. **Simulation mode analysis**:
   - Add Simple PDU from PC0 to PC1
   - Step through and observe:
     - PC0 sends to default gateway (ARP for router MAC)
     - Router receives, checks routing table
     - Router forwards to destination subnet
     - PC1 receives packet

**What you learned**:
- Basic router configuration
- Inter-VLAN routing concept
- Default gateway importance
- Routing table basics

---

## Lab 3: VLANs and Trunking

**Objective**: Separate traffic using VLANs

**Topology**:
```
PC0 (VLAN 10) ─┐
PC1 (VLAN 20) ─┼── Switch0 ==TRUNK== Switch1 ─┬─ PC2 (VLAN 10)
                                                └─ PC3 (VLAN 20)
```

**Steps**:

1. **Build topology**:
   - Add 4 PCs, 2 switches (2960)
   - Connect PC0, PC1 to Switch0
   - Connect PC2, PC3 to Switch1
   - Connect Switch0 Gi0/1 to Switch1 Gi0/1 (trunk link)

2. **Configure Switch0**:

```
enable
configure terminal

vlan 10
 name SALES
vlan 20
 name ENGINEERING
exit

interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 exit

interface FastEthernet0/2
 switchport mode access
 switchport access vlan 20
 exit

interface GigabitEthernet0/1
 switchport mode trunk
 exit

end
```

3. **Configure Switch1** (same VLAN creation, assign Fa0/1 to VLAN 10, Fa0/2 to VLAN 20, Gi0/1 as trunk)

4. **Configure PCs** (all in same subnet for testing):
   - All PCs: IPs 192.168.1.10-13, mask 255.255.255.0

5. **Test VLAN separation**:
   - PC0 (VLAN 10) can ping PC2 (VLAN 10) ✓
   - PC0 (VLAN 10) CANNOT ping PC1 (VLAN 20) ✗
   - PC1 (VLAN 20) can ping PC3 (VLAN 20) ✓

6. **Verify on switches**:
   - `show vlan brief`
   - `show interfaces trunk`
   - `show mac address-table`

**What you learned**:
- VLAN creation and assignment
- Trunk configuration
- Traffic isolation with VLANs

---

## Lab 4: Inter-VLAN Routing (Router-on-a-Stick)

**Objective**: Enable communication between VLANs using a router

**Topology**:
```
PC0 (VLAN 10, 192.168.10.10) ─┐
PC1 (VLAN 20, 192.168.20.10) ─┤── Switch0 ==TRUNK== Router0
```

**Steps**:

1. **Build topology**: 2 PCs, 1 switch, 1 router
2. **Configure Switch**:

```
vlan 10
vlan 20
exit

interface Fa0/1
 switchport mode access
 switchport access vlan 10
 exit

interface Fa0/2
 switchport mode access
 switchport access vlan 20
 exit

interface Gi0/1
 switchport mode trunk
 exit
```

3. **Configure Router (subinterfaces)**:

```
interface GigabitEthernet0/0
 no shutdown
 exit

interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 exit

interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 exit
```

4. **Configure PCs**:
   - PC0: IP `192.168.10.10`, mask `255.255.255.0`, gateway `192.168.10.1`
   - PC1: IP `192.168.20.10`, mask `255.255.255.0`, gateway `192.168.20.1`

5. **Test**: PC0 can now ping PC1 across VLANs!

**What you learned**:
- Router-on-a-stick concept
- Subinterfaces and 802.1Q encapsulation
- Inter-VLAN routing

---

## Lab 5: Static Routing (3 Routers)

**Objective**: Connect three networks using static routes

**Topology**:
```
PC0 (10.1.1.10/24) --- R1 (10.1.1.1) === (10.1.12.1) R2 (10.1.12.2) === (10.1.23.1) R3 (10.1.23.2) --- PC1 (10.1.3.10/24)
                                                                           (10.1.3.1)
```

**R1 Config**:
```
interface Gi0/0
 ip address 10.1.1.1 255.255.255.0
 no shutdown

interface Gi0/1
 ip address 10.1.12.1 255.255.255.0
 no shutdown

ip route 10.1.23.0 255.255.255.0 10.1.12.2
ip route 10.1.3.0 255.255.255.0 10.1.12.2
```

**R2 Config**:
```
interface Gi0/0
 ip address 10.1.12.2 255.255.255.0
 no shutdown

interface Gi0/1
 ip address 10.1.23.1 255.255.255.0
 no shutdown

ip route 10.1.1.0 255.255.255.0 10.1.12.1
ip route 10.1.3.0 255.255.255.0 10.1.23.2
```

**R3 Config**:
```
interface Gi0/0
 ip address 10.1.23.2 255.255.255.0
 no shutdown

interface Gi0/1
 ip address 10.1.3.1 255.255.255.0
 no shutdown

ip route 10.1.1.0 255.255.255.0 10.1.23.1
ip route 10.1.12.0 255.255.255.0 10.1.23.1
```

**Verify**:
- `show ip route` on each router
- `tracert 10.1.3.10` from PC0 (should show all hops)

---

## Lab 6: OSPF Dynamic Routing

**Objective**: Replace static routes with OSPF

**Using same topology as Lab 5**, replace static routes with OSPF:

**All Routers**:
```
no ip route ... (remove all static routes)

router ospf 1
 network 10.1.0.0 0.0.255.255 area 0
 end
```

**Verify**:
- `show ip route` (see O routes for OSPF)
- `show ip ospf neighbor`
- `show ip protocols`

**Test**: PC0 can still reach PC1, but now routing is dynamic!

---

## Lab 7: DHCP Server Configuration

**Objective**: Configure a router as DHCP server

**Router Config**:
```
ip dhcp excluded-address 192.168.1.1 192.168.1.10

ip dhcp pool LAN
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8
 exit
```

**PC Config**: Set to DHCP (Desktop → IP Configuration → DHCP)

**Verify**:
- PC receives IP in range
- `show ip dhcp binding` on router

---

## Lab 8: NAT/PAT Configuration

**Objective**: Translate private IPs to public IP

**Topology**: Inside network (192.168.1.0/24) → Router → Outside (Internet simulation)

**Router Config**:
```
interface Gi0/0
 ip address 192.168.1.1 255.255.255.0
 ip nat inside
 no shutdown

interface Gi0/1
 ip address 203.0.113.1 255.255.255.252
 ip nat outside
 no shutdown

access-list 1 permit 192.168.1.0 0.0.0.255

ip nat inside source list 1 interface Gi0/1 overload
```

**Verify**:
- `show ip nat translations`
- `show ip nat statistics`

---

## Advanced Packet Tracer Tips

### Simulation Mode (Your Best Learning Tool!)

1. **Filter events**: Click "Edit Filters" to show only specific protocols (ARP, ICMP, TCP, etc.)
2. **Auto Capture**: Click "Auto Capture / Play" to watch continuous flow
3. **Scenario**: Save complex PDU patterns as scenarios
4. **OSI Model View**: In simulation, click packet in Event List → OSI Model tab shows layer-by-layer processing

### Useful Commands for Practice

**Router/Switch Discovery**:
- `show version`
- `show running-config`
- `show startup-config`

**Interface Status**:
- `show ip interface brief`
- `show interfaces status`
- `show interfaces Gi0/0`

**Routing**:
- `show ip route`
- `show ip ospf neighbor`
- `show ip protocols`

**Switching**:
- `show vlan brief`
- `show mac address-table`
- `show interfaces trunk`
- `show spanning-tree`

**Troubleshooting**:
- `ping <ip>`
- `traceroute <ip>`
- `show arp`

### Saving and Loading

- **Save topology**: File → Save As (.pkt file)
- **Export as PDF**: File → Print → Save as PDF (includes notes)
- **Activity Wizard**: Create scored labs with instructions

---

## Practice Schedule for CCNA

### Week 1-2: Fundamentals
- Labs 1-2: Basic connectivity and routing
- Practice subnetting on paper daily (10 problems)
- Build and test different subnet scenarios

### Week 3-4: Switching
- Labs 3-4: VLANs, trunking, inter-VLAN routing
- Add spanning tree manipulation
- Practice port security

### Week 5-6: Routing
- Labs 5-6: Static routing and OSPF
- Add IPv6 versions of labs
- Practice route manipulation

### Week 7-8: Services & Security
- Labs 7-8: DHCP, NAT/PAT
- Add ACL filtering scenarios
- Practice SSH configuration

### Week 9-10: Complex Scenarios
- Build complete enterprise networks (multiple routers, switches, VLANs, routing protocols)
- Troubleshoot broken topologies
- Time yourself configuring from scratch

---

## Common Packet Tracer Mistakes to Avoid

1. **Wrong cable type**: Use straight-through for unlike devices (PC-Switch), crossover for like devices in older topologies (Switch-Switch) — modern devices auto-sense
2. **Forgetting `no shutdown`**: Interfaces are administratively down by default
3. **Incorrect subnet masks**: Double-check mask matches on both ends
4. **Native VLAN mismatches**: Use same native VLAN on both trunk ends
5. **Not saving config**: Use `copy running-config startup-config`

---

## Next Steps

1. **Complete all 8 labs above** - these cover 60% of CCNA hands-on topics
2. **Find Packet Tracer lab packs**: Cisco NetAcad provides additional structured labs
3. **Build exam scenarios**: Practice common CCNA exam topology patterns
4. **Time yourself**: Configure networks from scratch under time pressure
5. **Break and fix**: Intentionally break labs and practice troubleshooting

## Resources

- **Cisco Packet Tracer Tutorials**: Built-in tutorials (Help → Tutorials)
- **NetAcad Lab Manual**: Available through your NetAcad account
- **CCNA Official Cert Guide**: Lab exercises you can recreate in Packet Tracer
- **YouTube**: Search "Packet Tracer CCNA labs" for video walkthroughs

---

Good luck with your CCNA studies! Build these labs, experiment, break things, and learn from the simulation mode. Packet Tracer is an incredible free tool for mastering networking concepts.
