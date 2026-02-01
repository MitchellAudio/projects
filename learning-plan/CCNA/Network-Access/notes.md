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

### Spanning Tree Protocol (STP) — Deep Dive

#### Overview and Purpose

**Spanning Tree Protocol (STP)** prevents Layer 2 loops in switched networks with redundant links. Without STP, loops cause:
- **Broadcast storms** — broadcasts loop infinitely, consuming all bandwidth
- **MAC address table instability** — switches see the same MAC on multiple ports
- **Duplicate frames** — hosts receive multiple copies of the same frame

STP creates a **loop-free logical topology** by blocking redundant paths while keeping them as backup links.

---

#### How STP Works

**1. Root Bridge Election**
- All switches exchange Bridge Protocol Data Units (BPDUs)
- Switch with **lowest Bridge ID** becomes the root bridge
  - Bridge ID = Priority (default 32768) + MAC address
  - Lower priority wins; if tied, lower MAC address wins
- Root bridge is the "center" of the spanning tree topology

**2. Root Path Cost Calculation**
- Each non-root switch calculates the cost to reach the root bridge
- **Path cost** based on link speed:
  - 10 Mbps = 100
  - 100 Mbps = 19
  - 1 Gbps = 4
  - 10 Gbps = 2
- Switch selects path with lowest cumulative cost as its **root path**

**3. Port Roles**
- **Root Port (RP)** — one per non-root switch, the port with lowest cost to root bridge
- **Designated Port (DP)** — one per segment, forwards traffic toward root
  - All ports on root bridge are designated ports
- **Blocking Port** — blocks traffic to prevent loops, does not forward data
  - Still receives BPDUs to monitor topology changes

**4. Port States**
- **Blocking** — blocks all traffic except BPDUs (20 seconds)
- **Listening** — prepares to forward, sends/receives BPDUs (15 seconds)
- **Learning** — builds MAC address table, no forwarding (15 seconds)
- **Forwarding** — normal operation, forwards traffic
- **Disabled** — administratively shut down

Total convergence time: **30-50 seconds** (blocking→listening→learning→forwarding)

---

#### STP Variants and Evolution

**Original STP (802.1D)**
- Single spanning tree for all VLANs
- Slow convergence (30-50 seconds)
- Rarely used today

**PVST+ (Per-VLAN Spanning Tree Plus)**
- Cisco proprietary
- Separate spanning tree instance per VLAN
- Allows load balancing across VLANs (different root bridges per VLAN)
- Still uses 802.1D timers (slow)

**RSTP (Rapid Spanning Tree Protocol — 802.1w)**
- Faster convergence: seconds instead of 30-50 seconds
- New port roles: **Alternate** (backup to root port), **Backup** (backup to designated port)
- Port states simplified: **Discarding, Learning, Forwarding**
- Backward compatible with 802.1D
- **Industry standard for modern networks**

**Rapid PVST+**
- Cisco implementation of RSTP with per-VLAN instances
- Best of both: RSTP speed + PVST+ load balancing
- **Recommended for Cisco networks**

**MSTP (Multiple Spanning Tree Protocol — 802.1s)**
- Maps multiple VLANs to single spanning tree instances
- Reduces CPU/memory overhead in large VLAN environments
- More complex to configure

---

#### STP Configuration and Best Practices

**View Spanning Tree Status:**
```
show spanning-tree
show spanning-tree vlan 10
show spanning-tree summary
show spanning-tree interface gi0/1
```

**Set Root Bridge (Manual Priority):**
```
! Method 1: Set specific priority (must be multiple of 4096)
spanning-tree vlan 10 priority 24576

! Method 2: Use helper commands (Cisco)
spanning-tree vlan 10 root primary    ! Sets priority to 24576 or lower
spanning-tree vlan 10 root secondary  ! Sets priority to 28672
```

