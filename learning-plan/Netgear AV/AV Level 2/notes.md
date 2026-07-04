# NETGEAR AV Certification — Level 2 Notes

> **About Level 2:** Builds directly on Level 1. Assumes solid understanding of IGMP Plus, Auto LAG/Trunk, MLAG, Engage, and the switch lineup. Level 2 goes deeper into multicast routing, QoS, security, Layer 3, advanced redundancy, AV-over-IP protocol stacks (ST 2110, AES67, NDI, SDVoE), troubleshooting, and network monitoring.

---

## Table of Contents

1. [Advanced Multicast — PIM Deep Dive](#1-advanced-multicast--pim-deep-dive)
2. [QoS — Deep Configuration](#2-qos--deep-configuration)
3. [Layer 3 Routing on AV Networks](#3-layer-3-routing-on-av-networks)
4. [Advanced Security](#4-advanced-security)
5. [Advanced Redundancy Patterns](#5-advanced-redundancy-patterns)
6. [AV-over-IP Protocol Stacks](#6-av-over-ip-protocol-stacks)
7. [Jumbo Frames, EEE, and Flow Control](#7-jumbo-frames-eee-and-flow-control)
8. [Network Monitoring and Diagnostics](#8-network-monitoring-and-diagnostics)
9. [Advanced Engage Controller](#9-advanced-engage-controller)
10. [Troubleshooting Methodology](#10-troubleshooting-methodology)
11. [Exam Tips — Level 2](#11-exam-tips--level-2)

---

## 1. Advanced Multicast — PIM Deep Dive

*Level 1 covered PIM modes at a concept level. Level 2 requires understanding how it is actually configured and how it interacts with IGMP Plus in multi-VLAN deployments.*

### Rendezvous Point (RP) Selection

In **PIM-SM**, the RP is the central coordination point for multicast. Choosing the right RP matters:

| Method | How It Works | Use Case |
|--------|-------------|---------|
| **Static RP** | Manually configure RP IP on every router | Small, stable networks; simple to understand |
| **Auto-RP** (Cisco proprietary) | RP announces itself via a dedicated multicast group | Cisco-dominated networks |
| **BSR (Bootstrap Router)** | RP candidates advertise via flood; best candidate wins | Standard (RFC 5059); preferred in mixed-vendor environments |
| **Anycast RP** | Multiple routers share the same RP IP address | Large networks requiring RP redundancy |

- For most ProAV networks: **static RP** is simplest
- The RP must be reachable from all multicast sources and receivers — place it on a core Layer 3 switch

### PIM Source-Specific Multicast (SSM)

- Receivers specify both the **group address AND the source IP** (`S, G` state)
- No RP needed — routers build a direct tree from receiver to the specific source
- More efficient and secure than PIM-SM (no RP to fail, no flooding)
- Requires **IGMPv3** on hosts (hosts must specify the source in IGMP Join)
- **AV use case:** A decoder that subscribes to a specific encoder — both source and group are known → SSM is ideal

### Multicast Address Ranges

| Range | Description |
|-------|-------------|
| `224.0.0.0/24` | Reserved — link-local multicast (never routed). STP, OSPF, PIM use these |
| `224.0.1.0–238.255.255.255` | Globally scoped — routable multicast |
| `239.0.0.0/8` | **Administratively scoped** — private, site-local (like RFC 1918 for multicast) |
| `232.0.0.0/8` | SSM range |

- **ProAV devices typically use the administratively scoped range** (`239.x.x.x`) to avoid routing conflicts
- Dante defaults to `239.255.x.x`; configure custom ranges in Dante Controller if needed

### Multicast State: (S,G) vs. (*,G)

| State | Meaning | Used By |
|-------|---------|--------|
| `(*,G)` | Any source sending to group G | PIM-SM shared tree (via RP) |
| `(S,G)` | Specific source S sending to group G | SSM, or after SPT switchover in PIM-SM |

- PIM-SM starts with `(*,G)` and may switch to `(S,G)` for efficiency once traffic flows
- SSM only ever uses `(S,G)` — never a shared tree

### IGMP Querier

- On a segment with no PIM router, IGMP still requires a **querier** to send periodic IGMP Query messages
- Without a querier, switches don't know when group members leave → multicast traffic lingers on ports indefinitely
- **IGMP Plus** on NETGEAR automatically handles querier election on the VLAN — another reason it simplifies deployment
- In multi-VLAN environments, ensure each AV VLAN has either a PIM-enabled router interface OR an IGMP querier (which Engage/IGMP Plus provides)

---

## 2. QoS — Deep Configuration

*Level 1 introduced QoS as a concept. Level 2 requires understanding DSCP values, queue configuration, and how to apply the right markings for each AV protocol.*

### DSCP (Differentiated Services Code Point)

- DSCP is a 6-bit field in the IP header — 64 possible values (0–63)
- Higher-priority traffic gets a higher DSCP value and is placed in a higher-priority queue
- Switches must be configured to **trust DSCP** (honour the markings set by end devices)

### Key DSCP Values for AV

| Traffic Type | DSCP Name | Value (decimal) | Binary | Hex |
|-------------|-----------|----------------|--------|-----|
| **Dante audio** | EF (Expedited Forwarding) | 46 | 101110 | 0x2E |
| **AES67 audio** | EF | 46 | 101110 | 0x2E |
| **ST 2110 video** | AF41 | 34 | 100010 | 0x22 |
| **Control/management** | CS1 or CS2 | 8 or 16 | — | — |
| **Best effort (data)** | BE | 0 | 000000 | 0x00 |

- **EF (Expedited Forwarding)** — highest priority, minimal jitter, for real-time audio
- **AF (Assured Forwarding)** — guaranteed bandwidth with drop priority options; for video
- **CS (Class Selector)** — backward-compatible with old IP Precedence; for control traffic

### Queue Architecture

NETGEAR AV switches implement **weighted or strict-priority queuing**:

| Queue | Priority | Traffic |
|-------|---------|--------|
| Q7 (highest) | Strict Priority | Dante/AES67 audio (EF 46) |
| Q6 | Strict Priority | Video streams (AF41 34) |
| Q5 | Weighted | Control/management |
| Q0–Q4 | Weighted (lower) | Data, best effort |

- **Strict Priority:** Queue is always served before lower queues — guaranteed low latency
- **Weighted Round Robin (WRR):** Lower queues get a proportional share of remaining bandwidth
- NETGEAR Engage profiles configure these queues automatically for supported AV protocols

### Trust Boundary

- Devices should only be trusted to mark their own traffic correctly up to the **trust boundary**
- At the switch port connected to an AV device: set the port to **DSCP trust** (honour markings from the endpoint)
- At the uplink toward the corporate network: may need to **re-mark or police** to prevent untrusted traffic flooding the high-priority queues

### Policing vs. Shaping

| Mechanism | Behaviour on Excess Traffic | Use Case |
|-----------|---------------------------|---------|
| **Policing** | Drops packets exceeding the rate | Enforcing upstream commitment |
| **Shaping** | Buffers/queues excess packets (adds latency) | Smoothing bursts before sending |

- For AV: **policing is preferred** — dropping is better than adding latency from shaping buffers
- Apply policing on the switch uplink from data VLAN to prevent IT traffic from consuming AV bandwidth

---

## 3. Layer 3 Routing on AV Networks

### Inter-VLAN Routing

- Required when AV streams need to cross VLAN boundaries (encoder on VLAN 10, decoders on VLAN 20)
- Implemented via:
  - **Layer 3 switch** with SVIs (Switched Virtual Interfaces) — preferred for AV
  - **Router-on-a-stick** — single uplink to a router with sub-interfaces (less common, creates bottleneck)

### SVI (Switched Virtual Interface)

- A logical interface on a Layer 3 switch assigned to a VLAN
- Acts as the default gateway for all devices in that VLAN
- Enables the switch to route between VLANs internally at wire speed (no external router hop)

```
VLAN 10 SVI: 10.10.10.1/24  ← default gateway for encoders
VLAN 20 SVI: 10.20.20.1/24  ← default gateway for decoders
Switch routes between them locally
```

### OSPF (Open Shortest Path First)

- Link-state routing protocol — each router knows the full topology
- Routers exchange **LSAs (Link State Advertisements)** to build a topology database
- Shortest path calculated via **Dijkstra's algorithm**
- Suitable for multi-switch AV networks where routes need to be dynamically discovered

**AV relevance:** In large multi-building AV installations with multiple Layer 3 switches, OSPF ensures that multicast routing (via PIM, which uses the unicast routing table) finds the correct paths automatically.

### Static Routes

- For simple AV networks (one or two VLANs, one router): static routes are sufficient and easier
- Add a static route for each remote subnet; no routing protocol overhead
- Example: `ip route 10.20.20.0/24 via 10.10.10.254` — tells the switch to send 10.20.20.x traffic to the gateway

### DHCP on NETGEAR Switches

- NETGEAR M-series switches can act as DHCP servers for AV devices
- Configure a DHCP pool per VLAN: IP range, subnet mask, default gateway, DNS
- Alternatively, use DHCP relay (`ip helper-address`) to forward DHCP requests from AV VLANs to a central DHCP server on the IT network

---

## 4. Advanced Security

### ACLs — Access Control Lists

- Rules that **permit or deny** traffic based on source IP, destination IP, protocol, and port
- Applied at the switch port level (ingress or egress)
- **AV use cases:**
  - Block IT/corporate VLAN traffic from entering the AV VLAN
  - Allow only specific management IPs to access switch management interface
  - Permit only expected multicast groups on AV ports

### Port Security

- Limits the number of MAC addresses allowed on a port (prevents rogue devices)
- Action on violation: **restrict** (drop + log), **protect** (drop silently), **shutdown** (disable port)
- Useful for: securing AV endpoints so only authorised encoders/decoders connect

### 802.1X — Port-Based Authentication

- Devices must **authenticate** before being granted network access
- Authentication via RADIUS server (corporate AAA infrastructure)
- For AV: less common (adds complexity, and many AV devices don't support 802.1X)
- When required (government/secure installs): configure 802.1X with MAB (MAC Authentication Bypass) for AV devices that can't authenticate themselves

### Management Security

- Change default switch passwords immediately
- Disable unused management protocols (Telnet — use SSH only)
- Restrict management access via ACL to a management VLAN IP range
- Enable **HTTPS** for web GUI access (disable HTTP)
- Use **SNMPv3** (authenticated, encrypted) — never SNMPv1/v2c in production
- Configure **login banners** for legal compliance

### Storm Control

- Limits the rate of **broadcast, multicast, and unknown unicast** traffic per port
- Prevents a misconfigured device or IGMP failure from flooding the entire switch with multicast
- Set a threshold (percentage of port bandwidth or packets per second)
- **AV tip:** Set conservative storm control thresholds on AV ports — a multicast flood can saturate an AV network and cause audio/video dropouts

---

## 5. Advanced Redundancy Patterns

### MLAG Deep Dive — Configuration and Peer Link

- The **peer link** (ISL) between the two MLAG switches carries:
  - Control traffic (MLAG heartbeat, state sync)
  - Data traffic when a connected device sends to a MAC address behind the other switch
- Peer link should be a **high-speed LAG** — typically 2× 10G or 2× 25G depending on switch model
- **Peer link failure** = MLAG split-brain scenario: each switch believes the other has failed
  - One switch becomes **primary** and keeps its ports active
  - The other switch enters **secondary/standby** and may take down its MLAG member ports
  - Preventing split-brain: ensure the peer link is redundant itself (multiple cables in a LAG)

### Stacking vs. MLAG (Expanded)

| Aspect | MLAG | Stacking |
|--------|------|---------|
| Geographical flexibility | **High** — different rooms, floors, racks | Low — short stacking cable limits |
| Failure domain | Independent switches — one failure doesn't affect other | Stack ring failure can split the stack |
| Management | Two switches, one logical | One logical management plane |
| Bandwidth | Limited by peer link | Higher aggregate (stack backplane) |

**When to use MLAG:** Core redundancy in spine-and-leaf, geographically separated switches  
**When to use Stacking:** Access layer expansion (more ports in same location), simplified management

### Graceful Restart / NSF (Non-Stop Forwarding)

- When a routing process restarts (software update, process crash), NSF allows the switch to **keep forwarding traffic** while the routing table is rebuilt
- Prevents a brief software restart from causing a network-wide disruption
- Supported on NETGEAR M4350/M4500 with OSPF NSF

### BFD — Bidirectional Forwarding Detection

- Very fast (sub-second) detection of link or neighbour failures
- Works with routing protocols (OSPF, static routes) to trigger faster failover than native protocol timers
- In AV: use BFD with OSPF on the core routing switches to ensure sub-second failover detection

---

## 6. AV-over-IP Protocol Stacks

### Dante

- **Developer:** Audinate
- **Layer:** IP Unicast and Multicast (UDP/RTP)
- **Sync:** PTP (IEEE 1588 v1)
- **Discovery:** Proprietary mDNS-based
- **Configuration tool:** Dante Controller (separate application)
- **Network requirements:** IGMP snooping (or IGMP Plus), QoS EF DSCP 46, EEE disabled, 1G minimum
- **Latency:** Configurable: 1 ms (near field), up to 10 ms (long distances)
- **Channel count:** Up to 512 transmit + 512 receive per device (hardware-dependent)
- **Copy protection:** None (open network transport)
- **Engage profile:** Dante profile — enables IGMP Plus, DSCP 46 trust, EEE off, jumbo frames off

### AES67

- **Developer:** AES (Audio Engineering Society), IEEE standard
- **Purpose:** Interoperability layer — allows Dante, Ravenna, Livewire, and Q-LAN to exchange audio
- **Layer:** IP Multicast (UDP/RTP)
- **Sync:** PTP (IEEE 1588 v2 / IEEE 802.1AS)
- **DSCP:** EF (46) — same as Dante
- **Key standard components:** RFC 3550 (RTP), RFC 3551 (RTP profile), IEEE 1588 PTP
- **Limitation:** AES67 is a transport standard only — does not define device discovery or control (each ecosystem retains its own discovery)

### NDI (Network Device Interface)

- **Developer:** Vizrt (formerly NewTek)
- **Layer:** IP (TCP/UDP)
- **Type:** Compressed video + audio over IP; proprietary
- **Discovery:** mDNS (Bonjour / Zeroconf)
- **Network requirements:** Jumbo frames (9000 MTU) recommended, IGMP snooping, multicast enabled
- **Bandwidth:** NDI Full ~125 Mbps per 1080p60 stream; NDI|HX (compressed) ~10–20 Mbps
- **Latency:** 1–3 frames (~17–50 ms at 60fps)
- **Engage profile:** NDI profile — enables jumbo frames, IGMP Plus, appropriate QoS

### SDVoE (Software Defined Video over Ethernet)

- **Developer:** SDVoE Alliance (Semtech is the ASIC maker behind most implementations)
- **Type:** Lossless/uncompressed video over 10G Ethernet
- **Network requirements:** **10G everywhere** (non-negotiable), non-blocking switch, IGMP snooping, multicast, jumbo frames
- **Bandwidth:** ~10 Gbps per 4K60 stream (hence 10G requirement)
- **Latency:** Sub-frame (< 1 ms glass-to-glass)
- **Discovery:** SDVoE API / third-party control systems
- **Engage profile:** SDVoE/uncompressed video profile — 10G, jumbo frames, strict QoS

### ST 2110 (Broadcast Standard — overview)

*(Covered in depth in the IPMX notes — brief summary here)*

- **Developer:** SMPTE
- **Type:** Uncompressed video (ST 2110-20), PCM audio (ST 2110-30), ancillary data (ST 2110-40)
- **Network requirements:** 10G (for HD uncompressed), 25G/100G for 4K; PTP sync; IGMP snooping
- **Sync:** PTP (IEEE 1588-2008 / IEEE 802.1AS-2011)
- **Discovery/control:** NMOS (IS-04 / IS-05)
- **Primary use:** Broadcast facilities; ProAV adoption via IPMX

### Protocol Comparison Matrix

| Protocol | Video | Audio | Compression | Max Bandwidth | Latency | Open Standard? |
|----------|-------|-------|-------------|--------------|---------|---------------|
| Dante | No | Yes | None (PCM) | ~100 Mbps | 1–10 ms | No (Audinate) |
| AES67 | No | Yes | None (PCM) | ~100 Mbps | varies | Yes (AES) |
| NDI | Yes | Yes | Proprietary | 125+ Mbps/stream | 17–50 ms | No (Vizrt) |
| SDVoE | Yes | Yes | None | ~10 Gbps/stream | <1 ms | No (Alliance) |
| ST 2110 | Yes | Yes | None (uncompressed) | 10–25 Gbps/stream | sub-frame | Yes (SMPTE) |
| IPMX | Yes | Yes | JPEG-XS + uncompressed | 1G+ /stream | sub-frame | Yes (AIMS) |

---

## 7. Jumbo Frames, EEE, and Flow Control

*(These were identified as Level 1 gaps — covered in depth here as exam-critical for Level 2)*

### Jumbo Frames — Configuration

- Standard MTU: **1500 bytes**. Jumbo MTU: **9000 bytes** (or 9216 bytes on some switches)
- Enable at the switch level **and** on every NIC/endpoint in the path
- On NETGEAR switches: set via GUI → Port Configuration → MTU, or via CLI `mtu 9216`
- **Check:** Use `ping -s 8972` (8972 + 28 byte IP/ICMP header = 9000) between endpoints to verify jumbo path
- If any switch or NIC in the path does not support jumbo frames, packets larger than 1500 bytes are fragmented or dropped

### EEE — Diagnosing and Disabling

- Symptom: Dante reports "clock drift" or "audio dropout" even with healthy network; problem is intermittent
- **Disable EEE per port** on NETGEAR: GUI → System → Green Ethernet → disable per port, or via CLI `no green-mode eee`
- Engage Dante/AES67/SDVoE profiles disable EEE automatically on assigned ports
- **Always verify EEE is off on every port in the audio path**, including intermediate switches

### Flow Control — When and Why

| Scenario | Use Flow Control? | Reason |
|----------|-----------------|--------|
| 1G AV-only switch | No | QoS is sufficient; flow control adds latency |
| 10G switch with SDVoE/ST 2110 | Consider PFC | High burst rates; prevents buffer overflow |
| Mixed AV + IT on same switch | No standard FC | Head-of-line blocking would hurt AV |

- **Priority Flow Control (PFC):** Pauses only specific traffic classes (per DSCP queue), not the entire link — prevents one traffic type from starving another
- PFC requires **Data Center Bridging (DCB)** capability — supported on M4350/M4500

---

## 8. Network Monitoring and Diagnostics

### SNMP (Simple Network Management Protocol)

- Polling-based monitoring: management system requests metrics from switches at intervals
- **SNMPv3** is the required version for production (authentication + encryption)
- Key MIBs for AV networks:
  - `ifXTable` — per-port utilisation, errors, discards
  - `dot1qVlan` — VLAN membership
  - `dot3Stats` — Ethernet error counters

### sFlow

- **Packet sampling** — the switch sends a copy of 1 in N packets to an sFlow collector
- Provides traffic analysis without capturing every packet (low overhead)
- Useful for: identifying top talkers, unexpected multicast sources, bandwidth planning
- Available on NETGEAR M4350/M4500

### Port Mirroring / SPAN

- **SPAN (Switched Port Analyzer):** Mirrors all traffic on one port to another port (where a capture device is connected)
- Use Wireshark on the capture device to inspect actual packet contents
- **AV use cases:** Verify DSCP markings, inspect IGMP messages, diagnose multicast group membership, capture PTP packets

### Logging and Syslog

- Configure NETGEAR switches to send **syslog** messages to a central log server
- Critical events to log: link up/down, port security violations, authentication failures, storm control triggers
- Use a syslog server (Graylog, Splunk, or even a simple rsyslog instance)

### Ping and Traceroute

- **Ping:** Tests basic IP reachability (ICMP echo); does not test UDP delivery (AV streams use UDP)
- **Traceroute:** Identifies the hop-by-hop path and latency at each hop; identifies routing loops or unexpected paths
- **For AV:** Ping/traceroute passing does not guarantee that multicast is working correctly — verify with IGMP show commands and actual stream tests

### NETGEAR Diagnostic Tools

| Tool | Access | Use Case |
|------|--------|---------|
| **Port statistics** | Engage GUI / Web GUI | Per-port packet counts, errors, discards |
| **Cable test** | Web GUI → Diagnostics | TDR — detects open, short, or length of cable |
| **Event log** | Web GUI → Maintenance | Switch event history (link up/down, errors) |
| **Ping / traceroute** | Web GUI → Diagnostics | Reachability and path verification |
| **Packet capture (SPAN)** | External Wireshark via SPAN port | Deep packet inspection |

---

## 9. Advanced Engage Controller

### Custom Profiles

- Beyond the built-in profiles (Dante, AES67, NDI, SDVoE), you can create **custom profiles**
- Custom profiles set: VLAN ID, IGMP Plus, QoS/DSCP trust, EEE state, storm control, jumbo frames, PoE settings
- Save custom profiles and push to any port across any managed switch in the site

### Multi-Site Management

- Engage can manage multiple **sites** from one installation
- Each site has its own set of switches and profiles
- Use cases: managed service providers, integrators managing multiple customer networks

### Firmware and Configuration Backup

- Engage → Firmware: update all switches from a single interface
- Always back up switch configuration before firmware updates (export config file)
- Engage can restore configurations to a replacement switch — critical for rapid on-site recovery

### Port Grouping and Bulk Assignment

- Select multiple ports across multiple switches and assign a profile in one action
- Essential for large deployments (e.g., applying Dante profile to all 48 ports on 6 switches at once)

### Topology View

- Visual representation of detected switches and their interconnections
- Helps quickly identify: unconnected devices, unexpected topologies, MLAG pairs, uplink links
- Colour-coded by profile assignment

---

## 10. Troubleshooting Methodology

### The AV Networking Troubleshooting Framework

```
1. CONFIRM THE SYMPTOM — specific (which stream? which device? intermittent or constant?)
2. CHECK PHYSICAL LAYER — cables, SFP optics, port link LEDs, cable test
3. CHECK LAYER 2 — VLAN membership, trunk ports, STP state, MAC table
4. CHECK MULTICAST — IGMP group membership, IGMP Plus state, querier present?
5. CHECK LAYER 3 — routing (if cross-VLAN), PIM state, RP reachable?
6. CHECK QoS — DSCP markings, queue assignment, port statistics (discards = congestion)
7. CHECK AV PROTOCOL — Dante Controller (clock, routes), NMOS, endpoint status
8. CHECK ENGAGE — profile applied? correct VLAN? EEE off? jumbo frames correct?
```

### Common Fault Patterns

| Symptom | First Check | Common Cause |
|---------|-----------|-------------|
| Audio dropout (intermittent) | EEE status on all ports | EEE enabled; disable it |
| No multicast stream received | IGMP group membership (switch show) | IGMP Plus not enabled on VLAN |
| Dante clock drift | PTP/clock domain in Dante Controller | Clock master conflict or high-jitter link |
| High latency on AV stream | Port statistics (discards/errors) | Congestion, QoS misconfiguration |
| Multicast flooding all ports | IGMP querier present? | No querier — IGMP Plus resolves this |
| NDI stream unstable | Jumbo frames end-to-end | MTU mismatch somewhere in path |
| MLAG not forming | Peer link up? Same MLAG domain ID? | Peer link down, domain ID mismatch |
| SFP not detected | SFP type match cable type? | SR optic in SMF cable (wrong) |
| VLAN traffic not crossing switches | Trunk port configuration | Trunk missing VLAN or Auto Trunk didn't trigger |

### Dante-Specific Diagnostics

- **Dante Controller → Network View:** Shows all Dante devices, sample rate, latency settings
- **Device View → Clock:** Identifies master/slave status; clock conflicts show in red
- **Routing matrix:** Green = active route, grey = no route — check that source channels are patched
- **Dante Controller events log:** Timestamps of lost/restored device connections

### Reading Switch Port Statistics

- **Input errors:** damaged frames arriving at the switch — physical layer issue (bad cable, SFP, connector)
- **Output discards:** frames dropped due to congestion — QoS or bandwidth issue
- **CRC errors:** frame corruption — usually physical layer (EMI, bad cable, duplex mismatch)
- **Runts/giants:** frames outside valid size range — duplex mismatch or faulty NIC

---

## 11. Exam Tips — Level 2

- Know the **multicast address ranges**: link-local (224.0.0.0/24), admin-scoped (239.x.x.x/8), SSM (232.x.x.x/8)
- Know **(S,G) vs. (*,G)** state and when each is used (SSM always S,G; PIM-SM starts with *,G)
- Know **DSCP values by heart**: EF = 46 (audio), AF41 = 34 (video), BE = 0 (data)
- Understand **strict priority vs. WRR** queuing and which traffic goes where
- Know the difference between **Dante, AES67, NDI, SDVoE, and ST 2110** — compression, latency, bandwidth, open/proprietary
- Know **why EEE breaks AV audio** and how to disable it (per port; Engage does it automatically)
- Know **jumbo frames**: when they're needed (NDI, SDVoE), how to verify (ping -s), what breaks if MTU mismatched
- Know **MLAG peer link** requirements — LAG recommended, what happens on peer link failure (split-brain)
- Understand the **AV troubleshooting framework** — physical → L2 → multicast → L3 → QoS → application
- Know how to read **port statistics** to identify congestion vs. physical errors
- Know **SNMP, sFlow, and SPAN** — what they are and when to use each
- Know **PIM RP selection methods** — static RP is simplest for ProAV; know BSR for standards-based approach
- Understand **inter-VLAN routing** and when it's needed for AV streams

---

## Key Terms Glossary — Level 2

| Term | Definition |
|------|-----------|
| **RP (Rendezvous Point)** | PIM-SM coordination point for multicast source registration |
| **SSM** | Source-Specific Multicast — receivers specify source AND group; no RP needed |
| **(S,G)** | Multicast state for specific Source + Group pair |
| **(*,G)** | Multicast state for any source sending to group G |
| **BSR** | Bootstrap Router — standards-based RP election mechanism |
| **DSCP** | Differentiated Services Code Point — 6-bit QoS marking in IP header |
| **EF** | Expedited Forwarding — highest-priority DSCP (value 46); used for audio |
| **AF41** | Assured Forwarding class 4, drop precedence 1 — DSCP 34; used for video |
| **SVI** | Switched Virtual Interface — Layer 3 interface on a VLAN for inter-VLAN routing |
| **OSPF** | Open Shortest Path First — link-state routing protocol |
| **NSF** | Non-Stop Forwarding — keeps traffic flowing during routing process restart |
| **BFD** | Bidirectional Forwarding Detection — fast failure detection for routing |
| **PFC** | Priority Flow Control — per-queue pause frames (DCB feature) |
| **SDVoE** | Software Defined Video over Ethernet — uncompressed 10G video protocol |
| **sFlow** | Packet sampling for traffic analysis; low overhead |
| **SPAN** | Switched Port Analyzer — port mirroring for packet capture |
| **Storm Control** | Rate-limits broadcast/multicast to prevent flooding |
| **MAB** | MAC Authentication Bypass — authenticates non-802.1X devices by MAC address |
| **IGMP Querier** | Sends periodic IGMP Queries to maintain multicast group membership |
