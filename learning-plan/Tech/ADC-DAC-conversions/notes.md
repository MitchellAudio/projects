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

### What Is Oversampling?

- **Oversampling** — the ADC internally samples at a much higher rate than the output sample rate (e.g., 64× or 128× oversampling)
- At 48 kHz × 128 = 6.144 MHz internal sample rate, the Nyquist frequency is 3.072 MHz
- The anti-aliasing filter now only needs to block frequencies above 3 MHz — a very gentle, easy filter with no audible phase artefacts

### How Oversampling Works (ADC)

1. The analogue signal is sampled at a very high internal rate (e.g., 128× the target rate)
2. A gentle analogue anti-aliasing filter removes frequencies above ~1 MHz (easy to build, no audible side effects)
3. A **digital decimation filter** then reduces the sample rate down to the target (48 kHz)
4. The digital filter can be extremely precise with no analogue component limitations

### How Oversampling Works (DAC)

1. The digital signal at 48 kHz is **upsampled** (interpolated) to a much higher rate internally
2. A **digital reconstruction filter** smooths the staircase waveform at the high sample rate
3. The DAC converts this oversampled digital signal to analogue
4. A gentle analogue low-pass filter removes the ultrasonic content
5. Result: a much smoother, more accurate analogue output

### Why Oversampling Matters

- Eliminates the need for steep analogue filters (which cause phase distortion)
- Moves all the heavy filtering into the digital domain where it can be done perfectly
- Spreads quantisation noise across a wider bandwidth, reducing the noise density in the audio band
- This is why modern converters sound dramatically better than early 1980s digital — same bit depth and sample rate, but much better filter design via oversampling

---

## The DAC: Digital Back to Analogue

### Reconstruction

- The DAC receives a stream of discrete samples and must reconstruct a smooth, continuous analogue waveform
- If you simply output each sample value as a voltage and hold it until the next sample, you get a **staircase waveform** — full of ultrasonic harmonics
- A **reconstruction filter** (low-pass filter) smooths the staircase back into a continuous waveform
- With oversampling, most of this smoothing happens digitally before the final analogue filter, giving a much cleaner result

### DAC Architectures

- **Delta-sigma (ΔΣ) DAC** — the most common architecture in modern audio. Uses heavy oversampling and noise shaping. Extremely linear and cost-effective
- **R-2R ladder DAC** — uses a precision resistor network. More expensive but some argue it sounds more "analogue." Used in high-end converters
- **Multibit DAC** — older architecture, largely replaced by delta-sigma

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


need more information on dac archetecture
oversampling - how does that work if it is not captured at that sampling rate or am i missing something