**Enable PortFast (Access Ports Only):**
```
interface GigabitEthernet0/3
 switchport mode access
 spanning-tree portfast
 ! Or globally: spanning-tree portfast default
```
- PortFast skips listening/learning states, goes directly to forwarding
- **ONLY use on ports connected to end devices** (PCs, servers, printers)
- Never use on trunk or inter-switch links (causes loops!)

**Enable BPDU Guard:**
```
interface GigabitEthernet0/3
 spanning-tree bpduguard enable
 ! Or globally with portfast: spanning-tree portfast bpduguard default
```
- Shuts down port if BPDU received (prevents unauthorized switches)
- Use on all access ports with PortFast

**Enable Root Guard:**
```
interface GigabitEthernet0/1
 spanning-tree guard root
```
- Prevents downstream switches from becoming root bridge
- Use on designated ports toward access layer

**Enable BPDU Filter (Use with Caution):**
```
interface GigabitEthernet0/5
 spanning-tree bpdufilter enable
```
- Stops sending/receiving BPDUs entirely
- Dangerous: disables STP protection on that port
- Only use in very specific scenarios

**Change to RSTP/Rapid PVST+:**
```
spanning-tree mode rapid-pvst
```

---

#### STP for Audio/Dante Networks — Critical Considerations

**Why STP Matters for Dante:**
- Dante uses **multicast** for device discovery and clock distribution
- Layer 2 loops cause **duplicate multicast packets** → audio glitches, sync issues
- Redundant switches/links are common in installed sound systems for reliability
- **STP convergence time affects audio recovery** after link failure

**Dante Network Redundancy Best Practices:**

**1. Dante Redundancy Mode**
- Dante devices support built-in redundancy with **Primary and Secondary networks**
  - Primary: main audio path (e.g., VLAN 10 or untagged)
  - Secondary: backup path on separate physical switches/cables
- **This is different from STP** — Dante handles failover at the application layer
- Both paths stay active; device switches seamlessly if one path fails (~2ms failover)

**2. Network Topology for Dante + STP**

**Option A: Dante Redundancy WITHOUT Switch Redundancy**
- Two completely separate switch stacks (no inter-switch links)
- Primary Dante on Switch Stack A
- Secondary Dante on Switch Stack B
- **No STP needed** between stacks (no loops possible)
- If a switch fails, Dante fails over to secondary network
- **Simplest, most reliable for audio**

**Option B: Dante Redundancy WITH Switch Redundancy (STP Required)**
- Redundant links between switches for IT infrastructure
- STP prevents loops while allowing backup paths
- **Use Rapid PVST+ or RSTP** for faster convergence
- Keep Dante on dedicated VLANs separate from general traffic
- Consider using **separate physical ports/VLANs** for Dante vs. control networks

**3. STP Configuration for Dante:**

```
! Enable Rapid PVST+ for faster convergence
spanning-tree mode rapid-pvst

! Configure root bridge priority (use distribution/core switches)
spanning-tree vlan 10 priority 4096     ! Primary root
spanning-tree vlan 10 priority 8192     ! Secondary root (on backup switch)

! Access ports connected to Dante devices
interface range gi0/1-24
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast        ! Immediate forwarding
 spanning-tree bpduguard enable  ! Prevent rogue switches
 no spanning-tree link-type shared  ! Optimize for point-to-point

! Uplink/trunk ports (inter-switch links)
interface gi0/48
 switchport mode trunk
 no spanning-tree portfast      ! Never use portfast on trunks!
```

**4. Multicast Considerations with STP**
- STP convergence can temporarily disrupt multicast flows
- Enable **IGMP snooping** on Dante VLANs to optimize multicast
- Consider **IGMP snooping querier** on L3 switch or router
```
ip igmp snooping vlan 10
```

**5. Timing and Convergence**
- **802.1D STP**: 30-50 second convergence → **unacceptable audio dropout**
- **RSTP**: 1-6 second convergence → **better but still noticeable**
- **Dante redundancy**: ~2ms failover → **imperceptible to listeners**
- **Best practice:** Use Dante redundancy as primary failover, STP as infrastructure protection

