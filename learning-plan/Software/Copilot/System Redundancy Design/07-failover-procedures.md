# 07 — Failover Procedures: Step-by-Step for Every Failure Mode

## Overview

This document provides **step-by-step operator procedures** for every failure mode across all four system architectures. Each procedure is written for the specific operator position (A1 at FOH or A2 backstage) and includes expected timing, verification steps, and what the audience will experience.

Reference the architecture documents for full system context:
- [01-system-architecture-primary.md](01-system-architecture-primary.md) — A&H Baseline
- [03-variation-yamaha-rivage.md](03-variation-yamaha-rivage.md) — RIVAGE PM5
- [04-variation-digico-quantum.md](04-variation-digico-quantum.md) — DiGiCo Q338
- [05-variation-hybrid-automation.md](05-variation-hybrid-automation.md) — A&H + Python Automation

---

## Common Procedures (All Architectures)

These failure modes and responses are identical across all four system variations.

### F-01: Single Dante Network Cable Failure

| | |
|---|---|
| **Symptom** | None — audio continues normally |
| **Detection** | Dante Controller shows device on Secondary only; amber warning |
| **Audience impact** | None |
| **Response** | No immediate action required |

**Procedure:**
1. Note the failure in the show log
2. After the show: trace and replace the faulty cable
3. Verify both Primary and Secondary paths restored in Dante Controller

---

### F-02: Dante Primary Switch Failure

| | |
|---|---|
| **Symptom** | None — Dante Secondary takes over automatically |
| **Detection** | Dante Controller shows all devices on Secondary; Primary switch unreachable |
| **Audience impact** | None |
| **Response** | No immediate action during show |

**Procedure:**
1. Note the failure in the show log
2. **During intermission**: Assess whether to continue on Secondary only or attempt switch replacement
3. After the show: diagnose switch, replace if necessary
4. Verify Dante Primary path restored

---

### F-03: Individual Wireless Receiver Failure

| | |
|---|---|
| **Symptom** | Single performer's mic goes silent |
| **Detection** | A1 sees channel level drop; A2 hears silence on affected channel |
| **Audience impact** | One performer's mic lost |
| **Response** | A2 swaps to backup receiver + body pack |

**Procedure (A2):**
1. Identify the failed receiver (check Dante channel status and RF indicators)
2. Grab spare body pack and receiver from backup kit
3. If time permits (scene change): swap body pack on performer, connect spare receiver
4. If no time: performer continues without mic until next scene change
5. After swap: verify Dante channel from new receiver is active
6. **Estimated time**: 30–60 seconds (during scene change)

---

### F-04: QLab Mac A Failure (Primary Playback)

| | |
|---|---|
| **Symptom** | Playback stops mid-cue or fails to fire next cue |
| **Detection** | A1 sees no playback output; QLab application crash or Mac unresponsive |
| **Audience impact** | Playback content missing until Mac B takes over |
| **Response** | Switch to Mac B |

**Procedure (A1 or A2):**
1. Confirm Mac A is down (check QLab screen / Dante channel meters)
2. On Mac B: navigate to current cue position in QLab
3. Press GO on Mac B to resume playback from correct cue
4. **If using Dante subscription change**: Open Dante Controller on control laptop, re-subscribe console inputs from `QLAB-A-01..08` to `QLAB-B-01..08`
5. **If SQ already subscribes to both**: SQ already has Mac B — no Dante change needed for backup
6. Verify playback audio on console meters
7. **Estimated time**: 10–20 seconds

---

### F-05: DS10 Bridge Failure

| | |
|---|---|
| **Symptom** | All amplified output goes silent (all 8 zones) |
| **Detection** | A1 hears silence in house; D20 amps show no input signal on R1 |
| **Audience impact** | Complete loss of amplified sound |
| **Response** | Depends on architecture option |

**Option A (Single DS10):**
1. This is a critical failure with no immediate workaround
2. If a spare DS10 is available: connect and configure (requires pre-programmed Dante subscriptions)
3. **Estimated recovery**: 5–10 minutes (swap and reconnect)
4. **Mitigation**: Keep a spare DS10 patched in the amp rack with Dante connections ready

