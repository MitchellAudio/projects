# Notes: Broadcast Methods

## AES/EBU Digital Audio (AES3)

### Overview

**AES/EBU** (Audio Engineering Society / European Broadcasting Union) is a professional digital audio standard for transmitting two channels of uncompressed PCM audio over a single cable. It's formally known as **AES3** and uses the same XLR connectors and balanced wiring as analog audio.

**Key Specifications:**
- **Standard:** AES3 (published 1985, updated regularly)
- **Channels:** 2 channels per cable (stereo pair)
- **Connector:** XLR-3 (same as balanced analog)
- **Impedance:** 110Ω (vs 600Ω for analog)
- **Sample Rates:** 32 kHz, 44.1 kHz, 48 kHz, 88.2 kHz, 96 kHz, 176.4 kHz, 192 kHz
- **Bit Depth:** Up to 24-bit audio data
- **Cable Length:** Up to 100 meters (328 feet) typical

### How AES Data is Encoded

#### 1. **Biphase Mark Code (BMC)**

AES uses **Biphase Mark Coding** (also called FM encoding) to send digital data:

```
Binary '1': Transition at start + transition at middle of bit period
Binary '0': Transition at start only

Example timing:
    ___     ___           ___     ___
___|   |___|   |___   ___|   |___|   |___
     1       1           0       1
```

**Why Biphase Mark?**
- **Self-clocking:** Receiver can extract clock from data (no separate clock wire needed)
- **DC-free:** Equal high/low time prevents transformer saturation
- **Transition guarantee:** At least one transition per bit for synchronization

#### 2. **Frame Structure**

AES transmits audio in **frames** and **blocks**:

```
Frame Structure (one sample for both channels):
┌──────────────────────────────────────────────────────┐
│ Subframe A (Ch 1) │ Subframe B (Ch 2) │
│    32 bits        │    32 bits        │
└──────────────────────────────────────────────────────┘
           = 1 Frame (64 bits)

Block Structure:
┌────────────────────────────────────────┐
│ 192 Frames = 1 Block                    │
│ (Used for channel status data)         │
└────────────────────────────────────────┘
```

#### 3. **Subframe Format (32 bits per channel)**

Each audio sample is sent in a 32-bit subframe:

```
Bit Position:  0-3    4-7      8-27         28     29     30    31
              ┌────┬──────┬────────────────┬────┬──────┬─────┬────┐
              │Pre-│Aux   │ Audio Sample   │ V  │ U    │ C   │ P  │
              │amble│Data  │ (24-bit max)   │    │      │     │    │
              └────┴──────┴────────────────┴────┴──────┴─────┴────┘
               Sync  4 bits   20-24 bits    Valid User Channel Even
                                                      Status Parity
```

**Bit Breakdown:**
- **Bits 0-3:** Preamble (sync pattern, see below)
- **Bits 4-7:** Auxiliary data (often used for extra bits or control)
- **Bits 8-27:** Audio sample data (20-24 bits, LSB first)
- **Bit 28 (V):** Validity flag (0 = valid audio, 1 = not valid)
- **Bit 29 (U):** User data bit (192 bits per block for custom data)
- **Bit 30 (C):** Channel status bit (192 bits per block for metadata)
- **Bit 31 (P):** Parity bit (even parity for error detection)

#### 4. **Preambles (Sync Patterns)**

AES uses special **preambles** that violate biphase mark rules to mark frame boundaries:

```
Preamble Z: Start of Block, Subframe A (Channel 1, Frame 0)
    ___   _______
___|   |_|       |___

Preamble X: Start of Subframe A (Channel 1)
    ___       ___
___|   |_____|   |___

Preamble Y: Start of Subframe B (Channel 2)
    ___   ___
___|   |_|   |_______
```

These patterns are **impossible in normal biphase mark**, so receivers instantly recognize frame starts.

### Channel Status Block

The **Channel Status** bits (bit 30 of each subframe) form a 192-bit message over 192 frames:

**Important Channel Status Information:**
- **Bits 0-1:** Consumer vs Professional format flag
- **Bits 2-5:** Audio signal emphasis
- **Bits 6-8:** Sample rate information
- **Bits 24-27:** Sample word length (16, 20, 24 bits)
- **Bits 32-191:** Additional metadata (source, destination, timecode, etc.)

### Physical Layer: How It Uses XLR

#### **Same Cable, Different Signal**

While AES uses the same XLR connector as analog audio, the signal is very different:

| Parameter | Analog Audio | AES/EBU Digital |
|-----------|-------------|-----------------|
| Signal Type | Voltage waveform | Square wave pulses |
| Frequency Range | 20 Hz - 20 kHz | 128 kHz - 12.288 MHz (depends on sample rate) |
| Impedance | 600Ω (historic) / 10kΩ+ modern | 110Ω |
| Voltage | ~1.23V peak | 3-10V peak-to-peak |
| Pins | Pin 2 hot, Pin 3 cold, Pin 1 ground | Pin 2 positive, Pin 3 negative, Pin 1 shield |
| Cable Type | Standard mic cable works | Needs proper impedance (digital-grade or mic cable often works) |

