# Notes: SMAART

## What Is SMAART?

- **SMAART (System Measurement Acoustic Analysis Real-Time Tool)** — the industry standard software for live sound system measurement and alignment
- Developed by **Rational Acoustics** (founded by Jamie Anderson and Adam Black)
- Used to measure, analyse, and optimise sound systems in real time during setup and show
- Current version: **SMAART v9** (as of 2024)

### What SMAART Does

- Measures the **transfer function** of a sound system — comparing what you send to the system vs. what comes out into the room
- Measures **Real-Time Analysis (RTA)** — the frequency content of a live signal
- Measures **impulse response** — how a system or room responds to a short burst of energy
- Finds **delay times** — how much time offset exists between the reference signal and the measured signal
- Measures **coherence** — how reliable the measurement is at each frequency

### Why SMAART Matters for Live Sound

- Without measurement, you are tuning by ear in a room you may not know, with speakers you may not have used before
- SMAART gives you objective, repeatable data about what the system is actually doing
- It takes the guesswork out of EQ, delay, and level adjustments
- It is expected knowledge for system engineers at the professional level

---

## Core Measurement Modes

### 1. Transfer Function (Dual-FFT)

- **Transfer function** — compares an electrical reference signal (what you send) to a measured signal (what comes back from a microphone) and shows you what the system *changed*
- This is the most important mode in SMAART for system tuning

#### How It Works

1. You route a copy of the signal feeding the speaker (the **reference**) into one input of SMAART
2. You place a **measurement microphone** in the room and route it into the second input
3. SMAART compares the two signals using a **dual-FFT** (Fast Fourier Transform) calculation
4. The result shows you magnitude (level at each frequency) and phase — essentially the system's "fingerprint"

#### What the Transfer Function Tells You

- **Magnitude** — how much the system boosts or cuts each frequency relative to the reference. A flat line means the system reproduces the input exactly. Peaks mean resonances or room gain; dips mean cancellations
- **Phase** — the time/phase relationship at each frequency. Phase wrapping and group delay tell you about filter behaviour and alignment issues
- **Coherence** — a confidence metric (0 to 1) at each frequency. High coherence (close to 1) means the measurement is reliable at that frequency. Low coherence means noise, reflections, or other interference is corrupting the measurement there

#### Key Concept: The Reference Signal

- The reference must be a copy of the *electrical* signal feeding the system — not the acoustic signal
- Common sources for the reference:
  - **Direct output** from the console (pre-processing matrix or aux)
  - **Signal generator** built into SMAART (pink noise)
  - **Y-split** from the system processor output
- The reference allows SMAART to isolate what the *system and room* are doing, independent of the source material

### 2. Spectrum / RTA (Single-FFT)

- **RTA (Real-Time Analyser)** — shows the frequency content of a single signal in real time
- Does NOT compare to a reference — it just shows what is there
- Uses a single FFT to break the signal into frequency bands and display the level of each

#### Uses for RTA

- Checking the spectrum of programme material (music, speech)
- Monitoring ambient noise levels across frequency
- Quick "is the system making sound?" check
- Verifying pink noise output is actually flat before using it for measurement
- **Not** the primary tool for system EQ — transfer function is far more informative because it separates the system's response from the source material

### 3. Impulse Response

- Shows how the system responds to a very short, sharp input (an impulse)
- Displays energy over time — you can see:
  - The **direct sound** arrival (main peak)
  - **Reflections** arriving later (smaller peaks)
  - **Reverb tail** (gradually decaying energy)
- Useful for:
  - Verifying delay times between speakers
  - Identifying strong early reflections
  - Measuring RT60 (reverberation time)

---

## The Delay Finder

### What Is the Delay Finder?

- The **delay finder** measures the propagation delay between the reference signal and the measured signal
- It tells you exactly how many milliseconds it takes for sound to travel from the speaker to the measurement microphone
- This is essential for setting delay times on fill speakers, subwoofers, and delay towers

### How It Works

1. SMAART cross-correlates the reference and measurement signals
2. It finds the time offset that produces the maximum correlation — this is the propagation delay
3. You can read the delay directly in milliseconds

### How to Use It

1. Set up your transfer function measurement (reference from console, mic in the room)
2. Open the delay finder and let SMAART acquire a reading
3. The delay shown is the **total propagation time** from the system output to the microphone
4. Use this value to set the internal delay offset in SMAART (so the transfer function traces align correctly)
5. Use it to calculate speaker delay offsets (see Time Alignment notes)

