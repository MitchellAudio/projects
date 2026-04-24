# 02 — Automation Approaches for Dante Switchover & Amplifier Control

## Overview

The [primary A&H architecture](01-system-architecture-primary.md) requires manual operator intervention to switch from dLive to SQ-5 outputs — a ~5–10 second process using Dante Controller presets. This document explores five approaches to automating that switchover, ranging from simple scripted solutions to full commercial macro engines.

Each approach targets the same goal: **reduce or eliminate the operator intervention required when the DM48 MixRack fails**, by automatically re-subscribing the DS10 bridge's Dante inputs from dLive output channels to SQ output channels.

---

## Approach 1: QLab OSC → Python Script → Audinate conmon API

### How It Works

Audinate provides `conmon` (Connection Monitor), an SDK and undocumented CLI tool (`dante-conmon`) that can programmatically control Dante routing subscriptions. A Python or Node.js wrapper script listens for an OSC trigger from QLab and executes the subscription change.

### Signal Chain

```
QLab "FAILOVER" cue (Network OSC)
    │
    ▼
Python listener (python-osc library)
    │
    ▼
dante-conmon CLI / conmon SDK
    │
    ▼
DS10 Dante subscriptions change:
  dLive-Zone1..8  →  SQ-Zone1..8
```

### Implementation Details

1. **QLab cue**: Network OSC cue sending `/failover/execute` to Python script IP on port 9000
2. **Python script** (`failover_controller.py`):
   - Uses `python-osc` to listen on port 9000
   - On `/failover/execute` message: calls `dante-conmon` CLI to re-subscribe DS10 channels
   - Sends confirmation OSC back to QLab: `/failover/status "ACTIVE"`
3. **dante-conmon commands** (example):
   ```
   dante-conmon --device DS10 --rx-channel 1 --tx-device SQ5 --tx-channel SQ-Zone1
   dante-conmon --device DS10 --rx-channel 2 --tx-device SQ5 --tx-channel SQ-Zone2
   ... (repeat for all 8 zones)
   ```
4. **Restore command**: `/failover/restore` → re-subscribes back to dLive channels

### Requirements

- Audinate SDK license (contact Audinate for production use)
- Python 3.x with `python-osc` package
- `dante-conmon` binary (available in Audinate SDK, or extracted from Dante Controller installation)
- Dedicated machine on Dante network (Mac Mini, Raspberry Pi 4/5, or FOH Mac)

### Pros & Cons

| Pros | Cons |
|---|---|
| True single-button/single-cue automation | conmon is not officially supported for production automation |
| Fast execution (~1–2 seconds) | Audinate may change API without notice |
| No additional commercial licenses required | Requires development and testing time |
| QLab operator can trigger from FOH | Script maintenance burden |

### Estimated Switchover Time: ~2–3 seconds

---

## Approach 2: QLab OSC → Dante Domain Manager (DDM) REST API

### How It Works

Dante Domain Manager (DDM) is Audinate's official centralized management platform. It has a preset system for routing configurations and a REST API for programmatic control. A scripted QLab cue triggers a web API call to DDM to load a "BACKUP" routing preset.

### Signal Chain

```
QLab "FAILOVER" cue (Script cue or Network cue)
    │
    ▼
HTTP request to DDM REST API
    │
    ▼
DDM loads "BACKUP" routing preset
    │
    ▼
DS10 Dante subscriptions change:
  dLive-Zone1..8  →  SQ-Zone1..8
```

### Implementation Details

1. **DDM preset configuration** (done once during setup):
   - Preset "PRIMARY": DS10 subscribed to `dLive-Zone1..8`
   - Preset "BACKUP": DS10 subscribed to `SQ-Zone1..8`
2. **QLab Script cue** (AppleScript/shell):
   ```
   curl -X POST http://ddm-server:8888/api/presets/BACKUP/apply \
     -H "Authorization: Bearer <token>"
   ```
3. **QLab can also be triggered by DDM alerts**: DDM monitors device health and can fire webhooks when a device goes offline. This webhook could trigger QLab's backup cue automatically.

### Requirements

- DDM license (Audinate commercial product — subscription model)
- DDM server running on a dedicated machine
- Network connectivity between DDM, QLab, and all Dante devices
- DDM API documentation (available to licensees)

### Pros & Cons