**6. What to Avoid:**
- **Mixing Dante redundancy with spanning-tree blocked paths** — can cause confusion
- **Loops in Dante networks** — causes severe audio artifacts and clock sync issues
- **STP on ports between Dante primary/secondary switches** — keep networks truly separate
- **Using PortFast on inter-switch links** — creates temporary loops

---

#### Verification Commands

```
! Check spanning tree status
show spanning-tree
show spanning-tree vlan 10 detail
show spanning-tree root
show spanning-tree bridge

! Check interface states
show spanning-tree interface gi0/1 detail
show spanning-tree inconsistentports

! Monitor for topology changes
show spanning-tree summary
show spanning-tree vlan 10 | include changes

! Debug (use carefully in production)
debug spanning-tree events
```

---

#### Common STP Issues and Troubleshooting

**Problem: Slow Network Convergence**
- Solution: Upgrade from PVST+ to Rapid PVST+
```
spanning-tree mode rapid-pvst
```

**Problem: Unexpected Root Bridge**
- Check: `show spanning-tree root`
- Solution: Manually set priority on intended root
```
spanning-tree vlan 10 root primary
```

**Problem: Port Stuck in Blocking State**
- Check path cost: `show spanning-tree interface gi0/1 detail`
- Verify root bridge and designated ports
- Check for duplex mismatches: `show interface gi0/1 status`

**Problem: MAC Address Flapping**
- Indicates possible Layer 2 loop
- Check: `show mac address-table`
- Verify STP is enabled and functioning: `show spanning-tree`
- Look for ports in blocking state — if none, you may have a loop

**Problem: Dante Audio Glitches During Topology Change**
- Verify RSTP is enabled (faster convergence)
- Confirm PortFast on access ports
- Consider using Dante redundancy instead of relying on STP failover
- Check: `show spanning-tree summary` for excessive topology changes

---

#### Quick Reference: Port Roles & States

| **Port Role** | **Function** | **Forwards Data?** |
|---------------|--------------|---------------------|
| Root Port | Best path to root bridge | Yes |
| Designated Port | Forwards on a segment | Yes |
| Blocking/Alternate | Backup path | No |
| Disabled | Admin down | No |

| **Port State (RSTP)** | **Sends BPDUs?** | **Learns MACs?** | **Forwards Data?** |
|-----------------------|------------------|------------------|--------------------|
| Discarding | Yes | No | No |
| Learning | Yes | Yes | No |
| Forwarding | Yes | Yes | Yes |

---

#### STP Implementation Topologies — Real-World System Design

Understanding how STP creates redundancy requires looking at **physical topologies** and seeing which ports get blocked and where single points of failure remain.

---

**Scenario 1: Single Switch with Dual Links (EtherChannel Alternative)**

```
        ┌──────┐
        │  PC  │
        └───┬──┘
            │ Single connection
            │
        ┌───┴─────────┐
        │   Switch    │
        │             │
        └─┬─────────┬─┘
          │         │  Two uplinks
          │         │
      ┌───┴────┐ ┌──┴────┐
      │Router A│ │Router B│
      └────────┘ └───────┘
```

**What STP Does:**
- Both uplink ports are on the **same switch**
- STP will **block one uplink** to prevent a loop
- Only ONE uplink carries traffic until the other fails

**Single Points of Failure:**
- ✗ The switch itself (if it fails, PC loses connectivity)
- ✗ The cable from PC to switch
- ✓ Protects against: uplink failure, router failure

**Better Alternative:** Use **EtherChannel/LACP** instead
- Bundles both links into one logical link
- Both links carry traffic simultaneously (load balancing)
- No STP blocking needed
- Still vulnerable to switch failure

---

**Scenario 2: Two Switches in Series (Access → Distribution)**

