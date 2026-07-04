# Q-SYS Level 1 — Designer Certification Notes

> **About Level 1:** The core technical certification for Q-SYS. Validates ability to build, configure, and deploy a complete Q-SYS design from scratch. Proctored online exam; requires Level 0 as prerequisite. Earns AVIXA CTS RU credits.

---

## Table of Contents

1. [Design File Fundamentals](#1-design-file-fundamentals)
2. [Inventory and Hardware Assignment](#2-inventory-and-hardware-assignment)
3. [Audio Signal Flow and Gain Structure](#3-audio-signal-flow-and-gain-structure)
4. [Core DSP Components](#4-core-dsp-components)
5. [Acoustic Echo Cancellation (AEC)](#5-acoustic-echo-cancellation-aec)
6. [Dante Integration](#6-dante-integration)
7. [Routing: Matrix Mixers and Routers](#7-routing-matrix-mixers-and-routers)
8. [User Control Interfaces (UCI)](#8-user-control-interfaces-uci)
9. [Named Controls and Control Flow](#9-named-controls-and-control-flow)
10. [Snapshots and Change Groups](#10-snapshots-and-change-groups)
11. [Deploying and Running a Design](#11-deploying-and-running-a-design)
12. [System Status and Basic Troubleshooting](#12-system-status-and-basic-troubleshooting)
13. [Exam Tips — Level 1](#13-exam-tips--level-1)

---

## 1. Design File Fundamentals

### Creating a New Design

1. Open Q-SYS Designer → **File → New**
2. Select the **Core model** — must match the physical hardware the design will run on
3. Save as a `.qsys` file (keep under version control or document changes)

### Schematic Canvas

- The schematic is a drag-and-drop canvas where components are placed and wired
- Components are found in the **Component Library** (left panel)
- Use **pages** to organise large designs logically (e.g., Page 1: Audio, Page 2: Control, Page 3: UCI)
- Right-click canvas → **Add Text Block** to add descriptive notes/labels to the schematic

### Component Wiring Rules

| Connection Type | Pin Colour | Notes |
|-----------------|-----------|-------|
| Audio signal | Green | Carries audio; must match channel count |
| Control data | Blue/Purple | Carries values (levels, booleans, strings) |
| Video | Orange/Yellow | HDMI/Display stream routing |

- A single output pin can fan out to multiple input pins (one-to-many)
- An input pin can only receive from **one** source (many-to-one is not allowed for audio; use a mixer instead)
- Mismatched pin types (e.g., audio → control) will show as an error

### Design Validation

- **Design → Check Design** will highlight errors before deployment
- Common errors: unconnected required pins, channel count mismatches, hardware not assigned

---

## 2. Inventory and Hardware Assignment

### The Configurator

- Accessed via **Design → Configurator** or the tab at the bottom of Designer
- Lists all physical Q-SYS hardware discovered on the Q-LAN network
- Drag physical devices from the discovered list onto the corresponding inventory items in the design
- Hardware must be assigned before the design can be deployed to a Core

### Adding Hardware to the Design

- In the schematic, add hardware components (e.g., **IO-8 Flex**, **Dante NIC**, **NV-Series endpoint**) from the component library
- Each hardware component creates a corresponding inventory entry
- The Configurator maps: **Design Component ↔ Physical Device**

### Core Licensing

- Q-SYS features are licensed per Core:
  - **Scripting (Lua)** — included free on all Cores running v9.x+
  - **UCI** — included free on all Cores running v9.x+
  - **Video** — requires a separate video license (NV endpoints)
  - **SIP** — requires a SIP license
- Check Core licensing via Q-SYS Core Manager (web UI) or **Design → Core Properties**

---

## 3. Audio Signal Flow and Gain Structure

### Signal Flow Principle

```
Source → Input Gain → Processing → Output Gain → Destination
```

Every component in the signal chain adds or subtracts gain. Proper staging prevents:
- **Clipping** (too much signal — distortion/digital noise)
- **Noise floor** (too little signal — amplifying noise)

### Target Levels

| Signal Type | Target Nominal | Headroom |
|-------------|---------------|---------|
| Mic input (post-preamp) | -40 to -20 dBu | varies by mic |
| Line-level processing | **-18 dBFS** | ~18 dB before 0 dBFS |
| Output to amplifier | -10 to 0 dBFS | match amp sensitivity |

- Always aim for meters running in the **green to yellow range** at nominal
- Red (near 0 dBFS) means you are close to clipping — reduce gain upstream

### Setting Input Gain

- **Analog Input components** have a preamp gain control (0–60 dB typical for mic inputs)
- Set gain so the mic signal meters at approximately **-18 dBFS** during normal speech
- Too much gain = feedback risk and clipping; too little = noise

### Channel Count Matching

- Audio connections in Q-SYS Designer are **multichannel**
- Mono components (1 channel), Stereo (2), or multi-channel (N)
- Mismatched channel counts produce a wiring error — check output/input channel counts before connecting

---

## 4. Core DSP Components

### Mixer

- **Mixer component** combines multiple audio inputs to one (or more) outputs
- Each input has independent level, mute, and solo controls
- **Gain control range:** typically -100 dB (off) to +20 dB
- Use for: mic mixing, zone mixing, combining sources before output

### Gain (Simple Level Control)

- Single-channel or multi-channel level adjustment
- Used to trim levels between stages without mixing

### EQ (Parametric / Graphic)

| Type | Controls | Best Use |
|------|---------|---------|
| **Parametric EQ** | Frequency, Gain, Q (bandwidth) | Precise correction, feedback notching |
| **Graphic EQ** | Fixed-frequency band sliders | Quick room tuning, zone matching |
| **High/Low Pass** | Frequency, slope | Remove sub-rumble, cut high noise |

- In conferencing: high-pass filter at ~100–150 Hz removes HVAC rumble from mics
- Shelving filters boost/cut everything above/below a fixed frequency

### Compressor / Limiter

| Control | Purpose |
|---------|---------|
| **Threshold** | Level at which compression begins |
| **Ratio** | How much compression is applied (e.g., 4:1) |
| **Attack** | How fast compression engages after threshold is crossed |
| **Release** | How fast compression disengages after signal drops |
| **Knee** | Hard (abrupt) or soft (gradual) onset of compression |
| **Makeup Gain** | Restore output level after compression reduces it |

- **Limiter** = compressor with a very high ratio (∞:1 or >10:1) — acts as a hard ceiling

### Delay

- Adds time delay to a signal (in milliseconds or samples)
- **Use cases:**
  - Time-align under-balcony speakers with main cluster
  - Prevent comb filtering when two speakers cover the same area
- Rule of thumb: 1 ms delay ≈ 1 foot of sound travel (at 20°C / 68°F)

### Feedback Suppressor

- Detects feedback frequencies and applies narrow notch filters automatically
- Q-SYS: has **Fixed** (locked once identified) and **Dynamic** (continuously re-evaluates) modes
- Not a substitute for proper gain structure and mic placement — use as a safety net

### Automatic Gain Control (AGC)

- Automatically adjusts input gain to maintain a consistent output level
- Useful for: presenters who move toward/away from a mic, inconsistent microphone levels
- Set **target level**, **attack/release** for transparent operation

### Noise Reduction / Noise Gate

| Component | Behaviour |
|-----------|----------|
| **Noise Gate** | Cuts signal below a threshold (hard on/off) |
| **Noise Reduction** | Attenuates noise floor continuously (softer, AI-based in newer versions) |

---

## 5. Acoustic Echo Cancellation (AEC)

### What AEC Does

- In conferencing, the **far-end audio** played over the room speakers can re-enter the room microphones and be sent back to the far-end — called **acoustic echo**
- AEC removes the loudspeaker signal from the mic before it is transmitted
- Essential for any room with open microphones and a loudspeaker

### How It Works

```
Speaker Signal (Reference) ─────────────────────────────────┐
                                                             ▼
Mic Signal (Raw) ──────────────► AEC Component ──────────► Clean Mic Output
                                    (subtracts speaker signal from mic)
```

- The AEC component needs **both** the mic signal and a **reference signal** (the exact audio being played through the room speakers)
- The reference must be the **dry** signal going to the speaker, not a recording of the room

### AEC in Q-SYS Designer

- Use the **AEC Input** component (available on Cores with AEC capability, or IO Frames with AEC)
- The AEC reference input must be connected to the output of the mix/processing chain — before the amplifier
- **Number of AEC channels** is limited by the hardware; check the Core/frame spec sheet
- After AEC, apply **Noise Reduction** and a **high-pass filter** before sending to the conferencing codec

### Common AEC Mistakes

- Connecting a post-room recording as the reference (introduces latency and inaccuracy)
- Insufficient acoustic treatment in the room (echoes confuse the AEC algorithm)
- AEC reference and loudspeaker signal do not match (level mismatch causes residual echo)

---

## 6. Dante Integration

### Overview

- Q-SYS integrates natively with **Dante** audio over IP
- Dante devices appear in Q-SYS Designer as **Dante Transmitter** and **Dante Receiver** components
- Routing between Q-SYS and Dante devices is done in **Dante Controller** (Audinate's separate utility)

### Dante Components in Q-SYS Designer

| Component | Direction | Description |
|-----------|-----------|-------------|
| **Dante Transmitter** | Q-SYS → Dante | Sends audio from Q-SYS to a Dante network |
| **Dante Receiver** | Dante → Q-SYS | Receives audio from a Dante device into Q-SYS |

- The channel name assigned in Q-SYS Designer must match the channel name subscribed to in Dante Controller

### Dante Controller Workflow

1. Open Dante Controller on a PC on the same network
2. Discover all Dante devices (including Q-SYS Core)
3. Draw routing matrix connections: source channel → destination channel
4. Confirm sample rate and latency settings match across all devices (typically 48 kHz, 1 ms)

### Sample Rate and Clocking

- All Dante devices on the same network must use the **same sample rate** (usually 48 kHz)
- One device is the **Dante clock master** (PTP — Precision Time Protocol); others sync to it
- Q-SYS can be the Dante clock master or follow another master
- Mismatched sample rates cause audible noise/distortion

### Dante vs. Q-LAN

| Feature | Q-LAN | Dante |
|---------|-------|-------|
| Protocol | QSC proprietary | Audinate Dante |
| Used for | Q-SYS native devices | Third-party Dante devices |
| Routing tool | Q-SYS Designer | Dante Controller |
| Discovery | Q-SYS Designer/Configurator | Dante Controller |

---

## 7. Routing: Matrix Mixers and Routers

### Matrix Mixer

- Allows **any input** to be mixed to **any output** with individual cross-point level control
- Think of it as an N×M grid: rows = inputs, columns = outputs
- Use cases: distributed audio systems, zone mixing, combining multiple sources

**Key properties:**
- Number of inputs and outputs is set when placing the component
- Each cross-point has its own gain control (typically -100 to +20 dB) and mute button
- Can also be controlled via Named Controls or UCI

### Cross-Point Router

- Routes inputs to outputs on an **exclusive** basis (no mixing — output follows a single input at a time)
- Use cases: source selection (play 1 of N sources to a zone), switching backgrounds
- Cross-points are controlled with a **Route** control (integer = which input is selected)

### Zone Selector

- A simplified source-select component
- Routes one of several inputs to an output based on a selection number
- Simpler than a full matrix for "select background music source" type controls

### N-to-1 Mixer vs. Matrix Mixer

| | N-to-1 Mixer | Matrix Mixer |
|-|-------------|-------------|
| Input → output mapping | Many in → one out | Any in → any out |
| Cross-point gain control | Per input | Per cross-point |
| Good for | General mixing | Flexible zone routing |

---

## 8. User Control Interfaces (UCI)

### UCI Editor Basics

- Access via **Design → User Control Interface**
- Each design can have multiple UCIs
- UCIs are displayed on: touchscreen panels, tablet browsers (iPad/Android), Windows/macOS, embedded Q-SYS touch panels

### Layout

- Drag controls from the **Control palette** onto the canvas
- **Pages:** add multiple pages per UCI (use buttons or a tab bar to navigate)
- **Themes/Stylesheets:** control colour, font, and appearance globally
- **Background:** set an image or solid colour

### Control Elements

| Control | Use Case |
|---------|---------|
| **Knob / Fader** | Level control (gain, volume) |
| **Toggle Button** | On/off, mute |
| **Momentary Button** | Trigger action while held |
| **Combo Box / List** | Source selection, preset select |
| **Text Box** | Display status, show caller ID, labels |
| **Meter** | VU/PPM level display |
| **LED / Status Indicator** | Show mute state, fault status |
| **Image** | Logos, room diagrams, icons |

### Linking Controls to Named Controls

- Each UCI control element has a **Control** property
- Click the property, then select the **Named Control** in the design to link to it
- The UCI reflects the live value and allows interaction with it

### UCI Deployment

- UCIs are embedded in the `.qsys` design file and deployed to the Core with the rest of the design
- Any browser or touchpanel on the same network can access the UCI via:
  `http://<core-ip>/uci/<uci-name>`
- Q-SYS dedicated touchscreen panels (e.g., TSC series) auto-launch UCIs

---

## 9. Named Controls and Control Flow

### What is a Named Control?

- A **Named Control** is a labelled control point created within a component or at the design level
- It acts as an addressable handle for reading or writing a value in the design
- Can be accessed by:
  - UCI elements
  - Lua scripts
  - External control (TCP, REST, WebSocket, GPIO)
  - Other components in the design (via Control Pin wiring)

### Creating Named Controls

- Double-click any component to open its **Properties**
- Go to the **Controls** tab — find the control you want to expose
- Check **"Pin to schematic"** to create a visible pin on the component
- Right-click a control pin → **Set Name** — this is the Named Control name

### Control Pin Wiring

- Control pins (blue) can be wired between components to link values
- Example: wire a mixer's **Level** control pin to a fader on another component → fader controls level
- Control values flow from source → destination when connected

### Change Groups

- A **Change Group** is a mechanism that allows an external controller or script to subscribe to Named Controls and receive notifications only when values change
- More efficient than polling every control on a timer
- Essential for integrating with AMX, Crestron, or building responsive Lua scripts

---

## 10. Snapshots and Change Groups

### Snapshots

- A **Snapshot** stores the current state of a set of Named Controls (levels, routing, mute states, etc.)
- Recalling a snapshot restores all stored values — like a scene/preset
- Use cases: room configuration presets, time-of-day settings, performance vs. speech modes

**Workflow:**
1. Add a **Snapshot** component to the schematic
2. Configure which Named Controls to include (by entering their control names)
3. Save a snapshot by triggering the **Save** control with a slot number
4. Recall a snapshot by triggering **Load** with the same slot number

### Snapshot Banks

- Snapshots are organised into **banks** (groups of slots)
- Each bank can hold up to 255 snapshots
- Banks allow different groups of snapshots for different zones or pages of the UCI

---

## 11. Deploying and Running a Design

### Saving to Core

1. Connect Q-SYS Designer to the Core via the Q-LAN network
2. Go to **File → Save to Core** (or press F5)
3. Designer uploads the `.qsys` file to the Core and runs it
4. The Core validates the design (hardware assignment, license check) before going live
5. If there are errors, Designer reports them before running

### Emulation Mode vs. Running on Core

| Mode | Description | Use For |
|------|-------------|--------|
| **Emulation** | Runs locally in Designer on your PC | Design and testing, no hardware needed |
| **Live (Core)** | Deployed to physical Core | Production operation |

- In emulation, audio is simulated but does not pass real signal
- UCI elements work in emulation for layout testing
- Always test on hardware before final deployment

### Core Start-Up Behaviour

- Cores automatically load and run the last saved design on power-up
- Configure start-up behaviour in **Core Manager → Settings → Design Start**
- Can be set to: run immediately, wait for confirmation, or not auto-run

### Redundancy (Core-to-Core Failover)

- Some installations use a **redundant Core** (primary + standby)
- The standby Core monitors the primary and takes over if it fails
- Requires two Cores with matching designs and a dedicated sync connection

---

## 12. System Status and Basic Troubleshooting

### StatusPage

- Accessed in Q-SYS Designer when connected to a live Core
- Shows a summary of all devices: green = OK, yellow = warning, red = fault
- Double-click a device to see detailed fault information

### Core Manager (Web UI)

- Access via browser: `http://<core-ip>` (default port 80)
- Key pages:
  - **System:** CPU/RAM usage, temperature, active design
  - **Network:** IP configuration, Q-LAN interface status
  - **Faults:** Active faults list
  - **Update:** Firmware update page

### Common Fault Conditions

| Fault | Likely Cause | Fix |
|-------|-------------|-----|
| Peripheral offline | Network issue, device powered off | Check cable, power, IP |
| Dante link down | Sample rate mismatch, network issue | Verify rates in Dante Controller |
| Core CPU overload | Too many complex components | Reduce design complexity, upgrade Core |
| AEC fault | Reference not connected, hardware limit | Check AEC reference wiring |
| License fault | Feature used without license | Apply correct license to Core |

### Useful Diagnostics

- **Q-SYS Designer → Tools → Q-SYS Utilities** — network discovery, ping tools
- **Dante Controller** — verify Dante routes and clock status
- **Core Manager logs** — download system logs for deep troubleshooting

---

## 13. Exam Tips — Level 1

- Know the **wiring rules**: audio vs. control pins, one-to-many OK, many-to-one requires a mixer
- Understand **AEC signal flow** — where the reference connects and why
- Know the difference between **Matrix Mixer**, **Cross-Point Router**, and **Zone Selector**
- Understand **Named Controls** — how to create them, how UCI and scripts access them
- Know **Snapshot** behaviour — what is saved, how recall works
- Understand **Dante clock master / sample rate** alignment requirements
- Know the deployment workflow: emulation → save to Core → validate → run
- Be able to identify faults from StatusPage and Core Manager descriptions
- Understand **gain structure** targets (-18 dBFS nominal) and the purpose of headroom
- Know Q-SYS licensing: what is free (Scripting, UCI) vs. what requires a license (Video, SIP)
