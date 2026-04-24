# 06 — Comparison Matrix: All Architectures

## Overview

This document compares all four system architecture variations across 20+ criteria to support a final platform decision. Each architecture uses the same output path (d&b DS10 → D20 amplifiers), the same wireless receivers (Sennheiser Dante-enabled × 32), and the same dual QLab playback setup. The differences are in the console platform, redundancy method, and automation capabilities.

---

## Architecture Summary

| ID | Architecture | Primary Console | Backup Console | Key Feature |
|---|---|---|---|---|
| **A** | A&H Baseline | dLive S5000 + DM48 | SQ-5 | Manual Dante Controller preset switch |
| **B** | A&H + Python | dLive S5000 + DM48 | SQ-5 | Automated Dante switching via Python controller |
| **C** | Yamaha RIVAGE PM5 | CS-R5 + DSP-RX ×2 | DSP Mirroring (built-in) | Native automatic DSP failover |
| **D** | DiGiCo Q338 | Quantum 338 | SD9T | Show file portability + Optocore fiber |

---

## Full Comparison Matrix

### Redundancy & Failover

| Criteria | A: A&H Baseline | B: A&H + Python | C: RIVAGE PM5 | D: DiGiCo Q338 |
|---|---|---|---|---|
| **DSP failover method** | Manual (Dante preset) | Auto (Python script) | **Automatic (hardware)** | Manual (Dante preset) |
| **Failover time** | 5–10s | **~3s** | **0s (instant)** | 5–10s |
| **Audio interruption** | 5–10s silence | ~2–3s silence | **None** | 5–10s silence |
| **Operator action required** | Yes (A2) | No (auto) / Yes (manual) | **No** | Yes (A2) |
| **False trigger risk** | None (manual) | Low (1s debounce) | **None (hardware)** | None (manual) |
| **Network path redundancy** | Dante Pri/Sec (auto) | Dante Pri/Sec (auto) | Dante Pri/Sec (auto) | **Optocore dual loop + Dante Pri/Sec** |
| **Surface failure recovery** | iPad MixPad | iPad MixPad | PM Editor / StageMix | DiGiCo software |

### Show Programming

| Criteria | A: A&H Baseline | B: A&H + Python | C: RIVAGE PM5 | D: DiGiCo Q338 |
|---|---|---|---|---|
| **Show file compatible** | **NO** (dLive ≠ SQ) | **NO** | **YES** (Console File Converter) | **YES** (native SD/Quantum) |
| **Dual programming required** | **YES** | **YES** | **NO** | **NO** |
| **Programming time (relative)** | 2× | 2× | **1×** | **1×** |
| **Tech rehearsal changes** | Must update both | Must update both | **Update once** | **Update once, copy to backup** |
| **Backup mix quality** | Functional (limited) | Functional (limited) | **Identical (mirrored)** | **Near-identical (same algorithms)** |

### Console Features

| Criteria | A: A&H Baseline | B: A&H + Python | C: RIVAGE PM5 | D: DiGiCo Q338 |
|---|---|---|---|---|
| **Theatre-specific features** | TheatreMix (external) | TheatreMix + Python | **Theatre Mode + Genius.lab** | **Snapshots + Theatre Guide** |
| **Noise suppression** | None | None | **DaNSe (AI-based)** | None |
| **Immersive sound** | None native | None native | **Sound xR Image** | **Nodal Processing** |
| **Per-send processing** | No | No | No | **YES (Nodal Processing)** |
| **Cast swap management** | Manual EQ recall | Manual EQ recall | **Theatre Mode (4 banks/ch)** | Snapshot-based |
| **Waves + Dante simultaneous** | dLive: YES, SQ: **NO** | Same | **YES** (separate HY slots) | **YES** (dual DMI slots) |

### Automation & Control

| Criteria | A: A&H Baseline | B: A&H + Python | C: RIVAGE PM5 | D: DiGiCo Q338 |
|---|---|---|---|---|
| **Native OSC** | No (TCP only) | Via Python bridge | **YES (server + client)** | Via macro system |
| **Single-button failover** | No | **YES (scripted)** | **YES (Genius.lab)** | Partial (snapshot) |
| **Macro engine** | None | Custom Python | **Genius.lab (native)** | Macro system |
| **QLab integration** | TheatreMix | OSC (direct) | **OSC (native)** | MIDI/OSC |
| **Custom development needed** | None | **Significant** | **None** | None |

### Infrastructure

| Criteria | A: A&H Baseline | B: A&H + Python | C: RIVAGE PM5 | D: DiGiCo Q338 |
|---|---|---|---|---|
| **Stage network type** | Dante (copper) | Dante (copper) | Dante (copper) | **Optocore (fiber) + Dante** |
| **Electrical isolation** | No | No | No | **YES (fiber)** |
| **Stage I/O** | DT168 (16in/8out) | DT168 | Rio1608-D2 (16in/8out) | **D2-Rack (40in/24out)** |
| **Channel capacity** | 48 (tight) | 48 (tight) | 144+ (HY144-D) | **128 (Q338) / 2000 (Q7)** |
| **Bus/matrix headroom** | SQ: tight | SQ: tight | Large | **64 bus + 24×24 matrix** |

### Cost & Practicality

