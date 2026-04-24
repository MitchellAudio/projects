# 01 — Primary System Architecture: Allen & Heath dLive S5000 + SQ-5 Backup

## Overview

This document describes the complete baseline system architecture using an Allen & Heath dLive S5000/DM48 as the primary console with an SQ-5 as the backup console, connected via Dante networking to d&b D20 amplifiers through DS10 bridges.

**Key constraint**: dLive and SQ are fundamentally different platforms with no show file compatibility. This architecture requires dual programming and manual switchover (~5–10 seconds). For automated or seamless failover alternatives, see [03-variation-yamaha-rivage.md](03-variation-yamaha-rivage.md), [04-variation-digico-quantum.md](04-variation-digico-quantum.md), or [05-variation-hybrid-automation.md](05-variation-hybrid-automation.md).

---

## Equipment List

| Role | Equipment | Qty | Location |
|---|---|---|---|
| Primary console surface | Allen & Heath dLive S5000 (28 faders) | 1 | FOH |
| Primary MixRack | Allen & Heath DM48 (48 mic in, 24 line out, 3 I/O ports) | 1 | FOH rack |
| Primary Dante card | M-DL-DANT128-A (128×128 Dante) | 1 | DM48 Port A |
| Backup console | Allen & Heath SQ-5 (48ch, 36 bus, 17 faders) | 1 | Backstage A2 position |
| Backup Dante card | SQ Dante 64×64 | 1 | SQ-5 option slot |
| Pit stagebox | Allen & Heath DT168 (16 in / 8 out, Dante) | 1 | Pit |
| Wireless microphones | Sennheiser Dante-enabled receivers × 32 | 32 | FOH rack |
| Playback A | Mac + QLab + Dante Virtual Soundcard | 1 | FOH |
| Playback B | Mac + QLab + Dante Virtual Soundcard (backup) | 1 | FOH |
| Amp bridge (primary) | d&b DS10 (16ch Dante→AES3, integrated 5-port switch) | 1 | Amp rack |
| Amp bridge (backup) | d&b DS10 (16ch Dante→AES3) — Option B only | 1 | Amp rack |
| Amplifiers | d&b D20 (4ch each) | 2 | Amp rack |
| Network switches | Managed Gigabit (e.g., Netgear M4250) | 2 | FOH + Amp rack |
| Show automation | TheatreMix (laptop or FOH Mac) | 1 | FOH |
| Emergency surface control | iPad with dLive MixPad app | 1 | FOH / A2 |

---

## Critical Issues & Honest Assessment

### Issue 1: Cross-Platform Show File Incompatibility (MAJOR)

- dLive and SQ use completely different show file formats
- **No conversion tool exists** — Allen & Heath does not provide one
- Every snapshot, DCA assignment, EQ, compressor setting, routing, and FX must be programmed **independently** on both consoles
- Any change to the dLive show must be manually duplicated on the SQ
- **Impact**: Doubles programming time. Requires rigorous change management discipline.
- **Mitigation**: TheatreMix can send parallel cue recalls to both consoles, keeping them in sync during the show. But the SQ show data itself must be built separately.

### Issue 2: No Automatic Seamless Failover (HONEST CONSTRAINT)

- dLive-to-SQ switchover **cannot be automatic or seamless** — these are fundamentally different platforms
- dLive supports native dual-MixRack failover (truly seamless), but a second DM48 isn't available
- Dante protocol supports network-path redundancy (Primary/Secondary), NOT source-level automatic failover
- **What IS automatic**: If a Dante network cable fails, the secondary path takes over seamlessly. This covers network/stagebox failures.
- **What is NOT automatic**: If the DM48 MixRack crashes, switching from dLive outputs to SQ outputs on the DS10 requires manual action.
- **Best achievable**: ~5–10 second switchover with trained A2 using pre-configured Dante Controller presets

### Issue 3: SQ-5 Channel & Bus Limitations

- SQ-5: 48 input channels — sufficient for 32 wireless + 16 pit but **no headroom**
- SQ-5: 12 stereo mixes + LR + 3 stereo matrix = enough for 8 zones, but tight
- SQ-5: 17 faders — managing 48 channels in an emergency requires well-organized fader layers
- SQ-5: DEEP processing available but more limited library than dLive
- **Impact**: Backup mix will be functional but may lack some processing finesse of the dLive
- **Consideration**: If an SQ-6 (25 faders) or SQ-7 (33 faders) were available, the emergency mixing experience would be significantly better

