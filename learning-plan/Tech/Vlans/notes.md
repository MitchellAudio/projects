# Notes: VLANs

## What Is a VLAN?

- **VLAN (Virtual Local Area Network)** — a way to divide a single physical switch (or group of switches) into multiple separate, isolated broadcast domains
- Devices in the same VLAN can communicate as if they are on the same physical switch, even if they are on different switches
- Devices in different VLANs **cannot** communicate without a **router** or **Layer 3 switch** — they are logically separated
- Think of it as drawing invisible walls inside a switch — each wall creates a separate network

### Why VLANs Exist

- Without VLANs, every device plugged into a switch is in the same broadcast domain — every broadcast frame reaches every port
- As the network grows, broadcast traffic increases and consumes bandwidth
- VLANs solve this by segmenting the network logically without needing separate physical switches
- They also provide **security isolation** — sensitive traffic (e.g., control systems) can be separated from general traffic (e.g., internet access)

---

## How VLANs Work

### VLAN IDs

- Every VLAN is identified by a **VLAN ID** (1–4094)
- **VLAN 1** is the default VLAN on most switches — all ports belong to VLAN 1 out of the box
- You create additional VLANs (e.g., VLAN 10, VLAN 20, VLAN 100) and assign ports to them
- The VLAN ID is a number — the name you give it is just for human readability

### Port Types

#### Access Ports

- An **access port** belongs to exactly **one VLAN**
- The device plugged into an access port does not know it is on a VLAN — it sends and receives normal, untagged Ethernet frames
- The switch internally associates all traffic on that port with the configured VLAN
- **Use for:** end devices — computers, Dante devices, printers, phones

#### Trunk Ports

- A **trunk port** carries traffic for **multiple VLANs** simultaneously
- It uses **802.1Q tagging** (see below) to identify which VLAN each frame belongs to
- **Use for:** switch-to-switch links, switch-to-router links — anywhere traffic for multiple VLANs needs to travel over a single cable

### 802.1Q Tagging

- **802.1Q** — the IEEE standard for VLAN tagging
- When a frame enters a trunk port, the switch inserts a **4-byte VLAN tag** into the Ethernet frame header
- The tag contains the **VLAN ID** (12-bit field, hence 1–4094) and a **priority field** (3 bits, used for QoS — see QoS notes)
- The receiving switch reads the tag to determine which VLAN the frame belongs to, then either forwards it within that VLAN or strips the tag if delivering to an access port
- **End devices never see VLAN tags** — tags are added and removed by switches on trunk ports

### Native VLAN

- The **native VLAN** is the VLAN that carries **untagged** traffic on a trunk port
- By default, this is **VLAN 1**
- If a frame arrives on a trunk without a VLAN tag, the switch puts it in the native VLAN
- **Critical rule:** the native VLAN must match on both sides of a trunk link — a mismatch causes frames to end up in the wrong VLAN and can create security vulnerabilities
- **Best practice:** change the native VLAN from 1 to an unused VLAN for security, or tag all VLANs (no native)

---

## VLAN Design Principles

### Separate by Function

- Group devices by their **function and traffic type**, not by physical location
- Common VLAN design:

| VLAN ID | Name | Purpose |
|---|---|---|
| 1 | Default | **Do not use** — leave empty or for management only |
| 10 | Management | Switch management interfaces, SNMP |
| 20 | Dante Primary | Primary Dante audio network |
| 30 | Dante Secondary | Secondary Dante audio network (redundancy) |
| 40 | Control | Console control, show control, OSC, MIDI-over-IP |
| 50 | General | Internet access, laptops, general IT |

### Broadcast Domain Size

- Each VLAN is its own broadcast domain — broadcasts only reach devices in the same VLAN
- Keep VLANs reasonably sized — a VLAN with 500 devices generates a lot of broadcast traffic
- For audio networks, small VLANs (< 100 devices) are typical and ideal

### Security and Isolation

- VLANs provide Layer 2 isolation — devices on different VLANs cannot communicate at all without explicit routing
- This is useful for separating sensitive networks (e.g., keeping the control network away from the general internet VLAN)
- **VLANs are not firewalls** — if you enable inter-VLAN routing, traffic can flow between VLANs. Use access control lists (ACLs) on the router to restrict specific traffic if needed

---

## Inter-VLAN Routing

### The Problem

