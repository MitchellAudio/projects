# Live Application Audio Plugins

Comprehensive notes on audio plugins in a live production context — what they are, how they work, the different formats, host environments, and practical considerations for live sound.

---

## Table of Contents

1. [What Is an Audio Plugin?](#1-what-is-an-audio-plugin)
2. [Plugin Formats](#2-plugin-formats)
3. [Plugin Processing Types](#3-plugin-processing-types)
4. [How Plugins Integrate with Live Systems](#4-how-plugins-integrate-with-live-systems)
5. [Plugin Hosts in Live Audio](#5-plugin-hosts-in-live-audio)
6. [Latency Considerations](#6-latency-considerations)
7. [Native vs. DSP-Accelerated Processing](#7-native-vs-dsp-accelerated-processing)
8. [Common Plugin Categories in Live Sound](#8-common-plugin-categories-in-live-sound)
9. [Stability and Reliability](#9-stability-and-reliability)
10. [Key Manufacturers](#10-key-manufacturers)

---

## 1. What Is an Audio Plugin?

An audio plugin is a **software component** that processes audio within a host application or hardware environment. In a live context, plugins replace or supplement the outboard gear (compressors, EQs, reverbs, delays, etc.) that would traditionally exist as dedicated hardware units.

- Plugins are loaded into a **host** — a DAW, digital console, or dedicated plugin server
- The host passes audio to the plugin, the plugin transforms it, and returns the result
- Multiple plugins can be chained together in series (**chain**)

### Plugin vs. Built-in Processing

| Feature | Built-in Console DSP | Third-Party Plugin |
|---|---|---|
| Integration | Seamless | Requires host environment |
| Sound character | Varies by manufacturer | Wide variety |
| CPU load | Off-loaded to console | Depends on host platform |
| Flexibility | Fixed feature set | Swappable, updateable |
| Latency | Typically minimal | Varies — must be checked |

---

## 2. Plugin Formats

Plugin formats define the **API** (application programming interface) — i.e., the specification that both the plugin developer and the host must adhere to so they can communicate.

### 2.1 VST / VST3 (Virtual Studio Technology)
- Developed by **Steinberg** (Cubase)
- Most widely supported format on Windows; also common on macOS
- **VST3** improves on VST2 with better side-chain support, MIDI handling, and per-sample processing
- Used by many live plugin hosts (e.g., Waves SoundGrid Studio)

### 2.2 AU (Audio Units)
- Developed by **Apple**
- macOS/iOS only
- Natively supported by Logic Pro, MainStage, GarageBand
- Preferred format on Mac-based live rigs

### 2.3 AAX (Avid Audio eXtension)
- Developed by **Avid** (Pro Tools)
- Two variants:
  - **AAX Native** — runs on the host CPU
  - **AAX DSP** — runs on Avid HDX hardware DSP cards (dedicated processing)
- Relevant in broadcast and live-to-air environments where Pro Tools is used

### 2.4 RTAS / TDM (Legacy)
- Older Pro Tools formats — largely obsolete but may be encountered in older touring rigs
- TDM ran on dedicated DSP cards; RTAS ran natively

### 2.5 Waves SoundGrid (WSGP)
- Proprietary Waves format
- Plugins run on a **SoundGrid server** over a dedicated Ethernet network
- Low latency, hardware-accelerated; see the Waves notes for full detail

---

## 3. Plugin Processing Types

### 3.1 Dynamics
- **Compressors** — reduce dynamic range; peak limiting; bus glue
- **Limiters** — hard ceiling on signal level; protect PA and amplifiers
- **Gates / Expanders** — attenuate signals below a threshold (e.g., drum gating, mic bleed)
- **De-essers** — frequency-selective compression targeting sibilance

### 3.2 Equalisation (EQ)
- **Parametric EQ** — fully adjustable frequency, gain, and Q (most common in live)
- **Graphic EQ** — fixed frequency bands; common on PA system outputs
- **Dynamic EQ** — EQ that responds to level, like a frequency-selective compressor
- **Linear Phase EQ** — zero phase shift; better for system work, adds latency

### 3.3 Time-Based Effects
- **Reverb** — simulates acoustic spaces (halls, plates, rooms)
- **Delay / Echo** — single or multiple repeats of a signal; tap-tempo common in live
- **Chorus / Flanger / Phaser** — modulation-based effects; less common at FOH, more common in monitoring or guitar processing

### 3.4 Pitch and Harmony
- **Pitch correction (auto-tune)** — corrects vocal intonation in real time
- **Harmonisers** — generate harmony voices from a dry input
- **Pitch shifting** — transpose a signal up or down in semitones

### 3.5 Saturation / Distortion / Character
- **Tape emulation** — adds harmonic saturation, subtle compression
- **Transformer / preamp emulation** — adds analogue colour
- **Overdrive / Distortion** — intentional harmonic distortion; guitar rigs, creative FX

### 3.6 Spatial / Imaging
- **Mid-Side (M/S) processing** — separate mono-centre and stereo-side processing
- **Stereo imaging** — widening or narrowing a stereo field
- **Upmixing** — deriving surround or immersive audio from stereo sources

### 3.7 Noise Reduction
- **Noise suppression** — broadband background noise reduction
- **Hum / buzz removal** — targeted notch filtering at 50/60Hz harmonics
- **Transient shaping** — manipulate attack and sustain characteristics

---

## 4. How Plugins Integrate with Live Systems

In a live system, plugins can appear at several points in the signal chain:

```
Microphone/Source
      |
   Preamp (analogue or digital console)
      |
   Channel Insert (pre or post fader)
      |---- Plugin (e.g., compressor, gate, EQ)
      |
   Aux / Bus Send
      |---- Plugin (e.g., reverb, delay on an FX return)
      |
   Main Bus / LR / Groups
      |---- Plugin (e.g., bus compressor, multiband limiter)
      |
   System Output (to amplifiers / PA)
```

### Insert Points
- Plugins placed as **inserts** are inline in the signal path
- The signal goes out to the plugin and returns in place — the plugin replaces that section of signal processing
- Most consoles allow multiple plugins in series per channel

### Send/Return (FX Bus)
- A portion of the signal is **sent** to a plugin (e.g., reverb)
- The wet return is blended back with the dry signal at the console
- Allows multiple channels to share one reverb instance

### Parallel Processing
- The dry signal and processed signal are mixed together
- Common with compression (New York compression) and reverb

---

## 5. Plugin Hosts in Live Audio

A **host** provides the environment in which plugins run. In live audio, hosts fall into a few categories:

### 5.1 Digital Mixing Consoles with Native Plugin Support
- Some consoles (e.g., Yamaha Rivage, SSL Live, DiGiCo Quantum) have native plugin slots built into the console environment
- No external hardware needed — plugins run on the console's own DSP or CPU

### 5.2 Software Hosts on a Laptop/Desktop
- Applications like **Waves SoundGrid Studio**, **VENUE Stage**, or **Plogue Bidule** can host plugins on a computer
- The computer is connected to the audio network (e.g., Dante, SoundGrid, MADI) and processes audio in real time

### 5.3 Dedicated Plugin Servers
- Hardware units running a specialised OS designed only for plugin processing
- **Waves SoundGrid Servers** are the most common example
- Accept audio from the network, process it through plugins, and return it — all at very low latency

### 5.4 DAW in Live Mode
- Pro Tools, Logic Pro (MainStage), or Reaper used as live plugin hosts
- Requires careful buffer/latency setup
- Typically used in complex productions, musical theatre, broadcast, or studio recording of live events

---

## 6. Latency Considerations

Latency is the **time delay** introduced as audio passes through a digital system. In live audio, even small amounts of latency are audible and must be managed.

### Sources of Latency
| Source | Typical Range |
|---|---|
| A/D and D/A conversion | 0.5 – 2ms per conversion |
| Console DSP processing | 0.5 – 5ms |
| Plugin processing (native) | 0.5 – 10ms depending on buffer |
| Network transmission (Dante, SoundGrid) | < 1ms (well-configured) |
| Linear phase EQ / FFT processes | 5 – 30ms+ |

### Buffer Size and Latency
- Native plugin hosts use an **audio buffer** — a block of samples processed at once
- Smaller buffer = lower latency, but higher CPU demand and risk of dropouts
- **Round-trip latency** = input buffer + processing + output buffer

```
At 48kHz sample rate:
64 samples  = ~1.3ms per buffer
128 samples = ~2.7ms per buffer
256 samples = ~5.3ms per buffer
512 samples = ~10.7ms per buffer
```

> **Rule of thumb for live audio:** Total system latency should be kept under ~5ms where possible. Anything above ~25ms becomes perceptible as a discrete echo in monitors.

### Look-Ahead Plugins
- Some plugins (especially limiters and de-essers) use **look-ahead** buffering — they read slightly ahead in the buffer to respond before a transient arrives
- This intentionally introduces latency equal to the look-ahead time
- Must be accounted for in delay compensation on the console

---

## 7. Native vs. DSP-Accelerated Processing

### Native Processing
- Plugins run on the **host CPU** (computer processor)
- Flexible: any CPU-compatible plugin can be used
- Susceptible to CPU load spikes, system interrupts, and other processes competing for resources
- Lower upfront cost (just a computer)
- Risk: system instability under heavy load at small buffer sizes

### DSP-Accelerated Processing
- Plugins run on dedicated **Digital Signal Processors** (e.g., Waves SoundGrid servers, Avid HDX cards)
- The DSP is purpose-built for audio — deterministic, reliable, no OS interruptions
- Lower, more consistent latency
- Each DSP chip has a fixed capacity — you can run out of DSP
- Higher cost, but higher reliability

| Factor | Native | DSP |
|---|---|---|
| Cost | Lower | Higher |
| Reliability | Moderate | High |
| Latency | Variable | Consistent |
| Plugin choice | Very wide | Limited to supported plugins |
| Expandability | Add more CPU/RAM | Add more DSP hardware |

---

## 8. Common Plugin Categories in Live Sound

| Use Case | Typical Plugins |
|---|---|
| Vocal channel | Gate → EQ → De-esser → Compressor |
| Drum bus | Compressor (bus glue) → Limiter |
| PA system output | Multiband limiter → Linear phase EQ |
| IEM mix | Reverb (room) → EQ → Limiter |
| Guitar (in-ear) | Amp sim → Cabinet IR → Delay |
| Broadcast feed | Loudness meter → Broadcast limiter |
| Pitch correction | Auto-tune (real-time mode) → EQ |

---

## 9. Stability and Reliability

Live audio has **zero tolerance for failure** — a plugin crash during a show is unacceptable. Best practices:

- **Only use plugins on the approved/tested list** for your console or server platform
- **Freeze or lock the session** before the show — no updates on show day
- **Test all plugins at full sample rate and buffer size** during soundcheck
- Use a **dedicated machine** — no other applications running, no internet connection
- Keep a **backup preset** of all plugin settings saved to the console or session
- Know how to **bypass quickly** — every console should have a one-button method to bypass all inserts in an emergency
- **Version control** your plugin software — rolling back a broken update can save a show

---

## 10. Key Manufacturers

| Manufacturer | Notable Products | Notes |
|---|---|---|
| Waves | SoundGrid ecosystem, C6, H-Comp, Vocal Rider | Dominant in live plugin processing |
| iZotope | RX (noise reduction), Neutron, Ozone | Strong in noise reduction and mastering |
| FabFilter | Pro-Q 3, Pro-C 2, Pro-L 2 | Excellent transparency and visual feedback |
| Eventide | H910, H3000, Blackhole reverb | Classic pitch and reverb |
| Universal Audio | UAD (hardware DSP), Neve, API, SSL emulations | High-end analogue emulation |
| McDSP | 6060, 4040, ML4000 | Designed for live and broadcast |
| TC Electronic | Reverb 4000, VSS3 | Industry-standard reverb |
| Empirical Labs | Distressor (EL8), Mike-E | Analogue-style character |
| Sonnox | Oxford EQ, Inflator, Limiter | Broadcast-standard processing |

---

## References & Further Reading

- Waves Audio knowledge base: [www.waves.com/support](https://www.waves.com/support)
- Sound On Sound — Live Sound Technology articles
- Meyer Sound — System design resources (latency, alignment)
- Yamaha Pro Audio — Console plugin integration guides
- Rational Acoustics — SMAART live measurement resources
