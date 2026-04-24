# 05 — Variation C: Hybrid A&H dLive + Python Automated Failover Controller

## Overview

This variation keeps the **Allen & Heath dLive S5000 + SQ-5** architecture from [01-system-architecture-primary.md](01-system-architecture-primary.md) but adds a custom **Python automation layer** that continuously monitors the DM48 MixRack's health and automatically triggers the Dante subscription switchover when a failure is detected. This brings the A&H system close to the Yamaha RIVAGE PM's automatic failover capability (~2–4 seconds) without changing console platforms.

**Trade-off**: You accept the dual programming burden and custom development/maintenance cost in exchange for keeping existing A&H equipment while gaining automated failover.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  FAILOVER CONTROLLER                        │
│            (Raspberry Pi 4/5 or Mac Mini)                   │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Health      │  │ Dante        │  │ OCA/AES70         │  │
│  │ Monitor     │  │ Subscription │  │ D20 Input         │  │
│  │ (conmon     │  │ Controller   │  │ Controller        │  │
│  │  polling)   │  │ (conmon API) │  │ (Option B only)   │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬───────────┘  │
│         │                │                   │              │
│  ┌──────┴────────────────┴───────────────────┴───────────┐  │
│  │              Core Failover Engine                     │  │
│  │  - State machine: NORMAL → FAILOVER → RESTORED        │  │
│  │  - Auto-detect DM48 offline (conmon polling)          │  │
│  │  - Auto-trigger DS10 re-subscription                  │  │
│  │  - Manual override buttons on web dashboard           │  │
│  │  - OSC interface for QLab triggers                    │  │
│  └──────┬────────────────┬───────────────────┬───────────┘  │
│         │                │                   │              │
│  ┌──────┴──────┐  ┌──────┴───────┐  ┌───────┴───────────┐  │
│  │ Web         │  │ OSC          │  │ Logging &         │  │
│  │ Dashboard   │  │ Interface    │  │ Alerting          │  │
│  │ (FastAPI)   │  │ (python-osc) │  │ (file + optional  │  │
│  │ Port 8080   │  │ Port 9000    │  │  email/webhook)   │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## How It Works

### Step 1: Health Monitoring (Continuous)

The controller continuously polls the Dante network for device presence using the Audinate `conmon` API (or raw mDNS/Bonjour discovery).

```
Every 500ms:
  1. Query Dante network for DM48 device presence
  2. Query Dante network for SQ-5 device presence
  3. Query Dante network for DS10 device presence
  4. Check PTP clock status
  5. Update dashboard with device health
```

**Detection criteria for DM48 failure:**
- DM48 disappears from Dante device list (conmon reports device offline)
- DM48 Dante transmit channels report "no signal" for > 1 second
- PTP clock from DM48 is lost

### Step 2: Automatic Failover Trigger

When the controller detects DM48 failure:

```
DM48 offline detected
    │
    ├── Wait 1 second (debounce — avoid false triggers from brief network glitches)
    │
    ├── Verify SQ-5 is still online and transmitting
    │
    ├── Execute DS10 Dante subscription switch:
    │   DS10 rx-ch 1 ← SQ-Zone1 (was dLive-Zone1)
    │   DS10 rx-ch 2 ← SQ-Zone2 (was dLive-Zone2)
    │   ... (all 8 zones)
    │
    ├── (Option B only) Send OCA commands to D20s to switch input source
    │
    ├── Send OSC /failover/active to QLab (status display)
    │
    ├── Update web dashboard: "FAILOVER ACTIVE — SQ-5 is now primary"
    │
    └── Log event with timestamp
```

### Step 3: Manual Override

The web dashboard and OSC interface also support manual triggers:

| Action | Web Dashboard Button | OSC Command | QLab Cue |
|---|---|---|---|
| Force failover | "FAILOVER NOW" | `/failover/execute` | Network OSC cue |
| Restore to dLive | "RESTORE PRIMARY" | `/failover/restore` | Network OSC cue |
| Disable auto-failover | "MANUAL MODE" | `/failover/mode manual` | — |
| Enable auto-failover | "AUTO MODE" | `/failover/mode auto` | — |
| Status query | Dashboard auto-updates | `/failover/status` → returns state | — |

---

## Technology Stack