```
   Dante Device        Dante Device
        │                   │
    ┌───┴────┐          ┌───┴────┐
    │Access  │          │Access  │
    │Switch A│          │Switch B│
    └───┬────┘          └───┬────┘
        │                   │  
        │     ┌──────────┐  │
        └─────┤   Dist   ├──┘
              │ Switch C │  (Root Bridge)
              └────┬─────┘
                   │
              (To Core/Router)
```

**What STP Does:**
- Switch C (distribution) is the **root bridge**
- Access switches A and B each have **one root port** (forwarding)
- No loops exist = **no ports blocked**
- All links active

**Single Points of Failure:**
- ✗ Distribution Switch C (if it fails, entire network down)
- ✗ Each uplink cable
- ✗ Each access switch (devices on that switch lose connectivity)

**No redundancy at this layer** — this is a **tree topology** without backup paths

---

**Scenario 3: Two Distribution Switches with Redundant Uplinks (Common Design)**

```
   Dante Device
        │
    ┌───┴────┐
    │Access  │
    │Switch  │
    └─┬────┬─┘
      │    │  Two uplinks (redundancy!)
      │    │
   ┌──┴──┐ └──┬─────┐
   │Dist │    │Dist │
   │SW A │────│SW B │ Inter-switch link
   └──┬──┘    └──┬──┘
      │          │
   (Core/Router Network)
```

**What STP Does:**
- **Root Bridge Election:** Let's say Dist SW A wins (lower priority/MAC)
- **Access Switch Port Analysis:**
  - Port to Dist A: Best path to root → **Root Port (Forwarding)**
  - Port to Dist B: Higher cost path → **Blocked/Alternate Port**
- **Distribution Switch Ports:**
  - Dist A ports: All **Designated (Forwarding)** — it's the root
  - Dist B port to Dist A: **Root Port (Forwarding)**
  - Dist B port to Access: **Designated (Forwarding)**

**Result:**
- Only **one uplink** from access switch carries traffic (to Dist A)
- Link to Dist B is **blocked** (backup path)
- Inter-switch link between dist switches is **forwarding**

**What Happens When Dist SW A Fails?**
1. Access switch loses BPDUs from root bridge
2. After max age timer (20 seconds with 802.1D, faster with RSTP)
3. STP reconverges: Dist B becomes new root
4. Previously blocked port **unblocks** and becomes root port
5. Traffic flows through Dist B

**Single Points of Failure:**
- ✗ Access Switch (devices on it go down)
- ✓ Distribution switches: **redundant** (failover via STP)
- ✓ Uplinks: **redundant** (one blocked, ready as backup)

**This is a COMMON design** for small-to-medium networks.

---

**Scenario 4: Full Mesh / Triangle Topology (Maximum Redundancy)**

```
        ┌────────────┐
        │  Switch A  │ (Root)
        │            │
        └─┬────────┬─┘
          │        │
          │        │ Both links forwarding
          │        │ (no loop between A-B and A-C separately)
    ┌─────┴──┐  ┌──┴─────┐
    │Switch B│  │Switch C│
    │        │  │        │
    └────┬───┘  └───┬────┘
         │          │
         └────┬─────┘
              │ **This link BLOCKED by STP**
           (Creates loop)
```

**What STP Does:**
- Switch A is root (manually configured or won election)
- Switches B and C both have root ports pointing to A (forwarding)
- Switch A's ports to B and C are designated ports (forwarding)
- **Link between B and C**: One end is designated (forwarding), other end **BLOCKED**
  - This link is the "backup" — only used if A fails or an uplink to A fails

**Why Block B↔C Link?**
- If all three links forwarded, you'd have a **triangle loop**:
  - Broadcast from A → B → C → back to A → infinite loop
- STP blocks the "least useful" link (usually B↔C) to break the loop

