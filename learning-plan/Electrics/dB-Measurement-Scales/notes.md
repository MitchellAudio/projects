# dB Measurement Scales

Comprehensive notes on the different decibel reference standards used in audio, electrical, and AV systems.

---

## Table of Contents

1. [What is a Decibel?](#1-what-is-a-decibel)
2. [Why Different dB Scales Exist](#2-why-different-db-scales-exist)
3. [Voltage-Referenced dB Scales](#3-voltage-referenced-db-scales)
4. [Power-Referenced dB Scales](#4-power-referenced-db-scales)
5. [Sound Pressure dB Scales](#5-sound-pressure-db-scales)
6. [Digital Audio dB Scales](#6-digital-audio-db-scales)
7. [Comparison and Conversion](#7-comparison-and-conversion)
8. [Practical Applications in AV](#8-practical-applications-in-av)

---

## 1. What is a Decibel?

A decibel (dB) is a **logarithmic ratio** between two values. On its own, dB is a *relative* measurement — it only tells you the difference between two levels. It does not represent an absolute value unless paired with a **reference point**.

### Core Formulas

**For power quantities (watts, milliwatts):**
```
dB = 10 × log₁₀(P₁ / P₂)
```

**For field quantities (voltage, sound pressure):**
```
dB = 20 × log₁₀(V₁ / V₂)
```

> The 20× multiplier for voltage/pressure comes from the fact that power is proportional to voltage squared: P = V²/R. When you apply the log rule, the exponent of 2 becomes a multiplier, so 10 × 2 = 20.

### Why Logarithmic?

- Human hearing perceives loudness logarithmically, not linearly
- Audio signals span enormous ranges (a whisper to a jet engine = ~1,000,000:1 in pressure)
- Logarithmic scales compress these ranges into manageable numbers
- Makes gain/loss calculations simple addition and subtraction

**Example:**
```
An amplifier with 20dB gain followed by a cable with 3dB loss:
Total = +20 + (−3) = +17dB

Without logarithms, this would be:
Amplifier gain: ×10 voltage
Cable loss: ×0.707 voltage
Total: 10 × 0.707 = ×7.07 voltage
```

---

## 2. Why Different dB Scales Exist

A plain "dB" value is meaningless without context because it's only a ratio. To express an **absolute level**, you need a **reference point**. Different industries and applications chose different reference points based on what was practical and useful, resulting in multiple dB scales.

**The suffix tells you the reference:**
- dB**u** → reference is 0.775V
- dB**V** → reference is 1V
- dB**m** → reference is 1 milliwatt
- dB**W** → reference is 1 watt
- dB **SPL** → reference is 20 micropascals
- dB**FS** → reference is digital full scale

---

## 3. Voltage-Referenced dB Scales

### 3.1 dBu (decibels referenced to 0.775 volts)

**Reference:** 0.775V RMS (unloaded)

**Origin:** The reference voltage of 0.775V was chosen because 0.775V across a 600Ω load dissipates exactly 1 milliwatt of power. Historically, telephone and broadcast systems used 600Ω impedance, so this reference tied voltage and power together neatly. The "u" stands for "unloaded" or "unterminated," meaning the measurement is purely voltage regardless of impedance.

**Formula:**
```
dBu = 20 × log₁₀(V / 0.775)
```

**Key Values:**

| dBu | Voltage (RMS) | Context |
|-----|---------------|---------|
| −60 dBu | 0.000775V (0.775mV) | Very low mic level |
| −40 dBu | 0.00775V (7.75mV) | Typical mic level |
| −20 dBu | 0.0775V (77.5mV) | Strong mic level |
| −10 dBu | 0.245V | Consumer semi-pro crossover |
| 0 dBu | 0.775V | Reference level |
| +4 dBu | 1.228V | **Professional nominal operating level** |
| +24 dBu | 12.28V | Typical professional maximum (clipping) |

**Where You'll See dBu:**
- Professional audio mixing consoles (meters, specifications)
- Outboard audio processors (compressors, EQs, etc.)
- DSP input/output level specifications
- Pro audio signal generators and test equipment

**Important:** +4 dBu is the **standard professional nominal operating level**. When a pro audio device says its output is "+4," it means +4 dBu = 1.228V RMS.

---

### 3.2 dBV (decibels referenced to 1 volt)

**Reference:** 1V RMS

**Origin:** A simpler, more intuitive reference — just 1 volt. Widely used in consumer audio and some test equipment.

**Formula:**
```
dBV = 20 × log₁₀(V / 1.0)
```

**Key Values:**

| dBV | Voltage (RMS) | Context |
|-----|---------------|---------|
| −60 dBV | 0.001V (1mV) | Very low level |
| −40 dBV | 0.01V (10mV) | Typical mic level |
| −10 dBV | 0.316V | **Consumer nominal operating level** |
| 0 dBV | 1.0V | Reference level |
| +2.2 dBV | 1.228V | = +4 dBu (same voltage) |
| +20 dBV | 10V | High output level |

**Where You'll See dBV:**
- Consumer audio equipment specifications
- Some test equipment
- Hi-fi amplifier specifications
- Headphone amplifiers

**Important:** −10 dBV (0.316V) is the **standard consumer nominal operating level**. When consumer gear says "−10," it means −10 dBV.

---

### 3.3 dBu vs dBV: The Relationship

These two scales measure the same thing (voltage) but with different references. The fixed offset between them is:

```
dBu = dBV + 2.2 dB

Because:
20 × log₁₀(1.0 / 0.775) = 20 × log₁₀(1.29) = 2.2 dB
```

**The Pro vs Consumer Level Gap:**

| Standard | Nominal Level | Voltage |
|----------|--------------|---------|
| Professional (+4 dBu) | +4 dBu = +1.8 dBV | 1.228V |
| Consumer (−10 dBV) | −10 dBV = −7.8 dBu | 0.316V |
| **Difference** | **11.8 dB** | **~4× voltage** |

This ~12 dB difference is why you need to adjust gain when connecting consumer equipment to professional systems (or vice versa). Without compensation:
- Consumer into pro: signal is ~12 dB too low (quiet, poor SNR)
- Pro into consumer: signal is ~12 dB too hot (distortion, clipping)

---

## 4. Power-Referenced dB Scales

### 4.1 dBm (decibels referenced to 1 milliwatt)

**Reference:** 1 milliwatt (0.001W)

**Origin:** Developed for telephone systems where signals were transmitted over long distances and power levels needed to be carefully managed. Originally defined as power dissipated in a 600Ω load, but now used as an absolute power measurement regardless of impedance.

**Formula:**
```
dBm = 10 × log₁₀(P / 0.001)
```

**Key Values:**

| dBm | Power | Voltage across 600Ω | Context |
|-----|-------|---------------------|---------|
| −30 dBm | 0.001 mW (1 µW) | Very low signal | Near noise floor |
| −10 dBm | 0.1 mW | 0.245V | Weak signal |
| 0 dBm | 1 mW | 0.775V | Reference (= 0 dBu across 600Ω) |
| +4 dBm | 2.51 mW | 1.228V | Pro audio nominal (600Ω systems) |
| +10 dBm | 10 mW | 2.45V | Strong signal |
| +20 dBm | 100 mW | 7.75V | Very high signal |
| +30 dBm | 1 W | — | 1 watt (= 0 dBW) |

**Where You'll See dBm:**
- RF/wireless systems (transmitter power, receiver sensitivity)
- Network equipment (fiber optic power levels)
- Legacy broadcast and telephone equipment
- Test equipment measurements

**dBm vs dBu — When They're the Same:**

When impedance is 600Ω, dBm and dBu give the **same number** because 0.775V across 600Ω = 1mW. In modern audio (high impedance, bridging connections), dBu is preferred because impedance is not a fixed value.

```
dBm = dBu  ONLY when impedance = 600Ω
```

> In modern AV, most audio connections use bridging (high impedance input, low impedance output). The load impedance varies, so power-based measurements (dBm) are less meaningful. Use dBu for voltage-based level references in modern systems.

---

### 4.2 dBW (decibels referenced to 1 watt)

**Reference:** 1 watt

**Formula:**
```
dBW = 10 × log₁₀(P / 1.0)
```

**Key Values:**

| dBW | Power | Context |
|-----|-------|---------|
| −30 dBW | 0.001W (1mW) | = 0 dBm |
| 0 dBW | 1W | Reference level |
| +3 dBW | 2W | Double power |
| +10 dBW | 10W | Small amplifier |
| +20 dBW | 100W | Medium amplifier |
| +27 dBW | 500W | Large amplifier |
| +30 dBW | 1,000W (1kW) | High-power amplifier |
| +40 dBW | 10,000W (10kW) | Very high power |

**Where You'll See dBW:**
- Amplifier power specifications
- Speaker power handling
- Large-scale sound system design
- RF transmitter power (alternative to dBm for higher powers)

**dBW to dBm Conversion:**
```
dBm = dBW + 30

Because 1W = 1000mW, and 10 × log₁₀(1000) = 30
```

---

## 5. Sound Pressure dB Scales

### 5.1 dB SPL (decibels Sound Pressure Level)

**Reference:** 20 micropascals (20 µPa = 0.00002 Pa)

**Origin:** 20 µPa is approximately the **threshold of human hearing** — the quietest sound a healthy young ear can detect at 1 kHz. This makes 0 dB SPL the boundary of audibility.

**Formula:**
```
dB SPL = 20 × log₁₀(P / 20 µPa)
```

**Key Values:**

| dB SPL | Sound Source | Notes |
|--------|-------------|-------|
| 0 | Threshold of hearing | Reference level |
| 20 | Quiet studio, rustling leaves | Very quiet |
| 30 | Quiet library | Whisper range |
| 40-50 | Quiet office, moderate rainfall | Background noise |
| 60 | Normal conversation (at 1m) | Moderate |
| 70 | Busy restaurant, vacuum cleaner | Starting to get loud |
| 80 | Busy street, alarm clock | Prolonged exposure risk |
| 85 | **OSHA action level** | Hearing protection recommended |
| 90 | Lawn mower, subway train | **OSHA PEL (8-hour TWA)** |
| 100 | Motorcycle, hand drill | Very loud |
| 110 | Rock concert, power saw | Risk of immediate damage |
| 120 | Jet takeoff (at 100m), thunder | **Threshold of pain** |
| 130 | Jet takeoff (at 25m) | Physical discomfort |
| 140+ | Firearms, explosions | Instant hearing damage |

**Weighting Filters:**

SPL meters often apply frequency weighting to approximate human hearing perception:

| Weighting | Description | Use |
|-----------|-------------|-----|
| **dBA** | A-weighting, de-emphasizes low and very high frequencies | Most common, noise regulations, OSHA |
| **dBC** | C-weighting, nearly flat, slight HF rolloff | Peak measurements, low-frequency assessment |
| **dBZ** (or dB Linear) | No weighting, flat response | Acoustic measurement, analysis |

**Important for AV:**
- **dBA** is the standard for noise regulations and background noise specifications
- Background noise levels in AV specs are typically given in dBA or NC (Noise Criteria)
- OSHA hearing protection requirements are based on dBA measurements

### 5.2 dB SPL Relationships

**Perception vs. Measurement:**

| Change in dB SPL | Power Change | Perceived Loudness |
|-------------------|-------------|-------------------|
| +1 dB | 1.26× | Barely perceptible |
| +3 dB | 2× power | Just noticeable |
| +6 dB | 4× power | Clearly noticeable |
| +10 dB | 10× power | **Perceived as "twice as loud"** |
| +20 dB | 100× power | Perceived as 4× as loud |

**Inverse Square Law:**
```
Every doubling of distance from a point source = −6 dB SPL

SPL₂ = SPL₁ − 20 × log₁₀(d₂ / d₁)

Example: 
Speaker is 94 dB SPL at 1m
At 2m: 94 − 20 × log₁₀(2/1) = 94 − 6 = 88 dB SPL
At 4m: 94 − 20 × log₁₀(4/1) = 94 − 12 = 82 dB SPL
At 8m: 94 − 20 × log₁₀(8/1) = 94 − 18 = 76 dB SPL
```

**Adding Sound Sources:**
```
Two identical sources = +3 dB
Four identical sources = +6 dB
Ten identical sources = +10 dB

Formula: dB increase = 10 × log₁₀(number of sources)
```

---

## 6. Digital Audio dB Scales

### 6.1 dBFS (decibels Full Scale)

**Reference:** The maximum digital level (full scale = all bits at maximum)

**Origin:** In digital audio, there is an absolute maximum level defined by the bit depth. You cannot exceed 0 dBFS — there are no more bits available to represent a higher value. Going above 0 dBFS causes **hard clipping** (distortion).

**Formula:**
```
dBFS = 20 × log₁₀(sample value / maximum sample value)
```

**Key Values:**

| dBFS | Meaning | Context |
|------|---------|---------|
| 0 dBFS | **Maximum digital level** | Absolute ceiling, clipping occurs above |
| −1 dBFS | Just below maximum | Broadcast peak limit (some standards) |
| −6 dBFS | Half of maximum voltage | Healthy peak level |
| −12 dBFS | Quarter of maximum voltage | Good working level for mixing |
| −18 dBFS | Typical nominal operating level | Aligns with +4 dBu in many converters |
| −20 dBFS | Common alignment point | EBU R68 standard (0 dBu = −18 dBFS) |
| −24 dBFS | Conservative operating level | SMPTE RP-155 (+4 dBu = −20 dBFS) |
| −60 dBFS | Very low level | Near noise floor for 16-bit |
| −96 dBFS | Theoretical noise floor (16-bit) | 16 bits × 6 dB/bit = 96 dB range |
| −144 dBFS | Theoretical noise floor (24-bit) | 24 bits × 6 dB/bit = 144 dB range |

**Where You'll See dBFS:**
- DAW meters (Pro Tools, Logic, etc.)
- Digital mixer meters
- Digital audio recorder meters
- DSP processor meters
- Broadcast level standards

### 6.2 Headroom in Digital vs Analog

This is a critical concept:

```
ANALOG:                           DIGITAL:
                                  
+24 dBu ── Clipping              0 dBFS ── HARD CLIPPING (no going above)
   ↑                                ↑
   │ ~20 dB headroom                │ ~18 dB headroom (typical)
   ↓                                ↓
+4 dBu ── Nominal level          −18 dBFS ── Nominal level
   ↑                                ↑
   │ ~70+ dB to noise floor         │ ~78 dB to noise floor (16-bit)
   ↓                                │ ~126 dB to noise floor (24-bit)
−66 dBu ── Noise floor              ↓
                                  −96 dBFS ── Noise floor (16-bit)
                                  −144 dBFS ── Noise floor (24-bit)
```

**Key Difference:** Analog systems can exceed their nominal level with increasing distortion (soft clipping). Digital systems have a **hard ceiling** at 0 dBFS — exceeding it causes immediate harsh distortion.

### 6.3 Digital-to-Analog Alignment

When connecting digital and analog systems, you must align the reference levels:

| Standard | Alignment |
|----------|-----------|
| EBU R68 (European broadcast) | 0 dBu = −18 dBFS |
| SMPTE RP-155 (US broadcast) | +4 dBu = −20 dBFS |
| AES | No single standard — manufacturer dependent |
| Common pro audio default | +4 dBu = −18 dBFS or −20 dBFS |

**Why This Matters:**

If a digital recorder is set to EBU alignment (0 dBu = −18 dBFS) and you feed it a +4 dBu signal:
```
+4 dBu input → −14 dBFS on the digital meter
(−18 + 4 = −14 dBFS)
Headroom remaining: 14 dB before digital clipping
```

---

## 7. Comparison and Conversion

### 7.1 Quick Reference: All Scales at a Glance

| Scale | Reference | Quantity Measured | Formula Multiplier | Primary Use |
|-------|-----------|-------------------|--------------------|-------------|
| dBu | 0.775V | Voltage | 20× | Pro audio levels |
| dBV | 1V | Voltage | 20× | Consumer audio levels |
| dBm | 1 mW | Power | 10× | RF, telecom, fiber |
| dBW | 1 W | Power | 10× | Amplifier power |
| dB SPL | 20 µPa | Sound pressure | 20× | Acoustic levels |
| dBA | 20 µPa (A-weighted) | Sound pressure | 20× | Noise regulations |
| dBFS | Digital full scale | Digital amplitude | 20× | Digital audio metering |

### 7.2 Common Conversions

**Voltage scales:**
```
dBu = dBV + 2.2
dBV = dBu − 2.2
```

**Power scales:**
```
dBm = dBW + 30
dBW = dBm − 30
```

**Voltage to absolute value:**
```
Voltage = 0.775 × 10^(dBu/20)
Voltage = 1.0 × 10^(dBV/20)
```

**Power to absolute value:**
```
Power (mW) = 10^(dBm/10)
Power (W) = 10^(dBW/10)
```

### 7.3 Handy dB Rules of Thumb

| dB Change | Voltage Multiplier | Power Multiplier |
|-----------|--------------------|------------------|
| +1 dB | ×1.12 | ×1.26 |
| +3 dB | ×1.41 | **×2** (double power) |
| +6 dB | **×2** (double voltage) | ×4 |
| +10 dB | ×3.16 | **×10** |
| +20 dB | **×10** | **×100** |
| +40 dB | ×100 | ×10,000 |
| +60 dB | ×1,000 | ×1,000,000 |

> **Memory aid:** +6 dB = double voltage, +3 dB = double power. This is because power is proportional to voltage squared (doubling voltage = quadrupling power = +6 dB power = +6 dB voltage).

---

## 8. Practical Applications in AV

### 8.1 Signal Flow Level Reference

A typical AV signal path with approximate levels:

```
Microphone output:        −50 to −20 dBu
Mic preamp output:        −10 to +4 dBu (adjustable gain)
Pro line level:           +4 dBu nominal
Consumer line level:      −10 dBV nominal
DSP input/output:         +4 dBu nominal (pro) / −10 dBV (consumer)
Power amplifier input:    +4 dBu for full output (typical)
Power amplifier output:   Measured in watts/dBW at speaker impedance
Speaker output:           Measured in dB SPL
```

### 8.2 When to Use Which Scale

| Situation | Use This Scale |
|-----------|---------------|
| Setting levels on a pro mixer | dBu |
| Checking levels on a DAW | dBFS |
| Specifying amplifier power | dBW or watts |
| Measuring room noise | dBA (dB SPL, A-weighted) |
| Checking wireless mic transmitter | dBm |
| Testing fiber optic signal levels | dBm |
| Comparing consumer to pro gear | dBV and dBu (know the 11.8 dB gap) |
| Measuring speaker output | dB SPL |

### 8.3 Common AV System Specifications Using dB

| Specification | Typical Value | Scale |
|---------------|---------------|-------|
| Mixer output level (nominal) | +4 dBu | dBu |
| Mixer output level (max) | +20 to +24 dBu | dBu |
| Amplifier input sensitivity | +4 dBu (for full rated output) | dBu |
| Speaker sensitivity | 85-100 dB SPL @ 1W/1m | dB SPL |
| Background noise target (conference room) | 30-35 dBA | dBA |
| Background noise target (theater) | 25-30 dBA | dBA |
| Signal-to-noise ratio (good mixer) | >90 dB | dB (ratio) |
| Digital recording peak limit | −1 to −3 dBFS | dBFS |
| Wireless mic transmitter power | 10-50 mW (10-17 dBm) | dBm |

---

*Last updated: February 2026*
