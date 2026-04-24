# 04 — Variation B: DiGiCo Quantum 338 System Architecture

## Overview

This variation replaces the Allen & Heath dLive + SQ-5 with a **DiGiCo Quantum 338** as the primary console and an **SD9T** (or SD11/SD12) as the backup. The DiGiCo ecosystem solves the A&H architecture's biggest pain point — **show file incompatibility** — because DiGiCo show files are natively portable across the entire SD/Quantum range. One programming session serves both primary and backup consoles.

For comparison with other architectures, see [06-comparison-matrix.md](06-comparison-matrix.md).

---

## Why DiGiCo Solves the Core Problems

| A&H Problem | DiGiCo Solution |
|---|---|
| Show file incompatibility between primary & backup | **Native show file portability** — SD9T can load a Quantum 338 session directly (with automatic processing scaling) |
| Dual programming required | **Single programming session** — program the Q338, copy the session to SD9T |
| SQ can't run Dante + Waves simultaneously | **Dual DMI slots** — DMI-DANTE (64×64) + DMI-WAVES (64×64) run simultaneously, no compromise |
| No fiber option for stage network | **Optocore fiber loop** — up to 504 channels per loop, electrically isolated, immune to dimmer interference |
| Limited bus/matrix for 8 zones | **128 busses + 48×48 matrix** (Q7) or **64 busses + 24×24 matrix** (Q338) — massive headroom |
| No per-send processing | **Nodal Processing** — unique to DiGiCo: independent EQ/dynamics on each input's send to each bus |

---

## Quantum 338 vs Quantum 7

| Feature | Quantum 338 | Quantum 7 |
|---|---|---|
| Input channels | 128 | Up to 2,000 across 688 paths @96kHz |
| Busses | 64 | 128 |
| Matrix | 24×24 | 48×48 |
| Internal engines | 1 (no dual-engine redundancy) | **2 (dual redundant engines — automatic failover)** |
| DMI slots | 2 | 2 |
| Optocore | Optional (dual loop available) | Standard (dual loop) |
| Physical size | Compact (similar to dLive S5000) | Large (dedicated furniture) |
| Converters | 32-bit Ultimate Stadius | 32-bit Ultimate Stadius |
| MADI | Triple redundant | Triple redundant |
| Price | $$ | $$$$ |

**For this application**: The Quantum 338 is the right choice — it has more than enough channels and busses for a 48-input, 8-zone system. The Quantum 7's dual-engine redundancy is the luxury upgrade, but for the price difference, the SD9T backup with show file portability provides adequate failover.

---

## Equipment List

| Role | Equipment | Qty | Location |
|---|---|---|---|
| Primary console | DiGiCo Quantum 338 | 1 | FOH |
| Backup console | DiGiCo SD9T (Theatre version) | 1 | Backstage A2 position |
| Stage I/O | DiGiCo D2-Rack (40 in / 24 out, Optocore) | 1 | Stage (pit side) |
| FOH I/O | DMI-DANTE card in Q338 (64×64) | 1 | FOH (in console) |
| Waves processing | DMI-WAVES card in Q338 (64×64) | 1 | FOH (in console) |
| SD9T Dante card | DMI-DANTE card (32×32 or 64×64) | 1 | SD9T |
| Wireless microphones | Sennheiser Dante-enabled × 32 | 32 | FOH rack |
| Playback A | Mac + QLab + Dante Virtual Soundcard | 1 | FOH |
| Playback B | Mac + QLab + Dante Virtual Soundcard | 1 | FOH |
| Amp bridge | d&b DS10 (16ch Dante→AES3) | 1 | Amp rack |
| Amplifiers | d&b D20 (4ch each) | 2 | Amp rack |
| Network switches | Managed Gigabit × 2 (Dante network) | 2 | FOH + Amp rack |
| Optocore fiber | Multimode fiber (optional, for D2-Rack) | — | Stage ↔ FOH |

---

## Network Architecture