### Required Software

| Component | Library / Tool | Purpose |
|---|---|---|
| Python 3.10+ | — | Runtime |
| FastAPI | `pip install fastapi uvicorn` | Web dashboard + REST API |
| python-osc | `pip install python-osc` | OSC server (receive QLab triggers) + OSC client (send status) |
| dante-conmon | Audinate SDK or extracted binary | Dante device monitoring + subscription control |
| aes67-utils (optional) | — | Dante device discovery via mDNS |
| OCA library (optional) | AES70 Python implementation | D20 input source control (Option B) |
| Jinja2 | `pip install jinja2` | Dashboard HTML templates |

### Hardware Requirements

| Option | Device | Notes |
|---|---|---|
| Option 1 (recommended) | Raspberry Pi 4 or 5 (4GB+) | Dedicated, low power, reliable. Runs headless. |
| Option 2 | Mac Mini | Can also run other control software (R1, Dante Controller) |
| Option 3 | FOH QLab Mac | Shares machine with QLab — adds failure coupling (not ideal) |

The controller device must be on the Dante network (VLAN 20/30) AND the Control network (VLAN 40).

---

## Software Architecture

### State Machine

```
                    ┌──────────┐
                    │  NORMAL  │ ◄─── System startup
                    └────┬─────┘
                         │
              DM48 offline detected
              (auto) or /failover/execute (manual)
                         │
                    ┌────▼─────┐
                    │ FAILOVER │ ── DS10 subscribed to SQ channels
                    └────┬─────┘    D20 inputs switched (Option B)
                         │
              DM48 back online
              AND /failover/restore (manual confirmation)
                         │
                    ┌────▼──────┐
                    │ RESTORING │ ── Verify DM48 stable for 30s
                    └────┬──────┘
                         │
              DM48 stable, operator confirms restore
                         │
                    ┌────▼─────┐
                    │  NORMAL  │ ── DS10 re-subscribed to dLive channels
                    └──────────┘
```

**Important**: Restore is NOT automatic. After a failover, the controller waits for the operator to manually confirm restore — this prevents bouncing between consoles if the DM48 is intermittently failing.

### Core Module Structure

```
failover_controller/
├── main.py                 # FastAPI app + startup
├── config.py               # Device IPs, Dante channel names, timing
├── dante_monitor.py        # Health monitoring (conmon polling)
├── dante_switcher.py       # Subscription switching (conmon commands)
├── oca_controller.py       # D20 input source switching (Option B)
├── osc_interface.py        # OSC server + client (QLab integration)
├── state_machine.py        # NORMAL → FAILOVER → RESTORING state
├── logger.py               # Event logging
├── templates/
│   └── dashboard.html      # Web dashboard template
├── static/
│   └── style.css           # Dashboard styling
├── requirements.txt        # Python dependencies
└── README.md               # Setup instructions
```

### Configuration (config.py)

```python
# Dante device names (as they appear in Dante Controller)
DLIVE_DEVICE = "DM48"
SQ_DEVICE = "SQ5"
DS10_DEVICE = "DS10"

# Dante channel mapping (DS10 receiver channels)
ZONE_CHANNELS = {
    1: {"primary": "dLive-Zone1", "backup": "SQ-Zone1"},
    2: {"primary": "dLive-Zone2", "backup": "SQ-Zone2"},
    3: {"primary": "dLive-Zone3", "backup": "SQ-Zone3"},
    4: {"primary": "dLive-Zone4", "backup": "SQ-Zone4"},
    5: {"primary": "dLive-Zone5", "backup": "SQ-Zone5"},
    6: {"primary": "dLive-Zone6", "backup": "SQ-Zone6"},
    7: {"primary": "dLive-Zone7", "backup": "SQ-Zone7"},
    8: {"primary": "dLive-Zone8", "backup": "SQ-Zone8"},
}

# Timing
HEALTH_POLL_INTERVAL = 0.5   # seconds
FAILURE_DEBOUNCE = 1.0        # seconds before triggering failover
RESTORE_STABILITY_WAIT = 30   # seconds DM48 must be stable before restore

# Network
OSC_LISTEN_PORT = 9000
OSC_QLAB_IP = "192.168.40.10"
OSC_QLAB_PORT = 53000
WEB_DASHBOARD_PORT = 8080

# D20 OCA addresses (Option B only)
D20_1_IP = "192.168.40.101"
D20_2_IP = "192.168.40.102"
```