**Key Point:** Standard XLR mic cables often work fine for AES at short distances (<50m), but dedicated 110Ω digital cables are recommended for:
- Long runs (>50m)
- High sample rates (>96 kHz)
- Critical installations
- Preventing signal reflections

#### **Bit Rate Calculation**

AES bit rate depends on sample rate:

```
Bit Rate = Sample Rate × 2 channels × 32 bits/subframe

Examples:
- 48 kHz: 48,000 × 2 × 32 = 3.072 Mbps
- 96 kHz: 96,000 × 2 × 32 = 6.144 Mbps
- 192 kHz: 192,000 × 2 × 32 = 12.288 Mbps
```

### AES vs Other Digital Audio Formats

| Format | Connector | Channels | Distance | Use Case |
|--------|-----------|----------|----------|----------|
| **AES/EBU** | XLR | 2 | 100m | Professional studios, broadcast |
| **S/PDIF** | RCA or Toslink | 2 | 10m (coax), 5m (optical) | Consumer equipment |
| **ADAT** | Toslink | 8 @ 48kHz, 4 @ 96kHz | 5-10m | Multi-channel recording |
| **MADI** | BNC or Optical | 64 channels | 100m (coax), 2km (optical) | High channel count systems |
| **Dante/AES67** | Ethernet | 100s | 100m per hop | Network audio |

**S/PDIF vs AES/EBU:**
- S/PDIF is consumer version of AES3
- Uses same biphase mark encoding
- Different connectors (RCA at 75Ω or Toslink optical)
- Channel status bits have different meanings
- Often compatible with format conversion

### Synchronization and Word Clock

**Critical Concept:** All digital audio devices must share the same **sample clock** to avoid clicks, pops, and drift.

**Clock Sources:**
1. **Embedded Clock:** AES receiver extracts clock from biphase mark transitions
2. **Word Clock:** Separate BNC connection with clock pulses (48 kHz = 48,000 pulses/sec)
3. **Master/Slave:** One device is clock master, others slave to it

**Best Practices:**
- Use one master clock source in the system
- All devices lock to same clock (via word clock, AES input, or network sync)
- Avoid clock loops (device A → B → C, not A → B → A)
- Monitor sample rate converters (SRCs) for rate mismatches

### Advantages of AES/EBU

1. **No noise accumulation:** Digital signal doesn't degrade through processing chain
2. **Perfect cloning:** Copy is identical to original (no generation loss)
3. **Embedded metadata:** Sample rate, bit depth, channel status transmitted with audio
4. **Long cable runs:** 100m vs ~10m for line-level analog before degradation
5. **No hum/buzz:** Immune to electromagnetic interference (digital threshold)
6. **Channel count:** Two channels per cable vs one for analog

### Disadvantages and Considerations

1. **Clock dependency:** Requires proper synchronization or audio glitches occur
2. **Latency:** A/D and D/A conversion adds ~1-3ms delay
3. **Jitter sensitivity:** Clock instability can affect audio quality
4. **Cable impedance:** Improper cables can cause reflections at high sample rates
5. **Binary cliff:** Works perfectly or not at all (no graceful degradation)
6. **Sample rate conversion:** Converting between rates (e.g., 44.1 kHz ↔ 48 kHz) can affect quality

### Common Equipment Using AES

**Inputs (Receivers):**
- Digital mixing consoles (DiGiCo, Yamaha, Midas, etc.)
- Audio interfaces (RME, Focusrite, Apogee)
- DSP processors (Lake, BSS, Xilica)
- Amplifiers with digital inputs (Lab.gruppen, Powersoft)

**Outputs (Transmitters):**
- Digital mixing consoles
- Microphone preamps with A/D converters
- Media players (CD players, DAW interfaces)
- Digital effects processors

### Troubleshooting AES Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No audio | Wrong sample rate | Match sample rates or use SRC |
| Clicks/pops | Clock sync issue | Check word clock connections |
| Intermittent dropout | Bad cable | Replace with quality cable |
| Won't lock at all | Impedance mismatch | Use proper 110Ω cable |
| Distortion | Not AES signal | Verify source is digital output |
| High sample rate fails | Cable too long | Shorten cable or use repeater |

### Practical Setup Example

**Typical studio chain:**
```
Microphone → Preamp with A/D → AES/EBU Cable (XLR) →
→ Digital Console → AES/EBU → DSP Processor →
→ AES/EBU → Amplifier (D/A) → Speakers

Word Clock Distribution:
Master Clock Generator → Word Clock (BNC) → All devices
                    (or master device sends clock via AES)
```

### Testing AES Connections