The DiGiCo system uses a **hybrid network** — Optocore fiber for high-density stage I/O and Dante for interoperability with wireless receivers, QLab, and DS10 bridges.

### Dual Network Topology

```
┌────────────────────────────────────────────────────┐
│                  OPTOCORE FIBER LOOP                │
│            (504 channels per loop)                  │
│   ┌──────────┐         ┌──────────────┐            │
│   │ D2-Rack  │◄──fiber──►│ Quantum 338 │            │
│   │ (Stage)  │         │  (Optocore   │            │
│   │ 40in/24out│        │   ports)     │            │
│   └──────────┘         └──────┬───────┘            │
│                               │                    │
│   Optional dual loop:         │                    │
│   Second fiber path for       │                    │
│   automatic redundancy        │                    │
└───────────────────────────────┼────────────────────┘
                                │
                         ┌──────┴───────┐
                         │  DMI-DANTE   │
                         │  (64×64)     │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
        ┌─────┴─────┐   ┌──────┴──────┐   ┌──────┴──────┐
        │Sennheiser │   │  QLab A/B   │   │    DS10     │
        │  ×32 Lavs │   │  (2× Mac)   │   │ Dante→AES3  │
        │  (Dante)  │   │  (Dante)    │   │→ D20 amps   │
        └───────────┘   └─────────────┘   └─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
        ┌─────┴─────┐   ┌──────┴──────┐
        │  SD9T     │   │  Dante      │
        │  (Backup) │   │  Switches   │
        │ DMI-DANTE │   │  (Prim+Sec) │
        └───────────┘   └─────────────┘
```

### Why Hybrid (Optocore + Dante)?

- **Optocore for stage I/O**: Fiber is immune to electrical interference from dimmer racks, lighting equipment, and long cable runs. The D2-Rack connects via fiber — no ground loops, no RFI.
- **Dante for everything else**: Wireless receivers, QLab, DS10 bridges, and the SD9T backup are all Dante devices. The DMI-DANTE card bridges the Q338's Optocore world to the Dante network.
- **Optocore dual-loop redundancy**: Two fiber paths between D2-Rack and Q338. If one fiber breaks, the other carries all traffic automatically. This is equivalent to Dante Primary/Secondary but on fiber.

---

## Input Architecture

### Stage I/O: D2-Rack

- **40 mic/line inputs + 24 outputs** — more than enough for 16 pit channels with significant headroom
- Connected via Optocore fiber to Q338
- Preamp gain, phantom power, pad — all controlled from Q338 surface and stored in snapshots
- **Advantage over DT168**: Higher channel count, fiber transport (no electrical interference from pit), native integration with DiGiCo snapshot system

### FOH Wireless: Sennheiser × 32

- Same Dante architecture as A&H variation
- Q338 receives wireless channels via DMI-DANTE card
- SD9T also subscribes to same wireless Dante channels via its own DMI-DANTE card
- Both consoles receive all 32 lavs simultaneously

### Playback: Dual QLab Macs

- Same dual-Mac architecture
- Q338 subscribes to Mac A via DMI-DANTE
- SD9T subscribes to both Mac A and Mac B for immediate failover

---

## Show File Portability

This is DiGiCo's **key differentiator** for redundancy:

### How It Works

1. Program the full show on the Quantum 338 — all snapshots, channel processing, routing, DCAs
2. Save the session file
3. Copy the session file to the SD9T via USB or network
4. SD9T **loads the session natively** — no conversion tool needed

### What Transfers

| Parameter | Transfers? | Notes |
|---|---|---|
| Channel count & routing | Yes | SD9T scales to its own channel limit (72 inputs) — sufficient for 48 |
| Snapshots/scenes | Yes | All cue data intact |
| EQ & dynamics | Yes | Processing algorithms are the same across SD/Quantum |
| DCA assignments | Yes | |
| FX rack (reverbs, delays) | Yes | Same FX library across range |
| Matrix routing | Yes | SD9T has smaller matrix but sufficient for 8 zones |
| DMI card routing | Yes | Adapted to SD9T's DMI slot configuration |
| Mustard Processing | Partial | Available on Quantum, limited on SD9T |
| Nodal Processing | Partial | Available on Quantum, limited on SD series |

