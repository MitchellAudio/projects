# Notes: Word Clock

## What Is Word Clock?

- **Word clock** — a timing signal that tells digital audio devices *when* to sample or output audio
- It is a square wave that pulses once per audio sample — at 48 kHz sample rate, word clock ticks 48,000 times per second
- Every device in a digital audio chain must agree on *exactly* when each sample begins and ends
- Without a shared clock, devices sample at slightly different moments, which corrupts the audio

### Why "Word" Clock?

- In digital audio, a single sample across all channels is called a **word**
- Word clock marks the boundary between one word and the next
- It does *not* carry audio data — it is purely a timing reference

---

## Why Digital Audio Needs a Shared Clock

### The Core Problem

- Every digital audio device has its own internal crystal oscillator
- Crystal oscillators are very accurate but not *identical* — they drift by tiny amounts (measured in **parts per million / ppm**)
- If two devices run on independent clocks, their sample boundaries gradually slip apart
- This causes **sample slips** — a sample is either dropped or repeated to resync — which produces audible clicks, pops, or distortion

### What Happens Without Proper Clocking

- **Sample slips** — the receiving device's buffer overflows or underflows, it drops or duplicates a sample
- A single sample slip at 48 kHz is only 20.8 µs of time, but it creates a sharp discontinuity in the waveform
- You hear this as a click or pop — even one slip per minute is audible and unacceptable
- At worst, sustained clock mismatch causes continuous distortion or intermittent dropouts
- **Jitter** (see below) causes subtler degradation — smearing of the stereo image, loss of detail in high frequencies

---

## Clock Sources and Hierarchy

### Clock Source Types

- **Internal clock** — the device uses its own crystal oscillator as master. Only ONE device in a system should do this
- **External word clock** — the device locks to an incoming word clock signal on a dedicated BNC connector
- **Embedded clock** — the device recovers timing from a digital audio stream (AES3, MADI, ADAT, Dante). The clock is encoded *within* the data signal itself
- **Network clock (PTP/IEEE 1588)** — used by Dante, AES67, and other audio-over-IP protocols. A grandmaster clock is elected on the network and all devices sync to it via Ethernet

### Master/Slave Relationships

- **Clock master** — the single device that generates the reference clock for the entire system
- **Clock slaves** — every other device, which locks its internal oscillator to the master's timing
- **Rule: there must be exactly one master.** Two masters = two clocks = sample slips
- The master should be the most stable, highest-quality clock source available

### Choosing a Clock Master

- **Dedicated master clock generator** (e.g., Antelope, Mutec, Brainstorm) — purpose-built for stability, typically ±1 ppm or better
- **Console or primary interface** — many mixing consoles have high-quality internal clocks and are natural masters
- **Dante Controller / PTP grandmaster** — in Dante systems the network elects a grandmaster automatically using IEEE 1588 (best clock wins)
- Avoid using a cheap interface or outboard processor as master — their oscillators are often lower quality

---

## Jitter

### What Is Jitter?

- **Jitter** — small, rapid variations in the timing of the clock signal's edges
- Instead of the clock edge arriving at *exactly* regular intervals, it arrives slightly early or late each time
- Measured in **nanoseconds (ns)** or **picoseconds (ps)**

### Types of Jitter

- **Period jitter** — variation in the time between consecutive clock edges (cycle-to-cycle)
- **Long-term jitter** — drift that accumulates over many cycles
- **Random jitter** — caused by thermal noise in the oscillator circuit, has a Gaussian distribution
- **Deterministic jitter** — caused by interference, crosstalk, or power supply noise, has a repeatable pattern

### How Jitter Affects Audio

- At the moment of sampling (ADC) or reconstruction (DAC), the sample is captured/output at a slightly wrong time
- This creates **amplitude errors** — the voltage read is slightly too high or too low
- The effect is worst on high-frequency signals (where the waveform changes most rapidly between samples)
- Perceptually: loss of high-frequency detail, smeared stereo image, reduced depth and clarity
- The ear is more sensitive to jitter on the DAC side (monitoring/output) than the ADC side (recording)

### Jitter Specifications

- Professional-grade word clock: **< 1 ns RMS** jitter
- Decent interface/console: **1–5 ns RMS**
- Poor clock source: **> 10 ns RMS** — audible degradation in critical listening

---

## Phase-Locked Loops (PLL)

### What Is a PLL?

- A **Phase-Locked Loop (PLL)** is the circuit inside every digital audio device that locks the internal oscillator to the incoming reference clock
- It continuously compares the phase of the incoming clock to the internal oscillator and adjusts to match

### How It Works