- By default, VLANs are completely isolated — VLAN 20 cannot talk to VLAN 40
- Sometimes you need controlled communication between VLANs (e.g., a laptop on the Control VLAN needs to access the internet on the General VLAN)

### Router on a Stick

- A single router interface connects to the switch via a **trunk port**
- The router creates **sub-interfaces**, one per VLAN, each with its own IP address (acting as the default gateway for that VLAN)
- Traffic between VLANs passes through the router, which can apply routing rules and ACLs
- **Limitation:** all inter-VLAN traffic shares a single physical link — can be a bottleneck

### Layer 3 Switch

- A **Layer 3 switch** can route between VLANs internally at wire speed — no external router needed
- You create **Switched Virtual Interfaces (SVIs)** — one per VLAN — each with an IP address
- This is faster and simpler than router-on-a-stick for most deployments
- Most managed switches used in professional AV (e.g., Cisco Catalyst, Netgear M4300) support Layer 3 switching

### When to Route Between VLANs

- **Do route:** management access to devices on different VLANs, internet access from control VLAN
- **Do NOT route:** Dante audio between VLANs. Dante Primary and Secondary must remain isolated — they are separate redundancy networks, not VLANs that should talk to each other

---

## VLANs for Dante Audio Networks

### Why Dante Needs VLANs

- Dante uses **multicast** heavily for audio transport, device discovery (mDNS), and clock distribution (PTP)
- Multicast floods to all ports in a VLAN — without VLANs, Dante multicast floods the *entire* network
- VLANs contain the multicast to only the devices that need it, reducing unnecessary traffic on non-audio ports
- Dante also benefits from **QoS** (quality of service) priority — VLANs make it easier to apply QoS policies per traffic type

### Recommended Dante VLAN Design

| VLAN | Purpose | Devices | Notes |
|---|---|---|---|
| **VLAN 20 — Dante Primary** | Primary audio network | All Dante devices (primary NIC) | Carries all audio, clocking (PTP), discovery |
| **VLAN 30 — Dante Secondary** | Redundant audio network | All Dante devices (secondary NIC) | Independent from Primary — do NOT bridge or route between them |
| **VLAN 40 — Control** | Device control, console control | Laptops, consoles, show control | OSC, remote control apps, Dante Controller |

### Key Dante VLAN Rules

- **Dante Primary and Secondary must be on separate VLANs** (or separate physical switches) — they must never share a broadcast domain
- **Do not route between Dante Primary and Secondary** — the entire point is that they are independent redundancy paths
- **Dante Controller** needs access to the Dante Primary VLAN — typically the control laptop is on an access port in VLAN 20, or on a trunk port carrying both VLAN 20 and VLAN 40
- **IGMP snooping must be enabled** on Dante VLANs — without it, multicast floods to every port (see Managed Switches notes)
- **Configure an IGMP querier** on each VLAN that carries multicast — without a querier, IGMP snooping has no membership information and falls back to flooding

### Single Switch vs. Dual Switch Dante

#### Single Switch with VLANs

- Use VLANs to separate Dante Primary and Secondary on the same physical switch
- **Pro:** simpler cabling, fewer devices
- **Con:** the switch itself is a single point of failure — if it dies, both Dante networks go down
- This is common for small-to-medium systems

#### Dual Switch (True Redundancy)

- Dante Primary on one physical switch, Dante Secondary on a separate physical switch
- If one switch fails, the other continues operating
- **This is the gold standard** for critical shows
- VLANs are still used on each switch for separating control traffic from audio

---

## VLAN Configuration Basics (Cisco IOS Examples)

### Creating VLANs

```
Switch# configure terminal
Switch(config)# vlan 20
Switch(config-vlan)# name Dante-Primary
Switch(config-vlan)# exit
Switch(config)# vlan 30
Switch(config-vlan)# name Dante-Secondary
Switch(config-vlan)# exit
Switch(config)# vlan 40
Switch(config-vlan)# name Control
```

### Assigning an Access Port

```
Switch(config)# interface GigabitEthernet0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 20
Switch(config-if)# description "Stage Box - Dante Primary"
```

### Configuring a Trunk Port

```
Switch(config)# interface GigabitEthernet0/24
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 20,30,40
Switch(config-if)# switchport trunk native vlan 999
Switch(config-if)# description "Trunk to FOH switch"
```

### Verifying VLAN Configuration