### What Doesn't Transfer Perfectly

- **Fader layout**: SD9T has fewer faders than Q338; layer organization will differ
- **Mustard/Spice Rack plugins**: Not all available on SD9T — processing falls back to standard algorithms
- **Channel count ceiling**: SD9T supports 72 inputs at 48kHz — more than enough for this 48-channel show

### Impact

- **One programming session** instead of two
- Changes to the Q338 show can be immediately copied to SD9T
- The SD9T backup will sound nearly identical to the Q338 (same processing algorithms)
- This is **impossible** with the A&H dLive→SQ architecture

---

## Console Configuration

### Quantum 338 — Primary

1. Install **DMI-DANTE** card (64×64 at 48kHz) in DMI Slot 1
2. Install **DMI-WAVES** card (64×64) in DMI Slot 2 (optional — Waves and Dante coexist)
3. Configure Optocore port for D2-Rack connection
4. Subscribe Dante inputs: 32 wireless + QLab channels
5. Route Optocore inputs: 16 pit channels from D2-Rack
6. Configure 8 output zones via Dante (DMI-DANTE card outputs → DS10)
7. Program full show:
   - All snapshots with theatre-specific features (auto-increment, crossfade, channel safes)
   - DCAs (8–12 typical)
   - FX rack (reverbs, delays)
   - EQ/dynamics on all channels
   - Nodal Processing on critical monitor/zone sends
8. If using Waves: configure Waves inserts on desired channels via DMI-WAVES

### SD9T — Backup

1. Install **DMI-DANTE** card in SD9T's DMI slot
2. Subscribe to same Dante inputs as Q338 (32 wireless + QLab)
3. Load Q338 session file from USB
4. Verify routing adapts correctly to SD9T's I/O configuration
5. Configure SD9T Dante outputs: `SD9T-Zone1` through `SD9T-Zone8`
6. Position at A2 backstage with headphone monitoring

### TheatreMix / External Automation

- TheatreMix or QLab can drive both consoles via MIDI/OSC
- DiGiCo consoles accept MIDI for snapshot recall
- Both consoles advance through the show in lockstep
- SD9T is always on the correct cue — ready for instant takeover

---

## Waves Integration (Unique Advantage)

Unlike the SQ-5's single option slot, the Q338 has **two independent DMI slots**:

| DMI Slot | Card | Function |
|---|---|---|
| Slot 1 | DMI-DANTE (64×64) | Dante I/O for wireless, QLab, DS10 |
| Slot 2 | DMI-WAVES (64×64) | Waves SoundGrid processing |

- Both cards run simultaneously — no compromise
- Waves inserts available on any channel without sacrificing Dante connectivity
- SoundGrid server connects via DMI-WAVES
- **SD9T can also have DMI-WAVES** if a second DMI slot is available on that model, OR fall back to onboard processing if not

This means the redundancy architecture can include Waves processing on BOTH primary and backup consoles — eliminating the sonic asymmetry problem of the A&H architecture.

---

## Output Architecture

Same DS10 → D20 path as other architectures:

- Q338 outputs 8 zones via DMI-DANTE → Dante network → DS10 → AES3 → D20 amps
- SD9T outputs `SD9T-Zone1..8` via its DMI-DANTE card
- Failover: Dante Controller preset switch on DS10 (same as A&H Option A)

### Alternative: DMI-AES Direct Output

The Q338 can also output directly via **DMI-AES** card if installed in a third slot (if available) or replacing DMI-WAVES:
- DMI-AES provides direct AES3 output from the console
- Eliminates the DS10 entirely — Q338 → AES3 → D20
- However, this removes the DS10's Dante network bridging for the backup console
- **Not recommended** unless simplifying the output path for a specific reason