### Delay Finder and Internal Delay

- SMAART needs to know the propagation delay so it can correctly align the reference and measurement signals for the transfer function calculation
- If the delay is wrong, the phase trace will be wildly wrapping (because SMAART is comparing misaligned signals)
- After finding the delay, you enter it as the **measurement delay** for that input — SMAART then compensates internally

---

## Coherence

### What Is Coherence?

- **Coherence** — a measure of how linearly related the reference and measurement signals are at each frequency
- Scale of **0 to 1** (or 0% to 100%)
- **High coherence (> 0.8)** = the measurement is reliable at that frequency — the measured signal is dominated by the direct sound from the system
- **Low coherence (< 0.5)** = the measurement is unreliable — noise, reflections, or other sources are dominating at that frequency

### What Causes Low Coherence?

- **Background noise** — audience, HVAC, other sources that are not correlated with your reference signal
- **Strong reflections** — multiple arrivals of the same signal from different paths. Each reflection changes the phase relationship, reducing coherence
- **Mic position too far from speakers** — the direct-to-reflected sound ratio drops
- **Wrong delay setting** — if SMAART's internal delay compensation is wrong, coherence drops across the board
- **Very low frequencies** — long wavelengths are heavily influenced by room modes, reducing coherence naturally

### How to Read Coherence

- Display coherence as a trace overlaid on the transfer function
- **Trust the magnitude and phase data only where coherence is high**
- Where coherence drops below ~0.5, the data at those frequencies is suspect — do not EQ based on unreliable data
- If coherence is low everywhere, check: delay setting, signal level, mic placement, or background noise

---

## Measurement Setup

### Required Equipment