**What Happens When Link A-B Fails?**
1. Switch B loses its root port
2. STP reconverges (seconds with RSTP)
3. B↔C link **unblocks**
4. Switch B now reaches A via: B → C → A

**Single Points of Failure:**
- ✓ No single link failure isolates any switch
- ✓ If Switch A fails: B and C elect new root, B↔C link unblocks
- ✗ Complete switch failure: devices on that switch go down

**This is TRUE REDUNDANCY** at the network layer — any single link or switch can fail without network partition.

---

**Scenario 5: Dual-Attached Access Switch (Enterprise Standard)**

```
           ┌────────┐
           │ Server │
           │or Dante│
           │ Device │
           └───┬────┘
               │
         ┌─────┴──────┐
         │   Access   │
         │  Switch    │
         └──┬─────┬───┘
            │     │  TWO uplinks to TWO different switches
            │     │
       ┌────┴──┐ ┌┴─────┐
       │Dist A │ │Dist B│ (Both distribution switches)
       └───────┘ └──────┘
```

**What STP Does:**
- One distribution switch is root bridge (say Dist A)
- Access switch:
  - Port to Dist A: **Root Port (Forwarding)**
  - Port to Dist B: **Alternate Port (Blocked)**
- Only ONE uplink active at a time

**Single Points of Failure:**
- ✗ Access Switch (the switch itself)
- ✓ Distribution switches: redundant
- ✓ Uplinks: redundant

**To Eliminate Access Switch as Single Point of Failure:**
You need **dual-homing at the device level** (next scenario)

---

**Scenario 6: Device-Level Redundancy (Dante Primary/Secondary)**

**CRITICAL DISTINCTION:** This can be implemented two ways with VERY different redundancy levels.

---

**Option 6A: TRUE REDUNDANCY — Two Separate Physical Switches (RECOMMENDED)**

```
    ┌──────────────────────┐
    │   Dante Device       │
    │  (Dual NICs)         │
    └──┬──────────────┬────┘
       │ Primary      │ Secondary
       │ NIC 1        │ NIC 2
       │              │
   ┌───┴─────┐    ┌───┴─────┐
   │Switch A │    │Switch B │  **No physical connection between switches!**
   │         │    │         │  (Completely separate switches)
   └─────────┘    └─────────┘
```

**How It Works:**
- Two **completely separate physical switches** (no connection between Switch A and B)
- Different power supplies, different network hardware, physically separated
- No loops possible → **STP not needed** between the two networks
- Dante device sends/receives audio on **both networks simultaneously**
- If Primary network fails, Dante seamlessly uses Secondary (~2ms switchover)

**Single Points of Failure:**
- ✗ The Dante device itself (hardware failure)
- ✓ Switch A failure: Secondary network takes over immediately
- ✓ Switch B failure: Primary network continues unaffected
- ✓ Cable failure: Other network active
- ✓ Power failure to one switch: Other network continues

**This is the GOLD STANDARD for audio redundancy** — better than relying on STP convergence.

---

**Option 6B: PARTIAL REDUNDANCY — Same Switch, Different VLANs (NOT RECOMMENDED)**

```
    ┌──────────────────────┐
    │   Dante Device       │
    │  (Dual NICs)         │
    └──┬──────────────┬────┘
       │ Primary      │ Secondary
       │ Port 1       │ Port 2
       │              │
       │  ┌───────────┴────────┐
       └──┤    Single Switch   │  **Same physical switch!**
          │  VLAN 10 | VLAN 20 │  (VLANs logically separate)
          └────────────────────┘
```

**How It Works:**
- Same physical switch, but Primary and Secondary use different VLANs
- VLANs keep traffic logically separated (no layer 2 mixing)
- Dante device treats them as separate networks

**What This Protects:**
- ✓ Cable failure: Other cable/port still works
- ✓ Port failure: Other port still works
- ✓ VLAN misconfiguration: Other VLAN unaffected

