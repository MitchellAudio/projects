# 08 — Detailed Architecture: dLive FOH + SQ-5 Monitor/Backup with ME-500, Waves & RSTP Ring

## Overview

This document describes a production-ready system where:

- **dLive S5000 + DM48** handles FOH mixing with Waves SoundGrid processing
- **SQ-5** handles all monitoring (stage IEMs, backstage, green room) plus hosts the ME-500 personal mixing system for pit musicians, while remaining ready as an emergency FOH backup
- **ME-500 × 8** personal mixers give pit musicians individual control over their monitor balance
- **3-switch RSTP ring** with Dante Primary/Secondary across different switches eliminates every single-node failure point on the network
- **Waves** runs on FOH only via dedicated M-DL-WAVES card — does not affect the monitoring or backup path

---

## Equipment List

### FOH Position

| Equipment | Role | Notes |
|---|---|---|
| dLive S5000 surface | FOH mixing control | 28 faders |
| DM48 MixRack | FOH audio processing | 48 mic in, 24 line out, 3 I/O port slots |
| M-DL-DANT128-A | DM48 Port A — Dante I/O | 128×128 Dante, dual RJ45 (Primary + Secondary) |
| M-DL-WAVES | DM48 Port B — Waves SoundGrid | Dedicated Ethernet to SoundGrid server |
| SoundGrid server | Waves DSP processing | Rack-mount, dedicated Ethernet to M-DL-WAVES |
| Sennheiser receivers × 32 | Wireless lavs | Dante-enabled, dual ports (Primary + Secondary) |
| Mac A (QLab) | Primary playback | Dante Virtual Soundcard |
| Mac B (QLab) | Backup playback | Dante Virtual Soundcard |
| Switch A | FOH managed switch | Netgear M4250 or equivalent, RSTP-capable |
| iPad | Emergency dLive surface control | dLive MixPad app |

### Backstage / A2 Position

| Equipment | Role | Notes |
|---|---|---|
| SQ-5 | Monitor mixing + ME-500 host + backup FOH | 48ch, 17 faders, rack-mounted |
| SQ Dante 64×64 card | SQ option slot — Dante I/O | Dual RJ45 (Primary + Secondary) |
| Switch B | Backstage managed switch | RSTP-capable, same model as Switch A |
| IEM transmitters × 4 | Stage performer wireless IEMs | Fed from SQ mix outputs via Dante or local |
| Backstage wedge | A2 / backstage monitoring | Fed from SQ mix output |
| Green room speaker | Cast green room feed | Fed from SQ mix or matrix output |
| A2 control laptop | Dante Controller + failover presets | Connected to Switch B on Control VLAN |

### Pit

| Equipment | Role | Notes |
|---|---|---|
| A&H DT168 | Pit stagebox | 16 in / 8 out, Dante, dual ports (Primary + Secondary) |
| ME-U hub | ME-500 distribution | Dante input, distributes to ME-500 daisy-chain |
| ME-500 × 8 | Pit personal monitors | 16 channels each, Cat5e daisy-chain from ME-U |

### Amp Rack

| Equipment | Role | Notes |
|---|---|---|
| d&b DS10 | Dante→AES3 bridge | 16ch, dual Dante ports (Primary + Secondary) |
| d&b D20 × 2 | Power amplifiers | 4ch each = 8 output zones, AES3 input |
| Switch C | Amp rack managed switch | RSTP-capable, same model as A and B |

---

## SQ-5 I/O Budget — Detailed Breakdown

### Input Channels (48 of 48 used)

| SQ Channel | Source | Dante Subscription |
|---|---|---|
| Ch 1–32 | Sennheiser wireless lavs | `LAV-01` through `LAV-32` |
| Ch 33–48 | DT168 pit instruments | `PIT-01` through `PIT-16` |

**Status: At capacity (48/48).** No spare input channels. If additional inputs are needed (e.g., talkback, additional playback), they would need to replace existing channels or use the SQ's local mic inputs (16 built-in).

### Mix Bus Allocation (7 of 12 stereo mixes used)