### Issue 4: Waves SoundGrid Creates Asymmetry (RECOMMEND AGAINST)

- dLive supports Waves SoundGrid via dedicated option card (uses second DM48 I/O port)
- SQ supports Waves via SQ Waves card, BUT:
  - SQ only has **ONE option card slot** — must choose Dante OR Waves, not both
  - If you use Waves on dLive, the SQ backup will NOT have Waves processing
  - This creates audible differences between primary and backup mixes
- **Recommendation**: Use dLive's onboard DEEP processing only (no Waves). This keeps primary and backup mixing platforms symmetrical and eliminates an external failure point.

### Issue 5: d&b D20 Input Interfacing

- D20 has 4× analog inputs (XLR) and 2× AES3 inputs (2 pairs = 4 channels)
- D20 has **NO Dante built-in** — requires DS10 bridge for Dante→AES3 conversion
- D20 input mode (analog vs AES3) is set per-channel in R1 software — not automatically failover-capable
- **Solution**: Use DS10 bridge(s) — see Output Architecture section below

### Issue 6: Sennheiser Wireless Dante Specifics

- Verify exact Sennheiser model for Dante output capabilities (EW-DX with DN2 Dante module, or Digital 6000)
- Most Sennheiser Dante-enabled receivers have dual Dante ports (Primary/Secondary) — good for network redundancy
- Dante multicast allows both consoles to subscribe to the same wireless channels simultaneously — no splitter needed

---

## Phase 1: Network Infrastructure

### Step 1 — Managed Switch Configuration

Configure 2× managed Gigabit switches (e.g., Netgear M4250):

| Switch | Role | VLANs | Location |
|---|---|---|---|
| Switch A | Primary Dante + Control | VLAN 20 (Dante Primary) + VLAN 40 (Control/OSC/MIDI) | FOH rack |
| Switch B | Secondary Dante | VLAN 30 (Dante Secondary) | FOH rack or amp rack |

Configuration requirements:
- IGMP snooping: **enabled** on both switches
- QoS: DSCP EF (46) for Dante traffic
- Port speed: 1Gbps minimum for all Dante ports
- Trunk link: Fiber or Cat6a between FOH and amp rack — **redundant run** (one per switch)
- All Dante devices connect to **BOTH** switches via dual Dante ports

### Step 2 — PTP Clock Hierarchy

| Priority | Device | Rationale |
|---|---|---|
| 1 (Grandmaster) | DM48 MixRack | Highest quality clock in system |
| 2 (Fallback) | DT168 stagebox | Second-best clock reference |
| 3 (Fallback) | Sennheiser receivers | Last resort |

- Verify PTP domain settings match across all Dante devices
- Monitor clock stability in Dante Controller for 30+ minutes before show

---

## Phase 2: Input Architecture

### Step 3 — Pit Stagebox: A&H DT168

- Position in pit: 16 mic preamps for band/orchestra
- Connect Dante Primary port → Switch A, Dante Secondary port → Switch B
- Both dLive and SQ-5 subscribe to DT168's Dante transmit channels
- dLive controls DT168 preamp gains by default
- SQ configured with matching gain structure (manually set or via Dante gain sharing if supported)
- **Important**: If dLive MixRack fails, preamp gain settings on DT168 persist — SQ receives the same levels

### Step 4 — FOH Wireless Receivers: Sennheiser × 32

*Can be configured in parallel with Step 3*

- Mount 32 Sennheiser receivers in FOH rack
- Connect each receiver: Dante Primary → Switch A, Dante Secondary → Switch B
- Both dLive and SQ-5 subscribe to the same 32 Dante wireless channels
- Dante channel labeling: `LAV-01` through `LAV-32`
- Verify dual-port Dante redundancy on selected Sennheiser model

### Step 5 — Playback: Dual QLab Macs

*Depends on Step 1 (network ready)*