1. **Phase detector** — compares the incoming reference clock to the device's internal oscillator and measures the phase difference
2. **Loop filter** — smooths out the error signal, filtering out high-frequency noise and jitter
3. **Voltage-controlled oscillator (VCO)** — adjusts its frequency based on the filtered error signal to track the reference
4. This feedback loop runs continuously, keeping the device locked to the reference within nanoseconds

### PLL Lock Time

- When you change clock source or sample rate, the PLL needs time to acquire lock — typically **0.5–5 seconds**
- During lock acquisition, audio may be muted or produce clicks
- Some devices show a "LOCK" LED — do not pass audio until it is solid

### PLL Bandwidth

- **Wide bandwidth PLL** — locks fast, tracks the reference closely, but also tracks the reference's jitter
- **Narrow bandwidth PLL** — locks slowly, but filters out more jitter from the reference, producing a cleaner output clock
- High-end clock generators use narrow-bandwidth PLLs to "clean up" incoming clock signals — this is called **clock regeneration** or **jitter attenuation**

---

## Word Clock Distribution

### BNC Word Clock (Traditional)

- Word clock is distributed as a **TTL-level square wave** on **75 Ω BNC coaxial cable**
- The cable impedance must be **75 Ω** — using the wrong impedance causes reflections that distort the clock edges and increase jitter
- **Termination** — the last device in a word clock chain must be terminated with a **75 Ω terminator** (either a physical BNC terminator or an internal switch)
- Without proper termination, the signal reflects off the unterminated end and interferes with itself

### Star vs. Daisy-Chain Topology

- **Star distribution** — clock master sends word clock to a **distribution amplifier (DA)**, which has multiple isolated outputs, one per device. Each device gets its own clean copy of the clock. **This is the preferred method**
- **Daisy-chain** — word clock passes from device to device via T-connectors or loop-through BNC jacks. Only the LAST device is terminated. Each device the signal passes through adds jitter and degrades the clock. **Avoid for more than 2–3 devices**
- **Active word clock distribution amplifier** — re-clocks the signal at each output, reducing accumulated jitter. Recommended for large systems

### Cable Considerations

- Use proper **75 Ω BNC cable** (RG-59 or similar video-grade coax)
- Do NOT use 50 Ω cable (designed for RF, not video/clock) — impedance mismatch causes reflections
- Keep cable runs as short as practical — long runs accumulate more jitter
- Avoid running word clock cables parallel to power cables or near noisy digital equipment

### Network-Based Clocking (Dante/AES67)

- Dante and AES67 use **IEEE 1588 Precision Time Protocol (PTP)** for clocking
- No dedicated clock cable needed — timing is distributed over the same Ethernet network as audio
- A **grandmaster clock** is automatically elected (the device with the best clock wins)
- PTP timestamps allow each device to reconstruct the sample clock locally with very low jitter
- This is why Dante networks require **managed switches with PTP support** (or at minimum, switches that pass multicast reliably)

---

## Word Clock Over Ethernet — IEEE 1588 PTP In Depth

### What Is PTP?

- **PTP (Precision Time Protocol)** — IEEE standard 1588, designed to synchronise clocks across an Ethernet network to sub-microsecond accuracy
- Originally developed for industrial automation and finance; adopted by audio/video standards (Dante, AES67, AVB, SMPTE ST 2059)
- Unlike NTP (Network Time Protocol, used for computers), PTP achieves nanosecond-level accuracy by measuring the actual network propagation delay between devices
- PTP does not carry audio — it only carries timing information so devices can reconstruct a shared clock

### How PTP Works — The Message Exchange

PTP uses a structured exchange of timestamped messages to measure and correct for network delay:

1. **Announce** — the grandmaster (or candidates) periodically broadcast their clock quality. All devices use this to elect the best grandmaster via the BMCA
2. **Sync** — the grandmaster sends a Sync message with a precise transmit timestamp (T1). The slave records the time it received it (T2)
3. **Follow_Up** — immediately after Sync, the grandmaster sends the exact T1 timestamp (two-step mode). One-step mode embeds T1 directly in the Sync
4. **Delay_Req** — the slave sends a Delay Request message, recording its transmit time (T3)
5. **Delay_Resp** — the grandmaster replies with the time it received the Delay_Req (T4)

From these four timestamps the slave calculates:

- **Mean path delay** = ((T2 − T1) + (T4 − T3)) ÷ 2
- **Offset from master** = (T2 − T1) − mean path delay
- The slave adjusts its local clock by this offset, continuously correcting itself

### Best Master Clock Algorithm (BMCA)

- When multiple PTP-capable devices are on the same network, they all announce their clock quality
- The **BMCA** (Best Master Clock Algorithm) automatically elects the grandmaster — no manual configuration needed
- The election is based on a priority hierarchy (lower number wins at each level):
  1. **Priority 1** — manually configured preference (0–255, lower is better). Default is 128
  2. **Clock class** — indicates clock accuracy category (e.g., locked to GPS = class 6; free-running = class 135)
  3. **Clock accuracy** — the rated accuracy of the oscillator (< 25 ns, < 100 ns, < 1 µs, etc.)
  4. **Offset scaled log variance** — stability of the clock over time
  5. **Clock identity** — the MAC address-derived unique ID, used as a final tiebreaker