| Bus | Assignment | Destination | Dante Output Channels |
|---|---|---|---|
| Mix 1 | IEM Mix — Performer 1 (stereo) | IEM Transmitter 1 | `SQ-IEM1-L`, `SQ-IEM1-R` |
| Mix 2 | IEM Mix — Performer 2 (stereo) | IEM Transmitter 2 | `SQ-IEM2-L`, `SQ-IEM2-R` |
| Mix 3 | IEM Mix — Performer 3 (stereo) | IEM Transmitter 3 | `SQ-IEM3-L`, `SQ-IEM3-R` |
| Mix 4 | IEM Mix — Performer 4 (stereo) | IEM Transmitter 4 | `SQ-IEM4-L`, `SQ-IEM4-R` |
| Mix 5 | Vocal Stem for ME-500 (stereo) | ME-U via Dante | `SQ-VSTEM-L`, `SQ-VSTEM-R` |
| Mix 6 | Backstage Wedge (stereo) | Backstage amp/powered speaker | `SQ-BKSTG-L`, `SQ-BKSTG-R` |
| Mix 7 | Green Room Feed (stereo) | Green room amp/powered speaker | `SQ-GR-L`, `SQ-GR-R` |
| Mix 8–12 | **SPARE** (5 stereo mixes) | Available for additional IEMs, feeds, etc. | — |

### LR Bus

| Bus | Assignment | Destination |
|---|---|---|
| LR | Backup FOH main output | DS10 via Dante (standby — activated on failover) |

Dante output channels: `SQ-FOH-L`, `SQ-FOH-R` (plus 6 more zone outputs routed from matrix or additional mixes for full 8-zone backup)

### Matrix Allocation (available)

| Bus | Assignment | Notes |
|---|---|---|
| Matrix 1 | Backup FOH zone distribution | Fed from LR, provides zone-specific level/EQ |
| Matrix 2 | Backup FOH zone distribution | Additional zones |
| Matrix 3 | Spare / additional backstage distribution | — |

### Dante Card I/O Budget (64 in / 64 out)

**Inputs used: 48 of 64**

| Dante Input Channels | Count | Source |
|---|---|---|
| LAV-01 through LAV-32 | 32 | Sennheiser wireless |
| PIT-01 through PIT-16 | 16 | DT168 pit stagebox |
| QLAB-A-01 through QLAB-A-08 | 8* | QLab Mac A (*if SQ subscribes) |
| **Total** | **48–56** | |

**Outputs used: ~34 of 64**

| Dante Output Channels | Count | Destination |
|---|---|---|
| SQ-IEM1 through SQ-IEM4 (stereo) | 8 | IEM transmitters |
| SQ-VSTEM-L/R | 2 | ME-U (vocal stem for ME-500) |
| SQ-PIT-01 through SQ-PIT-14 | 14 | ME-U (pit instrument direct outs) |
| SQ-BKSTG-L/R | 2 | Backstage wedge |
| SQ-GR-L/R | 2 | Green room |
| SQ-FOH-L/R + zone outputs | 6–8 | DS10 (backup FOH, standby) |
| **Total** | **~34** | **30 spare output channels** |

**Verdict: Comfortable headroom on all SQ-5 resources.**

---

## ME-500 System Architecture

### How the ME-500 Personal Mix Works

Each ME-500 unit receives up to **16 audio channels** and provides the pit musician with individual level control over each channel. The musician creates their own monitor mix from these 16 sources.

### Channel Assignment (16 channels to ME-U)

| ME-500 Channel | Source | SQ-5 Route |
|---|---|---|
| 1 | Drums — Kick | Direct out from SQ Ch 33 → Dante → ME-U |
| 2 | Drums — Snare | Direct out from SQ Ch 34 → Dante → ME-U |
| 3 | Drums — Kit (stereo L) | Direct out from SQ Ch 35 → Dante → ME-U |
| 4 | Drums — Kit (stereo R) | Direct out from SQ Ch 36 → Dante → ME-U |
| 5 | Bass | Direct out from SQ Ch 37 → Dante → ME-U |
| 6 | Keys 1 (L) | Direct out from SQ Ch 38 → Dante → ME-U |
| 7 | Keys 1 (R) | Direct out from SQ Ch 39 → Dante → ME-U |
| 8 | Keys 2 / Synth | Direct out from SQ Ch 40 → Dante → ME-U |
| 9 | Guitar 1 | Direct out from SQ Ch 41 → Dante → ME-U |
| 10 | Guitar 2 | Direct out from SQ Ch 42 → Dante → ME-U |
| 11 | Reeds / Winds 1 | Direct out from SQ Ch 43 → Dante → ME-U |
| 12 | Reeds / Winds 2 | Direct out from SQ Ch 44 → Dante → ME-U |
| 13 | Brass / Winds 3 | Direct out from SQ Ch 45 → Dante → ME-U |
| 14 | Click / Guide Track | Direct out from SQ Ch 46 → Dante → ME-U |
| 15 | Vocal Stem L | SQ Mix 5 L → Dante → ME-U |
| 16 | Vocal Stem R | SQ Mix 5 R → Dante → ME-U |