| Pros | Cons |
|---|---|
| Officially supported by Audinate | DDM license cost (ongoing subscription) |
| Stable, maintained API | Requires dedicated server |
| Centralized monitoring + audit trail | Additional complexity in network |
| Can alert operators proactively | Depends on DDM server being online |
| Preset system is GUI-configurable | |

### Estimated Switchover Time: ~3–5 seconds

---

## Approach 3: OCA/AES70 Direct Control of d&b D20 Input Sources

### How It Works

d&b R1 communicates with D20 amplifiers via OCA/AES70 (Open Control Architecture / AES70) over Ethernet. OCA is a standardized protocol — its messages can be constructed and sent programmatically, bypassing R1's GUI entirely. A script sends OCA commands directly to D20 amps to switch their input source from AES3 to Analog (or vice versa).

This approach is relevant only for **Option B** (dual DS10 architecture) where the D20s have both AES3 and analog inputs connected.

### Signal Chain

```
QLab "FAILOVER" cue (Network OSC)
    │
    ▼
Python OCA controller
    │
    ▼
OCA/AES70 command to D20 #1: Switch Ch1-4 from AES3 → Analog
OCA/AES70 command to D20 #2: Switch Ch1-4 from AES3 → Analog
    │
    ▼
D20s now receive SQ audio via DS10 "B" → analog path
```

### Implementation Details

1. **OCA protocol**: Defined in AES70 standard. Uses TCP or UDP transport.
2. **D20 OCA object tree**: Each D20 exposes objects for:
   - Input source selection per channel (OCA property)
   - Signal presence monitoring
   - Amplifier status (clip, protect, temperature)
3. **Python implementation** using `aes70` Python library or raw OCA messages:
   ```python
   # Pseudocode — actual OCA object IDs from d&b documentation
   d20_1 = OCAConnection("192.168.40.101")  # D20 #1 IP on control network
   d20_1.set_property(input_source_ch1, "analog")
   d20_1.set_property(input_source_ch2, "analog")
   d20_1.set_property(input_source_ch3, "analog")
   d20_1.set_property(input_source_ch4, "analog")
   ```
4. **R1 compatibility**: These OCA commands are the same messages R1 sends. Both the script and R1 can be connected simultaneously — R1 will reflect the changes.

### Requirements

- d&b OCA documentation (may need to request from d&b technical support)
- Python 3.x with OCA/AES70 library
- D20 amps on Control VLAN (VLAN 40) or dedicated OCA network
- Dual DS10 architecture (Option B) with both AES3 and analog paths connected

### Pros & Cons

| Pros | Cons |
|---|---|
| Works even if R1 software crashes | Only applicable to dual DS10 (Option B) |
| Standard protocol (AES70) | OCA object IDs may need reverse-engineering |
| Lower level than GUI — more reliable | Slower switchover than Dante subscription change |
| d&b amps widely support OCA | D20 input switching may cause brief audio interruption |

### Estimated Switchover Time: ~3–5 seconds (D20 input source switch is not instantaneous)

---

## Approach 4: Yamaha RIVAGE PM Genius.lab Macros

### How It Works

This approach requires switching to a **Yamaha RIVAGE PM** console (see [03-variation-yamaha-rivage.md](03-variation-yamaha-rivage.md)). RIVAGE PM V7.0+ includes **Genius.lab**, a macro engine that chains multiple console actions into a single-button trigger. Combined with native OSC server/client support, this is the most integrated automation solution available in a commercial mixing console.

### What Genius.lab Can Do

A single Genius.lab macro can:
- Recall a scene/snapshot
- Change routing (internal to console)
- Mute/unmute channels or buses
- Send OSC messages to external devices
- Receive trigger from physical button, MIDI, or OSC

### Example Macro: "EMERGENCY FAILOVER"

```
Trigger: User Button 1 on CS-R5 surface (or MIDI CC, or OSC /genius/failover)
    │
    ├── Action 1: Recall Scene "EMERGENCY" (routes backup inputs to outputs)
    ├── Action 2: Send OSC /failover/dante-switch to Python script
    │             (re-subscribes DS10 from primary to backup Dante channels)
    ├── Action 3: Send OSC /failover/log to monitoring dashboard
    └── Action 4: Flash Surface button LED red (visual confirmation)
```

### Why This Is Unique

