# Notes: ADC & DAC Conversions

## What Are ADC and DAC?

- **ADC (Analogue-to-Digital Converter)** — converts a continuous analogue audio signal (voltage) into a stream of discrete digital numbers (samples)
- **DAC (Digital-to-Analogue Converter)** — converts a stream of digital samples back into a continuous analogue signal that can drive speakers or headphones
- These two conversions are the gateway between the analogue world (microphones, speakers, your ears) and the digital world (consoles, processors, recording, Dante)

### Where ADC and DAC Live in a Signal Chain

1. Microphone → preamp → **ADC** → digital processing (console, DSP, network) → **DAC** → amplifier → speaker
2. The quality of these conversions directly affects the audio quality of the entire system
3. Everything between the ADC and DAC is just maths — the conversion points are where real-world imperfections enter

---

## Sampling: Capturing Audio in Time

### What Is Sampling?

- The ADC measures the amplitude (voltage level) of the analogue signal at regular intervals
- Each measurement is called a **sample**
- The number of samples taken per second is the **sample rate** (measured in Hz or kHz)
- At 48 kHz, the ADC captures 48,000 snapshots of the waveform every second

### The Nyquist Theorem (Shannon-Nyquist)

- **Nyquist theorem** — to accurately capture a signal, the sample rate must be at least **twice the highest frequency** in the signal
- The highest frequency that can be represented is called the **Nyquist frequency** — it is exactly half the sample rate
- At **48 kHz sample rate**, the Nyquist frequency is **24 kHz** — well above the ~20 kHz upper limit of human hearing
- At **44.1 kHz** (CD standard), the Nyquist frequency is **22.05 kHz** — just barely above 20 kHz

### What Happens If You Violate Nyquist?

- If a frequency above the Nyquist limit enters the ADC, it does not simply disappear — it **folds back** into the audible range as a false frequency
- This is called **aliasing** — the high frequency "aliases" as a lower frequency that was never in the original signal
- Aliasing sounds harsh, metallic, and inharmonic — it creates frequencies with no musical relationship to the original
- **Example:** at 48 kHz sample rate, a 25 kHz signal (1 kHz above Nyquist) aliases to 23 kHz. A 30 kHz signal aliases to 18 kHz — right in the audible range

### Anti-Aliasing Filter

- To prevent aliasing, the ADC has a **low-pass filter** before the sampling stage called the **anti-aliasing filter**
- This filter must pass everything below ~20 kHz and block everything above the Nyquist frequency (24 kHz at 48 kHz SR)
- The transition band between passband and stopband is very narrow — this is an extremely steep filter
- Early digital audio used analogue "brick-wall" filters that caused phase problems; modern converters use **oversampling** to relax the filter requirements (see below)

---

## Quantisation: Capturing Audio in Amplitude

### What Is Quantisation?

- After sampling captures *when* to measure, **quantisation** captures *how precisely* to measure the amplitude
- The continuous voltage is rounded to the nearest value on a fixed grid of discrete levels
- The number of levels available is determined by the **bit depth**

### Bit Depth and Dynamic Range

| Bit Depth | Number of Levels | Theoretical Dynamic Range |
|---|---|---|
| **16-bit** | 65,536 levels | **96 dB** |
| **24-bit** | 16,777,216 levels | **144 dB** |
| **32-bit float** | ~4.3 billion levels | **~1528 dB** (virtually infinite) |

- **Dynamic range** = the difference between the loudest signal and the noise floor
- Each additional bit adds approximately **6 dB** of dynamic range
- **16-bit** is sufficient for playback (CD quality) but leaves little headroom for processing
- **24-bit** is the professional standard — 144 dB of dynamic range far exceeds what any analogue circuit can achieve (~120 dB for the best preamps)
- **32-bit float** is used internally by DAWs for processing — it cannot clip because the floating-point representation scales automatically

### Quantisation Error (Quantisation Noise)

- Because the ADC rounds each sample to the nearest level, there is always a small error between the actual voltage and the recorded value
- This rounding error is called **quantisation error** or **quantisation noise**
- It sounds like low-level broadband noise (hiss)
- With 16-bit audio, quantisation noise is at -96 dB — audible in very quiet passages
- With 24-bit audio, quantisation noise is at -144 dB — well below the noise floor of any analogue component, effectively inaudible