**What This DOES NOT Protect (Single Points of Failure):**
- ✗ **The switch itself** — if switch fails or reboots, BOTH networks go down simultaneously
- ✗ Power failure to the switch — both networks dead
- ✗ Switch CPU overload or crash — both networks affected
- ✗ Firmware bug or hardware failure — affects both networks

**Why This Defeats The Purpose:**
- Dante redundancy is designed to survive switch failures
- Using the same switch means you've gained **cable redundancy only**
- You've lost **switch redundancy**, which is the more critical failure point
- **This is NOT true redundancy** for professional audio systems

---

**Comparison Table:**

| **Failure Scenario** | **Two Separate Switches** | **Same Switch, Diff VLANs** |
|----------------------|---------------------------|------------------------------|
| Cable fails | ✓ Survives (2ms failover) | ✓ Survives (2ms failover) |
| Port fails | ✓ Survives (2ms failover) | ✓ Survives (2ms failover) |
| **Switch fails** | **✓ Survives (2ms failover)** | **✗ BOTH networks down** |
| Power failure | ✓ Survives | ✗ BOTH networks down |
| Switch reboot | ✓ Survives | ✗ Brief outage on both |
| Dante device fails | ✗ Device is down | ✗ Device is down |

---

**Real-World Example:**

**Broadway Theater (Correct Implementation):**
```
Dante Primary:   Cisco SG350 #1 → Dante devices NIC 1
Dante Secondary: Cisco SG350 #2 → Dante devices NIC 2
(No connection between the two switches)
```
- If Switch #1 has a power supply failure during a show, audio continues seamlessly on Switch #2
- **Show goes on!**

**Incorrect Implementation (What NOT To Do):**
```
Dante Primary:   Cisco SG350 VLAN 10 → Dante devices NIC 1
Dante Secondary: Same Cisco SG350 VLAN 20 → Dante devices NIC 2
```
- If the switch fails during a show, **both Dante networks fail**

---

**When Might Same-Switch VLANs Be Used? (Limited scenarios)**

In **small, temporary setups** where:
- Budget constraints prevent buying two switches
- Failure is acceptable (rehearsals, practice spaces)
- You want cable/port redundancy but acknowledge switch is single point of failure
- You're testing Dante redundancy functionality

**Never use this for:**
- Live performances
- Broadcast facilities  
- Houses of worship services
- Corporate events
- Installed systems where downtime is unacceptable

---

**Additional Consideration: Physical Separation**

Even with two separate switches, best practices include:
- **Different power circuits** (or UPS backup)
- **Different physical locations** (separate racks if possible)
- **Different cable paths** (avoid single conduit failure)
- **Different network uplinks** (if connected to larger network)

**Why?** A rack power failure, fire, water damage, or physical damage should only affect ONE of the two networks.

---

**Scenario 7: Hybrid: Dante Dual Networks + STP within Each Network**

```
Dante Primary Network (VLAN 10):
    Device          Device
      │              │
   ┌──┴──┐        ┌──┴──┐
   │Acc A│────────│Acc B│  STP blocks this link if needed
   └──┬──┘        └──┬──┘
      │              │
   ┌──┴──────────────┴──┐
   │   Dist Switch A    │  (Root for VLAN 10)
   └────────────────────┘

Dante Secondary Network (VLAN 20 or separate switch fabric):
    Device          Device
      │              │
   ┌──┴──┐        ┌──┴──┐
   │Acc C│────────│Acc D│  STP blocks this link if needed
   └──┬──┘        └──┬──┘
      │              │
   ┌──┴──────────────┴──┐
   │   Dist Switch B    │  (Root for VLAN 20)
   └────────────────────┘

No connection between Network A and Network B stacks!
```

**What This Achieves:**
- **Dante-level redundancy**: Primary/Secondary networks completely separate
- **STP within each network**: Prevents loops if you have redundant inter-switch links
- **Best of both worlds**: Fast Dante failover + infrastructure loop protection