*Adjust instrument assignments to match actual pit layout. The key point: channels 1–14 are direct outputs from SQ input channels (post-processing), and channels 15–16 are the vocal stem from a dedicated SQ mix bus.*

### Signal Path

```
Pit instruments → DT168 (mic preamps)
                      │
                      ▼ Dante
                 ┌─────────────┐
                 │  SQ-5       │
                 │  (processes  │
                 │   pit ch's)  │
                 │             │
                 │  Direct outs │──Dante──► ME-U hub ──Cat5e──► ME-500 ×8
                 │  (ch 33-46)  │           (16 ch)    (daisy-chain)
                 │             │
                 │  Mix 5 bus  │──Dante──►  (vocal stem = ME ch 15-16)
                 │  (vocal stem)│
                 └─────────────┘
```

### ME-U Hub Configuration

- **Dante input**: ME-U subscribes to SQ's 16 Dante output channels (`SQ-PIT-01..14` + `SQ-VSTEM-L/R`)
- **ME-U Primary Dante port** → Switch B (backstage)
- **ME-U Secondary Dante port** → Switch C or Switch A (for redundancy)
- **ME-500 daisy-chain**: Up to 8 ME-500 units chain from ME-U's Cat5e ports
- **A2 control**: A2 can adjust what the ME-500 users receive by changing SQ direct out levels, processing, or the vocal stem mix

### ME-500 Direct Out Configuration on SQ-5

On the SQ-5, configure direct outputs for pit channels:

1. Go to **I/O Patch** → **Direct Outs**
2. For each pit channel (Ch 33–46), set the direct out to **Post-Processing** (post-EQ, post-compressor, post-fader)
3. Route each direct out to the corresponding SQ Dante output channel
4. This ensures pit musicians hear processed audio, not raw preamp signals
5. The A2 can adjust the direct out tap point (pre-fader, post-fader) depending on whether musicians should hear the A2's fader moves

---

## dLive FOH Configuration with Waves

### DM48 I/O Port Allocation

| Port | Card | Function |
|---|---|---|
| Port A | M-DL-DANT128-A | Dante 128×128 — all inputs, 8 FOH zone outputs |
| Port B | M-DL-WAVES | Waves SoundGrid — FOH processing |
| Port C | **Available** | Spare (MADI, additional expander, etc.) |

### Waves SoundGrid Integration

```
DM48 MixRack
    │
    ├── Port A: M-DL-DANT128-A ──► Dante Network (switches)
    │
    └── Port B: M-DL-WAVES ──► SoundGrid Server (dedicated Ethernet, NOT on Dante network)
                                    │
                                    └── Direct Ethernet cable (Cat5e/6)
                                         to SoundGrid server
```

**Critical**: The SoundGrid server connects via a **dedicated Ethernet cable** directly to the M-DL-WAVES card. This is a separate network from Dante — SoundGrid and Dante do NOT share switches or VLANs.

### Waves Plugin Architecture

| Plugin Slot | Usage | Notes |
|---|---|---|
| Channel inserts | EQ, compression, de-essing on vocals | Per-channel Waves inserts |
| Mix bus inserts | Reverb, delay on FX returns | Bus-level Waves inserts |
| LR insert | Master processing (limiting, final EQ) | Optional |

**Important for redundancy**: Waves plugins add latency and a failure point. Configure the dLive so that if the SoundGrid server fails:
1. The M-DL-WAVES card has a built-in **bypass mode** — if the server goes offline, audio passes through un-processed
2. The dLive's **DEEP processing** (onboard) should carry a "safety" setup on every channel — basic EQ and compression that works without Waves
3. Program a **scene/snapshot** called "NO WAVES" that disables all Waves inserts and activates DEEP processing as a fallback