### Dithering

- **Dither** — a tiny amount of carefully shaped random noise added to the signal *before* quantisation
- Without dither, quantisation error is correlated with the signal — it produces **harmonic distortion** that is more audible and unpleasant than random noise
- Adding dither breaks up this correlation, converting the distortion into a constant, low-level noise floor that is far less objectionable
- **When to dither:** whenever you reduce bit depth (e.g., mixing a 24-bit session down to 16-bit for CD). Dither is applied once, at the final bit-depth reduction
- **Types of dither:** flat (TPDF — Triangular Probability Density Function) is the standard; noise-shaped dither (POW-r, UV22HR) pushes the noise into less audible frequency ranges

---

## Oversampling

### Addressing the Core Confusion

> *"If the output is 48 kHz, how does sampling at a higher rate help — isn't the audio still only captured at 48 kHz?"*

This is the right question to ask. Here is the key insight:

**The audio IS captured at the high internal rate. Every single sample taken at 6 MHz is real.** The ADC genuinely measures the voltage 6 million times per second. The 48 kHz output is then produced by *mathematically discarding* most of those samples in a very controlled way (called decimation). The reason you still get high-quality 48 kHz audio is that the information content of human-audible sound (below 20 kHz) was already fully captured by the high-rate sampling — you just do not need 6 million samples per second to represent it. The extra samples are used to make the anti-aliasing filter trivially easy, and then discarded.

Think of it like taking a very high-resolution photo and then printing it at a smaller size. The detail was genuinely captured — you just don't need all of it at the output size, and having it during capture meant you could use a better lens without worrying about diffraction limits.

---

### What Is Oversampling?

- **Oversampling** — the ADC internally samples at a much higher rate than the final output sample rate
- Expressed as a multiplier: **64×**, **128×**, **256×** oversampling means the internal rate is 64, 128, or 256 times the target rate
- At 48 kHz × 128 = **6.144 MHz** internal sample rate
- At 48 kHz × 64 = **3.072 MHz** internal sample rate

### The Problem Oversampling Solves

Recall from the Nyquist section: to prevent aliasing, the ADC must use an **anti-aliasing filter** to block all frequencies above the Nyquist limit before sampling. At 48 kHz, the Nyquist frequency is 24 kHz. The filter must:
- Pass everything below ~20 kHz with no attenuation (the audible range)
- Block everything above 24 kHz completely (to prevent aliasing)
- Do all of this in just 4 kHz of transition band (from 20 kHz to 24 kHz)

This requires an **extremely steep analogue filter** — called a "brick wall" filter. The problem:
- Steep analogue filters cause significant **phase shift** near the cutoff frequency
- Phase shift in the 15–20 kHz range is audible — it smears transients and affects imaging
- Steep analogue filters are also expensive and component-sensitive
- Early digital audio (1980s CD players) sounded harsh partly because of these brutal analogue filters

### How Oversampling Solves It (ADC Side)

By sampling at 128× the target rate (6.144 MHz instead of 48 kHz), the Nyquist frequency moves to **3.072 MHz**. Now the anti-aliasing filter only needs to:
- Pass everything below ~20 kHz (unchanged)
- Block everything above 3 MHz
- The transition band is now **~3 MHz wide** instead of 4 kHz wide

This is an **incredibly easy filter to build** — a simple, gentle single-pole filter will do it with no audible phase shift whatsoever. The brutal brick-wall analogue filter is gone.

**The process step by step:**

1. **Gentle analogue filter** — a simple low-pass filter removes any content above ~1 MHz. This is easy to build with no audible side effects (the rolloff is nowhere near the audio band)
2. **High-rate sampling** — the ADC samples the signal at 6.144 MHz (128×48 kHz). Every sample is genuine — the chip's comparator fires 6 million times per second
3. **Digital decimation filter** — a sophisticated mathematical filter (FIR/IIR) running in the digital domain then:
   - Applies a perfect brick-wall filter at 20 kHz digitally (easy in digital maths — no phase problems)
   - **Discards** (decimates) the majority of samples, keeping only 1 in every 128
   - The remaining samples are now at 48 kHz, but they carry the full quality of the original capture