| Mac | Role | Dante Channel Names |
|---|---|---|
| Mac A | Primary playback | `QLAB-A-01` through `QLAB-A-08` |
| Mac B | Backup playback | `QLAB-B-01` through `QLAB-B-08` |

- Both Macs run identical QLab workspace
- Both advance cues via MSC (MIDI Show Control) or manual operator trigger
- dLive subscribes to Mac A playback channels
- SQ subscribes to **both** Mac A (primary) and Mac B (emergency)
- On Mac A failure: dLive re-subscribes to Mac B channels in Dante Controller; SQ already has Mac B

### Step 6 — Talkback

- Talkback mic at FOH → DM48 local input (or DT168 spare channel)
- SQ has its own local talkback via built-in mic inputs
- Configure both talkback paths independently

---

## Phase 3: Console Configuration

### Step 7 — dLive S5000 + DM48 Configuration (PRIMARY)

1. Install **M-DL-DANT128-A** (128×128 Dante option card) in DM48 Port A
2. Configure DM48 Dante inputs: subscribe to all 48 input sources
   - Channels 1–32: Sennheiser wireless (`LAV-01` through `LAV-32`)
   - Channels 33–48: DT168 pit (`PIT-01` through `PIT-16`)
3. Configure 8 output zones via Dante: `dLive-Zone1` through `dLive-Zone8`
4. Program full show:
   - All snapshots with appropriate channel safes and crossfade timing
   - DCAs (typically 8–12): Principals, Ensemble, Band, Playback, etc.
   - FX returns (reverbs, delays) using DEEP processing only
   - DEEP compression and EQ on all channels
5. Configure TheatreMix connection for DCA automation and cue tracking
6. Surface link: S5000 ↔ DM48 via **gigaACE** (dedicated Cat5e, NOT through Dante switches)
7. Save backup scene to USB regularly

### Step 8 — SQ-5 Configuration (BACKUP)

*Parallel with Step 7 — same programmer should do both*

1. Install **SQ Dante 64×64 card** in SQ's single option card slot
2. Configure SQ Dante inputs: subscribe to same 48 input sources as dLive
   - Same channel order: LAV-01..32, PIT-01..16
3. Configure 8 output zones via Dante: `SQ-Zone1` through `SQ-Zone8`
4. Program **matching** show independently:
   - Same cue numbers as dLive (critical for TheatreMix sync)
   - Same DCA assignments
   - Simplified but functional EQ/compression (match critical settings)
   - Same routing structure
5. Configure TheatreMix connection — SQ receives parallel cue commands
6. Rack-mount SQ-5 at backstage A2 position
7. A2 monitors SQ mix via headphones **at all times** (verifying backup is tracking correctly)

**Fader Layer Organization for SQ-5 (17 faders):**

| Layer | Faders 1–16 | Fader 17 |
|---|---|---|
| Layer 1 | LAV-01 through LAV-16 | DCA Master |
| Layer 2 | LAV-17 through LAV-32 | DCA Master |
| Layer 3 | PIT-01 through PIT-16 | DCA Master |
| Layer 4 | DCAs 1–8, FX Returns | Main LR |
| Layer 5 | Zone Outputs 1–8 | Main LR |

### Step 9 — TheatreMix Configuration

*Depends on Steps 7 & 8*

- TheatreMix controls **BOTH** consoles simultaneously
- Each QLab cue triggers TheatreMix → sends DCA/snapshot recall to both dLive and SQ
- Both consoles advance through the show in lockstep
- If dLive fails, SQ is already on the correct cue with correct DCA positions
- Verify TheatreMix can address both console types on the same network simultaneously
- TheatreMix connects via the Control VLAN (VLAN 40)

---

## Phase 4: Output Architecture & Failover Path

### Step 10 — Amp Rack: d&b DS10 Bridges + D20 Configuration

This is the **critical path** for failover design. Two options:

#### Option A: Single DS10, Dante Subscription Switching (RECOMMENDED)

```
dLive DM48 ──Dante──► DS10 ──AES3──► D20 ×2 ──► Speakers
                         ▲
SQ-5 ──Dante──► (standby subscription, activated on failover)
```