### Key Code Patterns

**Health Monitor (dante_monitor.py):**
```python
import asyncio
import subprocess

class DanteHealthMonitor:
    def __init__(self, config):
        self.config = config
        self.dm48_online = True
        self.sq5_online = True
        self.ds10_online = True

    async def poll(self):
        """Poll Dante network for device presence."""
        while True:
            # Use dante-conmon to query device list
            result = subprocess.run(
                ["dante-conmon", "--list-devices"],
                capture_output=True, text=True, timeout=2
            )
            devices = result.stdout.strip().split("\n")

            self.dm48_online = self.config.DLIVE_DEVICE in devices
            self.sq5_online = self.config.SQ_DEVICE in devices
            self.ds10_online = self.config.DS10_DEVICE in devices

            await asyncio.sleep(self.config.HEALTH_POLL_INTERVAL)
```

**Dante Switcher (dante_switcher.py):**
```python
import subprocess

class DanteSwitcher:
    def __init__(self, config):
        self.config = config

    def switch_to_backup(self):
        """Re-subscribe DS10 from dLive channels to SQ channels."""
        for zone_num, channels in self.config.ZONE_CHANNELS.items():
            subprocess.run([
                "dante-conmon",
                "--device", self.config.DS10_DEVICE,
                "--rx-channel", str(zone_num),
                "--tx-device", self.config.SQ_DEVICE,
                "--tx-channel", channels["backup"]
            ], timeout=5)

    def switch_to_primary(self):
        """Re-subscribe DS10 from SQ channels back to dLive channels."""
        for zone_num, channels in self.config.ZONE_CHANNELS.items():
            subprocess.run([
                "dante-conmon",
                "--device", self.config.DS10_DEVICE,
                "--rx-channel", str(zone_num),
                "--tx-device", self.config.DLIVE_DEVICE,
                "--tx-channel", channels["primary"]
            ], timeout=5)
```

**OSC Interface (osc_interface.py):**
```python
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

class OSCInterface:
    def __init__(self, config, state_machine):
        self.config = config
        self.state_machine = state_machine
        self.qlab_client = SimpleUDPClient(
            config.OSC_QLAB_IP, config.OSC_QLAB_PORT
        )

    def setup_dispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.map("/failover/execute", self._handle_failover)
        dispatcher.map("/failover/restore", self._handle_restore)
        dispatcher.map("/failover/status", self._handle_status)
        dispatcher.map("/failover/mode", self._handle_mode)
        return dispatcher

    def _handle_failover(self, address, *args):
        self.state_machine.trigger_failover(source="osc")

    def _handle_restore(self, address, *args):
        self.state_machine.trigger_restore(source="osc")

    def notify_qlab(self, message):
        """Send status to QLab for display."""
        self.qlab_client.send_message("/failover/status", message)
```

---

## Web Dashboard

The dashboard provides real-time system status visible at FOH and backstage:

### Dashboard Features

| Element | Information |
|---|---|
| System state indicator | Large color block: GREEN (normal), RED (failover), YELLOW (restoring) |
| Device status | DM48: Online/Offline, SQ-5: Online/Offline, DS10: Online/Offline |
| Active console | "PRIMARY: dLive" or "BACKUP: SQ-5" |
| Last failover event | Timestamp + trigger source (auto/manual) |
| Failover button | Large red button: "FAILOVER NOW" |
| Restore button | Large green button: "RESTORE PRIMARY" (only visible in failover state) |
| Mode toggle | Auto / Manual mode switch |
| Event log | Last 50 events with timestamps |

### Access

- `http://192.168.40.50:8080` (controller IP on control VLAN)
- Displayed on a spare monitor at FOH and/or A2 position
- Mobile-responsive — accessible from phone/tablet in emergency

---

## Failover Timeline

### Automatic (DM48 failure detected by health monitor)

| Time | Event |
|---|---|
| T+0.0s | DM48 disappears from Dante network |
| T+0.5s | Health monitor detects absence (next poll cycle) |
| T+1.5s | Debounce period passes — failure confirmed |
| T+1.5s | DS10 subscription switch begins |
| T+2.5s | All 8 zones re-subscribed to SQ channels |
| T+3.0s | SQ audio reaches D20 amplifiers |
| T+3.0s | Dashboard updates, QLab notified |