**Option B (Dual DS10):**
1. If DS10 "A" (dLive path) fails: switch D20 input mode from AES3 to Analog in R1
2. DS10 "B" (SQ path) is already feeding the analog inputs
3. **Estimated time**: 10–20 seconds (R1 interaction)
4. If DS10 "B" fails: no impact on primary path (dLive still goes through DS10 "A")

---

### F-06: D20 Amplifier Failure (Single Amp)

| | |
|---|---|
| **Symptom** | 4 zones go silent (one D20 = 4 channels) |
| **Detection** | A1 hears zones drop out; R1 shows amp fault (clip/protect/thermal) |
| **Audience impact** | Loss of 4 output zones |
| **Response** | No immediate fix during show |

**Procedure:**
1. Note which zones are affected (D20 #1 = Zones 1–4, D20 #2 = Zones 5–8)
2. Check R1 for fault type (thermal shutdown, clip protect, PSU failure)
3. If thermal: wait 2–3 minutes for cool-down and attempt restart
4. If PSU or hardware: no recovery during show
5. **During intermission**: Swap amp if spare available; re-configure in R1
6. **Mitigation**: Keep a spare D20 racked and patched (AES3 cables connected to a patch panel)

---

### F-07: Power Failure — FOH Position Only

| | |
|---|---|
| **Symptom** | Console, QLab, and control systems go dark at FOH |
| **Detection** | Obvious — everything at FOH loses power |
| **Audience impact** | Audio stops (console down) but amps stay live (separate circuit) |
| **Response** | Restore FOH power; cold-boot all systems |

**Procedure:**
1. **Immediate**: Check if amps are still powered (separate circuit). If yes, the speakers are still live — any signal will play.
2. Alert house crew / electrician to restore FOH power
3. **If A&H architecture with SQ backstage**: SQ may still be powered (if on separate circuit). A2 can potentially re-route SQ output through DS10.
4. Once power restored:
   - Boot consoles (dLive: ~60–90 seconds, SQ: ~30–45 seconds)
   - Boot QLab Macs (60–90 seconds)
   - Consoles reload last saved show file automatically
   - Verify Dante connections re-establish
5. **Estimated full recovery**: 2–5 minutes from power restoration

---

## Architecture-Specific Procedures

### A&H Baseline (Architecture A) — Specific Failures

#### F-A1: dLive S5000 Surface Crash (DM48 Still Running)

| | |
|---|---|
| **Symptom** | Surface screen freezes or goes dark; **audio continues** (DM48 processes independently) |
| **Detection** | A1 cannot adjust faders or recall cues on surface |
| **Audience impact** | None (DM48 continues last processing state) |
| **Response** | Switch to iPad control, or restart surface |

**Procedure (A1):**
1. Confirm audio is still passing (check house monitors / listen)
2. Launch **dLive MixPad** on iPad (should already be connected via WiFi or wired)
3. Verify iPad connects to DM48 and shows current mix state
4. Continue show control from iPad
5. **If iPad not available**: A2 can control via SQ (which is tracking via TheatreMix)
6. **Optional**: If convenient (intermission), power-cycle the S5000 surface — DM48 will reconnect automatically via gigaACE
7. **Estimated time**: 0 seconds (audio) / 30 seconds (control recovery on iPad)

#### F-A2: DM48 MixRack Failure (Complete dLive Failure)

| | |
|---|---|
| **Symptom** | Audio stops — DM48 is the processing engine |
| **Detection** | All dLive output channels drop; S5000 shows "MixRack offline" |
| **Audience impact** | 5–10 seconds of silence |
| **Response** | A2 switches DS10 Dante subscriptions to SQ |

**Procedure (A2 at backstage position):**
1. Confirm DM48 is down (Dante Controller shows device offline)
2. Confirm SQ-5 is running and on the correct cue (monitor SQ headphones)
3. Open **Dante Controller** on backstage laptop
4. Load pre-saved preset: **"SQ BACKUP"**
   - This re-subscribes DS10 channels:
     - DS10 Ch1 ← `SQ-Zone1` (was `dLive-Zone1`)
     - DS10 Ch2 ← `SQ-Zone2` (was `dLive-Zone2`)
     - ... through all 8 zones
5. Click **Apply** in Dante Controller
6. Verify audio returns on D20 amps (R1 meters or house monitors)
7. Notify A1: "Backup active on SQ"
8. Continue show from SQ — TheatreMix has kept SQ on the correct cue
9. **Estimated time**: 5–10 seconds

**Pre-show setup required:**
- Create and save Dante Controller preset "SQ BACKUP" with all 8 zone subscriptions pointing to SQ
- Test this preset during tech rehearsal and measure actual switchover time
- Dante Controller must already be open on the backstage laptop

#### F-A3: DM48 Dante Card Failure (M-DL-DANT128-A)

| | |
|---|---|
| **Symptom** | DM48 still processing locally but cannot send/receive Dante audio |
| **Detection** | Dante Controller shows DM48 Dante channels offline; DM48 local I/O still works |
| **Audience impact** | Same as F-A2 — no audio reaching DS10 |
| **Response** | Same as F-A2 — switch DS10 subscriptions to SQ |

**Procedure**: Same as F-A2 above.

---

### A&H + Python Automation (Architecture B) — Specific Failures

#### F-B1: DM48 MixRack Failure (Automatic)

| | |
|---|---|
| **Symptom** | Audio stops momentarily |
| **Detection** | Python controller detects DM48 offline within 500ms |
| **Audience impact** | ~2–3 seconds of silence |
| **Response** | **Automatic** — no operator action required |

**What happens automatically:**
1. T+0.0s: DM48 goes offline
2. T+0.5s: Health monitor detects absence
3. T+1.5s: Debounce period passes — failure confirmed
4. T+1.5s: Controller executes DS10 subscription switch to SQ channels
5. T+2.5s: All 8 zones re-subscribed
6. T+3.0s: SQ audio reaches D20 amplifiers
7. Dashboard updates to RED: "FAILOVER ACTIVE — SQ-5 is primary"
8. OSC notification sent to QLab status display

**Operator verification:**
1. A2: Confirm dashboard shows "FAILOVER ACTIVE"
2. A2: Confirm SQ audio is the correct cue/scene
3. A1: Confirm house audio quality
4. Continue show from SQ

#### F-B2: Python Controller Failure

| | |
|---|---|
| **Symptom** | Web dashboard unreachable; auto-failover disabled |
| **Detection** | A1 or A2 notices dashboard is down |
| **Audience impact** | None (controller failure doesn't affect audio) |
| **Response** | Fall back to manual procedure (F-A2) |

**Procedure:**
1. Note that automatic failover is offline
2. If DM48 eventually fails: use manual Dante Controller preset switch (same as F-A2)
3. After show: diagnose controller (check Raspberry Pi, restart service)
4. **Mitigation**: Monitor dashboard at start of every show; restart controller if not responding

#### F-B3: DM48 Failure + Restore Procedure

| | |
|---|---|
| **Symptom** | DM48 comes back online after a failover event |
| **Detection** | Dashboard shows DM48 "ONLINE" but system is still in FAILOVER state |
| **Audience impact** | None (SQ is still active) |
| **Response** | Manual restore confirmation |

**Procedure (A2):**
1. Verify DM48 is stable (wait minimum 30 seconds — controller enforces this)
2. Verify dLive show file loaded correctly on DM48 (check S5000 surface)
3. On dashboard or in QLab: press "RESTORE PRIMARY" (or send OSC `/failover/restore`)
4. Controller re-subscribes DS10 to dLive channels
5. Verify dLive audio on D20 amps
6. Notify A1: "Primary restored on dLive"
7. **Important**: Do NOT restore during a critical moment — wait for a natural break or scene change

---

### Yamaha RIVAGE PM5 (Architecture C) — Specific Failures

#### F-C1: DSP-RX Engine A Failure (Primary DSP)

| | |
|---|---|
| **Symptom** | **None** — DSP Mirroring activates instantly |
| **Detection** | CS-R5 surface shows "DSP Mirror Active" warning; Engine A status LED changes |
| **Audience impact** | **None — zero dropout** |
| **Response** | Note the event; DSP-RX Engine B is now primary |

**Procedure (A1):**
1. Note the "DSP Mirror Active" warning on CS-R5 surface
2. Continue mixing normally — all parameters, routing, and processing are identical on Engine B
3. Inform A2 and production: "Running on mirror DSP"
4. After show: diagnose Engine A, restart or replace
5. **Estimated time**: 0 seconds (fully automatic)

#### F-C2: CS-R5 Surface Failure (DSP Engines Still Running)

| | |
|---|---|
| **Symptom** | Surface screen freezes or goes dark; **audio continues** |
| **Detection** | A1 cannot interact with surface |
| **Audience impact** | None (DSP-RX engines are independent of surface) |
| **Response** | Switch to PM Editor or StageMix |

**Procedure (A1):**
1. Confirm audio is still passing
2. Open **RIVAGE PM Editor** on laptop or **StageMix** on iPad
3. Verify connection to DSP-RX and current show state
4. Continue show control from software
5. **Estimated time**: 0 seconds (audio) / 30 seconds (control recovery)

#### F-C3: Both DSP-RX Engines Fail (Catastrophic)

| | |
|---|---|
| **Symptom** | Audio stops completely |
| **Detection** | Surface shows both engines offline |
| **Audience impact** | Complete audio loss |
| **Response** | Cold restart — or switch to backup CL/QL console if available |

**Procedure:**
1. This is an extremely rare event (both engines failing simultaneously)
2. If backup CL/QL console is available with converted show file:
   - Connect CL/QL to Dante network
   - Load converted show file
   - Re-subscribe DS10 to CL/QL output channels
   - **Estimated time**: 2–5 minutes
3. If no backup console: attempt cold restart of DSP-RX engines
   - Power cycle both engines
   - Wait for boot (~90 seconds)
   - Show file auto-loads
   - **Estimated time**: 2–3 minutes

#### F-C4: Rio I/O Rack Failure (Pit)

| | |
|---|---|
| **Symptom** | All pit inputs go silent |
| **Detection** | DSP-RX shows Rio offline; pit channels show no signal |
| **Audience impact** | Band/orchestra goes silent |
| **Response** | No immediate backup for pit I/O |

**Procedure:**
1. Same as DT168 failure in A&H architecture — pit is a single point of failure
2. Band continues playing acoustically (visible to audience)
3. If spare Rio1608-D2 available: connect and configure Dante subscriptions
4. **Mitigation**: Use TWINLANe ring topology (if available) for automatic Rio path redundancy

---

### DiGiCo Quantum 338 (Architecture D) — Specific Failures

#### F-D1: Quantum 338 Total Failure

| | |
|---|---|
| **Symptom** | Audio stops — console is the single processing engine |
| **Detection** | Q338 screens go dark; all outputs drop |
| **Audience impact** | 5–10 seconds of silence |
| **Response** | A2 switches DS10 Dante subscriptions to SD9T |

**Procedure (A2 at backstage position):**
1. Confirm Q338 is down
2. Confirm SD9T is running and on the correct cue
3. Open **Dante Controller** on backstage laptop
4. Load preset: **"SD9T BACKUP"**
   - Re-subscribes DS10 to `SD9T-Zone1..8`
5. Click Apply
6. Verify audio on D20 amps
7. Notify A1: "Backup active on SD9T"
8. Continue show from SD9T — TheatreMix has kept it on the correct cue
9. **Estimated time**: 5–10 seconds

**Key advantage over A&H**: The SD9T is running the **same show file** as the Q338 — audio quality and processing are near-identical.

#### F-D2: Optocore Fiber Break (Single Loop)

| | |
|---|---|
| **Symptom** | None — dual loop takes over automatically |
| **Detection** | Q338 shows Optocore loop warning; single ring instead of dual |
| **Audience impact** | None |
| **Response** | Note the event; diagnose after show |

**Procedure:**
1. Note the Optocore warning on Q338 surface
2. Continue show normally
3. After show: inspect fiber runs, re-terminate or replace damaged fiber
4. **Estimated time**: 0 seconds (automatic)

#### F-D3: Optocore Fiber Break (Both Loops)

| | |
|---|---|
| **Symptom** | D2-Rack disconnected — pit inputs lost |
| **Detection** | Q338 shows Optocore offline; pit channels drop |
| **Audience impact** | Band/orchestra goes silent |
| **Response** | Same as pit stagebox failure in other architectures |

**Procedure:**
1. Band continues acoustically
2. No immediate fix for fiber during show
3. After show: inspect and repair both fiber runs

#### F-D4: DMI-DANTE Card Failure

| | |
|---|---|
| **Symptom** | Dante I/O lost — wireless receivers and DS10 disconnected from Q338 |
| **Detection** | Q338 shows DMI slot error; Dante channels drop |
| **Audience impact** | All wireless mics and amplified output lost (if using Dante path for output) |
| **Response** | Switch to SD9T (which has its own DMI-DANTE) |

**Procedure:**
1. Confirm DMI-DANTE failure on Q338
2. SD9T is still receiving all Dante inputs via its own DMI-DANTE card
3. Switch DS10 subscriptions to SD9T (same as F-D1)
4. **Estimated time**: 5–10 seconds
5. **Note**: Optocore I/O (D2-Rack) still works on Q338 — pit inputs are unaffected

---

## Pre-Show Checklist (All Architectures)

Complete this checklist before every performance:

### Network & Dante
- [ ] All Dante devices visible in Dante Controller
- [ ] PTP clock stable (no errors for 5+ minutes)
- [ ] Primary AND Secondary Dante paths active
- [ ] All Dante subscriptions correct (verify routing)

### Primary Console
- [ ] Show file loaded and correct version
- [ ] All input channels receiving signal (line check)
- [ ] All output zones active and correct
- [ ] TheatreMix connected and tracking

### Backup Console
- [ ] Show file loaded and correct version (matching primary)
- [ ] All input channels receiving signal (verify via headphones)
- [ ] Output channels configured (even though DS10 isn't subscribed yet)
- [ ] TheatreMix connected and tracking parallel cues

### Failover Readiness
- [ ] Dante Controller preset "BACKUP" saved and verified
- [ ] (Arch B) Python failover controller running, dashboard GREEN
- [ ] (Arch B) Test OSC trigger from QLab → controller responds
- [ ] Backstage laptop powered on with Dante Controller open
- [ ] iPad/tablet control app connected (for surface failure)
- [ ] A2 headphones monitoring backup console

### Amplifiers
- [ ] R1 connected to both D20 amps
- [ ] All D20 channels showing signal (from DS10)
- [ ] D20 input mode correct (AES3 for DS10 connection)
- [ ] All zones producing audio (walk the house during sound check)

### Playback
- [ ] Mac A and Mac B both running QLab
- [ ] Both Macs on correct cue position
- [ ] Dante Virtual Soundcard active on both Macs

### Communication
- [ ] A1 ↔ A2 comms working (headset/radio)
- [ ] A2 knows the failover procedure (confirm verbally)
- [ ] Stage manager informed of failover protocol

---

## Emergency Quick Reference Card

Print this card and tape it to the A2 position:

```
╔══════════════════════════════════════════════════════╗
║            FAILOVER QUICK REFERENCE                  ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  IF MAIN CONSOLE DIES:                              ║
║                                                      ║
║  Arch A/D (Manual):                                 ║
║    1. Open Dante Controller on laptop               ║
║    2. Load preset "SQ BACKUP" / "SD9T BACKUP"       ║
║    3. Click APPLY                                   ║
║    4. Verify audio on R1 meters                     ║
║    5. Tell A1: "Backup is active"                   ║
║                                                      ║
║  Arch B (Automatic):                                ║
║    1. Check dashboard — should auto-switch          ║
║    2. If dashboard is RED: failover worked          ║
║    3. If dashboard is DOWN: use manual procedure    ║
║                                                      ║
║  Arch C (RIVAGE PM):                                ║
║    1. DSP Mirror is automatic — do nothing          ║
║    2. If surface freezes: use iPad StageMix         ║
║    3. If BOTH engines fail: cold restart (2 min)    ║
║                                                      ║
║  IF PLAYBACK DIES:                                  ║
║    1. Switch to Mac B                               ║
║    2. Navigate to current cue                       ║
║    3. Press GO                                      ║
║                                                      ║
║  IF AMP OUTPUT DIES:                                ║
║    1. Check R1 — is it the amp or the DS10?         ║
║    2. DS10: swap to spare if available              ║
║    3. D20: check for thermal/clip protect           ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```
