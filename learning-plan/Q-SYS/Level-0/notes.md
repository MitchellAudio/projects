# Q-SYS Level 0 — Foundations Notes

> **About Level 0:** Free, self-paced online course at [training.qsc.com](https://training.qsc.com). Required prerequisite before attempting any higher-level Q-SYS certification. Covers the Q-SYS ecosystem, hardware, software, and basic platform concepts.

---

## Table of Contents

1. [What is Q-SYS?](#1-what-is-q-sys)
2. [Q-SYS Hardware](#2-q-sys-hardware)
3. [Q-SYS Designer Application](#3-q-sys-designer-application)
4. [Networking in Q-SYS](#4-networking-in-q-sys)
5. [Audio Routing Basics](#5-audio-routing-basics)
6. [Control and User Control Interfaces (UCI)](#6-control-and-user-control-interfaces-uci)
7. [System Management and Monitoring](#7-system-management-and-monitoring)
8. [Key Terms Glossary](#8-key-terms-glossary)

---

## 1. What is Q-SYS?

### Platform Overview

- Q-SYS is a **software-based Audio, Video, and Control (AV&C) platform** made by QSC
- Runs on dedicated QSC hardware (Core processors) and can also run as a **software-only Core** for design and simulation
- Combines audio DSP, video routing, and third-party device control into a single unified system
- Designed primarily for fixed-install environments: conference rooms, performing arts venues, houses of worship, corporate AV, education

### Q-SYS Ecosystem at a Glance

```
┌─────────────────────────────────────────────────────────┐
│                    Q-SYS ECOSYSTEM                      │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐  ┌──────────────┐ │
│  │  Q-SYS Core  │   │   I/O Frames │  │  Peripherals │ │
│  │  (Processor) │◄──│  & Expanders │  │  (Cameras,   │ │
│  │              │   │              │  │   Displays,  │ │
│  └──────┬───────┘   └──────────────┘  │   Panels)    │ │
│         │                             └──────────────┘ │
│         │ Q-LAN (dedicated AV network)                 │
│         ▼                                               │
│  ┌──────────────┐   ┌──────────────┐                   │
│  │  Q-SYS       │   │  External    │                   │
│  │  Designer    │   │  Control     │                   │
│  │  (Software)  │   │  (Lua, API)  │                   │
│  └──────────────┘   └──────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

### Key Capabilities

- **Audio:** DSP mixing, routing, EQ, compression, level control, feedback suppression
- **Video:** Softcodec video conferencing bridging, display routing, streaming
- **Control:** Third-party device control (RS-232, TCP/IP, UDP, IR), custom UCI panels
- **Scalability:** Single room to multi-site enterprise deployments

---

## 2. Q-SYS Hardware

### Core Processors

The Core is the brain of every Q-SYS system. It runs the Q-SYS OS and executes the design file.

| Core | Target Use | Notes |
|------|-----------|-------|
| **Core 110f** | Small rooms (up to ~1,000 connections) | Built-in local I/O (8 mic/line in, 8 line out, 4 AEC) |
| **Core 510i** | Mid-size systems | No built-in I/O; uses external I/O frames |
| **Core 5200** | Large-scale / enterprise | High channel count, redundant power supply |
| **Core 8 Flex** | Flexible mid-range | 8 local analog I/O, expandable via Q-LAN |
| **Core Nano** | Small rooms / conferencing | Compact form, limited DSP resources |
| **Core Flex (software)** | Development / simulation | Runs on a PC; no physical hardware needed |

- All Cores run the same **Q-SYS OS** and **Designer** design files
- Firmware is updated via **Q-SYS Core Manager** (web interface at the Core's IP address)

### I/O Frames and Network Peripherals

| Device Type | Examples | Purpose |
|-------------|---------|---------|
| **I/O Frames** | IO-8 Flex, IO-22 | Local analog I/O expansion, AEC |
| **Dante Peripherals** | SPA series, NL series amplifiers | Audio over IP (Dante protocol) |
| **AV Network Interfaces** | NV-series | HDMI/DisplayPort over Q-LAN (video) |
| **Accessories** | AD-series mic arrays, cameras | USB/AV bridging for conferencing |

### Physical Interface Connections

- **Analog I/O:** XLR (mic/line), RCA, or 3.5mm depending on model
- **Network:** Standard 1GbE or 10GbE Ethernet (Q-LAN)
- **USB:** For conferencing peripherals (webcams, speakerphones)
- **GPIO:** General Purpose I/O for contact closures, logic signals
- **Serial:** RS-232 for third-party device control

---

## 3. Q-SYS Designer Application

### Overview

- **Q-SYS Designer** is the free software used to build, configure, and deploy Q-SYS systems
- Available for Windows and macOS
- Runs in **emulation mode** (offline) or connects to a live Core
- Design files are saved as `.qsys` files

### Application Interface

| Area | Description |
|------|-------------|
| **Schematic** | Main drag-and-drop design canvas; where components are placed and wired |
| **Configurator** | Hardware inventory; assigns physical hardware to design components |
| **Control** | View and interact with control pins live (when connected to a Core) |
| **StatusPage** | Real-time system status, fault monitoring, and alerts |

### Basic Design Workflow

1. **Create a new design** → set Core model (must match physical hardware)
2. **Add components** from the component library (mixer, EQ, AGC, router, etc.)
3. **Wire components** by drawing connections between pins on the schematic
4. **Configure component properties** (levels, filters, routing)
5. **Add UCI** (User Control Interface) panels for operator controls
6. **Save and deploy** design to a Core (File → Save to Core)

### Component Types

- **Signal processing:** Mixer, Gain, EQ, Compressor/Limiter, Delay, Feedback Suppressor
- **I/O:** Analog In/Out, Dante Receiver/Transmitter, AEC Input
- **Control:** Named Controls, Control Pins, Scriptable Controls
- **Routing:** Cross-point Router, Zone Selector, Matrix Mixer
- **AV:** Camera Controller, Display Controller, SoftCodec

### Wiring Conventions

- **Audio pins:** Green connections (signal level)
- **Control pins:** Blue connections (control data / parameter values)
- **Named Controls:** Allow external control from UCI or scripts without direct wiring

---

## 4. Networking in Q-SYS

### Q-LAN

- **Q-LAN** is QSC's branded name for the Ethernet network used to transport audio, video, and control between Q-SYS devices
- Standard Ethernet infrastructure (Cat6/Cat6a recommended)
- Uses **Layer 3** switching and QoS for reliable media transport
- Supports **IGMP snooping** for multicast audio/video streams

### Network Separation (Best Practice)

- Q-SYS recommends a **dedicated AV network** (Q-LAN) separate from the corporate IT network
- Reduces interference from unrelated traffic
- Can use **VLANs** to logically separate Q-LAN from corporate traffic on the same physical switches
- Switch requirements: Gigabit, IGMP snooping, QoS (DSCP marking)

### Dante Integration

- Q-SYS integrates with **Dante** (Audinate's audio over IP protocol)
- Dante peripherals appear in Q-SYS Designer as Dante Transmitter/Receiver components
- Dante devices are discovered and patched using **Dante Controller** (separate Audinate software)
- Q-SYS acts as a Dante device on the network when Dante components are present in the design

### AES67

- Q-SYS supports **AES67** (standard audio-over-IP interoperability protocol)
- Allows integration with non-Dante AoIP devices (e.g., Ravenna, Livewire)

### IP Addressing

- Each Core and Q-SYS peripheral requires a static or DHCP-assigned IP address
- Default factory IP addresses are typically in the `169.254.x.x` (link-local / APIPA) range
- Best practice: assign static IPs or use DHCP reservations for all Q-SYS devices

---

## 5. Audio Routing Basics

### Signal Flow Fundamentals

```
Source → Input Component → Processing Chain → Output Component → Destination
(Mic)    (Analog Input)    (EQ, Comp, etc.)   (Analog Output)   (Speaker)
```

### Gain Structure

- Proper gain staging prevents clipping and noise
- Target nominal operating level: **-18 dBFS** (leaves headroom for transients)
- Each component has adjustable gain; set so meters operate in the nominal range
- Q-SYS meters show **dBFS** (digital full scale); 0 dBFS = maximum, should never clip

### Key Processing Components

| Component | Purpose |
|-----------|---------|
| **Gain** | Simple level control (amplification/attenuation) |
| **EQ** | Parametric/graphic equalization; shape frequency response |
| **Compressor/Limiter** | Dynamic control; prevents clipping, reduces dynamic range |
| **AGC (Automatic Gain Control)** | Automatically adjusts level to maintain consistent output |
| **Delay** | Time-align speakers; prevent comb filtering |
| **Feedback Suppressor** | Detects and notches feedback frequencies |
| **AEC (Acoustic Echo Cancellation)** | Removes loudspeaker signal from mic input (conferencing) |
| **Noise Reduction** | Reduces background noise in mic signals |

### Matrix Mixer vs. Cross-Point Router

| Feature | Matrix Mixer | Cross-Point Router |
|---------|--------------|--------------------|
| Signal mixing | Yes (blend multiple inputs) | No (route only) |
| Level control | Per cross-point | On/off only |
| Use case | Mixing audio zones | Distribution/routing without mixing |

---

## 6. Control and User Control Interfaces (UCI)

### What is a UCI?

- A **User Control Interface (UCI)** is a custom graphical panel designed in Q-SYS Designer
- Displayed on touchscreens, tablets, PCs, or web browsers
- Operators use UCIs to control the system (adjust volume, select inputs, mute, etc.) without accessing Designer directly

### UCI Design Basics

- Built using **UCI Editor** within Q-SYS Designer
- Drag-and-drop controls: knobs, faders, buttons, text displays, meters, images
- Controls are linked to **Named Controls** in the design schematic
- Multiple pages can be created per UCI

### Named Controls

- A **Named Control** is a labelled control point in the design that can be addressed by:
  - UCI panels
  - External control (Lua scripts, REST API, third-party controllers)
  - Other components within the design
- Named Controls are the bridge between the signal processing design and the control layer

### External Control Options

| Method | Use Case |
|--------|---------|
| **UCI (web/touchscreen)** | Operator-facing graphical panels |
| **Lua scripting** | Custom logic, scheduled events, third-party integration |
| **Q-SYS Control APIs** | REST, WebSocket, TCP — for AMX, Crestron, Control4, etc. |
| **GPIO** | Physical contact closures (wall plates, relays) |
| **RS-232 / TCP** | Serial or network control of projectors, displays, etc. |

---

## 7. System Management and Monitoring

### Q-SYS Core Manager

- Web interface accessed via the Core's IP address in a browser
- Used for:
  - Viewing Core status and health
  - Updating firmware
  - Viewing network configuration
  - Rebooting the Core
  - Viewing active design and alarms

### StatusPage

- Built into Q-SYS Designer (accessible when connected to a live Core)
- Shows real-time **fault monitoring** and **system alerts**
- Custom status conditions can be configured within the design

### Fault Monitoring

- Q-SYS has a built-in **fault system** with severity levels:
  - **OK** — No faults
  - **Warning** — Non-critical condition (e.g., network peripheral offline)
  - **Fault** — Critical condition (e.g., Core overloaded, signal clipping)
- Faults can trigger notifications via email (SMTP) or control logic within the design

### Q-SYS Reflect (Cloud Management)

- **Q-SYS Reflect Enterprise Manager** is QSC's cloud-based fleet management tool
- Allows remote monitoring of multiple Q-SYS deployments from a single dashboard
- Features: firmware updates, design deployment, fault monitoring, analytics
- Requires Reflect license (subscription)

---

## 8. Key Terms Glossary

| Term | Definition |
|------|-----------|
| **Core** | The Q-SYS hardware processor that runs the design; the central brain of the system |
| **Design File (.qsys)** | The project file created in Q-SYS Designer containing all components, wiring, and settings |
| **Q-LAN** | QSC's Ethernet-based AV network for audio, video, and control transport |
| **Component** | A DSP building block placed on the schematic (mixer, EQ, delay, etc.) |
| **Pin** | An input or output connection point on a component |
| **Named Control** | A labelled control point in the design that can be addressed externally |
| **UCI (User Control Interface)** | A graphical operator panel built in Q-SYS Designer |
| **Dante** | Audinate's audio-over-IP protocol; natively supported in Q-SYS |
| **AES67** | IEEE standard for interoperable audio-over-IP (supported by Q-SYS) |
| **Emulation Mode** | Running Q-SYS Designer on a PC without a physical Core (for design/testing) |
| **Core Flex** | A software-only Core that runs on a PC/server (no dedicated QSC hardware needed) |
| **IGMP Snooping** | Switch feature required for efficient multicast audio/video on Q-LAN |
| **StatusPage** | Q-SYS system health monitoring interface within Designer |
| **Q-SYS Reflect** | QSC's cloud platform for remote fleet management of Q-SYS systems |
| **dBFS** | Decibels relative to Full Scale; the digital metering standard used in Q-SYS |
| **AEC** | Acoustic Echo Cancellation; removes loudspeaker signal from mic input for conferencing |

---

## Exam Tips — Level 0

- Know the difference between **Core models** and their target use cases
- Understand the **Q-LAN vs. corporate network** separation concept
- Be able to describe the basic **signal flow** through a Q-SYS design
- Know the purpose of **Named Controls** and how UCIs connect to them
- Understand what **Q-SYS Designer** is and the steps to deploy a design to a Core
- Know the roles of **Dante** and **AES67** in the ecosystem
- Understand the purpose of **Q-SYS Core Manager** vs. **Q-SYS Reflect**
