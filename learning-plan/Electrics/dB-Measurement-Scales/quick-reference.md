# dB Measurement Scales — Quick Reference

Fast lookup for formulas, conversions, and key values.

---

## Core Formulas

**Power (watts, milliwatts):**
```
dB = 10 × log₁₀(P₁ / P₂)
```

**Field quantities (voltage, sound pressure):**
```
dB = 20 × log₁₀(V₁ / V₂)
```

---

## All Scales at a Glance

| Scale | Reference | Type | Formula | Primary Use |
|-------|-----------|------|---------|-------------|
| **dBu** | 0.775V RMS | Voltage | `20 × log₁₀(V / 0.775)` | Pro audio line levels |
| **dBV** | 1V RMS | Voltage | `20 × log₁₀(V / 1.0)` | Consumer audio levels |
| **dBm** | 1 mW | Power | `10 × log₁₀(P / 0.001)` | RF, wireless, fiber optics |
| **dBW** | 1 W | Power | `10 × log₁₀(P / 1.0)` | Amplifier power specs |
| **dB SPL** | 20 µPa | Pressure | `20 × log₁₀(P / 20×10⁻⁶)` | Acoustic measurements |
| **dBFS** | Digital full scale | Amplitude | `20 × log₁₀(sample / max)` | Digital audio metering |

---

## Quick Conversions

### Between Voltage Scales
```
dBu = dBV + 2.2
dBV = dBu − 2.2
```

### Between Power Scales
```
dBm = dBW + 30
dBW = dBm − 30
```

### To Absolute Values

**Voltage:**
```
V = 0.775 × 10^(dBu/20)
V = 1.0 × 10^(dBV/20)
```

**Power:**
```
P(mW) = 10^(dBm/10)
P(W) = 10^(dBW/10)
```

**Sound Pressure:**
```
P(Pa) = 20×10⁻⁶ × 10^(dB_SPL/20)
```

---

## Common dB Multipliers

| dB Change | Voltage × | Power × |
|-----------|-----------|---------|
| +1 dB | 1.12 | 1.26 |
| +3 dB | 1.41 | **2** |
| +6 dB | **2** | 4 |
| +10 dB | 3.16 | **10** |
| +20 dB | **10** | **100** |
| +40 dB | 100 | 10,000 |
| +60 dB | 1,000 | 1,000,000 |

**Memory aids:**
- **+6 dB = double voltage**
- **+3 dB = double power**
- **+10 dB = 10× power** (perceived as 2× louder)

---

## Key Values by Scale

### dBu (Professional Audio)

| dBu | Voltage | Use |
|-----|---------|-----|
| −60 dBu | 0.775 mV | Very low mic level |
| −40 dBu | 7.75 mV | Typical mic level |
| 0 dBu | 0.775V | Reference |
| **+4 dBu** | **1.228V** | **Pro nominal level** |
| +24 dBu | 12.28V | Pro maximum |

### dBV (Consumer Audio)

| dBV | Voltage | Use |
|-----|---------|-----|
| **−10 dBV** | **0.316V** | **Consumer nominal level** |
| 0 dBV | 1.0V | Reference |
| +2.2 dBV | 1.228V | = +4 dBu |

### dBm (Power — RF/Wireless/Fiber)

| dBm | Power | Use |
|-----|-------|-----|
| −30 dBm | 1 µW | Near noise floor |
| 0 dBm | 1 mW | Reference |
| +10 dBm | 10 mW | Typical wireless mic |
| +20 dBm | 100 mW | Strong RF signal |
| +30 dBm | 1 W | = 0 dBW |

### dBW (Amplifier Power)

| dBW | Power | Use |
|-----|-------|-----|
| 0 dBW | 1 W | Reference |
| +10 dBW | 10 W | Small amp |
| +20 dBW | 100 W | Medium amp |
| +27 dBW | 500 W | Large amp |
| +30 dBW | 1 kW | High-power amp |

### dB SPL (Sound Pressure)

| dB SPL | Source | Notes |
|--------|--------|-------|
| 0 | Threshold of hearing | Reference |
| 30 | Quiet library | Very quiet |
| 60 | Normal conversation | Moderate |
| **85** | **OSHA action level** | **Protection recommended** |
| **90** | **Lawn mower** | **OSHA 8-hr limit** |
| 100 | Motorcycle | Very loud |
| 120 | Jet takeoff | Pain threshold |

### dBFS (Digital Audio)

| dBFS | Meaning | Use |
|------|---------|-----|
| **0 dBFS** | **Maximum** | **Ceiling — clipping above** |
| −1 dBFS | Just below max | Broadcast peak limit |
| −6 dBFS | Half max voltage | Healthy peak |
| **−18 dBFS** | **Common nominal** | **Aligns with +4 dBu** |
| −96 dBFS | 16-bit noise floor | Theoretical minimum |
| −144 dBFS | 24-bit noise floor | Theoretical minimum |

---

## Critical Level Differences

### Professional vs Consumer Gap
```
Professional:  +4 dBu  = 1.228V
Consumer:      −10 dBV = 0.316V
Difference:    11.8 dB (≈ 4× voltage)
```

### Digital-to-Analog Alignment

| Standard | Alignment |
|----------|-----------|
| EBU R68 | 0 dBu = −18 dBFS |
| SMPTE RP-155 | +4 dBu = −20 dBFS |
| Common default | +4 dBu = −18 dBFS |

---

## Acoustic Calculations

### Inverse Square Law
```
SPL₂ = SPL₁ − 20 × log₁₀(d₂ / d₁)

Distance doubles = −6 dB SPL
```

**Examples:**
```
94 dB @ 1m  →  88 dB @ 2m  →  82 dB @ 4m  →  76 dB @ 8m
```

### Adding Identical Sound Sources
```
dB increase = 10 × log₁₀(number of sources)

2 sources = +3 dB
4 sources = +6 dB
10 sources = +10 dB
```

---

## Typical AV Signal Levels

| Point in Signal Chain | Level | Scale |
|----------------------|-------|-------|
| Microphone output | −50 to −20 dBu | dBu |
| Mic preamp output | −10 to +4 dBu | dBu |
| **Pro line level** | **+4 dBu** | **dBu** |
| **Consumer line level** | **−10 dBV** | **dBV** |
| Power amp input | +4 dBu (for full output) | dBu |
| Power amp output | 100-1000W | Watts/dBW |
| Speaker SPL | 85-100 dB @ 1W/1m | dB SPL |

---

## Typical System Specifications

| Spec | Typical Value | Scale |
|------|---------------|-------|
| Mixer output (nominal) | +4 dBu | dBu |
| Mixer output (max) | +20 to +24 dBu | dBu |
| Amplifier sensitivity | +4 dBu for full rated output | dBu |
| Speaker sensitivity | 85-100 dB SPL @ 1W/1m | dB SPL |
| Background noise (conference room) | 30-35 dBA | dBA |
| Background noise (theater) | 25-30 dBA | dBA |
| SNR (good mixer) | >90 dB | dB |
| Digital peak limit | −1 to −3 dBFS | dBFS |
| Wireless transmitter power | 10-50 mW (10-17 dBm) | dBm |

---

## When to Use Which Scale

| Situation | Use |
|-----------|-----|
| Pro mixer levels | **dBu** |
| Consumer gear levels | **dBV** |
| DAW/digital recorder meters | **dBFS** |
| Amplifier power | **dBW or Watts** |
| Speaker output | **dB SPL** |
| Room noise | **dBA** |
| Wireless transmitters | **dBm** |
| Fiber optic levels | **dBm** |

---

*For detailed explanations, see notes.md*