- **SMAART software** (laptop running SMAART v8 or v9)
- **Audio interface** — at least 2 inputs (one for reference, one for measurement mic). Must support ASIO (Windows) or Core Audio (Mac)
- **Measurement microphone** — flat frequency response, omnidirectional, calibrated. Common models:
  - **Rational Acoustics RTA-420** (SMAART's own mic)
  - **Earthworks M23 / M30**
  - **Behringer ECM8000** (budget option, reasonable accuracy)
  - **iSEMcon EMX-7150** (excellent value)
- **Mic preamp** (or built into the audio interface) — must have phantom power (48V)
- **Mic stand and long XLR cable** — you will be placing the mic in various positions around the venue
- **Reference signal routing** — a way to get the console output into SMAART (direct out, aux send, or Y-split)

### Signal Routing

```
Console output ──────→ System processor → Amp → Speaker
         │
         └──→ SMAART Reference Input (Input 1)

Measurement mic ──→ Preamp ──→ SMAART Measurement Input (Input 2)
```

### Measurement Microphone Placement

- **Start at the mix position** — this is the most important position to optimise
- Point the mic at the speaker (or straight up for omni mics — follow manufacturer guidance)
- **Height matters** — measure at ear height of the audience (seated: ~1.2 m, standing: ~1.6 m)
- Take measurements at **multiple positions** — no single position tells the whole story
- Typical positions: mix position, front/centre, mid-left/right, rear of coverage area, under balcony
- Avoid placing the mic right next to walls or reflective surfaces — you will see reflections dominate

---

## Using SMAART for System Alignment

### Workflow Overview

1. **Set up routing** — reference from console, measurement mic in position
2. **Play pink noise** (or programme material) through the system
3. **Find the delay** — use the delay finder to measure propagation time to the mic
4. **Set the internal delay** in SMAART to match
5. **Check coherence** — make sure the measurement is reliable
6. **Read the transfer function** — look at magnitude and phase
7. **Make adjustments** — EQ, delay, level, polarity as needed
8. **Move the mic** — repeat at additional positions to verify coverage

### What to Look for in the Transfer Function

#### Magnitude

- **Overall shape** — is the system's response reasonably flat across the audible range?
- **Peaks** — narrow peaks often indicate room resonances or comb filtering. Wide peaks might be system-related (EQ, crossover)
- **Dips** — narrow dips often indicate comb filtering from reflections. Wide dips might be coverage issues
- **Comb filtering pattern** — regularly spaced peaks and dips indicate a reflection at a fixed time offset (see Time Alignment notes)
- **Low-frequency build-up** — common near walls and boundaries; may indicate room mode excitation

#### Phase

- **Smooth, gradually wrapping phase** — indicates a well-aligned system with correct delay compensation
- **Wildly erratic phase** — check your delay setting, it is probably wrong
- **Phase shift at crossover points** — expected; the key is that the two frequency ranges are in phase at the crossover frequency

### Common EQ Mistakes to Avoid

- **Do not chase every dip** — dips caused by comb filtering (reflections) cannot be fixed with EQ. Boosting at a null just wastes amplifier headroom
- **Do not over-EQ** — gentle, broad corrections (parametric Q of 1–3) are more effective than narrow surgical cuts
- **EQ based on multiple mic positions** — a peak at one position might be a dip at another. EQ what is consistent across positions
- **Fix problems at the source first** — speaker position, aim, delay, and level before reaching for EQ

---

## SMAART-Specific Features

### Averaging

- **Time averaging** — smooths the transfer function over time, reducing the effect of short-term variations. Use 4–8 averages for a stable reading
- **Spatial averaging** — take measurements at multiple positions and average them together. This gives a picture of the system's response across the audience area rather than at a single seat

### SPL Metering

- SMAART v9 includes **SPL metering** with A, C, and Z weightings
- Useful for monitoring show levels and compliance with noise regulations
- Requires a calibrated microphone for accurate absolute SPL readings

### Multi-Measurement

- You can run **multiple measurement channels** simultaneously
- Useful for comparing two speaker systems, or measuring multiple positions without re-routing

---

## Transfer Function vs. RTA: When to Use Each

| | Transfer Function | RTA |
|---|---|---|
| **Requires reference?** | Yes | No |
| **Shows system response?** | Yes — isolates what the system does | No — shows what is in the air |
| **Use for EQ tuning?** | Yes — the primary tool | Only for rough checks |
| **Use for delay finding?** | Yes | No |
| **Use for checking programme content?** | No | Yes |
| **Use for noise monitoring?** | No | Yes |

---

## Common Mistakes

- **Wrong delay setting** — if the delay finder value is not entered correctly, the transfer function phase trace wraps excessively and the magnitude trace is unreliable. Always set delay before reading data
- **Reference signal includes processing** — the reference should be *before* any system EQ or processing. If you take the reference *after* the EQ, the transfer function will not show you what the EQ is doing
- **Mic too far from source** — reflections dominate, coherence drops, data becomes unreliable. Move the mic closer or accept that far-field measurements have lower coherence
- **Measuring with the wrong source** — pink noise gives the most reliable measurements because it has equal energy per octave. Music works but requires more averaging time. Speech is difficult to measure with
- **Confusing RTA with transfer function** — RTA shows the content of the source plus the system. Transfer function removes the source and shows only the system's effect

---

## Relationship to Other Topics

| Concept | Connection |
|---|---|
| **Time Alignment** | SMAART is the primary tool for measuring and setting delays between speakers, subs, and fills |
| **dB Measurement Scales** | SMAART displays magnitude in dB; understanding dB SPL, dBu, and dBFS helps interpret readings |
| **REW** | REW does similar measurements (RTA, impulse response) but is more suited to room acoustics. SMAART is designed for live sound system measurement |
| **Word Clock** | If your audio interface has clock problems, SMAART measurements will show artefacts — make sure the interface is properly clocked |
| **QoS / Managed Switches** | When using Dante-enabled SMAART I/O, your network must be properly configured |

---

## Key Takeaways

- **Transfer function is the primary tool** — it separates the system's response from the source material
- **Always find and set the delay first** — everything else depends on correct delay compensation
- **Trust coherence** — only EQ where coherence is high; low coherence means the data is unreliable
- **Measure at multiple positions** — no single mic position tells the whole story
- **Fix physical problems first** — speaker position, aim, delay, and level before EQ
- **Do not chase comb filter dips** — they are caused by reflections and cannot be fixed with EQ
- **Use a proper measurement microphone** — a flat, calibrated omni mic, not a vocal or instrument microphone

---

## Resources

- [Rational Acoustics — SMAART v9](https://www.rationalacoustics.com/) — official documentation and training
- [Rational Acoustics — SMAART Operator Fundamentals Course](https://www.rationalacoustics.com/training/)
- [SynAudCon — SMAART Training](https://www.synaudcon.com/)
- [Bob McCarthy — Sound Systems: Design and Optimization](https://www.amazon.com/) — the definitive textbook, heavily uses SMAART
- Relate to your notes on [Time Alignment](../../Tech/Time-alignment/notes.md) and [REW](../REW/notes.md)