### Waves Failure Procedure

| Event | Impact | Response |
|---|---|---|
| SoundGrid server crash | Waves processing bypassed; audio passes through clean | Continue mixing with DEEP processing; recall "NO WAVES" scene if needed |
| M-DL-WAVES card failure | Waves inserts lose audio for affected channels | Disable Waves inserts on affected channels; DEEP processing takes over |
| SoundGrid cable disconnect | Same as server crash | Reconnect cable; server will re-sync |

**The audience hears**: A brief change in sonic character (loss of Waves processing) but NO audio dropout. This is because Waves is inserted within the dLive's signal chain — if the insert point fails, the dLive's internal processing continues.

---

## Network Architecture: RSTP Ring Topology

### Why RSTP

**Spanning Tree Protocol (RSTP — IEEE 802.1w)** prevents network loops while providing automatic path redundancy. In a ring of switches, RSTP:

1. Detects the loop created by the ring topology
2. Blocks one link to prevent broadcast storms
3. If any link fails, RSTP unblocks the backup path within **milliseconds** (<1 second)
4. No operator action required — fully automatic

### 3-Switch Ring Topology

```
         ┌───────────────────────────────────────┐
         │                                       │
    ┌────┴────┐       Trunk Link A↔B       ┌─────┴────┐
    │Switch A │◄══════════════════════════►│ Switch B │
    │  (FOH)  │        Cat6a / Fiber       │(Backstage)│
    └────┬────┘                            └─────┬────┘
         │                                       │
         │  Trunk Link A↔C          Trunk Link B↔C
         │                                       │
    ┌────┴────────────────────────────────────────┴────┐
    │                   Switch C                       │
    │                 (Amp Rack)                        │
    └──────────────────────────────────────────────────┘

    RSTP blocks ONE link (e.g., B↔C) to prevent loop.
    If A↔B cable fails → RSTP unblocks B↔C → traffic flows A↔C↔B.
    Reconvergence: <1 second (RSTP / 802.1w).
```

### VLAN Configuration (All 3 Switches)

| VLAN ID | Name | Purpose | RSTP Instance |
|---|---|---|---|
| 20 | Dante-Primary | Dante Primary audio streams | STP instance 1 |
| 30 | Dante-Secondary | Dante Secondary audio streams | STP instance 2 |
| 40 | Control | OSC, OCA/AES70, R1, Dante Controller, web dashboards | STP instance 3 |

All trunk links between switches carry all three VLANs (tagged).

### Switch Configuration

**All 3 switches (identical base config):**

```
# RSTP configuration (per switch)
spanning-tree mode rapid-pvst          # Rapid Per-VLAN Spanning Tree
spanning-tree vlan 20 priority 4096   # (root bridge only — Switch A)
spanning-tree vlan 30 priority 4096   # (root bridge only — Switch A)
spanning-tree vlan 40 priority 4096   # (root bridge only — Switch A)

# QoS for Dante
qos dscp-map ef 46                     # Expedited Forwarding for Dante
qos trust dscp                         # Trust DSCP markings from Dante devices

# IGMP snooping
ip igmp snooping                       # Enable globally
ip igmp snooping vlan 20               # Enable on Dante Primary
ip igmp snooping vlan 30               # Enable on Dante Secondary

# Port speed
interface range all-dante-ports
  speed 1000                           # Force 1Gbps
  duplex full
  no auto-negotiate                    # Dante requires fixed settings
```

**Switch A (FOH) — Root Bridge:**
- Set STP priority to lowest value (4096) for all VLANs → becomes root bridge
- Root bridge = most central/important switch in the ring

**Switches B and C:**
- Set STP priority to default (32768) → become non-root bridges
- RSTP will automatically select which link to block

### Trunk Link Configuration

Each trunk link between switches:

```
interface trunk-port
  switchport mode trunk
  switchport trunk allowed vlan 20,30,40
  spanning-tree link-type point-to-point    # Fastest RSTP convergence
  spanning-tree guard root                   # (on non-root switches only)
```

---

## Dante Device Connections: Eliminating Single Switch Failures

The RSTP ring protects against **link** failures. To protect against a **switch** failure, connect each device's Primary and Secondary Dante ports to **different switches**:

### Connection Map

