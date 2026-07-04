# NETGEAR AV Certification — Level 1 Notes

> **Depth key:** Topics marked *(review)* are abbreviated — you already know these from CCNA/Dante/CTS-I study. Topics marked *(new)* or *(deep)* are Netgear-specific or new material covered in detail.

---

## Table of Contents

1. [Module 1 – The OSI Model (review)](#module-1--the-osi-model)
2. [Module 2 – Defining a Network (review)](#module-2--defining-a-network)
3. [Module 3 – Topology and Design (mixed)](#module-3--topology-and-design)
4. [Module 4 – Unicast, Multicast, and Broadcast (deep on IGMP Plus)](#module-4--unicast-multicast-and-broadcast)
5. [Module 5 – Understanding VLANs (review)](#module-5--understanding-vlans)
6. [Module 6 – Understanding Terminology (deep)](#module-6--understanding-terminology)
7. [Module 7 – NETGEAR Enterprise Switches (new)](#module-7--netgear-enterprise-switches)
8. [Module 8 – Engage Controller (new)](#module-8--engage-controller)
9. [Module 9 – Specifying NETGEAR Switches (new)](#module-9--specifying-netgear-switches)

---

## Module 1 – The OSI Model

*You know this thoroughly from CCNA. Quick reference for the exam.*

### 7-Layer Recap

| Layer | Name | Key Function | AV Relevance |
|-------|------|-------------|--------------|
| 1 | Physical | Raw signal transmission via PHY | Cable type, connector, speed |
| 2 | Data Link | MAC addressing, framing, error detection | Switches operate here |
| 3 | Network | IP routing, logical addressing | Multicast, subnetting |
| 4 | Transport | TCP (reliable) / UDP (fast, unordered) | AV streams use UDP/RTP |
| 5 | Session | Connection management, synchronization | Video conferencing sessions |
| 6 | Presentation | Encryption, compression, translation | Codec encoding |
| 7 | Application | End-user protocols (HTTP, FTP, SMTP) | Control interfaces, APIs |

### Key Exam Points

- **Hardware layers = 1–4**, Software layers = 5–7
- AV networking professionals focus on **Layers 1–4**
- **PHY** (Physical Layer Device) converts digital data ↔ physical signals
- **Encapsulation:** Each layer adds its own header as data moves down the stack
- **Packet switching:** Data broken into packets; resilient to congestion or link failure
- **Routers** handle Layer 3+ tasks: routing across networks, DHCP, failover, load balancing
- Switches primarily operate at **Layer 2** (some at Layer 3 for inter-VLAN routing)

---

## Module 2 – Defining a Network

*Heavily covered in your CCNA notes. Brief refresh.*

### Network Types

- **LAN** — Local Area Network (office, venue)
- **WAN** — Wide Area Network (cities, countries)
- **WLAN** — Wireless LAN (radio/Wi-Fi)
- All built on **Ethernet** (1970s standard, packet-based communication)

### MAC Addresses

- Unique identifier on every NIC, operates at **Layer 2**
- Networks are constructed at Layer 2 within **broadcast domains**

### Broadcast Domains

- A broadcast frame reaches **all devices** in the same domain
- Unmanaged = performance degradation from data floods
- VLANs segment broadcast domains (covered Module 5)

### Subnets & CIDR (Quick Reference)

- **Layer 3** concept — connects multiple broadcast domains via IP
- **Subnet mask** filters which IPs can communicate locally
- **CIDR** = variable-length subnet masks (e.g., /24, /22) — you know this well
- **Broadcast address** = always the last IP in each subnet
- NETGEAR Engage automates routing table creation (relevant later)

### IPv4 vs IPv6

- **IPv4:** 32-bit (~4B addresses), still dominates private networks
- **IPv6:** 128-bit (virtually unlimited), autoconfig support
- Both coexist; AV networks overwhelmingly use IPv4

---

## Module 3 – Topology and Design

*You know star/ring/bus/mesh from CCNA. The AV-specific topologies are the exam focus.*

### Common Topologies (Brief)

- **Star:** Central hub, easy fault isolation
- **Ring:** Closed loop, predictable flow
- **Bus:** Single cable, outdated
- **Mesh:** Multiple paths, redundancy

### Spine and Leaf Topology *(important for AV)*

- Modern architecture ideal for **high data loads in AV environments**
- **Spine switches** = core aggregation layer
- **Leaf switches** = access layer connected to endpoints
- Benefits:
  - Low latency via direct device-to-switch connections
  - No bottlenecks — high throughput for real-time AV
  - Flexible expansion with minimal disruption
- **This is the go-to topology for dynamic, high-performance AV networks**

### Stacked Core Topology *(important for AV)*

- Two or more switches consolidated into a **single logical unit**
- Benefits:
  - **Redundancy** — no single point of failure
  - **Simplified management** — one logical control plane
  - **Performance** — integrated traffic management
- Essential for **mission-critical networks** (live events, broadcast, emergency services)

### Network Speeds

- **1G:** General tasks, insufficient for modern high-bandwidth AV
- **10G:** Becoming the AV baseline for HD video, live streaming, real-time processing
- Supports simultaneous HD streams + file transfers without degradation

### Copper vs Fiber

| Feature | Copper (Cat5e–Cat8) | Fiber Optic |
|---------|-------------------|-------------|
| Cost | Lower | Higher |
| Distance | Short (up to 100m) | Long (kilometers) |
| Speed | Up to 10Gbps | 10G–100G+ |
| EMI immunity | No | Yes |
| Best for | Endpoint connections | Uplinks, long backhauls |

#### Single-Mode Fiber (SMF) vs Multi-Mode Fiber (MMF) — Deep Dive

| Property | Single-Mode (SMF) | Multi-Mode (MMF) |
|----------|-------------------|-------------------|
| **Core diameter** | 8–10 µm (tiny) | 50 µm (OM3/OM4/OM5) or 62.5 µm (OM1/OM2) |
| **Light source** | Laser (narrow, focused beam) | LED or VCSEL (broader beam) |
| **Light paths** | One mode (straight down the center) | Multiple modes (light bounces at many angles) |
| **Max distance** | Up to **80+ km** (depending on optic) | **OM3:** 300m at 10G / **OM4:** 400m at 10G / **OM5:** 400m at 10G, designed for WDM |
| **Bandwidth** | Virtually unlimited (low dispersion) | Lower — modal dispersion limits distance |
| **Cost of cable** | Similar or slightly more than MMF | Similar |
| **Cost of optics** | **More expensive** (laser transceivers) | **Cheaper** (VCSEL/LED transceivers) |
| **Connector color** | Yellow jacket / Blue SC or LC | Orange (OM1/OM2) or Aqua (OM3/OM4) jacket |
| **Typical use** | Long backhauls, campus links, building-to-building | In-building, switch-to-switch, data center backbone |

**Why this matters for AV:**

- **Long venue runs (> 300m):** SMF is the only option — think arena or campus backhauls from FOH to amp rooms in different buildings
- **Short switch-to-switch runs (< 300m):** MMF (OM3/OM4) is more cost-effective because the optics (SFP+ transceivers) are significantly cheaper
- **NETGEAR M4250/M4350 SFP+ ports** accept both SMF and MMF transceivers — you choose the optic to match the cable plant
- **10G uplinks in spine-and-leaf designs** typically use MMF (OM3/OM4) with short-reach SFP+ optics (SR = Short Range)
- **100G QSFP ports on M4350/M4500** can use either; for long runs, SMF with LR4 (Long Range) optics

**Key concept — modal dispersion:**
In MMF, light travels at multiple angles (modes). Different modes arrive at the destination at slightly different times, causing the signal to spread out ("disperse"). This limits both distance and bandwidth. SMF eliminates this entirely — only one mode propagates — which is why it can go so much further.

**Common SFP+ optic types you'll encounter:**

| Optic | Fiber Type | Wavelength | Max Distance | Cost |
|-------|-----------|------------|-------------|------|
| **SFP+ SR** (Short Range) | MMF (OM3/OM4) | 850nm | 300–400m | $ (cheapest) |
| **SFP+ LR** (Long Range) | SMF | 1310nm | 10 km | $$ |
| **SFP+ ER** (Extended Range) | SMF | 1550nm | 40 km | $$$ |
| **QSFP28 SR4** | MMF | 850nm | 100m at 100G | $$ |
| **QSFP28 LR4** | SMF | 1310nm | 10 km at 100G | $$$$ |

**Pro tip:** Fiber = reliable, uninterrupted signal quality for AV. Always match your optic type to the cable plant — you can't plug an SR optic into single-mode cable (wrong wavelength and core size).

### Bandwidth Management

- **QoS** to prioritize critical traffic (video > general data)
- Traffic shaping and rate limiting
- You know this from Dante QoS study — same principles apply

### Network Security

- Firewalls, intrusion detection, regular audits
- Compliance requirements for sensitive industries
- Integrated at every stage of network design

---

## Module 4 – Unicast, Multicast, and Broadcast

*You know unicast/multicast/broadcast and IGMP from Dante study. The new material here is **IGMP Plus™** and **PIM** — these are exam-critical.*

### Unicast (Brief)

- One-to-one: single sender → single receiver
- Used for control data in ProAV (small, bursty, on-demand)
- Examples: emails, server requests, point-to-point control streams

### Broadcast (Brief)

- One-to-all: sender → every device in the broadcast domain
- Necessary for discovery protocols but generates excess traffic
- Contained within VLANs

### Multicast *(AV Critical)*

- One-to-many: sender → only devices that **request** the stream
- Balances exclusivity of unicast with reach of broadcast
- **ProAV use cases:**
  - Live event streaming
  - Webinars
  - Real-time data sharing (scoreboards, tickers)
- **How it works:** Network infrastructure duplicates packets **only when necessary** (at branch points), not at the source
- Much more bandwidth-efficient than duplicating unicast streams per endpoint

### IGMP — Internet Group Management Protocol *(review)*

- Devices send **IGMP Join** requests to receive a multicast stream
- Routers maintain a **membership list** of active group members
- Periodic **IGMP Queries** confirm membership; inactive members are pruned
- Result: multicast streams sent only to active, interested recipients

### PIM — Protocol Independent Multicast *(exam topic)*

PIM is a **multicast routing protocol** that determines how multicast traffic is forwarded **between routers** across different network segments. It's a Layer 3 protocol that sits above IGMP.

#### Why "Protocol Independent"?

- PIM doesn't maintain its own routing table
- It uses whatever **unicast routing table** already exists (OSPF, EIGRP, static routes, etc.)
- It only cares about: "What's the best path to the multicast source?" and uses the existing unicast routes to answer that

#### PIM Modes (Know These)

| Mode | How It Works | Use Case |
|------|-------------|----------|
| **PIM Sparse Mode (PIM-SM)** | Traffic only sent to routers that explicitly request it; uses a Rendezvous Point (RP) to coordinate | Most common in enterprise/AV — efficient for selective receivers |
| **PIM Dense Mode (PIM-DM)** | Floods multicast everywhere, then prunes back where it's not needed | Small/simple networks — wasteful on large networks |
| **PIM Source-Specific Multicast (SSM)** | Receivers specify both the group AND the source — no RP needed | High-security or single-source applications |

#### PIM in the AV Context

- When multicast AV traffic needs to cross **between VLANs or between routers** (e.g., an encoder on one subnet and decoders on another), PIM is what routes it
- Within a single VLAN/switch, you only need IGMP snooping (or IGMP Plus on Netgear)
- **PIM + IGMP work together:** IGMP manages local group membership on a LAN segment; PIM uses that info to route multicast between segments

#### How PIM-SM Works (Simplified)

1. A **Rendezvous Point (RP)** is designated — this is a router that acts as a meeting point
2. Multicast sources register their streams with the RP
3. Receivers send IGMP Joins → their local router sends PIM Join toward the RP
4. The RP connects sources and receivers, building a multicast distribution tree
5. Once traffic is flowing, PIM can switch to a **shortest-path tree** directly from source to receiver (bypassing the RP for efficiency)

#### Key Distinction: PIM vs IGMP vs IGMP Plus

| Protocol | Layer | Scope | Function |
|----------|-------|-------|----------|
| **IGMP** | L3 (host↔router) | Single LAN segment | Hosts join/leave multicast groups |
| **IGMP Plus™** | L2 (switch) | Single LAN / VLAN | Switch-level multicast optimization (Netgear-specific) |
| **PIM** | L3 (router↔router) | Across multiple networks | Routes multicast between subnets/VLANs |

### IGMP Plus™ *(NETGEAR proprietary — deep, exam-critical)*

IGMP Plus is a **NETGEAR enhancement** implemented in their switches to simplify multicast traffic management. This is one of NETGEAR's key differentiators in AV.

#### What It Does

- Monitors IGMP conversations between hosts and routers
- **Eliminates the need for multiple CLI commands** to configure multicast on VLANs
- Conserves bandwidth by limiting multicast traffic to only the **relevant ports**

#### Key Difference from Standard IGMP Snooping

| Feature | Standard IGMP Snooping | IGMP Plus™ |
|---------|----------------------|-------------|
| Configuration | Multiple CLI commands per VLAN | **Single command** |
| Scope | Local segment management | Local segment management |
| Error risk | Higher (many steps) | Lower (simplified) |
| Multicast flooding | Can still occur with misconfiguration | Actively prevents flooding |
| AV optimization | Generic | **Purpose-built for ProAV** |

#### Without IGMP Plus

- Multicast traffic from transmitters/encoders is sent **indiscriminately to ALL ports**
- Creates excess traffic and potential bottlenecks
- Data devices receive AV multicast they don't need

#### With IGMP Plus

- Only **requested multicast traffic** is forwarded to the correct decoder/endpoint
- Significantly improves network efficiency
- ProAV and data traffic **coexist seamlessly** without performance compromise

#### Use Case: Spine and Leaf Architectures

- IGMP Plus can be applied **across all switches** in a multi-switch topology
- Enable IGMP Plus on a VLAN → multicast streams distributed efficiently across the entire fabric
- Avoids unnecessary traffic and bandwidth issues in complex setups

#### Practical Impact

- For Dante networks: IGMP Plus replaces the manual IGMP snooping + querier + mrouter configuration you'd do on Cisco
- Single toggle per VLAN instead of configuring snooping, querier, and static mrouter ports individually
- Dramatically reduces deployment time and configuration errors

---

## Module 5 – Understanding VLANs

*You know VLANs extensively from CCNA + Dante. Brief review with Netgear AV framing.*

### VLAN Basics (Quick Reference)

- Logical subdivision of a physical network
- Devices grouped logically, not physically
- Communication as if on the same physical network, even across switches
- Benefits: **security**, **performance** (own broadcast domain), **simplified management**

### VLAN Port Types

| Port Type | Function | Use Case |
|-----------|----------|----------|
| **Access** | Carries traffic for **one VLAN** only | Endpoint devices (encoders, decoders) |
| **Trunk** | Carries traffic for **multiple VLANs** | Inter-switch links, switch-to-router |

### VLAN Tagging (802.1Q)

- Adds a **VLAN ID** to each Ethernet frame
- Trunk ports use tagging to manage multi-VLAN traffic on a single link
- Ensures traffic directed to the correct VLAN

### Control VLANs *(important for AV design)*

- Dedicated VLAN for **network management and control traffic**
- Isolates management functions (switch management, STP) from production traffic
- Enhances security and ensures uninterrupted network control
- **Typical AV design:**
  - Control VLAN — switch management, STP
  - AV VLAN(s) — video/audio streams (e.g., Dante Primary, Dante Secondary)
  - Data VLAN(s) — general office/IT traffic
  - Access ports connect endpoints; trunks link switches

---

## Module 6 – Understanding Terminology

*This module bridges IT and AV. Some concepts are familiar from CCNA; the Netgear-specific automation features are new.*

### Link Aggregation *(review + new Netgear features)*

- Combines multiple physical links into a **single logical link**
- Benefits: **increased bandwidth**, **redundancy** (if one link fails, others maintain connectivity)

#### LACP (Link Aggregation Control Protocol)

- Dynamically detects and configures compatible links
- You know this from CCNA — same protocol, same behavior on Netgear

#### Auto LAG *(NETGEAR-specific — exam topic)*

Auto LAG is NETGEAR's automation layer on top of standard LACP. On Cisco or other vendors, you manually define port-channel groups, assign interfaces, and set LACP mode. NETGEAR removes that entirely.

**How Auto LAG works step by step:**

1. You connect multiple cables between two NETGEAR switches
2. The switches detect that these links connect to the **same partner switch** (via LLDP/LACP negotiation)
3. Auto LAG **automatically bundles them** into a single logical LAG group
4. LACP runs underneath to manage the bundle dynamically
5. If you add another cable between the same two switches, it's automatically added to the existing LAG

**What you DON'T have to do (compared to Cisco):**

| Manual step on Cisco | Auto LAG on Netgear |
|---------------------|--------------------|
| `interface range gi1/0/1 - 4` | Not needed |
| `channel-group 1 mode active` | Not needed |
| `interface port-channel 1` | Created automatically |
| `switchport mode trunk` | Handled by Auto Trunk |

**Key details:**
- Auto LAG is **enabled by default** on NETGEAR AV switches
- Works between NETGEAR switches and also with third-party switches that support standard LACP
- Combined with Auto Trunk, connecting two Netgear switches is literally plug-and-play: plug in cables → LAG forms → trunking negotiates → VLANs carry
- Maximum links per LAG group depends on the switch model (typically 8)
- Load balancing across LAG members uses a hash (typically src/dst MAC or IP)

#### Auto Trunk *(NETGEAR-specific — exam topic)*

Auto Trunk is the partner feature to Auto LAG. While Auto LAG bundles the physical links, Auto Trunk handles the **VLAN configuration** on those links.

**How Auto Trunk works step by step:**

1. A port detects that it's connected to **another switch** (via LLDP — Link Layer Discovery Protocol)
2. The port automatically transitions from access mode to **trunk mode**
3. The trunk is configured to carry **all VLANs** defined on the switch
4. 802.1Q tagging is enabled automatically

**What you DON'T have to do (compared to Cisco):**

| Manual step on Cisco | Auto Trunk on Netgear |
|---------------------|----------------------|
| `switchport mode trunk` | Detected automatically |
| `switchport trunk allowed vlan 10,20,30` | All VLANs allowed by default |
| `switchport trunk native vlan 1` | Default native VLAN used |

**Key details:**
- Auto Trunk uses **LLDP** to detect switch-to-switch connections
- If a port detects an endpoint (not a switch), it stays as an **access port** — it won't accidentally trunk to a computer
- You can still **manually override** Auto Trunk on specific ports if needed
- The combination works like this:

```
Plug cables between switches
  → LLDP detects switch-to-switch
  → Auto Trunk enables 802.1Q trunking
  → Auto LAG bundles the links
  → Result: multi-link trunk carrying all VLANs, zero CLI commands
```

**Why this matters for AV deployments:**
- An AV integrator who isn't a networking specialist can physically cable a spine-and-leaf topology and have it just work
- Drastically reduces deployment time on site
- Fewer configuration errors = fewer troubleshooting calls
- Still fully compatible with manual configuration for advanced scenarios

### Spanning Tree Protocol (STP) *(review)*

- Ensures **loop-free topology** in Layer 2 networks
- Root bridge manages topology; STP calculates best path
- Blocks redundant paths to prevent broadcast storms
- **You know RSTP/802.1D/PVST+ in depth from CCNA + Dante study**
- For the Netgear exam: know that STP is active on these switches and prevents loops

### MLAG — Multi-Chassis Link Aggregation *(deep — exam topic)*

MLAG extends Link Aggregation **across multiple physical switches**, treating them as a **single logical switch**. This is one of the most important high-availability features for AV networks.

#### The Problem MLAG Solves

Imagine you have an access switch connected to a single core switch. If that core switch fails, **everything connected through it loses connectivity**. The obvious solution is to connect to two core switches — but then STP kicks in and **blocks one of the uplinks** to prevent a loop. You have redundancy for failover, but you're wasting half your uplink bandwidth during normal operation.

MLAG solves both problems: **full redundancy AND full bandwidth utilization**.

#### How MLAG Works Step by Step

1. **Two core switches** are connected to each other via a dedicated **peer link** (also called an ISL — Inter-Switch Link)
2. The two switches negotiate and present themselves as a **single logical switch** to all downstream devices
3. An access switch connects **one or more links to each core switch**
4. From the access switch's perspective, all those links form a **single LAG** — it doesn't know it's talking to two physical switches
5. Traffic is **load-balanced across both core switches** simultaneously
6. If one core switch fails:
   - The peer link detects the failure
   - The surviving switch takes over all traffic
   - Convergence is near-instant (typically < 1 second)
   - No STP recalculation needed

#### MLAG vs Traditional STP Redundancy

| Aspect | STP Redundancy | MLAG |
|--------|---------------|------|
| **Active uplinks** | Only one (other blocked) | **All links active** |
| **Bandwidth utilization** | 50% (blocked link wasted) | **100%** |
| **Failover time** | 1–50 seconds (STP reconvergence) | **< 1 second** |
| **Loop prevention** | STP blocks redundant paths | MLAG peer coordination |
| **Complexity** | Simple but wasteful | Slightly more setup but much better performance |

#### MLAG vs Stacking

You might wonder how MLAG differs from physically stacking switches:

| Feature | MLAG | Stacking |
|---------|------|----------|
| **Physical location** | Switches can be in **different racks/rooms** | Must be physically adjacent (stacking cables are short) |
| **Failure domain** | If one switch fails, the other is fully independent | A stack failure can take down all switches |
| **Scalability** | 2 switches (peer pair) | Varies (4–8 in a stack) |
| **Use case** | Redundant core in AV spine-and-leaf | Expanding port density in one location |

#### MLAG in AV Network Design

```
                    ┌──────────┐
                    │  Access   │  (leaf switch — e.g., M4250)
                    │  Switch   │
                    └──┬───┬───┘
                       │   │
            ┌──────────┘   └──────────┐
            │ LAG member 1            │ LAG member 2
            ▼                         ▼
     ┌──────────┐   peer link   ┌──────────┐
     │  Core A  │◄─────────────►│  Core B  │  (MLAG pair — e.g., two M4350s)
     │ (M4350)  │               │ (M4350)  │
     └──────────┘               └──────────┘
```

- The access switch sees one logical LAG to "the core"
- Both core switches actively forward traffic
- If Core A fails → Core B handles everything, sub-second failover
- **This is the recommended topology for mission-critical live events and broadcast**

#### Why MLAG Matters for AV

- In traditional STP, one uplink is blocked → wasted bandwidth
- MLAG keeps **all links active** while preventing loops
- Sub-second failover means **no audible dropout** in Dante and **no visible glitch** in video streams
- Critical for high-availability AV networks: live events, broadcast, installed systems that can't go down
- Cornerstone of resilient network topologies
- **Exam tip:** Know that MLAG provides active-active redundancy without STP blocking, and that it works across physically separate switches (unlike stacking)

### Blocking vs Non-Blocking Networks *(important for AV)*

| Type | Behavior | Use Case |
|------|----------|----------|
| **Blocking** | Limited bandwidth; may delay/drop traffic at peak | Bursty data with lower throughput demands |
| **Non-blocking** | Sufficient bandwidth for **all traffic simultaneously** | AV multicast with high, constant data transfer |

#### AV Design Rule

- **Always design for non-blocking** in AV networks
- Calculate maximum possible throughput (max resolution × number of streams)
- Ensure enough links between switches to handle full load simultaneously
- If your switch has 48× 1G ports + 4× 10G uplinks, the uplinks must handle the aggregate — check the math

### AV Network Example (Putting It Together)

A high-demand AV network uses all these features together:

1. **Auto LAG + Auto Trunk** — simplify link aggregation and VLAN config
2. **STP** — loop-free topology
3. **MLAG** — switch redundancy and failover
4. **Non-blocking design** — eliminates congestion
5. **LACP** — dynamic link aggregation management

---

## Module 7 – NETGEAR Enterprise Switches

*This is all new material. Learn the switch lineup, power options, and port configurations.*

### Switch Lineup Overview

| Series | Positioning | Typical Role | Speed |
|--------|-----------|--------------|-------|
| **M4250** | Entry/mid-range AV | Access switches, small-medium deployments | 1G copper, 10G SFP+ uplinks |
| **M4300** | Mid-range enterprise | Balanced performance/value, larger installs | 1G/10G mixed |
| **M4350** | High-performance AV+IT | Core switches, 10G endpoints, broadcast | 1G–25G–100G depending on model |
| **M4500** | Premium/mission-critical | Large-scale, highest performance | Up to 100G QSFP |

All support the **Engage platform** for easy configuration with certified profiles for 200+ manufacturers.

### Power Bays

- **Dual power supply configurations** on enterprise models
- Provides **redundancy**: if one PSU fails, the other takes over seamlessly
- **Hot-swappable**: replace without downtime (critical for live events, data centers)
- **Energy-efficient**: reduced operational costs, supports green IT

### Power over Ethernet (PoE)

| Standard | IEEE | Max Power/Port | Typical Devices |
|----------|------|---------------|-----------------|
| **PoE** | 802.3af | 15.4W | IP phones, basic WAPs |
| **PoE+** | 802.3at | 30W | Mid-power devices, some cameras |
| **PoE++** | 802.3bt | 60W or 90W | PTZ cameras, ceiling speakers, lighting, WiFi 6/7 APs |

- **Total PoE budget** varies by model — always check the spec sheet
- Reduces cabling (data + power on one cable)
- Critical for AV: many endpoint devices are PoE-powered

### Port Configurations

| Port Type | Speed | Use Case |
|-----------|-------|----------|
| **Gigabit Ethernet** | 10/100/1000 Mbps | General endpoint connectivity |
| **10G SFP+** | Up to 10 Gbps | Server connections, switch uplinks |
| **Multigigabit** | 2.5G / 5G / 10G | WiFi 6/7 APs, high-performance endpoints |
| **25G SFP28** | 25 Gbps | High-density uplinks (M4350) |
| **100G QSFP28** | 100 Gbps | Core aggregation (M4350/M4500) |

### Choosing the Right Switch

Consider these factors when selecting:

1. **Power requirements** — count PoE devices, sum wattage, pick appropriate budget
2. **Port density and types** — how many 1G, 10G, multigigabit ports needed?
3. **Redundancy** — dual hot-swappable PSUs for critical applications
4. **Scalability** — room for future growth

### Practical Example: Office AV Project

**Requirements:**
- 12× PoE+ gooseneck mics
- 6× PoE++ ceiling speakers
- 2× Multi-Gig WiFi 7 PoE++ access points
- 4× PoE++ PTZ cameras
- 2× 10G Fiber for long backhaul
- High availability (redundancy required)

**Solution:** M4350-44M4X4V
- Sufficient PoE budget for all devices
- Mix of 1G and 10G ports
- Dual hot-swappable PSUs for redundancy
- Meets the high-availability requirement

### Additional Features

- **QoS:** Prioritizes critical network traffic (AV over general data)
- **VLAN support:** Network segmentation for traffic management
- **Security:** ACLs and network monitoring tools
- **IGMP Plus:** Multicast optimization (covered in Module 4)

---

## Module 8 – Engage Controller

*Entirely new — NETGEAR's proprietary management platform. Learn this thoroughly.*

### What Is Engage?

The NETGEAR Engage™ Controller is a **free, portable application** (Windows + macOS) that removes the complexity of network configuration and management in AV-over-IP installations.

**Supported switches:** M4250, M4300, M4350, M4500

### Core Capabilities

| Feature | What It Does |
|---------|-------------|
| **Auto switch detection** | Finds all supported switches on the network automatically |
| **Firmware management** | Upgrade firmware across all switches from one interface |
| **Profile-based configuration** | Pre-built profiles for Dante, AES67, AVB, Lighting, NDI, and 200+ manufacturers |
| **Network topology visualization** | Visual map of switches, ports, and connected devices |
| **Multi-site management** | Manage multiple AV networks/locations from one controller |
| **Port-level profile assignment** | Assign specific AV profiles to individual ports across the network |

### Why Engage Matters

- AV-over-IP installations traditionally require **manual CLI configuration** per switch
- Each VLAN, IGMP setting, QoS rule, and trunk port needs individual commands
- Engage replaces this with a **GUI-driven, profile-based workflow**
- Eliminates manual switch detection and firmware updates
- Configures switches for Dante, AES67, AVB, Lighting — otherwise error-prone for non-networking professionals

### Installation & Setup Process

1. **Download** the Engage Controller (from course resources / NETGEAR website)
   - Adjust firewall and antivirus if they interfere with installation
2. **Initial login** — set an admin password, create a default site
3. **Configure site settings** — name, description
4. **Network connection mode:**
   - **Dynamic IP** — Engage gets an IP via DHCP
   - **Static IP** — Manually assign Engage's IP
   - **Static IP + DHCP** — Engage has a static IP but also runs a DHCP server
5. **Onboard switches** — Engage displays all detected switches; enter device passwords to onboard
6. **Profile setup** — review available profiles, assign to ports/switches
   - Create new profiles or modify existing ones
   - Profiles control VLAN IDs, IGMP Plus settings, QoS, and more

### Profile Management

- Engage pulls existing network profiles from onboarded switches
- Pushes profiles to devices during onboarding
- Edit profiles directly: change names, VLAN IDs, colors for identification
- **Default network profile** always exists; custom profiles added for specific AV protocols

### Key Workflow Summary

```
Download Engage → Set admin password → Create site →
Choose network mode → Detect & onboard switches →
Assign profiles to ports → Done
```

### Practical Impact

- What used to require SSH/CLI access to each switch individually is now a **single GUI**
- Profile-based approach means you don't need to know every CLI command
- Centralized control = faster deployment, fewer errors, easier maintenance
- **When pitching a project: Engage is the key differentiator** — show customers how easy configuration is

---

## Module 9 – Specifying NETGEAR Switches

*New material — how to select the right switch for an AV project. Exam-critical.*

### Selection Process

1. **Understand project scope** — number of devices, types, bandwidth needs
2. **Check specification sheets** — match capabilities to requirements
3. **Apply budget constraints** — right-size without over-provisioning
4. **Plan for redundancy** — mission-critical = dual PSU + MLAG
5. **Use Engage** — simplify configuration and management

### Switch Series Selection Guide

| Deployment Size | Recommended Series | Why |
|----------------|-------------------|-----|
| Small–medium (< 96 endpoints) | **M4250** | Cost-effective, 1G copper + 10G SFP+ uplinks |
| Medium–large, demanding apps | **M4300 / M4350** | Balance of performance and value, multigig + 10G |
| Mission-critical, large-scale | **M4500** | Premium performance, 100G, maximum scalability |

### Example: 96-Port Network (M4250)

**Topology:** Core-and-access

- **Core switch (SW1):** M4250 with 10G SFP+ fiber ports
- **Access switches:** Each with 40× 1G copper ports
- **Interconnect:** Auto-LAG delivers **40Gb throughput** between core and each access switch
- **Capacity:** 96× 1G endpoints + 24 additional headroom
- Ideal for small-to-mid AV projects

### Example: Redundant Core (M4350)

**Topology:** Stacked core

- **Core:** Two M4350 switches in redundant configuration
- **Access:** Multiple M4250 switches
- **Failover:** If one core switch fails, the other maintains connectivity at 20Gb link aggregation
- Essential for **high-availability** systems (live events, broadcast)

### Example: ST2110 Broadcast Network (M4350 + M4250)

- **SW2–SW5:** M4350 switches for 10Gb endpoints (broadcast devices)
- **SW6–SW7:** M4250 switches for 1Gb traffic on the same network
- **Core (C3):** M4350 with **100G QSFP ports** aggregating all inter-switch traffic
- Supports high-performance 10G AV streams while staying cost-effective for non-10G devices

### Bandwidth Calculation Approach

1. Identify **all devices** and their required bandwidth
2. Sum total throughput needed
3. Determine **link aggregation** requirements between switches
4. Verify switch spec sheet supports the calculated throughput
5. Design for **non-blocking** — ensure uplink capacity ≥ aggregate endpoint capacity

### Communicating with Customers

When specifying for a client:
- Emphasize **AV over IP value**: simplified cabling, centralized management, scalability
- Tailor to their needs, budget, and existing infrastructure
- Highlight Netgear differentiators: IGMP Plus, Engage, Auto LAG/Trunk
- Use **real-world examples** and case studies
- Demo Engage to show ease of configuration

---

## Quick Reference: Netgear-Specific Features

| Feature | What It Does | Why It Matters |
|---------|-------------|----------------|
| **IGMP Plus™** | Single-command multicast optimization per VLAN | Replaces multi-step IGMP snooping config |
| **Auto LAG** | Automatic link aggregation detection and grouping | Zero-touch inter-switch bandwidth |
| **Auto Trunk** | Automatic trunk port configuration | Eliminates manual trunk setup |
| **MLAG** | Multi-chassis link aggregation across switches | Active-active redundancy, no STP blocking |
| **Engage Controller** | GUI-based switch management + profiles | Replaces CLI-per-switch workflow |
| **Dual PSU** | Hot-swappable redundant power supplies | Zero-downtime power failover |

---

## Coverage Assessment — Will This Pass the Exam?

> **Verdict: Yes, with the gaps below addressed.** The core proprietary content (IGMP Plus, Auto LAG, Auto Trunk, MLAG, Engage, switch lineup) is covered in depth. The networking fundamentals are solid from CCNA overlap. Three topics are under-covered and could appear on the exam:

### Gaps to Know

#### Jumbo Frames
- Standard Ethernet MTU = **1500 bytes**
- **Jumbo frames** extend the MTU to **9000 bytes** (sometimes 9216 bytes)
- Required for: NDI, some ST 2110 and IPMX configurations, high-bandwidth AV-over-IP streams
- Must be enabled **end-to-end** — every switch and NIC in the path must support and enable jumbo frames, or fragmentation/drops occur
- On NETGEAR switches: configurable per interface or globally; Engage profiles handle this automatically for supported protocols
- **Exam tip:** If asked why an NDI or high-res AV stream is dropping packets or showing artifacts, jumbo frame mismatch is a key suspect

#### EEE — Energy Efficient Ethernet (IEEE 802.3az)
- EEE reduces power on low-utilization links by entering a low-power idle (LPI) state
- **This is catastrophically bad for AV networks** — the transition in/out of LPI introduces **latency jitter** (10–100+ µs) that causes audio clicks, video glitches, and Dante "blip" faults
- **Rule: Always disable EEE on every port connected to AV devices**
- On NETGEAR AV switches: EEE is disabled by default on AV-configured ports via Engage profiles
- Engage Dante/AES67 profiles automatically set this correctly — another reason to use Engage rather than manual CLI

#### Flow Control (IEEE 802.3x)
- Flow control allows a receiving device to signal a sender to **pause transmission** when its buffer is nearly full
- Prevents packet loss from buffer overflow
- **For AV networks:** Standard flow control (PAUSE frames) can cause **head-of-line blocking** — a slow device pauses the whole link, stalling high-priority AV traffic
- **Priority Flow Control (PFC)** — a per-queue version (part of the 802.1Qbb Data Center Bridging spec) — is preferred in high-density systems, though less commonly required in typical ProAV installs
- **NETGEAR recommendation:** Disable standard flow control on AV ports; ensure QoS queuing is correctly configured so the switch drops low-priority traffic rather than pausing high-priority traffic

---

## Exam Preparation Checklist

- [ ] Can I list the 7 OSI layers and their AV relevance?
- [ ] Can I explain broadcast domains and why VLANs matter for AV?
- [ ] Can I describe spine-and-leaf vs stacked core topologies?
- [ ] Do I understand the difference between unicast, broadcast, and multicast?
- [ ] Can I explain **IGMP Plus** and how it differs from standard IGMP snooping?
- [ ] Can I explain **PIM** vs **IGMP** vs **IGMP Plus** scope differences?
- [ ] Do I know access ports vs trunk ports and VLAN tagging (802.1Q)?
- [ ] Can I explain what a **Control VLAN** is and why it's separate?
- [ ] Can I define Auto LAG, Auto Trunk, MLAG, and their benefits?
- [ ] Do I understand **blocking vs non-blocking** network design?
- [ ] Can I list the M4250/M4300/M4350/M4500 positioning and use cases?
- [ ] Do I know PoE standards (af/at/bt) and their wattage?
- [ ] Can I walk through the **Engage Controller** setup process?
- [ ] Can I size a switch for a given project (ports, PoE budget, uplinks, redundancy)?
- [ ] Can I calculate bandwidth requirements and specify the right switch series?

---

## Key Terms Glossary

| Term | Definition |
|------|-----------|
| **PHY** | Physical Layer Device — converts digital ↔ physical signals |
| **MAC** | Media Access Control — unique Layer 2 address per NIC |
| **CIDR** | Classless Inter-Domain Routing — flexible subnet masks |
| **IGMP** | Internet Group Management Protocol — multicast group membership |
| **PIM** | Protocol Independent Multicast — multicast routing across networks |
| **IGMP Plus™** | NETGEAR proprietary multicast optimization (single command per VLAN) |
| **LACP** | Link Aggregation Control Protocol — dynamic link bundling |
| **Auto LAG** | NETGEAR automatic link aggregation |
| **Auto Trunk** | NETGEAR automatic trunk port detection |
| **MLAG** | Multi-Chassis Link Aggregation — LAG across multiple switches |
| **STP** | Spanning Tree Protocol — loop prevention |
| **QoS** | Quality of Service — traffic prioritization |
| **PoE/PoE+/PoE++** | Power over Ethernet standards (802.3af/at/bt) |
| **Non-blocking** | Switch design where all ports can run at full speed simultaneously |
| **Engage™** | NETGEAR's free AV switch management controller |
| **Control VLAN** | Dedicated VLAN for network management traffic |
| **Spine and Leaf** | Modern topology with spine (core) + leaf (access) layers |
| **Stacked Core** | Two+ switches acting as a single logical unit for redundancy |