**Tools:**
- **Multimeter:** Can verify cable continuity (not signal quality)
- **Oscilloscope:** Shows biphase mark pattern and voltage levels
- **AES Analyzer:** Dedicated tool to read sample rate, bit depth, channel status
- **Audio Meter:** Confirms audio is present and at correct level

**Quick Test:**
1. Connect AES output to input
2. Verify sample rates match on both devices
3. Confirm lock indicators on receiving device
4. Play audio and verify clean signal
5. Check for flags (V bit = 0 for valid audio)

---

## Audio Over IP (AoIP)

### Overview

**Audio over IP** transports multiple channels of uncompressed digital audio over standard Ethernet networks (CAT5e/CAT6). This replaces dedicated point-to-point cables (XLR, AES, analog) with a scalable, flexible network infrastructure.

**Key Advantages:**
- **Scalability:** Hundreds of channels over a single cable
- **Flexibility:** Route any source to any destination via software
- **Cost:** Single cable infrastructure replaces many analog/AES cables
- **Distance:** 100m per Ethernet hop, unlimited with switches
- **Bidirectional:** Full duplex communication on one cable
- **Control:** Device control and audio on same network

---

### Fundamentals: How Audio Becomes Network Packets

#### **Step 1: Audio Sampling (A/D Conversion)**

Before audio enters the network, it must be digitized:

```
Analog Audio Waveform → ADC (Analog-to-Digital Converter)
                         ↓
                 Digital Samples (numbers)

Example @ 48 kHz, 24-bit:
- Microphone voltage measured 48,000 times per second
- Each measurement = 24-bit number (16,777,216 possible values)
- One second = 48,000 samples × 24 bits = 1,152,000 bits
```

**Key Concept:** Audio is now a stream of numbers, not a voltage waveform. These numbers represent the amplitude at each moment in time.

---

#### **Step 2: Packetization (Breaking Audio into Chunks)**

Instead of sending one sample at a time, audio is grouped into **packets**:

```
Continuous Sample Stream:
[Sample 1][Sample 2][Sample 3][Sample 4]...[Sample 48,000]

Grouped into Packets (example: 12 samples per packet):
┌────────────────────────────────────────┐
│ Packet 1: Samples 1-12                 │ → Send to network
├────────────────────────────────────────┤
│ Packet 2: Samples 13-24                │ → Send to network
├────────────────────────────────────────┤
│ Packet 3: Samples 25-36                │ → Send to network
└────────────────────────────────────────┘
```

**Why Packets?**
- Networks send data in discrete chunks, not continuous streams
- Packets can be routed, prioritized, and recovered independently
- Allows multiple audio channels to share same cable

**Packet Size Trade-offs:**
- **Larger packets:** Fewer packets = less overhead, but higher latency
- **Smaller packets:** Lower latency, but more overhead (headers consume bandwidth)
- **Dante default:** 48 samples @ 48kHz = 1ms packets (good balance)

---

#### **Step 3: Building the Network Packet (Headers and Payloads)**

Each audio packet needs addressing and timing information:

**Dante Packet Structure (Simplified):**

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 2 (Ethernet) Header - 14 bytes                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Destination MAC | Source MAC | EtherType/VLAN          │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Layer 3 (IP) Header - 20 bytes                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Source IP | Dest IP | TTL | Protocol (UDP=17)          │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Layer 4 (UDP) Header - 8 bytes                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Source Port | Dest Port | Length | Checksum            │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ RTP (Real-time Transport Protocol) Header - 12 bytes        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Sequence # | Timestamp | SSRC (stream ID)              │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ AUDIO PAYLOAD - 144 bytes (48 samples × 3 bytes/24-bit)    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [Sample 1][Sample 2][Sample 3]...[Sample 48]           │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Total: 54 bytes headers + 144 bytes audio = 198 bytes per packet
```

**What Each Layer Does:**

**Layer 2 (Ethernet):**
- **Destination MAC Address:** Physical address of receiving device's network card
- **Source MAC Address:** Physical address of sending device
- **VLAN Tag (optional):** Isolates audio traffic from other network traffic
- **Gets packet from device A to device B on same network segment**

**Layer 3 (IP):**
- **Source IP Address:** Logical address (e.g., 192.168.1.10)
- **Destination IP Address:** Where packet should go (e.g., 239.0.0.1 for multicast)
- **TTL (Time to Live):** Prevents packets from looping forever (decrements at each router hop)
- **Allows packet to travel through routers across different networks**

**Layer 4 (UDP):**
- **No reliability:** Doesn't wait for acknowledgments (audio can't afford delays)
- **Faster than TCP:** No handshaking or retransmission
- **Trade-off:** Lost packets = brief audio dropout (acceptable for real-time)

**RTP (Real-time Transport Protocol):**
- **Sequence Number:** Detects lost or out-of-order packets
- **Timestamp:** When this audio should be played (based on sample clock)
- **SSRC:** Identifies which audio stream this is (e.g., "Console Ch 1")

---

#### **Step 4: Sending Packets Across the Network**

**Unicast (One-to-One):**
```
Console (192.168.1.10)
    ↓ "Send audio to 192.168.1.20"
    ├─→ Switch looks at dest IP/MAC
    └─→ Forwards ONLY to port where 192.168.1.20 is connected
          ↓
    Amplifier (192.168.1.20) receives packet