**Single Points of Failure:**
- ✓ Any single switch failure: Devices fail to other Dante network
- ✓ Any single link failure: STP reconverges within that network
- ✗ Dante device itself (hardware)

**This is ENTERPRISE AUDIO DESIGN** — used in Broadway theaters, arenas, broadcast facilities.

---

#### Key Takeaways: Redundancy and Single Points of Failure

**Where STP Helps:**
- ✓ Protects against **link failures** (blocked links become active)
- ✓ Protects against **switch failures** (topology reconverges)
- ✓ Allows **redundant physical paths** without creating loops

**Where STP Doesn't Help (Single Points of Failure Remain):**
- ✗ **The device itself** (if the PC/server/Dante unit fails, redundant network doesn't help)
- ✗ **Access switches** without dual-homing (if access switch dies, connected devices go down)
- ✗ **Cables from device to switch** (unless device has dual NICs to different switches)

**To Achieve True Redundancy:**
1. **Network layer**: Use redundant switches + STP (or RSTP/MSTP)
2. **Device layer**: Dual NICs on critical devices, connected to different switches
3. **Application layer**: Dante redundancy (Primary/Secondary networks)
4. **Physical layer**: Different physical paths (separate cable runs, conduits, power)

**For Audio Systems (Dante Specifically):**
- **Option 1 (Best)**: Two completely separate switch stacks, Dante primary/secondary
  - No STP needed between stacks
  - ~2ms failover at application layer
  
- **Option 2 (Complex)**: Single network with redundant switches + STP
  - Relies on STP convergence (1-6 seconds with RSTP)
  - May cause brief audio dropout
  
- **Option 3 (Hybrid)**: Dante dual networks + STP within each for infrastructure protection
  - Maximum redundancy
  - More expensive (more switches, more cabling)

---

#### Visualizing STP Port Blocking in Real Time

When you run `show spanning-tree`, you'll see output like:

```
VLAN0010
  Spanning tree enabled protocol rstp
  Root ID    Priority    4096
             Address     0011.2233.4455
             This bridge is the root
             
Interface        Role Sts Cost      Prio.Nbr Type
---------------- ---- --- --------- -------- --------
Gi0/1            Desg FWD 4         128.1    P2p
Gi0/2            Desg FWD 4         128.2    P2p
Gi0/3            Altn BLK 4         128.3    P2p  ← **BLOCKED PORT**
```

**Translation:**
- `Gi0/1` and `Gi0/2`: **Designated ports, Forwarding** — active
- `Gi0/3`: **Alternate port, Blocking** — backup path, ready to activate on failure

**This blocked port is your redundancy** — it's not wasted, it's protecting you from loops while standing by for failover.

---

#### Quick Design Checklist

When designing a redundant network:

1. **Identify critical devices** — what CANNOT go down?
2. **Dual-home critical devices** — two NICs, two different switches
3. **Use redundant switches** — at least two at distribution layer
4. **Configure STP properly**:
   - Set root bridge manually (lowest priority on your primary dist switch)
   - Enable RSTP for fast convergence
   - Use PortFast + BPDU Guard on access ports
5. **For Dante: use separate Primary/Secondary networks** when possible
6. **Document the topology** — know which ports will block
7. **Test failover** — unplug cables and time the convergence

---

#### Practice Lab: STP Behavior

**Topology:** Three switches in a triangle (A, B, C) with links between each pair

**Tasks:**
1. Connect switches, observe default root election
2. Identify root port and designated ports on each switch
3. Manually set Switch A as root bridge
4. Disconnect the root port on Switch B, observe convergence
5. Enable PortFast on access ports, test PC connectivity speed
6. Enable BPDU Guard, connect an unauthorized switch, observe shutdown

**Expected Learning:**
- How BPDUs elect root bridge
- Path cost calculation
- Convergence time differences (PVST+ vs Rapid PVST+)
- Impact of PortFast on end-user experience

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