| Device | Primary Dante Port → | Secondary Dante Port → | Rationale |
|---|---|---|---|
| DM48 (M-DL-DANT128-A) | **Switch A** (FOH, VLAN 20) | **Switch B** (Backstage, VLAN 30) | If Switch A dies: DM48 still reaches network via Switch B |
| SQ-5 (SQ Dante card) | **Switch B** (Backstage, VLAN 20) | **Switch C** (Amp Rack, VLAN 30) | If Switch B dies: SQ still reaches network via Switch C |
| DS10 | **Switch C** (Amp Rack, VLAN 20) | **Switch A** (FOH, VLAN 30) | If Switch C dies: DS10 still reaches network via Switch A |
| DT168 (Pit) | **Switch B** (Backstage, VLAN 20) | **Switch A** (FOH, VLAN 30) | Pit near backstage; secondary reaches FOH |
| ME-U hub | **Switch B** (Backstage, VLAN 20) | **Switch C** (Amp Rack, VLAN 30) | Near SQ; secondary via amp rack |
| Sennheiser (×32) | **Switch A** (FOH, VLAN 20) | **Switch A** (FOH, VLAN 30)* | *Same switch — separate VLANs. 32 devices on 2 switches is impractical. |
| QLab Mac A | **Switch A** (VLAN 20) | — (DVS = single port) | Single-port limitation of DVS |
| QLab Mac B | **Switch A** (VLAN 20) | — (DVS = single port) | Single-port limitation of DVS |

*Sennheiser receivers: With 32 units, connecting Primary/Secondary to different switches would require 64 cable runs. Practical compromise: connect both Primary and Secondary to Switch A (different VLANs). The RSTP ring still protects the path from Switch A to the rest of the network.*

### Single Node Failure Analysis

| Failed Node | Devices Affected | Dante Recovery | Audio Impact |
|---|---|---|---|
| **Switch A dies** | Sennheiser Primary + Secondary gone. DM48 Primary gone. QLab gone. | DM48 still on Secondary (Switch B). DS10 Secondary still on Switch A — also gone. | **Major**: All wireless mics lost. FOH mixing continues from DM48 via Switch B. DS10 Primary on Switch C still works. SQ takes over FOH. |
| **Switch B dies** | SQ Primary gone. DT168 Primary gone. ME-U Primary gone. | SQ on Secondary (Switch C). DT168 on Secondary (Switch A). ME-U secondary (Switch C). | **Partial**: SQ continues via Secondary. Pit may have brief dropout. ME-500 may lose audio briefly during Dante reconvergence. |
| **Switch C dies** | DS10 Primary gone. SQ Secondary gone. ME-U Secondary gone. | DS10 on Secondary (Switch A). All others unaffected. | **None to minimal**: DS10 fails to Secondary transparently. |
| **Any single link** | None | RSTP reroutes within <1 second | **None**: RSTP reconvergence is transparent |
| **DM48 fails** | FOH audio stops | SQ takes over (Dante preset switch) | **5–10s silence** (manual failover) |

### Network Diagram with All Connections

```
╔═══════════════════════════════════════════════════════════════════════╗
║                        SWITCH A (FOH)                                ║
║                     [RSTP Root Bridge]                               ║
║                                                                      ║
║  Ports:                                                              ║
║  ├─ DM48 Primary (VLAN 20)                                          ║
║  ├─ Sennheiser ×32 Primary (VLAN 20)                                ║
║  ├─ Sennheiser ×32 Secondary (VLAN 30)                              ║
║  ├─ QLab Mac A (VLAN 20)                                            ║
║  ├─ QLab Mac B (VLAN 20)                                            ║
║  ├─ DS10 Secondary (VLAN 30)                                        ║
║  ├─ DT168 Secondary (VLAN 30)                                       ║
║  ├─ SoundGrid server — NOT on switch (direct to M-DL-WAVES)         ║
║  ├─ R1 laptop / control devices (VLAN 40)                           ║
║  ├─ TRUNK → Switch B                                                ║
║  └─ TRUNK → Switch C                                                ║
╚═══════════════╤═══════════════════════════════════════╤══════════════╝
                │ Trunk (Cat6a)                         │ Trunk (Cat6a)
                │                                       │
╔═══════════════╧══════════════════╗    ╔═══════════════╧══════════════╗
║      SWITCH B (Backstage)        ║    ║      SWITCH C (Amp Rack)     ║
║                                  ║    ║                              ║
║  Ports:                          ║    ║  Ports:                      ║
║  ├─ SQ-5 Primary (VLAN 20)      ║    ║  ├─ DS10 Primary (VLAN 20)   ║
║  ├─ DT168 Primary (VLAN 20)     ║    ║  ├─ SQ-5 Secondary (VLAN 30) ║
║  ├─ ME-U Primary (VLAN 20)      ║    ║  ├─ ME-U Secondary (VLAN 30) ║
║  ├─ DM48 Secondary (VLAN 30)    ║    ║  ├─ D20 amps (VLAN 40 only)  ║
║  ├─ IEM transmitters (VLAN 20)  ║    ║  ├─ TRUNK → Switch A          ║
║  ├─ Backstage wedge amp (VLAN 20)║   ║  └─ TRUNK → Switch B          ║
║  ├─ A2 Dante Controller laptop   ║   ║                              ║
║  │  (VLAN 40)                    ║    ╚══════════════════════════════╝
║  ├─ TRUNK → Switch A             ║
║  └─ TRUNK → Switch C             ║
╚══════════════════════════════════╝
```