- One copy per receiver
- More bandwidth used if many receivers
```

**Multicast (One-to-Many) - More Efficient:**
```
Console (192.168.1.10)
    ↓ "Send audio to 239.69.1.1" (multicast group)
    ├─→ Switch sees multicast MAC address
    └─→ Forwards to ALL ports with subscribers to 239.69.1.1
          ↓         ↓         ↓
       Amp 1     Amp 2     Amp 3  (all subscribed to group)

- One copy sent, multiple receivers
- Switch replicates only when needed
- Requires IGMP Snooping on switch
```

**IGMP (Internet Group Management Protocol):**
```
Amplifier: "I want to receive 239.69.1.1" → IGMP Join message to switch
Switch: Adds amp's port to multicast group table
Console: Sends packet to 239.69.1.1
Switch: Forwards to all ports in that group
Amplifier: "I'm done" → IGMP Leave message
Switch: Removes port from group
```

---

#### **Step 5: Receiving and Playing Audio**

**At the Receiving Device:**

```
1. Network Interface Card (NIC) receives packet
   ↓
2. Filters by MAC/IP address (am I the destination?)
   ↓
3. Strips headers (Ethernet → IP → UDP → RTP)
   ↓
4. Extracts audio samples from payload
   ↓
5. Places samples in audio buffer (FIFO queue)
   ↓
6. DAC (Digital-to-Analog Converter) reads buffer at exact sample rate
   ↓
7. Outputs analog audio waveform to speaker
```

**The Buffer (Critical Concept):**

```
Incoming Packets:        Audio Buffer (FIFO):         DAC Output:
┌─────────┐
│ Packet 1│──→     ┌──────────────────┐
└─────────┘        │ [Samples 1-48]   │
                   │ [Samples 49-96]  │──→  Reads at exact
┌─────────┐        │ [Samples 97-144] │     48,000 samples/sec
│ Packet 2│──→     │ [Samples 145...] │
└─────────┘        └──────────────────┘
    ↓                   ↑
Network (variable      Buffer absorbs      Constant rate
timing, jitter)        timing variations
```

**Buffer Depth = Latency:**
- **Larger buffer:** Tolerates more jitter, higher latency
- **Smaller buffer:** Lower latency, but packet loss/jitter causes dropouts
- **Dante @ 1ms latency:** ~1ms worth of audio in buffer

---

#### **Step 6: Clock Synchronization (The Critical Part)**

**The Problem:**
Every device has its own oscillator (crystal) that generates the sample clock. Even high-quality crystals drift:

```
Device A crystal: 48,000.1 Hz (runs slightly fast)
Device B crystal: 47,999.9 Hz (runs slightly slow)

After 1 minute:
Device A has sampled: 2,880,006 samples
Device B has sampled: 2,879,994 samples
Difference: 12 samples (buffer overflow or underrun!)
```

**The Solution: PTP (Precision Time Protocol)**

```
1. Grandmaster Clock elected (best clock in network)
   ↓
2. Grandmaster sends timestamp packets:
   "My time is exactly 1,234,567.890123456 seconds since epoch"
   ↓
3. Slave devices measure network delay:
   - Send "Delay Request" to Grandmaster
   - Grandmaster responds with precise timestamp
   - Calculate one-way delay: (T4-T1) - (T3-T2) / 2
   ↓
4. Slave adjusts its clock to match Grandmaster
   - Speeds up if running slow
   - Slows down if running fast
   - Maintains <1 microsecond accuracy
```

**PTP Timing Packet Exchange:**
```
Slave Device                    Grandmaster Clock
     │                                 │
     │  ──── Sync Message ────>        │  T1: Grandmaster sends timestamp
     │       (Timestamp T1)            │
     │                                 │
     │  <──── Follow_Up ─────          │  T2: Precise T1 value
     │       (Precise T1)              │
     │                                 │
     │  ──── Delay_Req ────>           │  T3: Slave sends request
     │                                 │
     │  <──── Delay_Resp ────          │  T4: Grandmaster responds
     │       (T3, T4)                  │

Slave calculates:
Offset = [(T2-T1) - (T4-T3)] / 2
Delay  = [(T2-T1) + (T4-T3)] / 2
```

**Why This Matters:**
- All devices sample at **exactly** the same instant
- Buffers stay synchronized (no overflow/underrun)
- Audio from multiple sources lines up perfectly (phase-aligned)

---

#### **Step 7: Quality of Service (QoS) - Traffic Prioritization**

Networks carry many types of traffic. QoS ensures audio gets priority:

**DSCP (Differentiated Services Code Point) - Layer 3 Priority:**

```
IP Packet Header includes 6-bit DSCP field:

