# Q-SYS Architect Certification Notes

> **About the Architect Course:** Aimed at AV system designers, consultants, and integrators who specify and architect Q-SYS systems. Focuses on hardware selection, system sizing, network design, scalability, and writing Q-SYS into specifications. Does not require hands-on programming knowledge.

---

## Table of Contents

1. [Q-SYS as a Platform — Architectural Perspective](#1-q-sys-as-a-platform--architectural-perspective)
2. [Hardware Selection and System Sizing](#2-hardware-selection-and-system-sizing)
3. [Network Architecture for Q-SYS](#3-network-architecture-for-q-sys)
4. [Scalability and Multi-Site Design](#4-scalability-and-multi-site-design)
5. [Redundancy and High Availability](#5-redundancy-and-high-availability)
6. [Integration with Building Systems](#6-integration-with-building-systems)
7. [Specification Writing for Q-SYS](#7-specification-writing-for-q-sys)
8. [Licensing Model](#8-licensing-model)
9. [Q-SYS in Vertical Markets](#9-q-sys-in-vertical-markets)
10. [Exam Tips — Architect](#10-exam-tips--architect)

---

## 1. Q-SYS as a Platform — Architectural Perspective

### Software-Defined AV

- Q-SYS is a **software-defined** platform — functionality is delivered through software running on standard (or dedicated) hardware
- This means:
  - Features can be added or updated via firmware without hardware replacement
  - The same Core hardware can serve different use cases depending on the design file
  - System behaviour is defined in the `.qsys` design file, not hardwired

### Q-SYS vs. Traditional AV Architecture

| Aspect | Traditional AV | Q-SYS Platform |
|--------|---------------|---------------|
| DSP | Dedicated hardware per room | Centralised or distributed software DSP |
| Control | Separate control processor | Built into the Core |
| Signal transport | Analogue snake / AES cable | Ethernet (Q-LAN) |
| Reconfiguration | Hardware rewiring | Software design change |
| Scalability | Add hardware per room | Scale Core DSP capacity |
| Monitoring | On-site only | Cloud (Q-SYS Reflect) |

### Three-Tier Architecture Model

```
┌────────────────────────────────────────────────────────┐
│  CLOUD TIER: Q-SYS Reflect Enterprise Manager          │
│  (Remote monitoring, firmware, design management)       │
└──────────────────────┬─────────────────────────────────┘
                       │ HTTPS (port 443)
┌──────────────────────▼─────────────────────────────────┐
│  EDGE TIER: Q-SYS Cores + Peripherals                  │
│  (Processing, routing, control, I/O)                    │
└──────────────────────┬─────────────────────────────────┘
                       │ Q-LAN (Ethernet)
┌──────────────────────▼─────────────────────────────────┐
│  ENDPOINT TIER: Devices, Panels, User Interfaces       │
│  (Cameras, mics, speakers, touchscreens, displays)      │
└────────────────────────────────────────────────────────┘
```

---

## 2. Hardware Selection and System Sizing

### Core Selection Criteria

When specifying a Core, evaluate:

1. **Channel count** — total simultaneous audio channels required
2. **I/O requirements** — how many local analog/Dante inputs and outputs
3. **Processing complexity** — number and type of DSP components
4. **Form factor** — rack space, physical installation constraints
5. **Redundancy requirement** — is failover needed?

### Core Model Comparison

| Core | DSP Capacity | Built-in I/O | Best For |
|------|-------------|-------------|---------|
| **Core Nano** | Low | 4 mic/4 line in, 2 out, 4 AEC | Small rooms (boardroom, huddle) |
| **Core 110f** | Low-Medium | 8 mic/line in, 8 out, 4 AEC | Small to medium rooms |
| **Core 8 Flex** | Medium | 8 mic/line in, 8 out, 4 AEC | Medium rooms + expansion |
| **Core 510i** | Medium-High | None (I/O via frames only) | Systems using networked I/O |
| **Core 5200** | High | None (I/O via frames only) | Large/enterprise, high channel count |

- **Rule:** when in doubt, spec one tier up — you cannot add DSP headroom post-deployment without a Core swap
- Check the Q-SYS **System Performance Estimator** (available from QSC) to calculate DSP load before specifying

### I/O Frame Selection

| Device | Channels | Notes |
|--------|---------|-------|
| **IO-8 Flex** | 8 mic/line in, 8 out, 4 AEC | Rackmount, pairs with Nano/510i/5200 |
| **IO-22** | 22 mic/line in, 22 out | Higher density analog I/O |
| **IO-USB Bridge** | USB audio bridge | For soft codec (laptop/UC) integration |
| **NC Series** | Various (conferencing mics) | USB/Dante ceiling mic arrays |

### Peripheral Selection

| Peripheral Type | Examples | Selection Factor |
|----------------|---------|-----------------|
| Dante amplifiers | QSC CX-Q series | Zone count, impedance, wattage |
| Network cameras | QSC NC-series | Resolution, PTZ, tracking |
| Touchscreen panels | QSC TSC series | Size, mounting, iOS/Android vs. dedicated |
| Video endpoints | QSC NV series | Resolution, HDBaseT vs. IP |

### Sizing Checklist

- [ ] Count all audio inputs (mics, line, Dante, AES67)
- [ ] Count all audio outputs (zones, Dante, analog, codec)
- [ ] Identify all processing requirements (AEC channels, conferencing codecs)
- [ ] Identify video requirements (sources, displays, streams)
- [ ] Determine control interface needs (touchscreens, 3rd party controllers)
- [ ] Identify external control integrations (lighting, shades, HVAC)
- [ ] Determine SIP/VoIP requirements (number of call lines)
- [ ] Assess redundancy requirements (failover, uptime SLA)

---

## 3. Network Architecture for Q-SYS

### Dedicated AV Network (Q-LAN)

- Always recommend a **dedicated Q-LAN** separate from the corporate IT network
- Prevents broadcast storms, rogue DHCP, or IT policy changes from affecting AV
- Implemented as a separate physical network or a **dedicated VLAN** with QoS prioritisation

### VLAN Design

| VLAN | Traffic | Rationale |
|------|---------|-----------|
| AV Management | Core Manager, Reflect, IT admin | Secure, managed access |
| Audio Q-LAN | Multicast audio streams | High-priority, low-latency |
| Video Q-LAN | NV video streams | Separate from audio to avoid contention |
| Control | UCI panels, QRC TCP, 3rd party controllers | Medium priority |
| Corporate | All other IT traffic | Completely separate |

### Switch Specification Requirements

For Q-SYS systems, specify switches with:

- **Gigabit Ethernet** (all ports)
- **IGMP Snooping v3** enabled (required for multicast audio/video)
- **QoS — DSCP trust** (honour markings from Q-SYS devices)
- **QoS — Priority Queuing** (at least 4 queues recommended)
- **PortFast / RSTP Edge** on all device-connected ports (prevent STP delay on link-up)
- **EEE (Energy Efficient Ethernet) disabled** on device ports (causes audio jitter)
- **LLDP** enabled (for device discovery)

Recommended: **QSC NS Series** (Netgear-based AV switches) — pre-validated for Q-SYS Q-LAN

### Bandwidth Budget Example

| Traffic Type | Per Stream | Notes |
|--------------|-----------|-------|
| Q-LAN audio (32 ch) | ~512 Kbps | Lossless, low-latency |
| NV video (1080p30) | ~15 Mbps | Compressed H.264 |
| Dante audio (64 ch) | ~100 Mbps | AES67/Dante overhead |
| UCI control | <1 Mbps | HTTP/WS |

### Physical Topology Considerations

- **Star topology** recommended (Core at centre, switches at edges)
- Avoid **ring topologies** without STP — can cause broadcast loops
- Use **fibre** for inter-building or long runs (>90 m Cat6)
- For multi-floor or multi-building: **collapsed core** switching design with dedicated AV uplinks

---

## 4. Scalability and Multi-Site Design

### Scaling Within a Single Site

| Approach | Method |
|----------|--------|
| Add I/O frames | Expand analog/AEC I/O without replacing the Core |
| Add Dante peripherals | Add channels over IP without rewiring |
| Upgrade Core | Swap Core to a higher-capacity model |
| Add a second Core | Use Q-LAN Transmitter/Receiver to share audio between Cores |

### Multi-Site Architecture

- Each site has its own Core(s) and Q-LAN
- Sites are connected via:
  - **WAN-connected Q-SYS Reflect** (management only)
  - **SIP trunking** (voice conferencing between sites)
  - **AES67 over WAN** or **compressed streaming** (audio between sites — requires careful bandwidth planning)

### Corporate/Enterprise Design Patterns

| Pattern | Use Case |
|---------|---------|
| **Centralised Core** | All rooms in a building feed one high-capacity Core |
| **Distributed Cores** | Each floor or zone has its own Core; linked via Q-LAN |
| **Hybrid** | Critical rooms get dedicated Cores; smaller rooms share |

- Centralised = simpler management, single point of failure (unless redundant)
- Distributed = resilient, but more Cores to manage

### Q-SYS Reflect for Multi-Site

- Aggregate all sites in a single Reflect tenant
- Monitor faults across all sites from a single dashboard
- Deploy design updates to all matching Cores simultaneously
- Useful for: national/global deployments, managed service providers

---

## 5. Redundancy and High Availability

### Core Redundancy

- Q-SYS supports **Core-to-Core failover** (primary + standby)
- The standby Core mirrors the primary; if the primary fails, the standby takes over automatically
- Requires:
  - Two matching Core models
  - A **redundancy sync cable** (direct Ethernet link between the two Cores)
  - Same design deployed to both
- Failover time: typically **<1 second** for audio; control and UCI may have a brief interruption

### Network Redundancy

- Use **redundant switch uplinks** (LACP port channelling or RSTP failover paths)
- Q-SYS Cores have multiple Ethernet ports — can be used for redundant Q-LAN connections
- Consider **dual-homed I/O frames** in critical installations

### Power Redundancy

- Specify **redundant power supplies** where available (Core 5200 supports dual PSU)
- Use **UPS** (Uninterruptible Power Supply) on Core, switches, and critical I/O
- Specify **separate electrical circuits** for primary and backup power paths

### Single Points of Failure Audit

Always identify and mitigate:
- Single switch on the Q-LAN backbone
- Single Core without failover
- Single power path
- Single internet connection (for Reflect-dependent management)

---

## 6. Integration with Building Systems

### Room Automation Integration Points

| System | Integration Method |
|--------|------------------|
| Lighting control (Lutron, Crestron) | QRC TCP/IP, RS-232 |
| HVAC / BMS | BACnet plugin, Modbus plugin, RS-232 |
| Occupancy sensors | GPIO (contact closure) |
| Shades / blinds | RS-232, contact closure via GPIO |
| Video conferencing (Teams/Zoom) | API plugins, Q-SYS Connect |
| Calendar/room booking | REST API integration via Lua |

### Q-SYS Connect

- **Q-SYS Connect** is QSC's integration application for UC (Unified Communications) platforms
- Bridges Q-SYS audio/control with:
  - Microsoft Teams Rooms (MTR)
  - Zoom Rooms
  - Cisco WebEx Rooms
- Handles automatic call joining, camera control, display switching
- Runs on a Windows PC on the network (separate from the Core)

### Third-Party Control System Integration

- Q-SYS works alongside — not as a replacement for — AMX/Crestron in complex installs
- The control system sends QRC commands to Q-SYS and Q-SYS responds with status
- Specify a **QRC driver** for the control system platform (many available from integrators or QSC community)

---

## 7. Specification Writing for Q-SYS

### CSI Format Sections

When writing Q-SYS into a specification (CSI MasterFormat):

- **Section 27 41 00** — Audio-Video Communications (or appropriate section per project)
- List Core model and firmware version requirement
- List all peripherals (I/O frames, Dante devices, NV endpoints)
- Specify network requirements (switch spec, VLAN, QoS)
- Specify training requirements for integrator and end-user

### Key Specification Language

```
The audio, video, and control platform shall be based on the QSC Q-SYS 
software-defined platform. The system shall be configured using Q-SYS Designer 
software and deployed on a QSC [Core model] processor with the following 
characteristics:

- Processing: [x] simultaneous audio channels
- Local I/O: [x] mic/line inputs, [x] outputs, [x] AEC channels
- Network: [x] GbE Q-LAN ports
- Features: Scripting, UCI, [SIP, Video — if required]

The integrator shall provide design files (.qsys) to the owner upon project 
completion. All Named Controls shall be documented and a system narrative 
shall be included.
```

### What to Include in a Q-SYS Specification

- [ ] Core model and quantity
- [ ] I/O frame models and quantities
- [ ] Dante peripheral models
- [ ] NV video endpoint models (if video required)
- [ ] Q-SYS Reflect subscription (if remote management required)
- [ ] Licenses required (SIP, Video, per-Core)
- [ ] Network switch specification (or reference to separate network spec)
- [ ] Training requirement (Level 1 certified integrator recommended)
- [ ] Deliverables: design file, named control list, system narrative, as-built drawings

---

## 8. Licensing Model

### Core Licensing Overview

Q-SYS licenses are applied per Core:

| License | Included By Default | Notes |
|---------|-------------------|-------|
| **Audio DSP** | Yes | Core processing capacity |
| **UCI** | Yes (v9+) | Unlimited UCIs per Core |
| **Scripting (Lua)** | Yes (v9+) | Included in software |
| **SIP (VoIP)** | No | Purchased separately, per Core |
| **Video (NV)** | No | Purchased separately, per Core |
| **Q-SYS Reflect** | No | Subscription, per Core, per year |

### License Application

- Licenses are tied to the **Core's serial number**
- Applied via **Q-SYS Core Manager → Licenses**
- Backup licenses to a safe location — cannot be regenerated without QSC support

### Subscription vs. Perpetual

- **Audio DSP, SIP, Video** — perpetual (buy once, keep indefinitely)
- **Q-SYS Reflect** — annual subscription
- Firmware updates are free; no software subscription required for core functionality

---

## 9. Q-SYS in Vertical Markets

### Corporate / Enterprise

- **Use cases:** boardrooms, huddle rooms, open offices, executive suites, all-hands spaces
- **Key needs:** seamless UC integration (Teams/Zoom), simple operator UI, centralised IT management
- **Differentiators:** Q-SYS Connect, Reflect fleet management, programmatic room booking integration

### Education

- **Use cases:** lecture halls, classrooms, collaborative learning spaces, performing arts
- **Key needs:** Reliability, ease of use by non-AV staff, system-wide monitoring by IT
- **Differentiators:** scalability across campus (Reflect), AEC for hybrid learning, BYOD integration

### House of Worship

- **Use cases:** main sanctuary, overflow rooms, broadcast/streaming, multi-campus
- **Key needs:** Broadcast-quality audio, flexible mixing, multi-site audio distribution
- **Differentiators:** Dante integration with mixing consoles, multi-Core distribution, low latency

### Government / Military

- **Use cases:** command centres, courtrooms, public address, EOC (Emergency Operations Centres)
- **Key needs:** High availability, redundancy, security, access control
- **Differentiators:** Redundant Core failover, GPIO integration, no cloud dependency option

### Hospitality

- **Use cases:** ballrooms, meeting rooms, F&B spaces, public address
- **Key needs:** Easy zone management, simple staff UI, flexibility for changing room configurations
- **Differentiators:** Matrix mixing, zone routing, intuitive UCI panels for non-technical staff

### Performing Arts / Theatre

- **Use cases:** stage monitoring, multi-zone distribution, paging, show control
- **Key needs:** Low latency, high channel count, integration with pro audio systems
- **Differentiators:** Dante bridging to FOH consoles, snapshot scene recall, low-latency monitoring

---

## 10. Exam Tips — Architect

- Know the **Core models** and their target use cases and capacities
- Understand the **three-tier architecture** (cloud / edge / endpoint)
- Be able to recommend a Core given a channel count and I/O requirement
- Know what **IGMP snooping, QoS/DSCP, and EEE** mean for Q-SYS network performance
- Understand **Core redundancy** — failover, sync cable, failover time
- Know the difference between **centralised vs. distributed Core architecture**
- Know what **Q-SYS Connect** does and when to specify it
- Understand the **licensing model** — what is free, what is purchased, what is subscription
- Be able to identify which vertical markets benefit from which Q-SYS features
- Know the key **specification deliverables** expected at project handover