---

## RSTP Behavior Walkthrough

### Normal Operation

RSTP elects Switch A as root bridge (lowest priority). One link in the triangle is **blocked** (e.g., the B↔C link). All traffic flows through Switch A as the hub:

```
Switch A ←→ Switch B     (forwarding)
Switch A ←→ Switch C     (forwarding)
Switch B ←→ Switch C     (BLOCKED by RSTP)
```

Audio flows: DM48 (Switch A) → Switch A → Switch C → DS10 (amp rack)

### Link Failure Example: A↔B Cable Cut

1. RSTP detects A↔B link is down
2. RSTP unblocks B↔C link (within milliseconds)
3. New path: Switch A → Switch C → Switch B
4. All devices on Switch B (SQ, DT168, ME-U) now reachable via Switch C
5. **Audio impact**: <1 second potential micro-dropout during reconvergence; Dante Secondary provides backup during this window

### Switch Failure Example: Switch B Dies

1. All devices with Primary on Switch B lose Primary Dante connection
2. **SQ-5**: Fails to Secondary on Switch C → continues operating
3. **DT168**: Fails to Secondary on Switch A → pit audio continues
4. **ME-U**: Fails to Secondary on Switch C → ME-500 audio continues
5. RSTP reconverges remaining ring (A↔C direct link only, no loop)
6. **Audio impact**: Brief (<1s) dropout possible on devices that were on Switch B Primary. Dante Secondary transparently takes over.

---

## Complete Signal Flow

```
                    ┌─────────────────────────────────┐
                    │         INPUT SOURCES            │
                    ├─────────────────────────────────┤
                    │  Sennheiser ×32  │  DT168 (Pit) │
                    │  (Dante)         │  (Dante)      │
                    │  LAV-01..32      │  PIT-01..16   │
                    └────────┬────────────────┬────────┘
                             │    Dante       │
                    ┌────────┴────────────────┴────────┐
                    │      RSTP RING NETWORK           │
                    │  (Switch A ↔ B ↔ C ↔ A)         │
                    │  VLAN 20 (Pri) + VLAN 30 (Sec)   │
                    └──┬──────────┬──────────┬─────────┘
                       │          │          │
              ┌────────┴──┐  ┌───┴────┐  ┌──┴─────────┐
              │  DM48     │  │  SQ-5  │  │   DS10     │
              │  (FOH)    │  │ (A2)   │  │  (Bridge)  │
              │           │  │        │  │            │
              │  128×128  │  │ 64×64  │  │ 16→AES3   │
              │  Dante    │  │ Dante  │  │            │
              │  +Waves   │  │        │  └──┬─────────┘
              └──┬────────┘  └─┬──────┘     │ AES3
                 │             │             │
              ┌──┴────┐     ┌──┴───────────┐ │
              │ S5000 │     │  OUTPUTS:    │ ├──► D20 #1 → Zones 1-4
              │Surface│     │  Mix 1-4:IEM │ └──► D20 #2 → Zones 5-8
              │(gACE) │     │  Mix 5: Stem │
              └───────┘     │  Mix 6: Bkst │
                            │  Mix 7: GR   │
            ┌───────┐       │  LR: Bkup FOH│
            │Waves  │       └──┬───────────┘
            │Server │          │ Dante
            │(dedi- │       ┌──┴─────────┐
            │cated) │       │   ME-U     │
            └───────┘       │  (16 ch)   │
                            └──┬─────────┘
                               │ Cat5e
                        ┌──────┴──────────────────────┐
                        │  ME-500 ×8 (daisy-chain)    │
                        │  Pit musicians              │
                        └─────────────────────────────┘
```

