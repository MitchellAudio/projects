# Q-SYS Level 2 — Advanced Systems Designer Notes

> **About Level 2:** Advanced certification for experienced Q-SYS designers. Covers Lua scripting, SIP telephony, video routing, advanced networking (multi-Core, multi-VLAN), external control integration, and complex system management. Proctored online exam; requires Level 1 as prerequisite.

---

## Table of Contents

1. [Lua Scripting in Q-SYS](#1-lua-scripting-in-q-sys)
2. [Advanced Control: External Systems](#2-advanced-control-external-systems)
3. [SIP Telephony](#3-sip-telephony)
4. [Video Routing and NV Endpoints](#4-video-routing-and-nv-endpoints)
5. [Advanced Networking: Multi-Core and Multi-VLAN](#5-advanced-networking-multi-core-and-multi-vlan)
6. [Plugins and the Q-SYS Library](#6-plugins-and-the-q-sys-library)
7. [Advanced UCI Design](#7-advanced-uci-design)
8. [Q-SYS Reflect Configuration](#8-q-sys-reflect-configuration)
9. [Troubleshooting and Diagnostics](#9-troubleshooting-and-diagnostics)
10. [Exam Tips — Level 2](#10-exam-tips--level-2)

---

## 1. Lua Scripting in Q-SYS

### Overview

- Q-SYS uses **Lua 5.3** for control scripting
- Scripts run inside the Q-SYS Core as part of the design
- Access Named Controls, respond to changes, schedule tasks, communicate with external devices
- Script components are placed on the schematic like any other component

### Scripting Components

| Component | Description |
|-----------|-------------|
| **Script** | General-purpose Lua script; runs on trigger or continuously |
| **Scripted Control** | Exposes Named Controls; logic defined by script |
| **Event Scheduler** | Trigger scripts on a calendar/time schedule |
| **Text Controller** | TCP/UDP or RS-232 communication component with Lua event handlers |

### Core Lua Syntax Reference

```lua
-- Get a Named Control value
local level = Controls["Gain.level"].Value       -- numeric
local isMuted = Controls["Mute.mute"].Boolean    -- boolean

-- Set a Named Control value
Controls["Gain.level"].Value = -10.0             -- set to -10 dB
Controls["Mute.mute"].Boolean = true             -- mute on

-- Print to debug console
print("Level is: " .. tostring(level))

-- String control (e.g., text display)
Controls["Display.text"].String = "Conference Room 1"
```

### EventHandler Pattern

- The primary pattern for reacting to Named Control changes:

```lua
Controls["SourceSelect.select"].EventHandler = function(ctl)
  local selection = ctl.Value
  if selection == 1 then
    Controls["Router.output1"].Value = 1
  elseif selection == 2 then
    Controls["Router.output1"].Value = 2
  end
end
```

### Timers

- Use `Timer` to schedule recurring or one-shot actions:

```lua
local myTimer = Timer.New()

myTimer.EventHandler = function()
  -- called every 5 seconds
  Controls["Heartbeat.pulse"].Boolean = not Controls["Heartbeat.pulse"].Boolean
end

myTimer:Start(5)   -- interval in seconds
-- myTimer:Stop() to stop
```

### TCP / UDP Communication (Text Controller)

- The **Text Controller** component handles serial and network communication with Lua event handlers:

```lua
-- Send a command to a display
tcp = TcpSocket.New()
tcp.Connected = function(sock)
  sock:Write("PON\r")   -- power on command
end
tcp.Data = function(sock)
  local data = sock:Read(sock.BufferLength)
  print("Received: " .. data)
end
tcp:Connect("192.168.1.100", 23)
```

- Use `TcpSocket` for TCP, `UdpSocket` for UDP
- `SerialPorts` table for RS-232 access

### RS-232 / Serial Control

```lua
SerialPorts["Serial1"]:Open(9600, 8, "None", 1)  -- baud, data bits, parity, stop bits
SerialPorts["Serial1"]:Write("command\r\n")
SerialPorts["Serial1"].Data = function(port)
  local data = port:Read(port.BufferLength)
end
```

### Script Debugging

- **Print statements** appear in the Designer debug console (View → Debugger)
- Use `pcall()` for protected calls to catch errors without crashing the script:

```lua
local ok, err = pcall(function()
  -- risky code here
end)
if not ok then
  print("Error: " .. tostring(err))
end
```

---

## 2. Advanced Control: External Systems

### Q-SYS External Control Protocol (QRC)

- **Q-SYS Remote Control (QRC)** is QSC's TCP-based protocol for external control
- Control systems (AMX, Crestron, Extron, RTI, Control4) use QRC to read/write Named Controls
- Connection: TCP to the Core IP on **port 1710**
- Commands are in **JSON** format:

```json
{
  "jsonrpc": "2.0",
  "method": "Control.Set",
  "params": { "Name": "Gain.level", "Value": -10.0 },
  "id": 1234
}
```

- **Control.Get** — read a control value
- **Control.Set** — write a control value
- **ChangeGroup.AddControl** + **ChangeGroup.Poll** — subscribe to value changes efficiently

### REST API

- Q-SYS also exposes a **REST API** for status and control over HTTP
- Access at: `http://<core-ip>/api/v0/`
- Useful for: web dashboards, mobile apps, simple integrations that don't need real-time subscriptions

### WebSocket API

- Real-time bidirectional communication over **WebSocket** (ws://)
- Preferred for UCIs, dashboards, and integrations requiring push notifications
- Same JSON-RPC message format as the TCP QRC protocol

### GPIO (General Purpose I/O)

- Q-SYS Cores have GPIO pins (configurable as input or output)
- Use cases: wall plate buttons, relay closures, occupancy sensors, LED indicators
- In Designer: **GPIO component** — pin maps to a physical GPIO port
- Input: read state (high/low) as a Named Control Boolean
- Output: write a Boolean to drive a relay or indicator

---

## 3. SIP Telephony

### SIP Overview

- **SIP (Session Initiation Protocol)** — standard protocol for VoIP telephone calls
- Q-SYS can make and receive SIP calls, integrating with corporate PBX or SIP trunks
- Requires a **SIP license** on the Core

### SIP Component

- Add the **SIP (VoIP) component** to the schematic
- Configure: **SIP server/proxy** address, extension number, username, password
- Audio routing: the SIP component has **Send** (mic to far-end) and **Receive** (far-end to speaker) audio pins

### SIP Signal Flow

```
Room Mic → AEC → Processing → SIP Send Input
                                           ↕ (phone call)
Room Speakers ← Processing ← SIP Receive Output
```

- **Critical:** the AEC reference must include the SIP receive audio, otherwise echo is sent to the caller

### DTMF

- SIP component supports sending **DTMF tones** (dial pad digits) via Named Controls
- Useful for: navigating IVR menus, conference call dial-in pins

### SIP Call Controls (Named Controls)

| Control | Type | Action |
|---------|------|--------|
| `Dial` | String | Dial a number |
| `Disconnect` | Trigger | Hang up |
| `AutoAnswer` | Boolean | Enable auto-answer |
| `Status` | String | Call state (Idle, Dialing, Connected) |
| `IncomingCall` | Boolean | Ringing indicator |

---

## 4. Video Routing and NV Endpoints

### NV-Series Network Video Endpoints

- QSC **NV-Series** devices extend HDMI/DisplayPort video over Q-LAN (Ethernet)
- Appear as **NV Transmitter** and **NV Receiver** components in Q-SYS Designer
- Video is compressed using **H.264** and transported over the Q-LAN
- Requires a **Video license** on the Core

### NV Component Types

| Component | Function |
|-----------|---------|
| **NV-32-H** | 32-channel HD video over IP encoder/decoder |
| **NV Transmitter** | Design component: sends video from HDMI source to Q-LAN |
| **NV Receiver** | Design component: receives video from Q-LAN to display |

### Video Routing

- Video routing is handled within Q-SYS Designer using the **NV Video Router** component
- Similar to audio routing: set which transmitter feeds each receiver
- Can be controlled via Named Controls (source selection)

### Latency Considerations

- NV video latency: typically **100–300 ms** depending on resolution and network
- Not suitable for real-time interaction where glass-to-glass latency must be <30 ms
- Best for: presentation switching, content distribution, digital signage

### Video and QoS

- Video traffic should be QoS-tagged (DSCP AF41 or similar)
- Must not compete with audio on the same network queue
- Separate Q-LAN from video where possible in very large systems

---

## 5. Advanced Networking: Multi-Core and Multi-VLAN

### Multi-Core Designs

- Large systems may use **multiple Cores** working together
- Cores communicate over Q-LAN and can share audio, control, and status
- **Core-to-Core audio** is achieved with **Q-LAN Transmitter/Receiver** components

### Multi-Core Audio Routing

```
Core A (stage) ──────► Q-LAN Transmitter ──────► Q-LAN ──────► Q-LAN Receiver ──────► Core B (FOH)
```

- Q-LAN audio uses **multicast** — requires IGMP snooping on all switches between Cores

### Multi-VLAN Design

- Best practice: separate Q-LAN VLANs per system role:
  - **Management VLAN** — Core Manager, IT management traffic
  - **Audio VLAN** — Q-LAN audio multicast
  - **Control VLAN** — UCI, external control
  - **Corporate/IT VLAN** — general network (kept separate)
- Use **inter-VLAN routing** on a Layer 3 switch only where cross-VLAN communication is needed (e.g., Core Manager from IT network)

### QoS Configuration

| Traffic Type | DSCP Marking | Priority |
|--------------|-------------|---------|
| Q-LAN Audio | EF (46) | Highest |
| Q-LAN Video | AF41 (34) | High |
| Control/UCI | CS1 or best effort | Medium |
| Management | Best effort | Low |

- Mark traffic at the Core/device egress port
- Configure switch **DSCP trust** on ports connected to Q-SYS devices

### Bandwidth Planning

- Q-LAN audio: approximately **1 Mbps per 64 channels** at 24-bit/48 kHz
- NV Video (1080p): approximately **10–30 Mbps per stream**
- Plan for worst-case simultaneous streams when sizing uplinks

### Switch Requirements (Review)

- **Gigabit Ethernet** on all ports used for Q-SYS
- **IGMP snooping enabled** (on all VLANs carrying multicast audio/video)
- **QoS (DSCP trust and scheduling)** configured
- **Spanning Tree PortFast** on device ports to prevent link delays on startup
- Avoid **EEE (Energy Efficient Ethernet)** on Q-SYS device ports (causes audio dropouts)

---

## 6. Plugins and the Q-SYS Library

### What Are Plugins?

- **Plugins** extend Q-SYS Designer with components that are not built-in
- Created by QSC or third-party manufacturers (Shure, Biamp-adjacent devices, display manufacturers, etc.)
- Available from: **Q-SYS Library** (in-app), **QSC Community**, manufacturer websites

### Q-SYS Library

- Access via **Design → Q-SYS Library** in Designer
- Browse and download: plugins, sample designs, UCI templates, stylesheets
- Installed plugins appear in the Component Library like any built-in component

### Common Plugin Categories

| Category | Examples |
|----------|---------|
| **Microphone Systems** | Shure MXA-series, Sennheiser TCC2, Biamp Tesira (bridging) |
| **Display Control** | Samsung, LG, NEC display plugins |
| **Video Conferencing** | Microsoft Teams Rooms, Zoom Rooms control bridges |
| **Room Automation** | Occupancy sensors, lighting control |
| **Amplifiers** | QSC CX-series, Lab.gruppen, Crown |

### Creating a Custom Plugin (Basic)

- Plugins are written in **Lua** with a defined structure
- Consist of: `Properties`, `Controls`, `NetTx/NetRx` (for network comms), and a `runtime` Lua file
- Published to the Q-SYS Library or distributed as `.qplug` files

---

## 7. Advanced UCI Design

### Multi-Page UCIs

- Use **Button Bar** or **Back/Forward buttons** to navigate between pages
- Keep UCI layout consistent across pages — use shared header/footer components
- Pages can be shown/hidden via Lua or Named Controls (for conditional UI)

### Dynamic UCI Elements

- UCI controls can be shown/hidden, enabled/disabled, and have their labels changed via Named Controls
- Example: hide a "Call" button unless a phone line is registered

```lua
-- Hide a button based on SIP status
Controls["CallButton.visible"].Boolean = (Controls["SIP.status"].String == "Idle")
```

### UCI Templates and Stylesheets

- **Stylesheets** define global appearance (colours, fonts, control styles)
- Apply a stylesheet to maintain brand consistency across multiple UCIs
- **Templates:** save frequently used layouts/widgets as templates for reuse

### Password Protection

- UCI pages can be protected with a PIN or password
- Configure via the UCI page's **properties** in the UCI editor
- Useful for: tech pages, advanced settings, administrator controls

### Multi-Language UCI

- Text labels can be driven by Named Controls (string type)
- A Lua script can swap labels based on a language selection
- Useful for venues serving multilingual audiences

---

## 8. Q-SYS Reflect Configuration

### What is Q-SYS Reflect?

- **Q-SYS Reflect Enterprise Manager** is QSC's cloud-based platform for managing multiple Q-SYS deployments
- Accessible via web browser from anywhere with internet access
- Requires a **Reflect license** (subscription, per Core)

### Key Features

| Feature | Description |
|---------|-------------|
| **Remote monitoring** | Real-time fault and status dashboard across all sites |
| **Design deployment** | Push `.qsys` files to Cores remotely |
| **Firmware management** | Schedule and deploy firmware updates across fleet |
| **Alerts** | Email/SMS notifications on fault conditions |
| **Analytics** | Usage data, uptime reports |
| **Remote UCI access** | Access UCIs from Reflect portal |

### Reflect Setup Workflow

1. Create a QSC account and Reflect tenant
2. Add Cores to the tenant — each Core must have internet access (HTTPS port 443 outbound)
3. Install Reflect license on each Core (via Core Manager)
4. Cores appear in the Reflect dashboard
5. Configure alert rules, user roles, and notification contacts

### Reflect and Firewall Requirements

- Cores communicate **outbound over HTTPS (port 443)** to QSC cloud — no inbound ports needed
- Cores do not need a public IP address
- DNS resolution must be working on the Core's network interface

---

## 9. Troubleshooting and Diagnostics

### Systematic Troubleshooting Approach

1. **Identify the symptom** — no audio? wrong routing? control not responding?
2. **Isolate the layer** — hardware, network, software/design, control?
3. **Check StatusPage / Core Manager** — faults, offline devices, CPU usage
4. **Verify signal flow** in Designer (in-design meters when connected live)
5. **Check network** — ping devices, verify VLANs, check switch port status
6. **Check logs** — Core Manager system logs, Dante Controller logs

### Common Level 2 Fault Scenarios

| Symptom | Check |
|---------|-------|
| Lua script not running | Check script syntax (print to debug), verify EventHandler is attached |
| External controller not connecting | Verify IP, port 1710 open, correct JSON format |
| SIP call audio echo | AEC reference not including SIP receive audio |
| Video feed not displaying | NV license active? NV device in inventory/configurator? Network IGMP? |
| Multi-Core audio dropouts | Switch IGMP snooping, QoS, EEE disabled |
| Dante clock sync issues | One and only one Dante clock master, all devices same sample rate |
| UCI page not loading | Core reachable? UCI name correct in URL? HTTPS vs HTTP? |

### Core CPU / Memory Usage

- High CPU can cause audio glitches, script latency, and control delays
- Monitor in **Core Manager → System**
- Reduce CPU by: simplifying the design, reducing unnecessary components, upgrading Core

### Design Version Control

- Q-SYS designs are binary files — use a file-naming convention:
  `ProjectName_v1.2_YYYY-MM-DD.qsys`
- Before modifying a production system: export a backup via **File → Save As**
- Consider using git-LFS or a shared network folder for design file management

---

## 10. Exam Tips — Level 2

- Know **Lua event patterns**: EventHandler, Timer, pcall error handling
- Understand the **QRC JSON protocol** — method names, Control.Set/Get, ChangeGroup
- Know **SIP signal flow** including AEC reference requirements for echo-free calls
- Understand **NV video** — licensing, latency, Q-SYS component types
- Know **multi-Core Q-LAN audio** — multicast, IGMP snooping requirements
- Understand **QoS markings** for audio, video, and control traffic
- Know **Reflect features** — what it can and cannot do remotely
- Understand the difference between **WebSocket, REST, and TCP QRC** APIs
- Know **plugin architecture** — what plugins are, where to get them, `.qplug` file format
- Be able to read Lua debug output and identify script errors from Designer console
- Know **GPIO control** — input vs. output, Boolean mapping, contact closure use cases