4. **Output** — a standard 48 kHz / 24-bit digital audio stream

### A Concrete Worked Example

Imagine the ADC is capturing a 10 kHz sine wave at 48 kHz with 128× oversampling:

- Internal sample rate: **6,144,000 samples/second**
- In one second, the ADC takes **6,144,000 samples** of that 10 kHz sine wave
- A 10 kHz wave completes 10,000 cycles per second
- That means **614 samples per cycle** of the 10 kHz wave at the internal rate
- After decimation (keeping 1 in 128), you have: 6,144,000 ÷ 128 = **48,000 samples/second**
- That is **4.8 samples per cycle** of the 10 kHz wave at the output rate
- Nyquist says you need at least 2 samples per cycle — 4.8 is more than enough
- The 10 kHz sine wave is perfectly represented in the final 48 kHz output

The 6 million samples were real — they were taken. The decimation filter then chose the best 48,000 to keep, having already ensured (via the digital filter) that no aliasing remained.

### Why the Digital Filter Is Better Than the Analogue Filter

| | Analogue Brick-Wall Filter | Digital Decimation Filter |
|---|---|---|
| **Transition band** | 4 kHz (20–24 kHz) | Same task, but digital maths |
| **Phase shift** | Significant near cutoff — audible | Can be **linear phase** (zero phase distortion) |
| **Precision** | Limited by component tolerances | Mathematically exact — no tolerance errors |
| **Temperature drift** | Yes — resistors and capacitors drift | None |
| **Cost** | High for steep filters | Negligible — done in the same chip |
| **Adjustable?** | No | Yes — different filter modes (e.g., linear phase vs minimum phase) |

### FIR vs IIR Decimation Filters

- **FIR (Finite Impulse Response)** — the most common type in oversampling ADCs
  - Has a fixed, finite length — it looks at a window of N past samples and computes a weighted sum
  - Can be designed to have **perfectly linear phase** — all frequencies are delayed by the same amount, so the phase relationship between frequencies is preserved
  - Linear phase FIR filters are the reason modern digital audio does not smear transients
  - **Downside:** long FIR filters add latency — the chip must buffer many samples before it can output the first result (this is the main source of ADC/DAC conversion latency)

- **IIR (Infinite Impulse Response)** — uses feedback (output samples feed back into the calculation)
  - Can achieve steeper roll-off with fewer taps (computationally cheaper)
  - BUT: IIR filters have **non-linear phase** — different frequencies are delayed by different amounts, similar to analogue filters
  - Used in some minimum-latency converters where phase accuracy is traded for lower delay

### Oversampling on the DAC Side

The DAC problem is the mirror image of the ADC problem: you have 48,000 samples per second and need to reconstruct a smooth analogue waveform without staircase artefacts and without a harsh analogue reconstruction filter.

**The process:**

1. **Upsampling (interpolation)** — the digital signal at 48 kHz is mathematically expanded to a higher rate (e.g., 128× = 6.144 MHz) by **inserting new samples between the existing ones**. These new samples are not guesses — they are calculated using an interpolation filter (similar to the decimation filter in reverse) that produces the mathematically correct intermediate values
2. **Digital reconstruction filter** — a steep digital low-pass filter is applied at 20 kHz (at the high internal rate), completely removing everything above the audio band with no phase problems
3. **DAC conversion** — the 6.144 MHz 1-bit (or multi-bit) stream is converted to analogue. Because the sample rate is so high, the "staircase" steps are 128× smaller in time and nearly invisible
4. **Gentle analogue filter** — a simple single-pole filter removes the ultrasonic content of the high-rate output. Because the staircase is already tiny and all audible frequencies are perfectly represented, this filter needs almost no work — it creates no audible phase shift

### Why Oversampling Matters for the Noise Floor

There is a second benefit beyond the filter problem: **noise spreading**.