DSCP 46 (101110): Expedited Forwarding (EF) - Highest Priority
    ↓
┌────────────────────────────────────┐
│ Audio Packets (Dante)              │ ← Sent first, never delayed
├────────────────────────────────────┤
│ Control Packets (Dante Controller) │ ← DSCP 34, medium priority
├────────────────────────────────────┤
│ Email, Web Browsing                │ ← DSCP 0, best effort (last)
└────────────────────────────────────┘
```

**How Switches Use QoS:**

```
Switch Receives Multiple Packets:
┌─────────────────────────────────────────────────────┐
│ Port 1: Email packet (DSCP 0)                       │
│ Port 2: Dante audio packet (DSCP 46)                │
│ Port 3: Video stream (DSCP 34)                      │
│ Port 4: Another Dante packet (DSCP 46)              │
└─────────────────────────────────────────────────────┘
            ↓
Switch Sorts by Priority Queue:
┌─────────────────────────────────────────────────────┐
│ HIGH Priority Queue (DSCP 46):                      │
│   [Dante audio #1] [Dante audio #2]  ← Sent FIRST  │
├─────────────────────────────────────────────────────┤
│ MEDIUM Priority Queue (DSCP 34):                    │
│   [Video stream]                      ← Sent second │
├─────────────────────────────────────────────────────┤
│ LOW Priority Queue (DSCP 0):                        │
│   [Email]                            ← Sent last    │
└─────────────────────────────────────────────────────┘
            ↓
Transmits high priority first, preventing audio dropouts
```

**Without QoS:**
- All packets treated equally (first-in, first-out)
- Large email attachment could delay audio packet
- Result: Buffer underrun, audio click/pop

**With QoS:**
- Audio packets jump to front of line
- Other traffic waits (doesn't matter for email/web)
- Audio never interrupted

---

#### **Step 8: Bandwidth and Network Load**

**Calculating Bandwidth per Channel:**

```
One channel @ 48 kHz, 24-bit, 1ms packets:

Audio payload:
- 48 samples/packet × 3 bytes/sample = 144 bytes audio

Headers (per packet):
- Ethernet: 14 bytes
- IP: 20 bytes
- UDP: 8 bytes  
- RTP: 12 bytes
- Ethernet preamble/IFG: 20 bytes
Total headers: 74 bytes

Total packet: 144 + 74 = 218 bytes

Packets per second:
- 48,000 samples/sec ÷ 48 samples/packet = 1,000 packets/sec

Bandwidth:
- 218 bytes × 1,000 packets × 8 bits/byte = 1,744,000 bits/sec
- ≈ 1.74 Mbps per channel

Add ~2× for multicast overhead and safety margin:
≈ 3.5 Mbps per channel (typical real-world)
```

**Gigabit Ethernet Capacity:**
- 1 Gbps theoretical
- ~700 Mbps practical (due to overhead)
- 700 Mbps ÷ 3.5 Mbps = **~200 channels max safely**

**Why Not Use Full Bandwidth?**
- Network switches have limited buffer memory
- Multiple packets arriving simultaneously = queuing
- Keep utilization <70% to prevent buffer overflow
- Leaves headroom for control traffic, PTP, discovery

---

#### **Step 9: Layer 2 vs Layer 3 Audio**

**Layer 2 Only (AVB/Milan):**
```
Device A                    Device B
  [MAC: AA:BB:CC:DD:EE:01]    [MAC: AA:BB:CC:DD:EE:02]
          ↓                            ↓
      Switch sees MAC addresses only
          ↓
  Cannot pass through routers (Layer 3 devices)
  All devices must be on same local network
```

**Packet Structure:**
```
┌──────────────────────────┐
│ Ethernet Header          │ ← MAC addresses
├──────────────────────────┤
│ AVB/1722 Header          │ ← Stream ID, timing
├──────────────────────────┤
│ Audio Samples            │
└──────────────────────────┘
```

**Layer 3 (Dante, AES67):**
```
Device A (192.168.1.10)     Device B (192.168.2.20)
          ↓                            ↓
    Network 1 ──→ Router ──→ Network 2
          ↓                            ↓
  Can route between different subnets/locations
  More complex, but more flexible
```

**Packet Structure:**
```
┌──────────────────────────┐
│ Ethernet Header          │ ← MAC addresses (rewritten at each hop)
├──────────────────────────┤
│ IP Header                │ ← IP addresses (unchanged)
├──────────────────────────┤
│ UDP Header               │
├──────────────────────────┤
│ RTP Header               │
├──────────────────────────┤
│ Audio Samples            │
└──────────────────────────┘
```

---

### Summary: The Complete Journey

```
1. Microphone captures sound → Analog voltage waveform
                                       ↓
2. ADC samples 48,000 times/sec → Stream of 24-bit numbers
                                       ↓
3. Packetizer groups 48 samples → One packet (1ms of audio)
                                       ↓
4. Add headers:                → Ethernet + IP + UDP + RTP
                                       ↓
5. Network card transmits      → Electrical signals on CAT6 cable
                                       ↓
6. Switch receives             → Checks destination, priority (QoS)
                                       ↓
7. Switch forwards             → Out correct port to destination
                                       ↓
8. Receiving NIC captures      → Packet arrives at destination
                                       ↓
9. Headers stripped            → Extract 48 audio samples
                                       ↓
10. Samples placed in buffer   → FIFO queue, absorbs jitter
                                       ↓
11. DAC reads at sample rate   → Converts back to analog voltage
                                       ↓
12. Speaker outputs sound      → Acoustic waveform in air

All synchronized by PTP clock (<1µs accuracy across network)
```

**Key Takeaways:**
- Audio is sampled, grouped into packets, and sent like any network data
- Headers add addressing, timing, and priority information
- Buffers absorb network jitter, introducing latency
- Clock synchronization is critical (PTP keeps all devices aligned)
- QoS ensures audio packets are never delayed by other traffic
- UDP is used (no retransmission) because audio is time-sensitive

---

### Major Audio-over-IP Protocols

#### 1. **Dante (Audinate)**

**Most Popular Protocol in Pro Audio**

**Specifications:**
- **Standard:** Proprietary (Audinate), but widely licensed
- **Transport:** Layer 3 (IP-based, works through routers with proper QoS)
- **Latency:** <1ms typical (150µs minimum)
- **Sample Rates:** 44.1, 48, 88.2, 96 kHz
- **Bit Depth:** Up to 24-bit
- **Channels:** 512 @ 48kHz per network interface
- **Network:** Standard Gigabit Ethernet (1 Gbps)

**How Dante Works:**
```
Layer 7 (Application): Audio routing, device discovery (Dante Controller)
Layer 4 (Transport):   UDP for audio, TCP for control
Layer 3 (Network):     IP addressing (multicast or unicast)
Layer 2 (Data Link):   Ethernet frames, QoS (DSCP priority tagging)
Layer 1 (Physical):    CAT5e/CAT6 cable, RJ45 connectors
```

**Dante Clocking:**
- **PTP (Precision Time Protocol - IEEE 1588):** Synchronizes all devices to <1µs
- **Master Clock Election:** Automatic - best clock becomes master
- **Manual Override:** Can force a specific device as master clock
- **Sample Rate:** Set globally via Dante Controller software

**Dante Network Topologies:**

**Primary/Secondary (Redundancy):**
```
Device A                     Device B
[NIC 1] ──Primary Net───── [NIC 1]
[NIC 2] ──Secondary Net─── [NIC 2]

- Two completely separate networks
- ~2ms failover if primary fails
- No connection between primary/secondary switches
```

**Daisy Chain (Simple Setup):**
```
Console ──→ Device 1 ──→ Device 2 ──→ Device 3
            [2-port      [2-port      [2-port
             switch]      switch]      switch]
```

**Star Topology (Recommended for Large Systems):**
```
           ┌─ Device 1
           ├─ Device 2
  Switch ──┼─ Device 3
           ├─ Console
           └─ DSP
```

**Dante Virtual Soundcard:**
- Software that creates Dante endpoints on a computer
- Connect DAW directly to Dante network
- Windows/Mac support

**Manufacturers Using Dante:**
- Yamaha (CL/QL/TF/Rivage consoles)
- DiGiCo (SD series)
- Allen & Heath (dLive, Avantis)
- d&b audiotechnik (DS10/DS20 DSP)
- Shure (wireless systems, microphones)
- QSC (Q-SYS, amplifiers)
- Focusrite/Focusrite RedNet
- Soundcraft (Vi series)

---

#### 2. **AES67 (Open Standard)**

**Interoperability Standard**

**Specifications:**
- **Standard:** Open (Audio Engineering Society)
- **Purpose:** Interoperability between different AoIP protocols
- **Transport:** Layer 3 (IP multicast)
- **Latency:** Configurable (typically 1-5ms)
- **Clock:** PTP (IEEE 1588-2008)
- **Sample Rates:** 44.1, 48, 88.2, 96 kHz

**What AES67 Does:**
- Allows different AoIP systems to communicate (Dante ↔ Ravenna ↔ Livewire)
- Defines minimum requirements for interoperability
- Not a complete protocol - focuses on transport layer

**AES67 Mode in Dante:**
- Dante devices can enable "AES67 Mode"
- Allows Dante to talk to non-Dante AES67 devices
- Requires manual IP address/multicast configuration
- Slightly higher latency than native Dante

**Compatibility:**
```
Dante Device (AES67 enabled) ←→ Ravenna Device
Dante Device (AES67 enabled) ←→ Livewire Device
Dante Device ←(native Dante)→ Dante Device (lower latency)
```

---

#### 3. **AVB/TSN (Audio Video Bridging / Time-Sensitive Networking)**

**IEEE Standard Protocol**

**Specifications:**
- **Standard:** IEEE 802.1 (open standard)
- **Transport:** Layer 2 only (cannot route through standard routers)
- **Latency:** <2ms guaranteed
- **Sample Rates:** Up to 192 kHz
- **Channels:** Streams of 2-8 channels each
- **Network:** Requires AVB-capable switches

**AVB Suite of Standards:**
- **802.1AS:** Timing and synchronization (gPTP - generalized Precision Time Protocol)
- **802.1Qav:** Traffic shaping (reserved bandwidth for audio)
- **1722:** Audio/video data encapsulation (AVTP - AV Transport Protocol)
- **1722.1:** Device discovery and connection management (AVDECC/ATDECC)

**Milan (AVB Certification):**
- Certification program by Avnu Alliance
- Ensures AVB devices from different manufacturers work together
- Stricter requirements than basic AVB
- Growing adoption in pro audio

**Manufacturers Using AVB/Milan:**
- Meyer Sound (Galileo Galaxy, MAPP processors)
- L-Acoustics (LA Network Manager, P1 processor, amplifiers)
- d&b audiotechnik (DS20/DS100 with Milan option)
- Biamp (Tesira)
- Avid (Pro Tools MTRX)

**AVB vs Dante:**
| Feature | Dante | AVB/Milan |
|---------|-------|-----------|
| Routing | Layer 3 (through routers) | Layer 2 (switch-only) |
| Switches | Standard Gigabit + QoS | AVB-capable switches required |
| Adoption | Very high (pro audio) | Growing (especially Milan) |
| Latency | <1ms | <2ms |
| Open/Proprietary | Proprietary (licensed) | Open standard |

---

#### 4. **Other Notable Protocols**

**MADI (Multichannel Audio Digital Interface):**
- **Channels:** 64 @ 48kHz (32 @ 96kHz)
- **Transport:** Coax (BNC, 100m) or Fiber (SC, 2km+)
- **Use:** Point-to-point high channel count (not networked)
- **Common:** Broadcast, recording studios, live consoles

**CobraNet (Cirrus Logic):**
- **Legacy protocol** (1990s)
- **Channels:** 64 @ 48kHz
- **Latency:** 1.33ms or 2.66ms
- **Status:** Largely replaced by Dante
- **Still used:** Some installed QSC systems

**Ravenna/AES67:**
- **Standard:** Open, similar to AES67
- **Manufacturer:** Developed by Lawo/Merging Technologies
- **Use:** Broadcast, high-end recording
- **Compatibility:** Natively compatible with AES67

**Livewire/AES67 (Telos Alliance):**
- **Use:** Broadcast radio/TV
- **Channels:** High capacity
- **Compatibility:** AES67 compatible

**WheatNet-IP (Wheatstone):**
- **Use:** Broadcast radio
- **Proprietary:** Wheatstone equipment only

---

### Network Infrastructure for Audio over IP

#### **Switch Requirements**

**Minimum Requirements:**
- **Gigabit Ethernet:** 1000 Mbps (100 Mbps insufficient for most systems)
- **QoS (Quality of Service):** DSCP or 802.1p priority tagging
- **IGMP Snooping:** Manages multicast traffic efficiently
- **Low Latency:** <30µs per switch hop
- **Energy Efficient Ethernet (EEE):** Disable! Causes packet loss

**Recommended Features:**
- **Managed Switch:** Configure VLANs, QoS, monitoring
- **Port Mirroring:** Traffic analysis and troubleshooting
- **Jumbo Frames:** Support for >1500 byte MTU (optional, but helpful)
- **Link Aggregation:** LACP for redundant uplinks

**Popular Switches for Audio over IP:**
- Cisco Catalyst (2960, 9300 series)
- Netgear M4300 series
- HPE/Aruba 2530/2540
- Ubiquiti UniFi (with proper QoS config)
- Extreme Networks

**QoS Configuration Example (Dante):**
- **Dante Audio:** DSCP 46 (Expedited Forwarding) - highest priority
- **Dante PTP (clock):** DSCP 46 - highest priority
- **Dante Control:** DSCP 34 (AF41) - medium-high priority
- **Other network traffic:** DSCP 0 (Best Effort) - lowest priority

#### **Network Topology Best Practices**

**Flat Network (Simple):**
```
All Dante devices on same subnet: 192.168.1.0/24
Works for small systems (<50 devices)
```

**VLANs (Better):**
```
VLAN 10: Dante Audio (192.168.10.0/24)
VLAN 20: Control/Tablet (192.168.20.0/24)
VLAN 30: IT/Office network (192.168.30.0/24)

Isolates audio from other traffic
```

**Redundant Network (Production):**
```
Core Switch A ←→ Core Switch B (redundant link)
     ↓                 ↓
Edge Switch 1    Edge Switch 2
     ↓                 ↓
Audio Devices (dual-homed to both edge switches)
```

#### **Cable Requirements**

- **CAT5e:** Adequate for Gigabit, up to 100m
- **CAT6:** Better shielding, recommended for audio
- **CAT6a/CAT7:** Overkill for current protocols (useful for future 10G)
- **Shielded (STP):** Use in high-EMI environments
- **Unshielded (UTP):** Fine for most installations

**Maximum Distance:**
- 100 meters (328 feet) per cable segment
- Use fiber for longer runs (can go kilometers)
- Fiber media converters: Ethernet ↔ Fiber

---

### Bandwidth Calculations

**Dante Bandwidth per Channel @ 48kHz:**
- Unicast: ~5.5 Mbps per channel (includes overhead)
- Multicast: ~5.5 Mbps total for all receivers (more efficient)

**Example System:**
- 32 channels console → DSP: 32 × 5.5 = 176 Mbps
- 16 channels DSP → Amps: 16 × 5.5 = 88 Mbps
- Total: ~264 Mbps (~26% of 1 Gbps link)

**Rule of Thumb:**
- Keep network utilization <70% for Dante
- 1 Gbps link = ~120 channels max @ 48kHz (safely)
- Consider 10 Gbps for very large systems (1000+ channels)

---

### Clocking and Synchronization

**Why Critical:**
- All digital audio devices must sample at exactly the same rate
- Even 1 sample difference causes clicks/pops
- Network jitter can affect audio quality

**PTP (Precision Time Protocol):**
```
Grandmaster Clock (most accurate clock)
     ↓
Boundary Clock (switch with PTP)
     ↓ ↓ ↓
Slave Devices (lock to grandmaster)

Accuracy: <1 microsecond across network
```

**Clock Priority:**
1. External GPS/Atomic clock (if present)
2. Dante device set as "Preferred Master"
3. Best available clock (automatic election)

**Sample Rate Conversion:**
- Avoid if possible (degrades audio quality slightly)
- Some devices have built-in SRCs (Dante ↔ analog at different rate)
- Keep entire system at one sample rate (usually 48kHz)

---

### Troubleshooting Audio over IP

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No audio | No clock sync | Check PTP lock status |
| Clicks/pops | Packet loss | Check cable, switch load, QoS |
| Dropouts | Network congestion | Reduce traffic, upgrade switch |
| Latency too high | AES67 mode or multi-hop | Use native protocol, reduce hops |
| Can't discover devices | Wrong subnet/VLAN | Verify IP addressing, IGMP snooping |
| Intermittent issues | EEE enabled | Disable Energy Efficient Ethernet |
| Clocking issues | Multiple masters | Set one preferred master |

**Monitoring Tools:**
- **Dante Controller:** Device status, latency, bandwidth
- **Wireshark:** Packet capture and analysis
- **Switch monitoring:** Port utilization, errors, QoS stats
- **Audinate DVS Monitor:** Real-time Dante network analysis

---

### Comparison: AES/EBU vs Audio over IP

| Feature | AES/EBU | Audio over IP (Dante/AVB) |
|---------|---------|---------------------------|
| **Channels per cable** | 2 | 100+ |
| **Cable type** | XLR | Ethernet (RJ45) |
| **Distance** | 100m max | 100m per hop (unlimited hops) |
| **Routing** | Fixed point-to-point | Flexible software routing |
| **Installation** | Complex (many cables) | Simple (one network) |
| **Latency** | ~0ms (direct) | <1-2ms |
| **Troubleshooting** | Simple (cable/sync) | Complex (network knowledge) |
| **Cost per channel** | High (many cables/connectors) | Low (one infrastructure) |
| **Best for** | Simple point-to-point | Large, complex systems |

---

### Practical Example: Medium Venue System

**System:**
- 64-channel digital console
- DSP processor (8 in, 16 out)
- 8 amplifiers with Dante inputs (2 channels each)

**Dante Network:**
```
           Cisco SG350 (Gigabit Managed Switch)
                 ↓
    ┌────────────┼────────────┬─────────────┐
    ↓            ↓            ↓             ↓
Console      DSP          Amp 1-4       Amp 5-8
(64 ch out)  (8 in,       (Dante in)    (Dante in)
             16 out)

Flows:
- Console → DSP: 8 channels (multicast)
- DSP → Amps: 16 channels total (unicast or multicast)
- Total bandwidth: ~132 Mbps (~13% of 1 Gbps)
```

**Configuration:**
1. All devices on VLAN 10 (Audio): 192.168.10.0/24
2. QoS enabled on switch (DSCP 46 for audio)
3. IGMP Snooping enabled
4. Console set as Preferred Master Clock
5. Dante latency: 1ms (default)
6. Primary network only (no redundancy)

**Advantages:**
- Single network cable to each device
- Flexible routing via Dante Controller
- Easy to expand (add more amps/DSP)
- Remote monitoring and control