---

## SQ-5 Programming for Triple Duty

### Layer Organization (17 Faders)

| Layer | Faders 1–16 | Fader 17 |
|---|---|---|
| **Layer 1** | LAV-01 through LAV-16 | DCA Master |
| **Layer 2** | LAV-17 through LAV-32 | DCA Master |
| **Layer 3** | PIT-01 through PIT-16 | DCA Master |
| **Layer 4** | IEM Mix 1–4 masters, Backstage, Green Room, Vocal Stem, Spare | Main LR |
| **Layer 5** | DCAs 1–8, FX Returns | Main LR |

### DCA Assignments (for monitoring and backup FOH)

| DCA | Assignment | Notes |
|---|---|---|
| DCA 1 | Principals (lead vocalists) | Core vocal group |
| DCA 2 | Ensemble (chorus vocalists) | Group vocal control |
| DCA 3 | Band (all pit instruments) | Overall band level |
| DCA 4 | Drums/Percussion | Rhythm section |
| DCA 5 | Keys/Synths | Keyboard section |
| DCA 6 | Playback (QLab) | Sound effects and tracks |
| DCA 7 | FX Returns | Reverb and delay returns |
| DCA 8 | Spare | Available |

### Snapshot Programming

- **Mirror the dLive cue numbers exactly** — critical for TheatreMix sync
- Each snapshot recalls: DCA levels, mute states, IEM mix adjustments per scene
- Channel-safe the pit channels and IEM mix masters (rarely change per cue)
- Recall-safe the backstage and green room feeds (always-on)

### Backup FOH Programming

The SQ must carry a complete FOH mix ready to go:

1. Program full FOH EQ, compression, and routing using DEEP processing
2. Configure 8 zone outputs matching the dLive's zone structure:
   - Use LR bus for main zone pair
   - Use Matrix 1–3 for additional zone distribution
   - Or: Use spare Mix buses 8–12 for additional zone outputs
3. All zone outputs routed to Dante output channels: `SQ-Zone1` through `SQ-Zone8`
4. These Dante outputs sit idle during normal operation — DS10 is subscribed to dLive outputs
5. On failover: A2 loads Dante Controller preset to switch DS10 to SQ zone outputs

**Dual-purpose output routing:**

During normal operation:
```
SQ Mix 1–7 → IEMs, backstage, green room, vocal stem (ACTIVE)
SQ LR + Matrix → Backup FOH zones (STANDBY — Dante outputs not subscribed by DS10)
```

During failover:
```
SQ Mix 1–7 → IEMs, backstage, green room, vocal stem (STILL ACTIVE)
SQ LR + Matrix → FOH zones (NOW ACTIVE — DS10 subscribed to SQ outputs)
```

The A2 continues to manage both monitoring AND FOH from the SQ-5 during a failover event. The 5 spare stereo mixes provide breathing room for any additional monitor needs that arise.

---

## Failover Procedures (This Architecture)

### F-08-1: DM48 MixRack Failure

| | |
|---|---|
| **Symptom** | FOH audio stops; S5000 shows "MixRack offline" |
| **Detection** | A1 loses control; Dante Controller shows DM48 offline |
| **Audience impact** | 5–10 seconds silence on FOH zones; monitoring continues uninterrupted |
| **Response** | A2 switches DS10 to SQ backup outputs |

**Key difference from original architecture**: IEMs, backstage, green room, and ME-500 pit monitors **continue without interruption** because they come from the SQ, which is independent of the dLive. Only the FOH zone outputs (audience speakers) are affected.

**Procedure (A2):**
1. SQ monitoring outputs are unaffected — IEMs and pit continue
2. Open Dante Controller on A2 laptop
3. Load preset: **"SQ BACKUP FOH"**
4. Click Apply — DS10 re-subscribes to `SQ-Zone1..8`
5. Verify FOH audio on R1 meters
6. Continue show — A2 now manages FOH + monitors from SQ-5
7. A1 can assist from iPad (dLive MixPad) if DM48 recovers 