- In practice, Dante devices automatically participate in the BMCA. The Dante Controller Clock Status page shows which device won and is acting as grandmaster
- You can manually force a preferred grandmaster by setting Priority 1 lower on that device

### PTP Clock Node Types

| Type | Role |
|---|---|
| **Ordinary Clock (OC)** | A regular endpoint device — either a grandmaster (one port, generates clock) or a slave (one port, receives and locks to clock). Most Dante devices are OCs |
| **Boundary Clock (BC)** | A device with multiple PTP ports that terminates PTP on one port and re-originates it on others. Managed switches can act as boundary clocks — they absorb the grandmaster's timing and redistribute a locally regenerated, cleaner clock to each port. This removes the variable delay that switches introduce from the timing path |
| **Transparent Clock (TC)** | A device (usually a switch) that measures how long a PTP message spent inside it and adds this residence time to the message's correction field. It does not re-originate the clock — it just corrects for the switch's own processing delay. Makes PTP much more accurate without requiring the switch to be a full boundary clock |

### Why Switches Matter for PTP

- Ethernet switches introduce variable delay (latency) between when a PTP message arrives and when it is forwarded — this is called **residence time** or **queuing delay**
- If a Sync message is delayed differently each time it passes through a switch, the slave's delay calculation becomes inaccurate, and the timing synchronisation degrades
- **Non-PTP-aware switch:** passes PTP messages as normal traffic, but the variable queuing delay adds jitter to the timing. Acceptable for Dante at short distances, but not ideal
- **Transparent clock switch:** measures its own delay and corrects the PTP message — the slave gets accurate delay information even through the switch
- **Boundary clock switch:** terminates PTP from the grandmaster and re-originates locally — the slaves on each port see a clean, local clock source with no accumulated upstream jitter

### Dante and PTP in Practice

- Dante uses **IEEE 1588v2** PTP operating in the **multicast** mode
- All Dante devices on a network participate in the BMCA and elect a grandmaster automatically
- The grandmaster is the device whose Sync messages all others lock to
- Dante uses a **1 ms synchronisation interval** — Sync messages are sent every millisecond
- PTP traffic in Dante is sent to specific multicast addresses (`224.0.1.129` for peer delay, `224.0.0.107` for general PTP)
- **IGMP snooping** must be enabled on the switch so PTP multicast is not flooded to every port unnecessarily
- Dante Controller's **Clock Status** page shows:
  - Which device is the grandmaster
  - The clock offset of each device from the grandmaster
  - Whether each device is Locked, Locking, or Not Locked

### AES67 and PTP

- **AES67** — the SMPTE/AES standard for audio-over-IP interoperability (the "Dante speaks to other systems" standard)
- AES67 also uses IEEE 1588v2 PTP but operates in **unicast** mode (point-to-point) rather than multicast
- AES67 typically uses **PTP domain 0** (Dante uses domain 0 by default — check device documentation)
- When Dante devices are set to **AES67 mode**, they participate in AES67's PTP domain and can sync with non-Dante AES67 devices (Ravenna, LIVEWIRE+, Q-SYS)
- **Key difference:** AES67 unicast PTP requires explicit configuration of who talks to whom; Dante multicast PTP self-configures

### AVB / gPTP (IEEE 802.1AS)

- **gPTP** (generalised PTP, IEEE 802.1AS) is a simplified, stricter version of PTP used by **AVB (Audio Video Bridging)** systems (Audinate hardware, some Apple devices, Dante-AVB-compatible equipment)
- gPTP requires switches to be AVB-aware (they must act as transparent or boundary clocks) — it will not work reliably through standard switches
- Dante uses standard IEEE 1588v2, NOT gPTP — Dante can work through any managed switch; AVB requires AVB-capable switches
- This is one reason Dante is dominant in live sound: it works on standard networking infrastructure

### PTP Troubleshooting

| Symptom | Likely Cause |
|---|---|
| Multiple grandmasters elected | Two network segments are isolated — PTP multicast not crossing a VLAN boundary or switch config issue |
| Clock offset > 1 µs | Switch not PTP-aware, high network load, long cable runs with many hops |
| Devices show "Not Locked" | PTP multicast not reaching them — check IGMP snooping, VLAN config, switch multicast settings |
| Grandmaster keeps changing | Network instability, BMCA re-running due to packet loss or device restarts |
| Audio dropouts in Dante with good network | Check clock status — a clock re-election event causes a brief dropout while all devices re-lock |

