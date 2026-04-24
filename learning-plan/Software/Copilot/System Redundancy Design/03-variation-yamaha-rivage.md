# 03 — Variation A: Yamaha RIVAGE PM5 System Architecture

## Overview

This variation replaces the Allen & Heath dLive + SQ-5 with a **Yamaha RIVAGE PM5** system. The RIVAGE PM platform offers the **only native automatic DSP failover** available in any commercial mixing console — DSP Mirroring — which eliminates the core problem of the A&H architecture: manual switchover on MixRack failure.

For comparison with other architectures, see [06-comparison-matrix.md](06-comparison-matrix.md).

---

## Why RIVAGE PM5 Solves the Core Problems

| A&H Problem | RIVAGE PM5 Solution |
|---|---|
| No automatic DSP failover | **DSP Mirroring**: Two DSP-RX engines — if primary fails, secondary takes over automatically with zero audio interruption |
| Show file incompatibility between primary & backup | **Console File Converter**: Share show files between RIVAGE PM10/PM7/PM5/PM3 AND CL/QL series |
| No native OSC control | **Native OSC server AND client** (V7.0+): Bidirectional OSC built into the console |
| No single-button automation | **Genius.lab**: Macro engine chains any console action into single-button/MIDI/OSC triggers |
| No theatre-specific features | **Theatre Mode**: Four banks per performer for EQ/dynamics — designed for cast swaps in musicals |
| No noise suppression | **DaNSe**: AI-based noise suppression, massive advantage for theatrical lavs |
| SQ Dante/Waves slot conflict | RIVAGE PM has multiple HY card slots — Dante AND Waves simultaneously, no compromise |

---

## Equipment List

| Role | Equipment | Qty | Location |
|---|---|---|---|
| Control surface | Yamaha CS-R5 | 1 | FOH |
| Primary DSP engine | Yamaha DSP-RX (Engine A) | 1 | FOH rack |
| Mirror DSP engine | Yamaha DSP-RX (Engine B — MIRROR) | 1 | FOH rack |
| Dante I/O card | Yamaha HY144-D (144ch Dante) | 1–2 | DSP-RX HY slots |
| Pit I/O rack | Yamaha Rio1608-D2 (16 in / 8 out, Dante) | 1 | Pit |
| FOH I/O rack | Yamaha Rio3224-D2 (32 in / 24 out, Dante) | 1 | FOH rack |
| Wireless microphones | Sennheiser Dante-enabled × 32 | 32 | FOH rack |
| Playback A | Mac + QLab + Dante Virtual Soundcard | 1 | FOH |
| Playback B | Mac + QLab + Dante Virtual Soundcard | 1 | FOH |
| Amp bridge | d&b DS10 (16ch Dante→AES3) | 1 | Amp rack |
| Amplifiers | d&b D20 (4ch each) | 2 | Amp rack |
| Network switches | Managed Gigabit × 2 | 2 | FOH + Amp rack |

---

## DSP Mirroring — How It Works

DSP Mirroring is RIVAGE PM's headline redundancy feature. It requires **two DSP-RX engines**.

### Architecture

```
CS-R5 Surface ──TWINLANe──► DSP-RX Engine A (PRIMARY)
                    │               │
                    │        [All processing, routing,
                    │         I/O happens here]
                    │               │
                    └──────► DSP-RX Engine B (MIRROR)
                             [Exact clone of Engine A —
                              same processing state,
                              same I/O routing, same
                              audio data, continuously
                              synchronized]
```

### Failover Behavior

| Event | What Happens | Audio Impact | Operator Action |
|---|---|---|---|
| Engine A fails | Engine B takes over automatically | **Zero dropout** — seamless | None (automatic) |
| Engine A recovers | Engine A can be re-synced while B runs | None | Optional restore via console |
| CS-R5 surface fails | Both DSP-RX engines keep processing | Audio continues | Use RIVAGE PM Editor or StageMix iPad |
| Both engines fail | Audio stops | Total loss | Cold restart required |

### Key Points

- DSP Mirroring is **always-on** — not snapshot-based, not cue-triggered
- Both engines process the **exact same audio simultaneously**
- The switchover is at the hardware level — no Dante subscription changes needed
- This is fundamentally different from having a backup console — the mirror engine IS the same console

---

## Network Architecture

### Dante I/O Layer

The RIVAGE PM5 supports Dante via **HY144-D** cards installed in the DSP-RX engines. Each HY144-D provides 144 channels (72 in / 72 out at 48kHz, or 36 in / 36 out at 96kHz).