- 1× DS10 in amp rack
- DS10 subscribed to dLive output channels (`dLive-Zone1` through `dLive-Zone8`)
- DS10 Dante Primary → Switch A, Secondary → Switch B
- DS10 AES3 outputs → D20 digital inputs (AES3)
- D20s configured for **AES3 input mode** in R1

**Failover**: A2 opens Dante Controller, loads pre-saved "SQ Backup" preset that re-subscribes DS10 inputs from `dLive-Zone1..8` to `SQ-Zone1..8`

| Metric | Value |
|---|---|
| Switchover time | ~5–10 seconds |
| Operator required | A2 (backstage) |
| Hardware cost | 1× DS10 |
| Wiring complexity | Minimal |
| Failure coverage | DM48 failure, dLive Dante card failure |

#### Option B: Dual DS10, Dual D20 Input Paths (MAXIMUM REDUNDANCY)

```
dLive DM48 ──Dante──► DS10 "A" ──AES3──► D20 AES3 inputs (primary)
SQ-5 ──Dante──► DS10 "B" ──AES3──► [AES3-to-Analog converter] ──► D20 Analog inputs (backup)
```

- DS10 "A": Subscribed to dLive outputs → AES3 → D20 digital inputs (D1/2, D3/4)
- DS10 "B": Subscribed to SQ outputs → AES3 → external AES3-to-analog converter → D20 analog inputs (A1–A4)
- D20 configured for AES3 input mode (primary)

**Failover**: A2 switches D20 input mode from AES3 to Analog in R1 software

| Metric | Value |
|---|---|
| Switchover time | ~10–20 seconds |
| Operator required | A2 (backstage) |
| Hardware cost | 2× DS10 + AES3-to-analog converters |
| Wiring complexity | High |
| Failure coverage | DM48 failure, DS10 failure, dLive Dante card failure |

**Advantage**: Both signal paths are always live and verifiable independently.

**Disadvantage**: More hardware, more complex wiring, slower switchover (R1 interaction).

> **RECOMMENDATION: Option A** — fewer components, faster switchover, easier to train A2.

### Step 11 — D20 Amplifier Configuration

*Depends on Step 10*

- 2× D20 amps (4 channels each = 8 output zones)
- Configure in R1 with correct d&b loudspeaker setups per channel
- Set delay, EQ, LoadMatch per channel
- Input mode: **AES3** (for DS10 connection)
- R1 laptop connected via OCA/AES70 Ethernet for monitoring and emergency input switching
- Verify DS10 passes channel labels through to D20s for easy identification

**D20 Channel Mapping:**

| D20 | Channel | AES3 Input Pair | Zone |
|---|---|---|---|
| D20 #1 | Ch 1 | D1 (pair 1, ch 1) | Zone 1 |
| D20 #1 | Ch 2 | D1 (pair 1, ch 2) | Zone 2 |
| D20 #1 | Ch 3 | D2 (pair 2, ch 1) | Zone 3 |
| D20 #1 | Ch 4 | D2 (pair 2, ch 2) | Zone 4 |
| D20 #2 | Ch 1 | D1 (pair 1, ch 1) | Zone 5 |
| D20 #2 | Ch 2 | D1 (pair 1, ch 2) | Zone 6 |
| D20 #2 | Ch 3 | D2 (pair 2, ch 1) | Zone 7 |
| D20 #2 | Ch 4 | D2 (pair 2, ch 2) | Zone 8 |

---

## Phase 5: Waves vs No-Waves Decision

### Option: No Waves (RECOMMENDED)

- Use dLive DEEP processing only (onboard)
- Both dLive and SQ support DEEP processing libraries
- Primary and backup sound similar
- No external failure points
- No additional hardware or licensing

### Option: Waves SoundGrid on dLive Only