```
Switch# show vlan brief                    — shows all VLANs and which ports are assigned
Switch# show interfaces trunk              — shows trunk ports and which VLANs are allowed
Switch# show interfaces GigabitEthernet0/1 switchport   — shows port config details
```

---

## Common VLAN Mistakes

### Mismatched Native VLANs

- If switch A's trunk has native VLAN 1 and switch B's trunk has native VLAN 99, untagged frames end up in different VLANs on each side
- Cisco switches will log a **Native VLAN mismatch** CDP/LLDP warning
- Fix: ensure native VLAN is the same on both sides of every trunk

### Forgetting to Allow VLANs on Trunks

- By default, a trunk may allow all VLANs — but if you configure `allowed vlan`, only the listed VLANs pass through
- If you create VLAN 30 but forget to add it to the trunk's allowed list, devices on VLAN 30 across the trunk cannot communicate
- Symptom: devices on the same VLAN on different switches can't ping each other

### Using VLAN 1 for Production Traffic

- VLAN 1 carries STP BPDUs, CDP, VTP, and other management protocols by default
- Putting production Dante traffic on VLAN 1 mixes it with management traffic — not ideal
- Best practice: leave VLAN 1 for management only; use dedicated VLANs for audio and control

### Not Enabling IGMP Snooping

- Without IGMP snooping, multicast traffic (Dante audio, PTP) floods to every port in the VLAN
- This wastes bandwidth and can overwhelm devices that are not Dante endpoints
- Enable IGMP snooping and configure a querier on every VLAN carrying multicast

### Routing Between Redundant Networks

- Never enable inter-VLAN routing between Dante Primary and Secondary VLANs
- If they can talk to each other, they are no longer independent — a broadcast storm on one affects both
- They must remain completely isolated Layer 2 domains

---

## VLAN and QoS Interaction

- The 802.1Q VLAN tag includes a **3-bit Priority Code Point (PCP)** field (also called **802.1p**)
- Values 0–7, where 7 is highest priority
- This is **Layer 2 QoS** — the switch can use PCP to prioritise frames within a VLAN

| PCP Value | Typical Use |
|---|---|
| 5 | Voice / time-critical audio (Dante PTP) |
| 4 | Video / streaming audio |
| 3 | Signalling / control |
| 0 | Best effort (default) |

- Dante devices typically tag their time-critical traffic with DSCP EF (Layer 3) — managed switches can map DSCP to PCP for Layer 2 prioritisation
- See QoS notes for details on DSCP, queue mapping, and Dante-specific QoS settings

---

## Relationship to Other Topics

| Concept | Connection |
|---|---|
| **Managed Switches** | VLANs are configured on managed switches — unmanaged switches do not support VLANs |
| **QoS** | 802.1Q tags carry priority bits; VLANs make it easier to apply QoS policies per traffic type |
| **Dante / Broadcast Methods** | Dante Primary and Secondary should be on separate VLANs (or separate switches) for proper redundancy |
| **CCNA / Network Access** | VLANs, trunking, 802.1Q, STP, and inter-VLAN routing are core CCNA topics |
| **IP Networking** | Each VLAN typically has its own IP subnet; inter-VLAN routing connects the subnets |

---

## Key Takeaways

- **VLANs segment a switch into isolated broadcast domains** — devices in different VLANs cannot communicate without a router
- **Access ports = one VLAN, trunk ports = many VLANs** with 802.1Q tags
- **Native VLAN must match** on both sides of a trunk — mismatches cause silent packet misrouting
- **Dante Primary and Secondary go on separate VLANs** and must never be routed to each other
- **Enable IGMP snooping + querier** on every VLAN carrying multicast (Dante) traffic
- **Do not use VLAN 1 for production** — keep it for management protocols
- **VLANs + QoS together** ensure audio traffic gets priority and isolation on shared infrastructure

---

## Resources

- [Audinate — Dante Networking Basics](https://www.audinate.com/learning)
- [Cisco — VLAN Configuration Guide](https://www.cisco.com/c/en/us/td/docs/)
- [Netgear — AV over IP VLAN Design Guide](https://www.netgear.com/business/solutions/av-over-ip/)
- Relate to your notes on [Managed Switches](../Managed-switches/notes.md), [QoS](../Qos/notes.md), and [CCNA Network Access](../../CCNA/Network-Access/notes.md)