- Quantisation noise has a fixed total power determined by bit depth (approximately -6.02 × bit depth dB)
- This noise is spread **across the entire frequency range** from 0 Hz to the Nyquist frequency
- At 48 kHz (Nyquist = 24 kHz), the noise is spread across 24 kHz of bandwidth
- At 6.144 MHz internal rate (Nyquist = 3.072 MHz), the same total noise is spread across **3.072 MHz** of bandwidth
- The noise density (noise per Hz) drops by the ratio: 3,072,000 ÷ 24,000 = **128× lower noise density in the audio band**
- In dB: 10 × log₁₀(128) ≈ **21 dB lower noise floor** in the 0–20 kHz audio band
- This effectively adds about 3.5 bits of resolution (21 dB ÷ 6 dB per bit) just from oversampling alone
- When combined with **noise shaping** (deliberately pushing the noise further into ultrasonic frequencies — used in delta-sigma converters), the noise floor improvement is even more dramatic

### Summary

- **The ADC really does sample at 6 MHz.** Those samples are real. Decimation then mathematically reduces them to 48 kHz with no loss of audible information
- **Oversampling moves the anti-aliasing problem** from a difficult analogue domain to an easy digital domain
- **Digital filters can be linear phase** — they do not smear transients like analogue brick-wall filters did
- **The noise floor improves** because quantisation noise is spread across a much wider band
- **Every modern ADC and DAC uses oversampling** — it is not optional in professional audio; it is how all current converter chips work

---

## The DAC: Digital Back to Analogue

### Reconstruction

- The DAC receives a stream of discrete samples and must reconstruct a smooth, continuous analogue waveform
- If you simply output each sample value as a voltage and hold it until the next sample, you get a **staircase waveform** — full of ultrasonic harmonics
- A **reconstruction filter** (low-pass filter) smooths the staircase back into a continuous waveform
- With oversampling, most of this smoothing happens digitally before the final analogue filter, giving a much cleaner result

### DAC Architectures

#### Delta-Sigma (ΔΣ) DAC — The Modern Standard

- **Delta-sigma** is the dominant DAC architecture in virtually all modern professional and consumer audio equipment
- Rather than converting a high-resolution word (e.g., 24 bits) directly to a voltage, it converts the digital signal into an extremely high-speed **1-bit stream** — a rapid sequence of 1s and 0s
- The density of 1s vs 0s in the stream represents the amplitude of the signal at any given moment — this technique is called **pulse density modulation (PDM)**

##### How It Works (Step by Step)

1. **Upsampling** — the input signal (e.g., 48 kHz / 24-bit) is upsampled to a very high sample rate internally (e.g., 3.072 MHz — 64× oversampling)
2. **Delta-sigma modulator** — a feedback loop (integrator + comparator) converts the multi-bit digital signal into a 1-bit PDM stream at the high sample rate. The modulator measures the error between the desired output and what it just output, and corrects continuously
3. **Noise shaping** — the quantisation noise from converting to 1-bit is pushed into ultrasonic frequencies (above 20 kHz) by the feedback loop. The in-band noise floor is dramatically reduced
4. **Analogue low-pass filter** — a simple analogue filter removes the ultrasonic noise and the high-frequency PDM carrier, leaving a clean analogue audio signal

##### Why It Sounds Good