### F-08-2: SQ-5 Failure

| | |
|---|---|
| **Symptom** | All monitoring stops — IEMs, backstage, green room, pit ME-500 |
| **Detection** | Performers report IEM loss; A2 sees SQ offline |
| **Audience impact** | None (FOH still on dLive) |
| **Response** | Performers go to wedge backup or acoustic; ME-500 goes silent |

**Procedure:**
1. FOH mix is unaffected — A1 continues on dLive
2. Stage performers lose IEMs — if backup wedge monitors available (from dLive aux sends), route to those
3. Pit musicians lose ME-500 — band plays acoustically by ear
4. A2 attempts SQ reboot
5. **Mitigation**: Pre-configure emergency monitor sends on dLive aux buses (requires dLive to have spare buses). This trades the "dLive does FOH only" simplicity for emergency monitoring capability.

### F-08-3: Waves SoundGrid Server Failure

| | |
|---|---|
| **Symptom** | FOH audio character changes — Waves processing drops out |
| **Detection** | A1 notices tonal change; SoundGrid server status offline |
| **Audience impact** | Subtle sonic change — no audio dropout |
| **Response** | Recall "NO WAVES" scene on dLive |

**Procedure (A1):**
1. Audio continues through dLive — Waves bypass is automatic
2. Recall dLive scene **"NO WAVES"** (disables Waves inserts, activates DEEP processing)
3. Adjust mix as needed with DEEP processing
4. After show: diagnose SoundGrid server

### F-08-4: ME-U Hub Failure

| | |
|---|---|
| **Symptom** | All ME-500 units lose audio — pit musicians can't hear monitors |
| **Detection** | Pit musicians signal loss of audio |
| **Audience impact** | None (pit plays acoustically) |
| **Response** | Band plays by ear; A2 attempts to reconnect ME-U |

**Procedure:**
1. FOH and stage IEMs unaffected
2. Pit band plays acoustically (they can still hear the house and each other)
3. If spare ME-U available: swap during intermission
4. If no spare: band continues without personal monitors for remainder

---

## Verification Checklist (Pre-Show)

### Dante Network
- [ ] All devices visible in Dante Controller (DM48, SQ-5, DS10, DT168, ME-U, Sennheiser ×32)
- [ ] PTP clock stable — DM48 as Grandmaster, no errors for 5+ minutes
- [ ] RSTP status: all switches show "forwarding" on active links, one link properly "blocking"
- [ ] Primary AND Secondary Dante paths verified for all dual-port devices

### FOH (dLive)
- [ ] All 48 input channels receiving signal
- [ ] Waves SoundGrid server online and processing
- [ ] "NO WAVES" backup scene saved and tested
- [ ] 8 FOH zone outputs reaching DS10 → D20 amps
- [ ] TheatreMix connected and tracking

### SQ-5 Monitoring
- [ ] All 48 input channels receiving signal (verify via SQ meters)
- [ ] IEM mixes 1–4 outputting to transmitters — performers confirm audio
- [ ] Vocal stem (Mix 5) reaching ME-U — pit musicians confirm
- [ ] Pit direct outs (14 channels) reaching ME-U — pit musicians confirm individual channel control
- [ ] Backstage wedge (Mix 6) outputting
- [ ] Green room feed (Mix 7) outputting
- [ ] Backup FOH zone outputs configured (LR + Matrix)
- [ ] TheatreMix connected and tracking SQ in parallel

### Failover Readiness
- [ ] Dante Controller preset **"SQ BACKUP FOH"** saved and verified on A2 laptop
- [ ] Test failover: temporarily load backup preset, verify SQ audio reaches D20 amps, then restore
- [ ] A2 verbally confirms failover procedure knowledge
- [ ] iPad MixPad app connected to DM48 (surface failure backup)

### RSTP Ring
- [ ] All 3 trunk links between switches are UP
- [ ] RSTP root bridge is Switch A (verify with `show spanning-tree`)
- [ ] Test: disconnect one trunk link → verify RSTP reconverges within 1 second → reconnect
- [ ] Verify no unexpected STP topology changes (TCN — Topology Change Notification)
