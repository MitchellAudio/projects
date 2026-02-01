# Notes: Single Vs Three Phase Power
## Overview

- Single-phase (split-phase) is common for residential power in North America (120/240V).
- Three-phase is used for higher-power distribution in commercial and industrial settings (examples: 208V, 400/415V, 480V systems depending on region and connection).

## Split-phase (120/240V) — how it works

- The transformer at the service splits the secondary into two 120V legs that are 180° out of phase.
- Between either hot leg and neutral = 120V. Between the two hot legs = 240V.
- 240V loads connect across both hot legs; 120V loads connect between a hot leg and neutral.

## Three-phase basics

- Three-phase systems have three sinusoidal voltages, each 120° apart.
- Common wiring:
	- Wye (star): line-to-line voltage = √3 × line-to-neutral voltage. Neutral available.
        - Wye is a wiring topology (an internal connection of windings), not a single physical connector — the neutral may be brought out to a terminal (neutral lug/bushing), but the Wye itself describes how windings are arranged.
	- Delta: line voltages between phases; neutral may not be present unless a center-tapped winding is used.


## Power calculations

- Single-phase: P (W) = V × I × PF (power factor). For purely resistive loads PF = 1.
- Three-phase (balanced): P (W) = √3 × V_line × I_line × PF.

## Why use three-phase?

- More efficient transmission of power for motors and heavy loads.
- Motors run smoother and with less vibration on three-phase.
- For the same power, three-phase requires less conductor material than multiple single-phase circuits.

## Phase rotation and balancing

- Phase rotation (A-B-C order) matters for three-phase motors — reversing rotation changes motor spin direction.
- Balance loads across phases to minimize neutral current and avoid overheating conductors.

## Neutral & grounding

- Neutral is the current return for unbalanced single-phase loads; ground is a safety conductor used only for fault currents.
- In a balanced three-phase system with purely three-phase loads, neutral current can be zero.

## Motor starting and inrush

- Motors draw high inrush currents when starting
- Soft-starts, VFDs (variable frequency drives), or star-delta starters can reduce inrush and mechanical stress.

---

## Three-Phase Power for Audio Systems

### Common North American Three-Phase Systems

**208V/120V Wye (Most Common for Audio):**
- Three hot legs (A, B, C) + Neutral + Ground
- **Line-to-neutral (L-N):** 120V between any hot leg and neutral
- **Line-to-line (L-L):** 208V between any two hot legs (120V × √3 ≈ 208V)
- **Connector:** Often 5-pin (3 hots + neutral + ground) or California-style Cam-Lok

**480V/277V Wye (Industrial/Large Venues):**
- Three hot legs + Neutral + Ground
- **Line-to-neutral:** 277V (used for high-bay lighting)
- **Line-to-line:** 480V between hot legs
- **Common in:** Arenas, convention centers, industrial facilities

### How PDUs Convert Three-Phase for Amplifiers

**PDUs (Power Distribution Units) distribute three-phase power in several ways:**

#### 1. **Direct Three-Phase Distribution (Pure 3-Phase Loads)**
- Some large amplifiers accept three-phase input directly (less common)
- PDU passes all three phases through to multi-phase outlets
- Each amplifier connects to all three phases

#### 2. **Phase Distribution to Single-Phase Loads (Most Common)**
**Example: 208V/120V 3-Phase to PDU**

```
Three-Phase Input (208V/120V Wye)
   ↓
┌─────────────────────────────────┐
│          PDU                     │
│                                  │
│  Phase A + Neutral → Outputs 1-6 │ → 120V single-phase
│  Phase B + Neutral → Outputs 7-12│ → 120V single-phase  
│  Phase C + Neutral → Outputs 13-18│ → 120V single-phase
│                                  │
│  OR                              │
│                                  │
│  Phase A + B → Outputs 1-4       │ → 208V single-phase
│  Phase B + C → Outputs 5-8       │ → 208V single-phase
│  Phase A + C → Outputs 9-12      │ → 208V single-phase
└─────────────────────────────────┘
```