- The noise shaping moves quantisation noise where the ear cannot hear it
- No precision component matching required — just a comparator and an integrator, which are easy to manufacture consistently
- Extremely linear — the 1-bit output is inherently linear (it's either on or off; no component tolerance errors)
- Works beautifully at high oversampling ratios — the more you oversample, the more noise you can push out of band

##### Limitations

- The modulator feedback loop can become unstable with large input signals — this is called **modulator clipping** and sounds harsher than traditional clipping
- Very high-order modulators (needed for best performance) are mathematically complex to design
- The 1-bit output requires a precise analogue filter — any resonance in the filter affects the sound

#### R-2R Ladder DAC — The Classic Architecture

- Uses a precision resistor network built from just two resistor values: **R** and **2R**
- Each bit of the digital word controls a switch that connects a precision current source to the ladder network
- The resistor network sums the weighted currents from each bit, producing an analogue voltage directly proportional to the digital value
- **MSB (Most Significant Bit)** contributes half the full-scale voltage; each lower bit contributes half of the bit above it

##### How the Ladder Works

```
Bit 7 (MSB) ── 2R ──┐
                     ├── Output voltage
Bit 6 ─────── 2R ──┤
                     │
Bit 5 ─────── 2R ──┤   R connects rungs together
...                  │
Bit 0 (LSB) ── 2R ──┘
```

- At each node, a resistor of value R connects down the ladder, creating a voltage divider chain
- Each switch contributes a current exactly half the current of the switch above it, corresponding to the binary weighting of each bit
- The total current at the output is the sum of all active bit currents — this directly represents the digital value as an analogue voltage

##### Practical Considerations

- Requires very precise resistor values (0.01% tolerance or better) — even small mismatches cause **differential non-linearity (DNL)** errors that add distortion
- Manufacturing high-precision resistor networks at 24-bit accuracy is extremely difficult and expensive
- Modern R-2R DACs achieve high linearity through laser-trimmed resistor networks and calibration
- **Why audiophiles like R-2R:** the conversion is direct — no noise shaping, no PDM, no feedback loops. The output is a straightforward weighted sum. Some argue this produces a more "natural" sound with different distortion characteristics
- **Used in:** Schiit Audio (Bifrost, Yggdrasil), Soekris, T+A DACs, some Analog Devices and Texas Instruments professional chipsets

##### Limitations

- Far more expensive per channel than delta-sigma at equivalent resolution
- Component matching is critical — temperature drift can cause errors if resistors age differently
- Maximum practical resolution is limited by achievable component precision (~20–22 bits of real linearity)

#### Current Steering DAC

- A variant of the R-2R concept, but using **switched current sources** instead of resistors
- Each bit controls a matched current source that is steered either to the output or to a reference (ground/supply)
- The output current is the sum of all active current sources
- **Advantage over R-2R:** current sources are easier to match precisely than resistors, and switching speed is faster
- Used extensively in high-speed DACs (video, RF, and high-performance audio chipsets)
- **I/V conversion:** the summed current must be converted to voltage by a transimpedance amplifier (TIA/op-amp with feedback resistor) — the quality of this I/V stage significantly affects sound quality in professional implementations

#### Output Stages — How the DAC Signal Reaches Your Ears

- After conversion, the raw DAC output is a low-level, often **differential** signal — two complementary signals (+ and −) rather than a single-ended signal
- **Differential outputs** — cancel common-mode noise and reduce distortion; used in professional balanced connections (XLR)
- **Single-ended output** — combines the + and − signals (or uses just the + side) for unbalanced connections (RCA, TRS consumer)
- The output stage typically includes:
  1. **I/V conversion** (if current-output DAC) — op-amp converts current to voltage
  2. **Low-pass filter** — removes ultrasonic noise and PDM carrier (analogue reconstruction filter)
  3. **Output buffer** — provides the current drive needed to connect to the next stage (preamp, amplifier input) without loading the DAC
- The quality of the output stage op-amp, power supply, and PCB layout often matters as much as the DAC chip itself

#### Comparison Summary

| | Delta-Sigma | R-2R Ladder | Current Steering |
|---|---|---|---|
| **Architecture** | 1-bit PDM + noise shaping | Resistor network | Switched current sources |
| **Cost** | Low | High | Medium–High |
| **Linearity** | Excellent | Very good (with precision parts) | Excellent |
| **Noise floor** | Very low (noise shaped out of band) | Low | Very low |
| **Clipping character** | Harsh (modulator instability) | Softer (more gradual) | Variable |
| **Common in** | Most pro & consumer audio, Focusrite, Universal Audio, RME | High-end audiophile DACs, some pro | High-end pro, video DACs |
| **Sensitive to jitter?** | Yes — especially the modulator clock | Yes — switch timing is critical | Yes |

### DAC and Jitter

- Jitter at the DAC is more critical than at the ADC
- The DAC outputs analogue voltage at each clock tick — if the tick arrives slightly early or late, the output voltage is wrong
- This creates amplitude errors proportional to the signal's slew rate (rate of change)
- High frequencies change fastest → jitter affects high frequencies most
- This is why the monitoring path (DAC side) benefits most from a clean clock source

---

## Practical Specifications

### What to Look for in Converter Specs

| Specification | What It Means | Good Value |
|---|---|---|
| **Dynamic range** | Difference between max signal and noise floor | ≥ 110 dB (24-bit) |
| **THD+N** | Total Harmonic Distortion + Noise — how much distortion the converter adds | ≤ -100 dB (0.001%) |
| **Frequency response** | How flat the response is across 20 Hz–20 kHz | ± 0.1 dB |
| **Jitter** | Clock timing accuracy | < 1 ns RMS |
| **Latency** | Time from analogue input to digital output (ADC) or digital input to analogue output (DAC) | < 1 ms per conversion |
| **Supported sample rates** | Which rates the converter handles | 44.1–192 kHz |

### Latency Through Conversion

- Every ADC and DAC introduces a small amount of latency due to the oversampling and filter processing
- Typical ADC latency: **0.5–1.5 ms**
- Typical DAC latency: **0.5–1.5 ms**
- Round-trip (ADC → processing → DAC): **1–3 ms** just from conversion, before adding any network or processing latency
- In live sound, this conversion latency is usually negligible compared to acoustic propagation time (~2.9 ms per metre)

---

## Common Mistakes and Misconceptions

### "Higher sample rate always sounds better"

- Above 48 kHz, the audible benefit is debatable — human hearing tops out at ~20 kHz
- Higher sample rates DO benefit from more relaxed anti-aliasing filters and less in-band noise
- But they also double (96 kHz) or quadruple (192 kHz) the data rate, bandwidth, and storage requirements
- For live sound, **48 kHz / 24-bit is the professional standard** and provides full audible bandwidth

### "32-bit recording is better than 24-bit"

- 32-bit float is excellent for *internal processing* (no clipping) but no ADC actually captures 32 bits of analogue dynamic range
- The best ADCs achieve ~120–125 dB of real dynamic range — about 20–21 bits of actual resolution
- The remaining bits in a 24-bit file are below the analogue noise floor
- 32-bit float is useful for recording because it gives virtually unlimited headroom — you can record without worrying about gain staging and adjust levels later

### "All DACs sound the same"

- At the purely digital level, the maths is identical
- But the analogue output stage, clock quality, power supply design, and filter implementation vary significantly between manufacturers
- In critical listening environments, DAC quality matters — in a noisy live venue, the difference between a good and great DAC is often inaudible

---

## Relationship to Other Topics

| Concept | Connection |
|---|---|
| **Word Clock** | Determines *when* each sample is captured (ADC) or output (DAC) — jitter at these moments directly degrades quality |
| **Broadcast Methods** | AES3/MADI/Dante transport the digital samples between devices — the conversion happens at the input and output endpoints |
| **dB Measurement Scales** | Dynamic range is measured in dB; bit depth determines the theoretical dB range (6 dB per bit) |
| **Impedance** | The analogue stages of ADCs/DACs still follow normal impedance matching rules for input/output connections |

---

## Key Takeaways

- **Sample rate must be ≥ 2× the highest frequency** (Nyquist) — 48 kHz captures everything the ear can hear
- **Bit depth determines dynamic range** — 24-bit gives 144 dB, far exceeding any analogue component
- **Oversampling is the key innovation** that made digital audio sound good — it moves filtering into the digital domain
- **Dither when reducing bit depth** — it replaces ugly distortion with inoffensive noise
- **Jitter matters most at the DAC** — invest in clean clocking for your monitoring chain
- **48 kHz / 24-bit is the live sound standard** — higher rates rarely provide audible benefit in practice
- **The ADC and DAC are the most critical points in the digital chain** — everything between them is just perfect maths

---

## Resources

- [Monty Montgomery — Digital Show & Tell (Xiph.org)](https://xiph.org/video/vid2.shtml) — excellent visual demonstration of sampling and reconstruction
- [Sound On Sound — The Science of Sampling](https://www.soundonsound.com/)
- [RME — Digital Audio Basics](https://www.rme-audio.de/)
- Relate to your notes on [Word Clock](../Word-clock/notes.md) and [Broadcast Methods](../Broadcast-methods/notes.md)