### Summary: Analogue Word Clock vs. PTP

| | Analogue Word Clock (BNC) | Network PTP (Dante/AES67) |
|---|---|---|
| **Cable** | Dedicated 75 Ω BNC coax | Shared Ethernet (same as audio) |
| **Accuracy** | < 1 ns with good DA | < 1 µs (typically < 100 ns with good switches) |
| **Self-configuring?** | No — you set master manually | Yes — BMCA elects grandmaster automatically |
| **Scales to many devices?** | Requires DA per group | Yes — any number of devices on the network |
| **Switch dependency** | None | Requires managed switch for best results |
| **Used by** | Analogue consoles, outboard gear | Dante, AES67, MADI-over-IP, AVB |

## Sample Rates and Word Clock

### Common Sample Rates

| Sample Rate | Use Case |
|---|---|
| **44.1 kHz** | CD audio, music production legacy |
| **48 kHz** | Live sound, broadcast, film, video — the professional standard |
| **88.2 kHz** | Double-rate, used in high-res music production (2× 44.1) |
| **96 kHz** | Double-rate professional (2× 48), film/post-production |
| **176.4 kHz** | Quad-rate (4× 44.1), rare |
| **192 kHz** | Quad-rate (4× 48), mastering and archival |

### Live Sound Default

- **48 kHz** is the standard for live sound and broadcast
- Higher sample rates double the bandwidth requirement and halve the channel count on fixed-bandwidth connections (e.g., MADI, AES3 in dual-wire mode)
- For most live applications, 48 kHz provides full 20 Hz–20 kHz audio bandwidth with plenty of margin

### All Devices Must Match

- Every device in the system must be set to the **same sample rate**
- If one device is set to 44.1 kHz and another to 48 kHz, the slave cannot lock — you will get sample slips or no audio at all
- Dante Controller shows sample rate mismatches as subscription errors

---

## Troubleshooting Word Clock Issues

### Symptoms of Clock Problems

| Symptom | Likely Cause |
|---|---|
| Clicks and pops | Sample slips — clock mismatch or no lock |
| Continuous distortion / digital noise | No valid clock reference, device free-running |
| Audio drops out intermittently | PLL losing lock, marginal clock signal |
| Stereo image feels smeared or flat | Excessive jitter |
| "LOCK" LED blinking or off | Device cannot lock to reference — wrong sample rate, bad cable, or no signal |

### Checklist

1. **Verify one master only** — check that exactly one device is set to Internal clock; all others are set to External, AES, or Network
2. **Verify sample rate matches** — every device must be set to the same rate (usually 48 kHz)
3. **Check BNC cables** — use 75 Ω cable, check for damaged connectors, verify termination on the last device
4. **Check termination** — only the last device in a daisy chain should be terminated; star-distributed outputs do not need termination
5. **Monitor LOCK indicators** — all slave devices should show solid lock before passing audio
6. **In Dante systems** — open Dante Controller and check the Clock Status page; verify one grandmaster is elected and all devices show "Locked"

---

## Relationship to Other Topics

| Concept | Connection |
|---|---|
| **ADC/DAC Conversions** | Word clock determines *when* the ADC samples and *when* the DAC outputs — jitter at these moments directly degrades audio quality |
| **Broadcast Methods (AES3, MADI, Dante)** | AES3 and MADI carry embedded clock in the data stream; Dante uses PTP over Ethernet |
| **Time Alignment** | Time alignment deals with acoustic timing between speakers; word clock deals with *sample-level* timing between digital devices — different problem, similar concept |
| **Managed Switches** | PTP-capable managed switches are critical for network-based clocking (Dante, AES67) |

---

## Key Takeaways

- **One master, all others slave** — the single most important rule
- **75 Ω BNC, properly terminated** — impedance mismatch is the #1 cause of clock problems with analogue word clock distribution
- **Star distribution > daisy-chain** — use a DA for systems with more than 2–3 devices
- **Dante handles clocking automatically via PTP** — but you still need proper network infrastructure (managed switches, correct IGMP/QoS settings)
- **Jitter matters most at the DAC** — invest in a good clock source for your monitoring chain
- **If you hear clicks/pops in a digital system, check clocking first** — it is the most common cause

---

## Resources

- [Antelope Audio — Word Clock Explained](https://en.antelopeaudio.com/)
- [RME — Digital Audio Basics: Clocking](https://www.rme-audio.de/)
- [Audinate — Dante Clocking (PTP)](https://www.audinate.com/learning)
- [Sound On Sound — Understanding Word Clock](https://www.soundonsound.com/)
- Relate to your notes on [Broadcast Methods](../Broadcast-methods/notes.md) and [ADC-DAC Conversions](../ADC-DAC-conversions/notes.md)