- Install M-DL-WAVES option card in DM48 (uses a second I/O port slot)
- SoundGrid server + backup SoundGrid server in FOH rack
- dLive has Waves processing; SQ does **NOT** (SQ's single slot is used for Dante)
- Backup mix will sound noticeably different (no Waves reverbs, compressors, etc.)
- Adds 3 additional failure points (2 servers + option card)

> **Not recommended for a redundancy-focused system.**

---

## Phase 6: Verification Procedures

1. **Dante network test**: Verify all 48 inputs visible on both consoles simultaneously. Check PTP sync stability in Dante Controller — no clock errors for 30+ minutes.
2. **Redundant network path test**: Unplug Primary switch uplink → verify Dante Secondary takes over with no audio dropout.
3. **Surface failure test**: Power off S5000 during playback → verify DM48 continues audio. Verify iPad MixPad takes control within 30 seconds.
4. **Full failover test**: Power off DM48 during playback → A2 executes Dante Controller preset switch → verify SQ audio reaches amps within target time. Record actual switchover time.
5. **QLab failover test**: Kill Mac A process → trigger Mac B → verify playback resumes on correct cue.
6. **DS10 bypass test** (if Option B): Verify both signal paths (AES3 and analog) reach D20 outputs correctly. Test R1 input mode switching.
7. **End-to-end level verification**: Confirm gain staging from wireless → Dante → console → Dante → DS10 → AES3 → D20 → speaker is consistent between primary and backup paths. Use SMAART transfer function or dB SPL meter.
8. **TheatreMix sync test**: Run through 10+ sequential cues. Verify both consoles advance to correct snapshots. Intentionally delay one console and verify recovery.
9. **Power failure test**: Kill FOH power → verify amp rack (on separate circuit) stays live. Verify system recovery procedure from cold boot.

---

## Signal Flow Summary

```
                          ┌─────────────────────┐
                          │   Dante Network      │
                          │  Primary (VLAN 20)   │
                          │  Secondary (VLAN 30) │
                          │  Control (VLAN 40)   │
                          └──────────┬───────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
    ┌────┴────┐                ┌─────┴─────┐              ┌─────┴─────┐
    │  DT168  │                │ Sennheiser │              │  QLab A/B │
    │  (Pit)  │                │  ×32 Lavs  │              │  (2× Mac) │
    │ 16 in   │                │  32 Dante  │              │  8+8 ch   │
    └────┬────┘                └─────┬──────┘              └─────┬─────┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     │
                          ┌──────────┴──────────┐
                          │   Dante Switches    │
                          │  (Primary + Sec)    │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
              │  DM48     │   │   SQ-5    │   │  DS10     │
              │  (dLive)  │   │  (Backup) │   │  (Bridge) │
              │ 128×128   │   │  64×64    │   │ 16→AES3   │
              │ Dante     │   │  Dante    │   │           │
              └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
                    │               │                │
              ┌─────┴─────┐   (standby)         ┌────┴────┐
              │  S5000    │                     │  AES3   │
              │  Surface  │                     │         │
              │ (gigaACE) │                     ├────┬────┤
              └───────────┘                     │ D20 #1  │
                                                │ D20 #2  │
                                                │ 8 zones │
                                                └─────────┘
```

---

## Decisions & Scope

- **Included**: Console redundancy, network redundancy, playback redundancy, amp interfacing, failover procedures, gain staging
- **Excluded**: Speaker system design (assumes existing d&b rig), acoustic optimization/SMAART tuning, wireless frequency coordination, comms/intercom
- **Assumption**: Sennheiser wireless receivers have Dante output (exact model to be verified)
- **Assumption**: Venue has adequate power circuits for separate FOH and amp rack feeds
- **Decision**: Waves SoundGrid NOT recommended — use DEEP processing for symmetry
- **Decision**: Recommend Option A (single DS10, Dante switching) over Option B (dual DS10)
- **Cross-platform limitation accepted**: ~5–10 second switchover is the best achievable without a second dLive MixRack

---

## Further Considerations

1. **Pit stagebox redundancy**: The DT168 at pit is currently a single point of failure. Adding a second DT168 with analog mic splits would protect band inputs, but adds cost and complexity. If band is critical, consider this addition.
2. **SQ-5 vs SQ-6/SQ-7**: Given 48 channels across only 17 faders, the A2 will need expertly organized layers. An SQ-6 (25 faders) or SQ-7 (33 faders) would make the emergency mixing experience significantly better.
3. **Dante Domain Manager (DDM)**: DDM provides centralized monitoring, alerting, and audit logging for the entire Dante network. While it won't automatically switch subscriptions by itself, it CAN alert the A2 to device failures instantly and has a preset system that can be triggered via its API.
