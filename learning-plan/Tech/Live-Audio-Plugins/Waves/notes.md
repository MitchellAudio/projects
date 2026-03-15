# Waves Audio — SoundGrid Ecosystem & Live Plugin Processing

Detailed notes on how the Waves SoundGrid platform works, how servers are interfaced, and how Waves plugins are deployed in live production environments.

---

## Table of Contents

1. [Overview of the Waves SoundGrid Ecosystem](#1-overview-of-the-waves-soundgrid-ecosystem)
2. [SoundGrid Network Architecture](#2-soundgrid-network-architecture)
3. [SoundGrid Servers](#3-soundgrid-servers)
4. [SoundGrid I/O Devices](#4-soundgrid-io-devices)
5. [Interfacing with Digital Consoles](#5-interfacing-with-digital-consoles)
6. [SoundGrid Studio (Host Software)](#6-soundgrid-studio-host-software)
7. [eMotion LV1 — Software Console](#7-emotion-lv1--software-console)
8. [Latency in the SoundGrid System](#8-latency-in-the-soundgrid-system)
9. [SoundGrid Driver and Integration Modes](#9-soundgrid-driver-and-integration-modes)
10. [Setting Up a SoundGrid System — Step by Step](#10-setting-up-a-soundgrid-system--step-by-step)
11. [DSP Capacity and Plugin Load](#11-dsp-capacity-and-plugin-load)
12. [Common Waves Plugins Used Live](#12-common-waves-plugins-used-live)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Overview of the Waves SoundGrid Ecosystem

**SoundGrid** is a Waves Audio proprietary **networked audio and plugin processing platform** designed for low-latency, real-time use in live sound, broadcast, and recording.

The system has three main components:

```
┌──────────────────────────────────────────────────────┐
│                    SoundGrid Network                  │
│                  (Gigabit Ethernet)                   │
│                                                      │
│  [SoundGrid I/O]  ←→  [SoundGrid Server]  ←→  [Host] │
│  (Stage Box/Rack)       (Plugin DSP)         (Console │
│                                               or PC)  │
└──────────────────────────────────────────────────────┘
```

- **I/O Devices** — Convert analogue audio to SoundGrid digital audio (e.g., stage boxes, rack I/O)
- **Servers** — Run the Waves plugins with dedicated DSP hardware
- **Host** — The control surface or software (console or computer) that routes audio and applies plugins

All three communicate over a **dedicated Gigabit Ethernet switch** using the SoundGrid protocol (a proprietary low-latency audio-over-IP system).

---

## 2. SoundGrid Network Architecture

### Physical Network Requirements
- **Dedicated Gigabit Ethernet switch** — SoundGrid traffic must be isolated from general IT traffic
- Cat5e minimum, Cat6 or better recommended
- Switch must support **IGMP snooping** (multicast management)
- Recommended switches: Cisco SG series, Netgear GS series, D-Link DGS series

### Network Topology
```
[Stage Box / I/O] ─────┐
                        │
[Console or PC]  ──────┤──── [Gigabit Ethernet Switch] ──── [SoundGrid Server]
                        │
[Additional I/O] ─────┘
```

- All devices communicate on the same Layer 2 network segment (no routing between subnets)
- IP addressing: SoundGrid devices use static IPs; typically 192.168.x.x or 10.x.x.x
- **SoundGrid Manager** software auto-discovers all devices on the network and handles routing

---

## 3. SoundGrid Servers

SoundGrid Servers are **dedicated hardware units** that provide DSP (Digital Signal Processing) capacity to run Waves plugins in real time. They do not have audio I/O directly — they receive and return audio over the SoundGrid network.

### Current Server Models (as of 2025/2026)

#### SoundGrid Impact Server
- Entry-level / compact
- 1U rack mount
- Suitable for smaller shows (theatre, corporate, mid-size live events)
- Lower DSP capacity than Extreme or Proton servers
- Recommended for ~16–32 channel rigs

#### SoundGrid Extreme Server C
- High DSP capacity
- 1U rack mount
- Designed for large-scale live events, festivals, touring
- Can host significantly more plugin instances simultaneously
- Common in professional touring and broadcast rigs

#### SoundGrid Proton (eMotion LV1 built-in)
- Purpose-built for the eMotion LV1 software console
- Contains both the server DSP and the computer to run LV1
- All-in-one solution for the Waves software console workflow

### How Servers Work
1. Audio arrives at the server via the SoundGrid network (Ethernet packets)
2. The server's **DSP chips** (similar to ASICs designed for audio maths) decode the network packets
3. Plugins are loaded onto the DSP — each plugin instance uses a defined amount of DSP
4. Processed audio is re-packaged and returned to the network
5. The host (console or SoundGrid Studio) assigns which channels go to which plugin instances

---

## 4. SoundGrid I/O Devices

I/O devices are the analogue (and digital) interfaces that connect microphones, instruments, and other audio sources to the SoundGrid network.

### Common Waves SoundGrid I/O

#### Waves DiGiGrid MGB / MGO
- Interfaces between SoundGrid and **MADI** (Multi-channel Audio Digital Interface)
- MGB = MADI over BNC coax
- MGO = MADI over optical fibre
- 64 channels bidirectional (at 48kHz)
- Used to connect SoundGrid to consoles that have MADI ports (DiGiCo, SSL, Lawo, etc.)

#### Waves DiGiGrid D (and DQ)
- Standalone SoundGrid I/O
- Built-in mic preamps
- Useful for standalone SoundGrid rigs without a separate console

#### Third-Party MADI / Dante Gateways
- Because many consoles output MADI or Dante natively, gateway devices (e.g., Focusrite RedNet MP8R, Optocore) are often used to bridge between the console's native protocol and the SoundGrid network

---

## 5. Interfacing with Digital Consoles

The most common live workflow involves inserting a SoundGrid system **between the console and its outputs** or via an insert point on the console. Here are the main integration methods:

### Method 1: MADI Interface (Most Common)
```
[Console] ──MADI out──► [DiGiGrid MGB/MGO] ──SoundGrid──► [Server (plugins)] ──SoundGrid──► [DiGiGrid MGB/MGO] ──MADI in──► [Console]
```
- Console sends audio out via MADI (up to 64ch)
- DiGiGrid converts MADI to SoundGrid
- Audio is processed by plugins on the server
- Processed audio is returned via MADI to the console insert return inputs
- Works with: DiGiCo, SSL Live, Lawo, Studer, Yamaha CL/PM (with MADI card)

### Method 2: Direct SoundGrid Integration (Native Console Plugin)
- Some consoles have built-in SoundGrid integration — **no external hardware needed**
- The console is on the SoundGrid network and communicates directly with the server
- Supported consoles include:
  - **Yamaha RIVAGE PM** series (with Waves card)
  - **DiGiCo Quantum** series (with SoundGrid option)
  - **SSL Live** (Waves integration)
  - **Allen & Heath dLive** (with SoundGrid option)

### Method 3: SoundGrid Studio on a Laptop
```
[Console] ──USB/Dante/MADI──► [Computer running SoundGrid Studio] ──SoundGrid──► [Server]
```
- A laptop or desktop runs **SoundGrid Studio** software
- Audio is routed to and from the computer via the console's USB or network interface
- The computer sends to the SoundGrid server for plugin processing
- Less common in professional touring; more common in smaller productions

### Method 4: eMotion LV1 as the Console
- The console **is** the SoundGrid host — no separate mixing desk
- A touchscreen computer runs eMotion LV1
- Audio comes from SoundGrid I/O devices (e.g., DiGiGrid stage boxes)
- The SoundGrid server handles all plugin processing
- Typically requires a dedicated laptop/tablet surface controller

---

## 6. SoundGrid Studio (Host Software)

**SoundGrid Studio** is the Waves software application that:
- Discovers and manages all SoundGrid devices on the network
- Routes audio between I/O devices and the server
- Allows you to open, configure, and use Waves plugins in a simple rack-style interface
- Acts as the bridge between the physical audio network and the plugins

### Key Views in SoundGrid Studio
- **Inventory** — shows all discovered SoundGrid devices (servers, I/O, and the computer itself)
- **Patch** — the audio routing matrix (which inputs go to which plugin racks, which outputs come from where)
- **Racks** — the plugin insert racks where you load and configure plugins per channel

> SoundGrid Studio is not a full mixing console — it has no faders or mix busses. It is purely a plugin host and routing matrix, designed to be used alongside an existing console.

---

## 7. eMotion LV1 — Software Console

**eMotion LV1** is Waves' own software-based digital mixing console that runs entirely in the SoundGrid ecosystem.

- Runs on a standard PC or Mac
- Touchscreen optimised (Dell, HP commercial touch displays are common)
- Supports up to **64 channels** (base) expandable with licenses
- All DSP (including mixing engine) runs on the SoundGrid server — not on the host computer's CPU
- Very popular in musical theatre, corporate events, festivals with limited console budgets
- Fully supports all Waves plugins without any extra hardware interfacing

### LV1 Signal Flow
```
[Stage Box / I/O] ──SoundGrid──► [SoundGrid Server (mix engine + plugins)] ──SoundGrid──► [Outputs / IEM / PA]
                                              ▲
                                    [LV1 Software on PC/Mac]
                                    (control surface only — no DSP)
```

---

## 8. Latency in the SoundGrid System

Latency is a key concern in live audio. SoundGrid is specifically designed to minimise it.

### Reported Latency Figures (Waves spec)
| Configuration | Latency |
|---|---|
| SoundGrid network (one hop) | < 0.25ms |
| Server processing (plugin chain) | ~0.8ms – 1.5ms |
| Full round trip (in → server → out) | ~1 – 3ms total |

> These figures are for a well-configured, dedicated SoundGrid network. Shared networks, incorrect switch configuration, or high plugin counts can increase latency.

### What Affects Latency
- **Number of plugin instances** — heavier chains may use more buffering
- **Switch quality and configuration** — an unmanaged switch or shared network will add jitter
- **Cable length** — not significant at Ethernet speeds over typical stage distances
- **Sample rate** — higher sample rates (96kHz) reduce buffering time but increase bandwidth demand

### Compensating for SoundGrid Latency at the Console
- When using SoundGrid as an insert on a console, the return signal is delayed vs. the direct (dry) signal
- Most modern consoles have **insert delay compensation** — you enter the round-trip latency in milliseconds and the console delays the dry path to match
- **Measure** the actual latency using a loopback test with SoundGrid Manager before compensating

---

## 9. SoundGrid Driver and Integration Modes

### SoundGrid ASIO / Core Audio Driver
- Waves provides a **SoundGrid ASIO** driver (Windows) and **SoundGrid Core Audio** driver (macOS)
- These allow a computer to appear as an audio interface device to any DAW or software, but using the SoundGrid network as the audio transport
- Useful when running a DAW (Pro Tools, Logic) alongside a SoundGrid system for recording or virtual soundcheck

### Virtual Soundcheck with SoundGrid
- A common live workflow: record the show to a DAW through SoundGrid
- At soundcheck, play back the recording through SoundGrid — the console sees it as if the band is playing live
- Engineers can tune the mix and plugin settings without the band present

---

## 10. Setting Up a SoundGrid System — Step by Step

### Pre-Show Setup Checklist
1. **Network Setup**
   - Connect all SoundGrid devices and the host computer to the dedicated Gigabit switch
   - Ensure all devices have unique static IP addresses on the same subnet
   - Verify IGMP snooping is enabled on the switch

2. **Device Discovery**
   - Open **SoundGrid Manager** (or SoundGrid Studio)
   - All online SoundGrid devices appear in the Inventory
   - Assign the server as the "active server" for the session

3. **Audio Routing**
   - In the Patch view, route console outputs (via MADI or direct SoundGrid) to plugin rack inputs
   - Route plugin rack outputs back to the console insert returns

4. **Plugin Loading**
   - Open plugin racks in SoundGrid Studio or LV1
   - Load the required plugins into each channel's rack
   - Load saved presets or initialise from scratch

5. **Latency Check**
   - Run a loopback test to measure actual round-trip latency
   - Enter the measured value into the console's insert delay compensation

6. **Soundcheck**
   - Confirm audio passing through each plugin instance
   - Check DSP meter is not at capacity (leave headroom)
   - Save the session

7. **Show Backup**
   - Export all plugin presets and the SoundGrid session file
   - Store on a USB drive separate from the primary computer

---

## 11. DSP Capacity and Plugin Load

Each SoundGrid server has a finite amount of DSP capacity. Waves quantifies this as a **percentage** shown in SoundGrid Manager.

### Factors That Increase DSP Usage
- Number of plugin **instances** (each channel strip = multiple instances)
- Plugin **complexity** (a simple EQ uses less DSP than a reverb)
- **Sample rate** (96kHz uses roughly double the DSP vs. 48kHz)
- Stereo instances use more DSP than mono instances

### Best Practices
- Keep DSP load below **75–80%** at all times to leave headroom for transients and unexpected load
- If running near capacity, consider:
  - Adding a second SoundGrid server (they can be clustered)
  - Using lighter-weight alternative plugins for less critical channels
  - Reducing sample rate if not required
- **Never** update server firmware or plugins during a show run

---

## 12. Common Waves Plugins Used Live

| Plugin | Type | Common Use |
|---|---|---|
| **C6 Multiband Compressor** | Dynamics | Vocal control, de-essing, bus processing |
| **H-Comp Hybrid Compressor** | Dynamics | Drums, bass, analogue-style compression |
| **SSL G-Master Bus Compressor** | Dynamics | FOH bus glue |
| **dbx 160 Compressor** | Dynamics | Drums — classic punch |
| **API 2500** | Dynamics | Bus compression, drums |
| **F6 Dynamic EQ** | EQ | Surgical frequency control, feedback management |
| **Paz Analyzer** | Metering | Frequency and stereo analysis |
| **H-Delay** | Time-based | Slapback, tap-tempo delay |
| **Abbey Road Reverb Plates** | Time-based | Vocal reverb, classic plate sound |
| **IR-Live Convolution Reverb** | Time-based | Acoustic space reverb |
| **Vocal Rider** | Automation | Automatic vocal level riding |
| **WLM Plus Loudness Meter** | Metering | Broadcast loudness compliance |
| **Clarity Vx** | Noise reduction | Vocal clarity, background noise reduction |
| **InPhase** | Phase | Phase alignment between mics / channels |

---

## 13. Troubleshooting

### No Devices Appearing in SoundGrid Manager
- Check all devices are on the same physical switch
- Verify IP addresses are on the same subnet
- Check for firewall blocking on the host computer
- Try a different Ethernet port or cable

### Audio Dropout / Clicks / Pops
- Check switch for packet collisions (shared network traffic)
- Check DSP load — if at 100%, drop plugin instances
- Increase the server's network buffer size in SoundGrid Manager
- Verify cable quality (Cat5e minimum, no damaged connectors)

### High Latency
- Check switch IGMP snooping is enabled (prevents multicast flooding)
- Ensure no other devices are on the same network segment
- Reduce plugin chain depth on critical channels

### Plugin Not Loading on Server
- Verify the plugin is licensed (check Waves License Center)
- Confirm plugin version is compatible with current server firmware
- Re-sync licenses in Waves License Center and restart SoundGrid Studio

### Console Insert Return Has No Signal
- Confirm SoundGrid patch routes plugin output back to the correct console MADI channel
- Check insert point is enabled on the console channel (not bypassed)
- Verify MADI channel count and mapping matches between DiGiGrid and console settings

---

## References & Further Reading

- Waves SoundGrid Setup Guide: [www.waves.com/support/soundgrid](https://www.waves.com/support/soundgrid)
- Waves SoundGrid Manager User Guide (PDF — available from Waves Support)
- DiGiGrid MGB/MGO User Guide
- Waves eMotion LV1 Operator's Manual
- Yamaha RIVAGE PM Series — SoundGrid Integration Application Note
- DiGiCo Quantum Series — Waves SoundGrid Integration Guide
- Allen & Heath dLive — Waves Plugin Integration Application Note