**Total: ~3 seconds of silence**

### Manual (operator presses FAILOVER button or QLab cue)

| Time | Event |
|---|---|
| T+0.0s | Operator presses button / QLab fires OSC cue |
| T+0.1s | Controller receives command |
| T+0.1s | DS10 subscription switch begins |
| T+1.1s | All 8 zones re-subscribed |
| T+1.5s | SQ audio reaches D20 amplifiers |

**Total: ~1.5 seconds of silence**

---

## Deployment & Setup

### 1. Hardware Setup (Raspberry Pi)

```bash
# Flash Raspberry Pi OS Lite (64-bit) to SD card
# Connect Pi to Dante network switch via Ethernet
# Assign static IP: 192.168.40.50 (Control VLAN)
# Optionally assign second IP on Dante VLAN if needed for conmon
```

### 2. Software Installation

```bash
# SSH into Pi
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv

# Create project directory
mkdir /opt/failover-controller
cd /opt/failover-controller

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn python-osc jinja2

# Copy dante-conmon binary (from Audinate SDK)
# Place in /usr/local/bin/dante-conmon
```

### 3. Service Configuration

```bash
# Create systemd service for auto-start
sudo tee /etc/systemd/system/failover-controller.service << 'EOF'
[Unit]
Description=Dante Failover Controller
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/failover-controller
ExecStart=/opt/failover-controller/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable failover-controller
sudo systemctl start failover-controller
```

### 4. QLab Integration

Create two QLab cues:

**Cue "FAILOVER" (Hot key: F12):**
- Type: Network OSC
- Target: 192.168.40.50:9000
- Message: `/failover/execute`

**Cue "RESTORE" (Hot key: Shift+F12):**
- Type: Network OSC
- Target: 192.168.40.50:9000
- Message: `/failover/restore`

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| conmon API changes in Audinate update | Failover script breaks | Pin dante-conmon version; test after any Dante Controller update |
| False positive (DM48 temporarily drops from network) | Unnecessary failover | 1-second debounce; manual mode available |
| Controller device (Pi) fails | No automatic failover | Still have manual Dante Controller presets as backup procedure |
| Network partition between controller and DS10 | Can't execute switch | Controller on same switch as DS10; redundant network path |
| conmon subscription change causes audio glitch | Brief click/dropout during switch | Test during tech rehearsals; verify DS10 handles subscription changes cleanly |

---

## Comparison with Other Approaches

| Metric | This (Hybrid Python) | RIVAGE PM DSP Mirroring | DiGiCo Q7 Dual Engine |
|---|---|---|---|
| Failover time | ~3s (auto) / ~1.5s (manual) | 0s (instant) | 0s (instant) |
| Audio interruption | ~2–3s of silence | None | None |
| Development required | Significant (Python) | None | None |
| Maintenance burden | Ongoing (script updates) | None | None |
| Dual programming | Yes (dLive + SQ) | No | No (show file portable) |
| Hardware cost | Low (Raspberry Pi + existing gear) | High (dual DSP-RX) | Very high (Q7) |
| Detection method | Network polling (~500ms resolution) | Hardware-level mirroring | Hardware-level mirroring |

**Bottom line**: This approach gets you to automated failover with existing A&H gear, but the ~3 second audio gap and custom development burden are the trade-offs. For a production where 0-second failover is critical, the RIVAGE PM or DiGiCo platforms are the correct choice.

---

## Future Enhancements

1. **DDM integration**: If Dante Domain Manager is available, replace conmon polling with DDM's official device monitoring and webhook alerting for more reliable detection
2. **Audio confidence monitoring**: Add audio level monitoring on DS10 outputs — detect silence even if the device appears online (catches partial failures)
3. **Dual-controller redundancy**: Run the failover controller on two Raspberry Pis with leader election — if the primary controller fails, the secondary takes over
4. **TheatreMix integration**: Extend the controller to monitor TheatreMix cue state and verify both consoles are tracking correctly
5. **Mobile app**: Simple iOS/Android app for A2 with failover button and status display (connects to FastAPI backend)