- The RIVAGE PM is the only console where the **console itself** can send OSC commands to external systems as part of a macro
- No external scripting needed for the console-side actions
- The external Dante subscription switch (DS10) can still be automated via the same macro sending an OSC trigger to a Python script
- Combined with **DSP Mirroring** (RIVAGE PM's dual DSP-RX engines), the DSP failover is already automatic — Genius.lab handles everything else

### Requirements

- Yamaha RIVAGE PM5 (or PM3/PM7/PM10) with firmware V7.0+
- Genius.lab license (included with V7.0+ firmware)
- OSC-capable external devices for DS10 switching (same Python script as Approach 1)

### Estimated Switchover Time: Near-instant for DSP failover (automatic); ~2 seconds for external device switching via macro

---

## Approach 5: QLab Master Cue (Orchestrating All Systems)

### How It Works

QLab 5 can fire multiple simultaneous targets from a single cue: Network OSC, MIDI, Script cues, and more. A single "EMERGENCY FAILOVER" cue orchestrates the entire switchover across all systems.

This approach works with **any** console platform — it's console-agnostic.

### QLab Cue Structure

```
GROUP CUE: "EMERGENCY FAILOVER" (Hot key: F12 or dedicated USB button)
│
├── Network OSC Cue #1: /dante/switch-to-backup
│   Target: Python conmon script @ 192.168.40.50:9000
│   Action: Re-subscribe DS10 from dLive to SQ channels
│
├── Network OSC Cue #2: /r1/input-switch/analog
│   Target: Python OCA script @ 192.168.40.50:9001
│   Action: Switch D20 inputs from AES3 to Analog (Option B only)
│
├── Network OSC Cue #3: /theatremix/console/sq/activate
│   Target: TheatreMix @ 192.168.40.60:7000
│   Action: Confirm SQ is the active console for cue tracking
│
├── Script Cue: Log failover event
│   Action: Write timestamp + event to log file
│
└── Network OSC Cue #4: /status/display "FAILOVER ACTIVE"
│   Target: Monitoring display @ 192.168.40.70:8000
    Action: Update status display for A1 and A2
```

### Implementation Details

1. **Hot key assignment**: Assign the group cue to F12 or a dedicated USB "panic button"
2. **All sub-cues fire simultaneously** (QLab fires OSC cues with no internal delay)
3. **Restore cue**: Create a matching "RESTORE PRIMARY" group cue that reverses all actions
4. **Monitoring**: The status display can be a simple web page served by the monitoring script, shown on a spare monitor at FOH and A2 positions

### Requirements

- QLab 5 (Pro license for Network OSC cues)
- Python scripts for Dante/OCA control (from Approaches 1 & 3)
- Network connectivity between QLab Mac and all targets on VLAN 40

### Pros & Cons

| Pros | Cons |
|---|---|
| Console-agnostic — works with any platform | Multiple scripts to maintain |
| Single button press for complete failover | Depends on QLab Mac being online |
| QLab is familiar territory for theatre operators | Not automatic — requires operator trigger |
| Visual confirmation via status display | |
| Can be tested independently per sub-cue | |

### Estimated Switchover Time: ~2–3 seconds total (all cues fire simultaneously)

---

## Approach Comparison

| Approach | Auto-Detect Failure | Single-Button | Switchover Time | Development Effort | External Dependencies |
|---|---|---|---|---|---|
| 1. conmon API | No (manual trigger) | Yes | ~2–3s | Medium | Audinate SDK |
| 2. DDM REST API | Yes (DDM monitoring) | Yes | ~3–5s | Low | DDM license |
| 3. OCA/AES70 | No (manual trigger) | Yes | ~3–5s | High | d&b OCA docs |
| 4. Genius.lab | N/A (DSP auto) | Yes | ~0–2s | None (config only) | RIVAGE PM console |
| 5. QLab Master | No (manual trigger) | Yes | ~2–3s | Medium | QLab Pro + scripts |

---

## Recommended Combination

For the A&H dLive + SQ architecture specifically, the recommended automation stack is:

1. **Approach 5 (QLab Master Cue)** as the operator interface — single panic button
2. **Approach 1 (conmon API)** as the Dante switching engine underneath
3. **Approach 2 (DDM)** added if budget allows — for health monitoring and alerting

For maximum automation (including auto-detection), add the **Python health monitor** from [05-variation-hybrid-automation.md](05-variation-hybrid-automation.md) which continuously polls DM48 presence and can auto-trigger the failover without operator intervention.

If switching to Yamaha RIVAGE PM: **Approach 4 alone** handles nearly everything natively, with Approach 1 or 5 only needed for the DS10 external subscription change.