**Key Concept:** The PDU **distributes** phases, it doesn't convert voltages. Each outlet gets power from specific phase combinations.

#### 3. **Balanced Load Distribution**
- PDU distributes loads across all three phases evenly
- Prevents one phase from being overloaded
- Reduces neutral current and heat

### D&B D80 Amplifier Example

**D&B D80 Specifications:**
- **Input:** 200-240V AC, 50/60 Hz (single-phase)
- **Power Consumption:** ~2000W max
- **Current Draw:** ~10A at 200V, ~8.3A at 240V

**How it connects to 208V/120V three-phase PDU:**

```
Building Supply: 208V/120V Three-Phase
   ↓
┌─────────────────────────────────────┐
│    PDU (50A three-phase input)      │
│                                     │
│  Phase A + Phase B → Outlet 1       │ → 208V → D80 Amp #1
│  Phase B + Phase C → Outlet 2       │ → 208V → D80 Amp #2
│  Phase C + Phase A → Outlet 3       │ → 208V → D80 Amp #3
│  Phase A + Phase B → Outlet 4       │ → 208V → D80 Amp #4
│                                     │
└─────────────────────────────────────┘
```

**What's Happening:**
1. PDU receives three-phase 208V/120V power
2. Each D80 gets **208V single-phase** from two of the three hot legs
3. Amps are distributed across phase combinations for balanced loading
4. Each D80 sees this as normal single-phase 208V power

### Calculating Load Balance

**Example: Six D&B D80 amplifiers on 208V three-phase PDU**

| Amp | Connection | Current Draw | Phase A | Phase B | Phase C |
|-----|------------|--------------|---------|---------|---------|
| D80 #1 | A-B | 10A | +10A | +10A | 0A |
| D80 #2 | B-C | 10A | 0A | +10A | +10A |
| D80 #3 | C-A | 10A | +10A | 0A | +10A |
| D80 #4 | A-B | 10A | +10A | +10A | 0A |
| D80 #5 | B-C | 10A | 0A | +10A | +10A |
| D80 #6 | C-A | 10A | +10A | 0A | +10A |
| **Total per Phase** | | | **30A** | **30A** | **30A** |

**Perfectly balanced!** Each phase carries the same current.

### Why Three-Phase for Audio?

**Advantages:**
1. **Higher total power capacity** from same size service
   - 208V/120V 3-phase @ 100A = ~36kW total
   - Single-phase 240V @ 100A = ~24kW total
2. **Better load distribution** across phases
3. **Smaller conductors** for equivalent power delivery
4. **More efficient** power distribution in large systems

**Practical Application:**
- Small shows: Single-phase 120/240V sufficient
- Medium shows: 208V three-phase (15-30 amps)
- Large venues/festivals: 480V three-phase (100+ amps) with step-down transformers

### PDU Features for Audio

**Common PDU types:**
1. **Basic distribution:** Input distro box with breakers, splits to multiple outputs
2. **Metered PDU:** Shows current draw per phase, helps balance loads
3. **Switched PDU:** Remote control of individual outlets
4. **Managed PDU:** Network monitoring, remote power cycling, logging

### Safety Notes

- **Never assume voltage!** Always measure with a multimeter
- **208V ≠ 240V:** Some equipment specifies 230V ±10% (207-253V), so 208V works
- **Neutral is not ground:** Even though both go to same point at service entrance
- **Lock out/tag out** when working on power distribution
- **Phase rotation:** Doesn't matter for amplifiers (resistive loads), critical for motors

### Typical Venue Power

| Venue Type | Typical Service | Voltage |
|------------|----------------|---------|
| Club/Small Theater | Single-phase | 120/240V |
| Medium Theater | Three-phase | 208V/120V |
| Large Theater/Arena | Three-phase | 480V/277V |
| Festival Main Stage | Three-phase | 480V or higher |

### Converting Three-Phase Voltages

**If venue has 480V but amps need 208V:**
- Use a **step-down transformer** (480V primary → 208V/120V secondary)
- Transformer is three-phase input, three-phase output
- Common for touring systems in industrial venues