| Criteria | A: A&H Baseline | B: A&H + Python | C: RIVAGE PM5 | D: DiGiCo Q338 |
|---|---|---|---|---|
| **Hardware cost** | **$ (lowest)** | $ + Raspberry Pi | $$$ | $$$ |
| **Software/license cost** | $0 | $0 (open source) | $0 (included) | $0 (included) |
| **Development cost** | $0 | $$ (time) | $0 | $0 |
| **Ongoing maintenance** | Low | **Medium (scripts)** | Low | Low |
| **Operator familiarity** | High (A&H common) | Same | Medium | **High (theatre standard)** |
| **Rental availability** | High | Same | Medium | High |
| **Training required** | Low | Medium (Python) | Medium (new platform) | Medium (new platform) |

---

## Scoring Summary

Weighted scoring based on the stated priorities: **reliability first**, musical with immersive sound, 32 wireless lavs, snapshot-driven mix.

| Category (Weight) | A: A&H Baseline | B: A&H + Python | C: RIVAGE PM5 | D: DiGiCo Q338 |
|---|---|---|---|---|
| Failover reliability (30%) | 4/10 | 7/10 | **10/10** | 5/10 |
| Show programming efficiency (20%) | 3/10 | 3/10 | **9/10** | **9/10** |
| Theatre features (15%) | 5/10 | 5/10 | **9/10** | 8/10 |
| Automation capability (15%) | 2/10 | 7/10 | **9/10** | 6/10 |
| Cost effectiveness (10%) | **9/10** | 7/10 | 5/10 | 5/10 |
| Operator experience (10%) | 6/10 | 5/10 | 7/10 | **8/10** |
| **Weighted Total** | **4.4** | **5.6** | **8.8** | **6.7** |

---

## Recommendation Ranking

### 1. Yamaha RIVAGE PM5 (Score: 8.8/10)

**Best overall choice** for a reliability-first musical production.

- DSP Mirroring = zero-dropout automatic failover (the only platform that does this)
- Genius.lab = native single-button macro automation
- Theatre Mode = purpose-built for musical cast management
- DaNSe = AI noise suppression for theatrical lavs
- Native OSC = no custom scripting needed
- Console File Converter = backup portability to CL/QL series
- Eliminates dual programming entirely
- Higher hardware cost offset by reduced programming labour and no custom development

### 2. DiGiCo Quantum 338 + SD9T (Score: 6.7/10)

**Best choice if DSP mirroring isn't available** or if DiGiCo is the preferred/available platform.

- Show file portability = one programming session
- Dual DMI slots = Dante + Waves simultaneously
- Optocore fiber = electrically isolated, interference-immune stage network
- Nodal Processing = per-send EQ/dynamics (unique competitive advantage)
- Industry standard for West End/Broadway musicals
- SD9T backup loads Q338 sessions natively
- Failover is still manual (~5–10s) unless paired with Python automation (Approach 5)

### 3. A&H dLive + SQ + Python Automation (Score: 5.6/10)

**Best choice if A&H dLive and SQ-5 are the available equipment.**

- Keeps existing gear — no new console purchase
- Python controller provides ~3s automated failover
- But: dual programming burden remains
- But: custom development and maintenance cost
- But: ~2–3s audio gap during failover (not seamless)

### 4. A&H dLive + SQ Baseline (Score: 4.4/10)

**Adequate but limited** — this is the starting point, not the destination.

- Works, but 5–10s manual switchover
- Dual programming burden
- No automation
- Suitable only if alternative platforms are genuinely unavailable

---

## Decision Flowchart

```
START: Do you need automatic failover with zero audio dropout?
  │
  ├── YES → Yamaha RIVAGE PM5 (DSP Mirroring)
  │
  └── NO (manual switchover acceptable)
        │
        ├── Is show file portability important (reducing programming time)?
        │     │
        │     ├── YES → DiGiCo Quantum 338 + SD9T
        │     │
        │     └── NO (willing to program both consoles)
        │           │
        │           ├── Do you want automated detection + switching?
        │           │     │
        │           │     ├── YES → A&H dLive + SQ + Python Automation
        │           │     │
        │           │     └── NO → A&H dLive + SQ Baseline
        │           │
        │           └── Is Nodal Processing or Optocore fiber valuable?
        │                 │
        │                 └── YES → DiGiCo Quantum 338
        │
        └── Is the production touring or long-running?
              │
              ├── YES → RIVAGE PM5 or DiGiCo Q338 (investment justified)
              │
              └── NO (short run) → A&H Baseline or Python Hybrid
```

---

## Platform-Specific Suitability

| Production Type | Recommended Platform | Rationale |
|---|---|---|
| Long-running musical (months+) | RIVAGE PM5 | DSP mirroring pays for itself; DaNSe invaluable for 8-show weeks |
| Touring musical | DiGiCo Q338 | Industry standard; SD9T backup fit-ups at every venue |
| Short-run musical (1–3 weeks) | A&H + Python, or Q338 rental | Balance cost vs reliability |
| One-off concert/event | A&H Baseline | Simplest; manual failover acceptable |
| Immersive/spatial theatre | RIVAGE PM5 (Sound xR) or Q338 (Nodal) | Purpose-built immersive tools |