---

## Failover Behavior

| Failure | Impact | Response | Time | Action By |
|---|---|---|---|---|
| Q338 surface freeze | Audio continues (processing engine intact) | Restart console software | 0s audio / 30s control | A1 |
| Q338 total failure | Audio stops | A2: Load DS10 "SD9T Backup" preset in Dante Controller | 5–10s | A2 |
| Optocore fiber break (single loop) | No impact — dual loop takes over | Diagnose after show | 0s | Automatic |
| Optocore fiber break (both loops) | Pit inputs lost (D2-Rack disconnected) | No backup for pit — same as A&H DT168 scenario | N/A | Accept risk |
| DMI-DANTE card failure | Dante I/O lost, Optocore I/O still works | Switch to SD9T for Dante I/O | 10–20s | A2 |
| D2-Rack failure | Pit inputs lost | No backup — same as DT168 scenario | N/A | Accept risk |
| DS10 failure | Amp rack goes silent | Same as A&H architecture | 10–30s | A2 |
| SD9T failure (while on standby) | No impact on primary | Note for post-show repair | 0s | N/A |

---

## Nodal Processing — Unique Feature

Nodal Processing is unique to DiGiCo and particularly valuable for theatrical applications:

### What It Does

Standard consoles: One set of EQ/dynamics per input channel, applied to ALL sends from that channel.

Nodal Processing: **Independent EQ/dynamics per input per bus send**. Each output zone can receive a different version of the same input.

### Theatrical Use Cases

| Scenario | Without Nodal | With Nodal |
|---|---|---|
| Lav needs more presence in Zone 1 (stalls) but is harsh in Zone 3 (balcony) | Compromise EQ for both | +3dB @ 3kHz in Zone 1 send, -2dB @ 3kHz in Zone 3 send |
| Band bleed in vocal zone | Reduce band level globally | Reduce band level only in vocal zone sends |
| Subwoofer feed needs HPF removed but mains need it | Can't do both | Independent HPF per send |

This level of control is not available on A&H or Yamaha platforms.

---

## Cost Analysis

| Component | DiGiCo Q338 System | A&H dLive + SQ System |
|---|---|---|
| Primary console | Quantum 338 ($$$) | dLive S5000 + DM48 ($$) |
| Backup console | SD9T ($$) | SQ-5 + Dante card ($) |
| Stage I/O | D2-Rack ($$) + Optocore fiber | DT168 ($) + Cat cable |
| Dante I/O | DMI-DANTE ×2 ($) | M-DL-DANT128-A ($) |
| Waves | DMI-WAVES ($ + license) | Not recommended / slot conflict |
| Amp bridge | DS10 ×1 (same) | DS10 ×1 (same) |
| Amplifiers | D20 ×2 (same) | D20 ×2 (same) |
| Programming time | 1× (one session, copy to backup) | 2× (independent programming) |
| Fiber infrastructure | $ (multimode fiber runs) | $0 (all copper) |

**Bottom line**: Higher hardware cost but significantly reduced programming and maintenance burden. Show file portability means changes during tech rehearsals propagate to the backup instantly.

---

## Summary of Advantages

1. **Show file portability** — one programming session, copy to SD9T
2. **Dual DMI slots** — Dante + Waves simultaneously, no compromise
3. **Optocore fiber** — electrically isolated stage network, immune to interference
4. **Nodal Processing** — per-send EQ/dynamics for precise zone control
5. **32-bit Ultimate Stadius converters** — highest converter quality in the D2-Rack
6. **Extensive bus/matrix** — 64 busses + 24×24 matrix provides massive headroom
7. **Theatre-specific snapshots** — auto-increment, crossfade, channel safes
8. **Industry standard** — DiGiCo is the dominant console brand in West End and Broadway musicals
9. **SD/Quantum ecosystem** — backup console uses identical processing algorithms
10. **Triple redundant MADI** — additional I/O backup path if Dante fails