```
                    ┌──────────────────────────┐
                    │     Dante Network         │
                    │   Primary (VLAN 20)       │
                    │   Secondary (VLAN 30)     │
                    │   Control (VLAN 40)       │
                    └─────────────┬─────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
    ┌────┴────┐            ┌──────┴──────┐          ┌──────┴──────┐
    │Rio1608  │            │Sennheiser   │          │  QLab A/B   │
    │ D2 (Pit)│            │  ×32 Lavs   │          │  (2× Mac)   │
    │16in/8out│            │ Dante out   │          │  DVS 8+8ch  │
    └────┬────┘            └──────┬──────┘          └──────┬──────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │  DSP-RX Engine A + B      │
                    │  (HY144-D Dante cards)    │
                    │  Subscribes to all 48     │
                    │  input channels + QLab    │
                    │                           │
                    │  Outputs: Zone1..Zone8    │
                    │  via Dante to DS10        │
                    └─────────────┬─────────────┘
                                  │
                           ┌──────┴──────┐
                           │    DS10     │
                           │  Dante→AES3 │
                           └──────┬──────┘
                                  │
                           ┌──────┴──────┐
                           │  D20 × 2   │
                           │  8 zones   │
                           └─────────────┘
```

### TWINLANe Layer (Optional)

For higher channel counts or where fiber is preferred:

- TWINLANe provides up to **400 channels** over fiber optic
- CS-R5 ↔ DSP-RX connection uses TWINLANe (fiber, not Ethernet)
- Rio racks can connect via either Dante (Ethernet) or TWINLANe (fiber)
- In this application, Dante is sufficient (48 inputs + 8 outputs = well within HY144-D capacity)

---

## Input Architecture

### Pit: Rio1608-D2

- 16 mic preamps, 8 line outputs
- Dante Primary → Switch A, Secondary → Switch B
- DSP-RX subscribes to all 16 pit channels
- Preamp gain controlled from CS-R5 surface or RIVAGE PM Editor
- **Advantage over A&H DT168**: Rio racks are natively integrated with RIVAGE PM — preamp gain, phantom power, and pad settings are saved in the console's scene memory and recalled with snapshots

### FOH Wireless: Sennheiser × 32

- Same configuration as A&H architecture
- DSP-RX subscribes to all 32 wireless Dante channels
- **RIVAGE PM advantage**: Native integration with Sennheiser EM 6000 and Shure AD4D/Q receivers — RF status, battery level, and audio meters displayed directly on CS-R5 surface

### Playback: Dual QLab Macs

- Same dual-Mac architecture as A&H
- DSP-RX subscribes to primary Mac; secondary Mac available if primary fails
- **Genius.lab macro** can automate the QLab failover — re-subscribing Dante channels and triggering the backup Mac via OSC

---

## Console Configuration

### Theatre Mode

RIVAGE PM's Theatre Mode provides **four banks per input channel**, each with independent:
- EQ settings
- Dynamics settings
- Insert processing

This is purpose-built for **cast swaps** in musicals — each bank represents a different performer. Scene recalls can switch banks per-channel without affecting other parameters.

Example:
| Channel | Bank A | Bank B | Bank C | Bank D |
|---|---|---|---|---|
| LAV-01 | Lead (Principal A) | Understudy | Swing 1 | — |
| LAV-02 | Lead (Principal B) | Understudy | — | — |
| LAV-03 | Ensemble 1 | Swing 2 | — | — |

### DaNSe Noise Suppression

- AI-based noise suppression available on every input channel
- Reduces ambient noise pickup from theatrical lavs without affecting voice quality
- Particularly effective for reducing:
  - Costume rustle
  - Set noise
  - Air conditioning
  - Pit bleed
- Can be enabled/disabled per channel per scene

### Snapshots & Scene Memory

- Full snapshot system with channel safes, crossfade timing, and recall filters
- Scene memories store all console parameters including Rio preamp settings
- Auto-increment available for sequential cue advancement
- Compatible with TheatreMix for external cue control (via OSC)

---

## Genius.lab Automation

### What Genius.lab Can Do

Genius.lab (available in firmware V7.0+) is a macro engine that chains console actions:

| Trigger Types | Action Types |
|---|---|
| Physical User Defined button on surface | Scene/snapshot recall |
| MIDI CC/Note/Program Change | Channel mute/unmute |
| OSC message (console is OSC server) | DCA level change |
| GPI (contact closure) | OSC send to external device |
| Timer/scheduled | MIDI send to external device |
| | Custom routing change |
| | Display message on surface |

### Example Macros for This Production

**Macro 1: "FAILOVER TO BACKUP PLAYBACK"**
```
Trigger: OSC /genius/playback-failover (from QLab or monitoring script)
Actions:
  1. Re-route Dante QLab subscriptions from Mac A to Mac B channels
  2. Send OSC /qlab/go to Mac B to start cue tracking
  3. Flash surface button "PLAYBACK-B ACTIVE"
```

**Macro 2: "EMERGENCY DS10 SWITCH"**
```
Trigger: User Defined Button 12 on CS-R5 (physical button)
Actions:
  1. Send OSC /dante/switch-to-backup to Python conmon script
  2. Send OSC /status/failover-active to monitoring display
  3. Recall Scene "EMERGENCY OUTPUT ROUTING" (internal backup routing)
  4. Flash surface LED red
```

**Macro 3: "CAST SWAP — UNDERSTUDY ON"**
```
Trigger: User Defined Button 5 on CS-R5
Actions:
  1. Switch LAV-01 from Bank A to Bank B (understudy EQ/dynamics)
  2. Update DCA name display
  3. Send OSC notification to stage manager display
```

### Native OSC Capabilities (V7.0+)

The RIVAGE PM can act as both **OSC server** (receives commands) and **OSC client** (sends commands):

| Direction | Capability |
|---|---|
| **Receive** (server) | Accept fader moves, scene recalls, channel mutes, macro triggers from external OSC sources (QLab, TouchOSC, custom apps) |
| **Send** (client) | Transmit console state changes to external systems — fader positions, scene changes, metering data, macro completion confirmations |

This bidirectional OSC makes the RIVAGE PM uniquely capable of being **both controlled by and controlling** external automation systems.

---

## Output Architecture

The output path to d&b D20 amplifiers is **identical** to the A&H architecture:

- DSP-RX outputs 8 zone channels via Dante
- DS10 receives 8 Dante channels, converts to AES3
- AES3 → D20 amplifiers
- R1 controls D20 configuration via OCA/AES70

The **only difference**: with DSP Mirroring, the DSP-RX outputs never fail over because the mirror engine takes over automatically. The DS10→D20 path is always receiving valid audio.

The DS10 Dante subscription switching automation (Approaches 1, 2, or 5 from [02-automation-approaches.md](02-automation-approaches.md)) is still relevant if you want to switch to an **entirely different console** as a tertiary backup. But with DSP Mirroring, this is a much lower priority.

---

## Backup Console Options

With DSP Mirroring handling the primary failover, a backup console is less critical. However, for catastrophic scenarios (both DSP-RX engines fail, or CS-R5 + both engines):

### Option 1: Yamaha CL5 or QL5 as Tertiary Backup

- **Console File Converter** can convert RIVAGE PM show data to CL/QL format
- CL5 or QL5 can load the converted show and mix from it
- Not identical processing, but functional — the show structure (routing, DCAs, snapshots) transfers
- This is **impossible** with the A&H dLive→SQ path
- CL/QL consoles are widely available in rental inventory

### Option 2: RIVAGE PM3 as Hot Spare

- PM3 uses the same DSP-RX engines
- Show file is directly compatible — load and go
- Smaller surface (CS-R3 = fewer faders) but identical processing

### Option 3: No Dedicated Backup Console

- With DSP Mirroring, the probability of needing a separate backup console is extremely low
- Use **RIVAGE PM Editor** on a laptop or **StageMix** on an iPad for surface failure scenarios
- This eliminates the cost of a backup console entirely

---

## Cost Analysis

| Component | RIVAGE PM5 System | A&H dLive + SQ System |
|---|---|---|
| Primary console | CS-R5 + DSP-RX ×2 ($$$$) | dLive S5000 + DM48 ($$) |
| Backup console | None needed (DSP Mirroring) | SQ-5 + SQ Dante card ($) |
| I/O racks | Rio1608-D2 + Rio3224-D2 ($$) | DT168 ($) |
| Dante I/O cards | HY144-D ×1–2 ($) | M-DL-DANT128-A ($) |
| Amp bridge | DS10 ×1 ($) | DS10 ×1 ($) |
| Amplifiers | D20 ×2 (same) | D20 ×2 (same) |
| Programming time | 1× (one console) | 2× (both consoles independently) |
| Custom development | None | Automation scripts (time) |

**Bottom line**: The RIVAGE PM5 hardware is more expensive, but you eliminate the backup console, eliminate dual programming, and eliminate custom automation development. The total system cost may be comparable when factoring in labour for dual programming and script development/maintenance.

---

## Summary of Advantages

1. **Automatic DSP failover** — zero audio interruption, zero operator action
2. **Genius.lab macros** — single-button automation for any console action + external OSC
3. **Theatre Mode** — purpose-built for musical cast management
4. **DaNSe** — AI noise suppression for theatrical lavs
5. **Native OSC** — bidirectional, no external bridges needed
6. **Console File Converter** — show data portable to CL/QL series for backup
7. **Sennheiser integration** — RF status and battery on console surface
8. **No dual programming** — one show file, one programming session
9. **No custom scripting** — all automation via Genius.lab configuration (GUI)
10. **Industry-proven** — RIVAGE PM is used in major musical theatre productions worldwide
