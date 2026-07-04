# NETGEAR AV Certification — IPMX Notes

> **About IPMX:** Internet Protocol Media Experience. An open standard for AV-over-IP developed by AIMS (Alliance for IP Media Solutions). Built on SMPTE ST 2110, AES67, AMWA NMOS, and VSF TR-10. The NETGEAR IPMX certification covers the standard itself, its technical building blocks, network requirements, and how NETGEAR switches support IPMX deployments.

---

## Table of Contents

1. [What Is IPMX?](#1-what-is-ipmx)
2. [The Standards Bodies Behind IPMX](#2-the-standards-bodies-behind-ipmx)
3. [The IPMX Technical Stack](#3-the-ipmx-technical-stack)
4. [SMPTE ST 2110 — The Foundation](#4-smpte-st-2110--the-foundation)
5. [NMOS — Device Discovery and Connection Management](#5-nmos--device-discovery-and-connection-management)
6. [PTP — Precision Time Protocol](#6-ptp--precision-time-protocol)
7. [JPEG-XS — The IPMX Codec](#7-jpeg-xs--the-ipmx-codec)
8. [HDCP in IPMX](#8-hdcp-in-ipmx)
9. [VSF TR-10 — The IPMX Technical Recommendations](#9-vsf-tr-10--the-ipmx-technical-recommendations)
10. [Network Requirements for IPMX](#10-network-requirements-for-ipmx)
11. [IPMX vs. Other AV-over-IP Protocols](#11-ipmx-vs-other-av-over-ip-protocols)
12. [NETGEAR Switch Configuration for IPMX](#12-netgear-switch-configuration-for-ipmx)
13. [Exam Tips — IPMX](#13-exam-tips--ipmx)

---

## 1. What Is IPMX?

### Definition

**IPMX (Internet Protocol Media Experience)** is a suite of open standards and specifications for transporting professional audiovisual content over IP networks. It is:

- **Open** — not owned by any single manufacturer; anyone can implement it
- **Interoperable** — any IPMX-certified device works with any other IPMX-certified device
- **Standards-based** — built on existing, proven broadcast and professional audio standards
- **Pro AV-focused** — extends broadcast standards (ST 2110) with features specific to the ProAV world

### The Core Problem IPMX Solves

The ProAV industry has fragmented into **proprietary AV-over-IP ecosystems**:

| Problem | Proprietary Example |
|---------|-------------------|
| Locked to one vendor | NDI (Vizrt), SDVoE (Semtech), DM NVX (Crestron) |
| No guaranteed interoperability | NDI device can't natively exchange with SDVoE device |
| Different network requirements per protocol | Integrators must learn each protocol separately |
| Upgrade = replace all endpoints | Moving from one ecosystem to another requires full rip-and-replace |

IPMX solves this by providing a **single, open standard** that all manufacturers can implement. A camera from manufacturer A will work natively with a display from manufacturer B — as long as both support IPMX.

### IPMX Vision: "Plug and Present"

The three use-case pillars of IPMX:

| Pillar | Description | Target User |
|--------|-------------|-------------|
| **Plug & Present** | Connect any source to any display instantly | Corporate, education, huddle rooms |
| **Plug & Produce** | Broadcast-quality production on standard IP networks | Live events, broadcast, esports |
| **Plug & Play** | Gaming, streaming, prosumer AV | Gaming, streaming, content creators |

---

## 2. The Standards Bodies Behind IPMX

IPMX is a collaborative effort — no single vendor owns it. The key organisations:

| Organisation | Role in IPMX | What They Normally Do |
|-------------|--------------|----------------------|
| **AIMS** (Alliance for IP Media Solutions) | Originated and coordinates IPMX | Trade org fostering IP media adoption |
| **VSF** (Video Services Forum) | Publishes the TR-10 technical recommendations | Video industry technical standards |
| **AMWA** (Advanced Media Workflow Association) | Defines NMOS (discovery, connection management) | Workflow standards for media |
| **SMPTE** | Provides ST 2110 as the transport foundation | Broadcast engineering standards |
| **AES** (Audio Engineering Society) | Provides AES67 as the audio transport standard | Professional audio standards |
| **EBU** (European Broadcasting Union) | Co-develops JT-NM reference architectures | Pan-European broadcast standards |
| **JT-NM** (Joint Task Force on Network Media) | Coordinates between AMWA, VSF, EBU, SMPTE | Cross-organisation alignment |

> **Key exam point:** IPMX is defined by the **VSF TR-10 series** of technical recommendations — but the components it's built on come from SMPTE (ST 2110), AMWA (NMOS), and AES (AES67).

---

## 3. The IPMX Technical Stack

Think of IPMX as a **layered technology stack**, where each layer is defined by an existing standard:

```
┌──────────────────────────────────────────────────────────┐
│                    IPMX STANDARD STACK                   │
├──────────────────────────────────────────────────────────┤
│  HDCP (TR-10-5)      │  Copy protection for content      │
├──────────────────────────────────────────────────────────┤
│  NMOS IS-04 / IS-05  │  Discovery + Connection Mgmt       │
├──────────────────────────────────────────────────────────┤
│  SMPTE ST 2110-20    │  Video transport (uncompressed)    │
│  VSF TR-10-2 / TR-10-7  │  Video (uncompressed + compressed) │
├──────────────────────────────────────────────────────────┤
│  SMPTE ST 2110-30 / AES67 │  Audio transport (PCM)       │
│  VSF TR-10-3         │  PCM audio requirements           │
├──────────────────────────────────────────────────────────┤
│  SMPTE ST 2110-40    │  Ancillary data (metadata, subtitles) │
│  VSF TR-10-4         │  Ancillary data requirements      │
├──────────────────────────────────────────────────────────┤
│  RTP / UDP / IP      │  Network transport layer          │
├──────────────────────────────────────────────────────────┤
│  IEEE 1588 PTP       │  Synchronisation (timing)         │
└──────────────────────────────────────────────────────────┘
```

### What IPMX Adds to ST 2110

SMPTE ST 2110 was designed for **broadcast facilities** — secure, managed environments. IPMX extends it for **ProAV**:

| Feature | ST 2110 (Broadcast Only) | IPMX (ProAV + Broadcast) |
|---------|--------------------------|--------------------------|
| HDCP content protection | Not included | **Added (TR-10-5)** |
| USB support | Not included | **Added (TR-10-14)** |
| Auto device discovery (NMOS) | Optional add-on | **Required** |
| Compressed video (JPEG-XS) | Optional | **Defined and required (TR-10-7)** |
| ProAV resolution support (4K60 on 1G) | Not a goal | **Core design goal** |

---

## 4. SMPTE ST 2110 — The Foundation

### What Is SMPTE ST 2110?

- A **SMPTE standard** for transporting **uncompressed, real-time** media (video, audio, and data) over an IP network as separate, independent streams
- Originally designed for **broadcast television facilities** replacing SDI (Serial Digital Interface) cabling
- Video, audio, and ancillary data travel as **separate RTP streams** — they are not muxed together as in traditional HDMI or SDI

### ST 2110 Sub-Standards

| Standard | Content | Notes |
|----------|---------|-------|
| **ST 2110-10** | System timing and definitions | PTP requirements, media clock |
| **ST 2110-20** | Uncompressed video | Raw video frames over RTP |
| **ST 2110-21** | Traffic shaping for video | Pacing of video packets to avoid bursts |
| **ST 2110-22** | Compressed video | JPEG-XS, HEVC in ST 2110 wrapper |
| **ST 2110-30** | PCM digital audio | AES67-compatible audio |
| **ST 2110-31** | AES3 transparent transport | Legacy AES3 digital audio over IP |
| **ST 2110-40** | Ancillary data | Subtitles, captions, time code, metadata |
| **ST 2110-41** | Other essence transport | Reserved for future essence types |

### ST 2110-20 Video — Key Details

- **Transport:** RTP over UDP/IP (multicast preferred)
- **Packet size:** Large — may require jumbo frames for high-resolution, high-framerate signals
- **Bandwidth (uncompressed):**

| Resolution | Frame Rate | Colour Space | Approximate Bandwidth |
|-----------|-----------|-------------|----------------------|
| 1080i50 | 25 | 4:2:2 10-bit | ~1.5 Gbps |
| 1080p60 | 60 | 4:2:2 10-bit | ~3 Gbps |
| 2160p30 (4K) | 30 | 4:2:2 10-bit | ~6 Gbps |
| 2160p60 (4K) | 60 | 4:2:2 10-bit | ~12 Gbps |

- These bandwidth requirements mean **10G or 25G network infrastructure** is required for uncompressed 4K
- This is why **JPEG-XS compression** (TR-10-7) is critical for making IPMX practical on 1G networks

### ST 2110-30 Audio

- PCM uncompressed audio over RTP (compatible with AES67)
- Up to **1024 audio channels** in a single stream
- Latency: configurable from sub-millisecond to milliseconds

### Traffic Shaping (ST 2110-21)

- Uncompressed video generates packets in bursts aligned to the video frame timing
- **Traffic shaping** spreads packets evenly across the inter-frame gap to prevent burst-induced congestion
- Specified as **Narrow Linear (NL)** or **Wide Linear (WL)** senders:
  - **NL:** Very tight pacing — requires precise timing; typical for broadcast
  - **WL:** More relaxed pacing — easier for network equipment to handle; typical for ProAV/IPMX

---

## 5. NMOS — Device Discovery and Connection Management

### What Is NMOS?

**NMOS (Networked Media Open Specifications)** is a set of REST API specifications from **AMWA** that define how IP media devices:
1. **Discover** each other on a network (IS-04)
2. **Connect** to each other (IS-05)
3. **Authenticate and authorise** connections (IS-10)
4. **Report events and status** (IS-07)

NMOS is to IPMX/ST 2110 what **mDNS/Dante Controller** is to Dante — the discovery and routing layer.

### IS-04 — Discovery and Registration

- Devices **register themselves** with an **NMOS Registry** (a server on the network)
- The Registry maintains a database of: all devices, their senders (sources), and their receivers
- Other devices or control systems **query the Registry** via HTTP REST API to discover what's available
- If no Registry is present, devices fall back to **peer-to-peer DNS-SD (mDNS)** discovery

**What gets registered:**
- Device identity (manufacturer, model, firmware)
- **Senders:** Each video/audio stream the device can transmit, including SDP (Session Description Protocol) file describing the stream
- **Receivers:** Each input the device can accept streams on

### IS-05 — Connection Management

- Once a device is discovered via IS-04, IS-05 is used to **make connections**
- A control system (or user) sends an IS-05 **PATCH request** to the receiver to connect it to a sender
- The receiver fetches the sender's **SDP file** and begins subscribing to the multicast stream
- IS-05 can also break connections (disconnect), and query current connection state

### SDP — Session Description Protocol

- An SDP file describes a media stream: IP multicast address, port, codec, sample rate, channel count, PTP domain, etc.
- Senders publish their SDP; receivers use the SDP to know exactly what to subscribe to
- NMOS IS-04 distributes SDP files automatically; in simpler setups, SDP files can be shared manually

### NMOS Registry Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   NMOS Registry Server                  │
│  (IS-04: stores all senders, receivers, device info)    │
└──────────┬──────────────────────┬───────────────────────┘
           │ Register             │ Query
           ▼                      ▼
    ┌──────────────┐      ┌──────────────────────┐
    │  IPMX Sender │      │   Control System     │
    │  (encoder)   │      │   (IS-05 connect)    │
    └──────────────┘      └──────────────────────┘
           │ multicast RTP stream
           ▼
    ┌──────────────┐
    │  IPMX Receiver│
    │  (decoder)   │
    └──────────────┘
```

### NMOS and DNS

- NMOS uses **DNS-SD** (DNS Service Discovery) for devices to find the Registry
- The Registry is advertised as a DNS service (`_nmos-register._tcp`)
- Devices query DNS for the Registry address — requires either a DNS server with the record, or mDNS

---

## 6. PTP — Precision Time Protocol

### What Is PTP?

**PTP (Precision Time Protocol)** — IEEE 1588 — synchronises clocks across a network to **nanosecond accuracy**. In media production, all devices must share the same reference clock so that:
- Video frames from different cameras are perfectly aligned
- Audio and video are lip-synced
- Multicast streams can be reconstructed in correct time order

### How PTP Works

1. A **Grandmaster Clock** (GMC) is elected — this is the reference time source (often GPS-disciplined)
2. All other PTP-capable devices sync their clocks to the Grandmaster
3. The switch **measures the propagation delay** of PTP messages and corrects for it
4. Result: all devices share a common clock with sub-microsecond accuracy

### PTP Message Types

| Message | Direction | Purpose |
|---------|-----------|---------|
| **Sync** | GM → follower | Sends current timestamp |
| **Follow_Up** | GM → follower | Corrects the Sync timestamp (two-step mode) |
| **Delay_Req** | Follower → GM | Follower requests delay measurement |
| **Delay_Resp** | GM → follower | GM responds with timestamp for delay calculation |

### PTP Profiles in IPMX/ST 2110

| Profile | Standard | Use Case |
|---------|---------|---------|
| **SMPTE ST 2059-2** | Broadcast PTP | Broadcast facilities (full feature set) |
| **AES67 PTP** | IEEE 1588-2008 | Audio-only AV installations |
| **IEEE 802.1AS (gPTP)** | Automotive / simpler networks | Simplified; no delay correction |

- IPMX uses **SMPTE ST 2059-2** as the default PTP profile
- All IPMX devices on the same network must be in the same **PTP domain** (default: domain 127 for ST 2110/IPMX, domain 0 for AES67)

### PTP and Network Infrastructure

- Switches must support **PTP Transparent Clock (TC)** or **PTP Boundary Clock (BC)**:

| Clock Type | Function | Impact |
|-----------|---------|--------|
| **End-to-End Transparent Clock (TC)** | Measures residence time in the switch and adds it to PTP correction field | Compensates for switch processing delay without needing full PTP sync |
| **Peer-to-Peer Transparent Clock** | Corrects for link delay at each hop | More accurate; hop-by-hop correction |
| **Boundary Clock (BC)** | Terminates PTP from upstream, generates new PTP downstream | Used to limit PTP fan-out in large networks |

- **NETGEAR NS Series (Gen 2) switches** support PTP Transparent Clock — key for IPMX deployments
- Without TC support, switch queuing adds variable delay to PTP messages → poor clock accuracy → video/audio sync problems

### PTP Domain

- Multiple PTP networks can coexist on the same switch by using different **domain numbers**
- IPMX/ST 2110 typically uses **domain 127**
- AES67 audio typically uses **domain 0**
- A Dante network uses its own internal timing — Dante does not use IEEE 1588 PTP (it uses PTP v1 internally)

---

## 7. JPEG-XS — The IPMX Codec

### Why a Codec?

Uncompressed ST 2110-20 video requires **3–12 Gbps per stream** — this demands 10G or 25G infrastructure everywhere. The ProAV world needs 4K60 to work on **1G links** that are already installed in most buildings.

**JPEG-XS** solves this without the latency cost of traditional codecs.

### What Is JPEG-XS?

- **JPEG-XS** (ISO/IEC 21122) is a **visually lossless** (near-lossless), **ultra-low-latency** intra-frame compression codec
- Developed specifically for real-time AV-over-IP and broadcast applications
- Standardised by ISO/IEC and adopted by SMPTE (ST 2110-22), VSF (TR-08), and IPMX (TR-10-7)

### Key Properties

| Property | JPEG-XS | H.264 / H.265 (for comparison) |
|----------|---------|-------------------------------|
| **Latency** | **Sub-frame** (< 1 ms encode/decode) | Hundreds of milliseconds (inter-frame) |
| **Quality** | **Visually lossless** (imperceptible loss) | Variable; lossy |
| **Compression ratio** | 4:1 to 10:1 typical | Up to 1000:1 |
| **Intra/Inter frame** | **Intra only** (no temporal prediction) | Inter (uses surrounding frames) |
| **Hardware complexity** | Low (simple encode/decode) | High (complex codec) |
| **ProAV standard** | Yes (IPMX TR-10-7) | H.265 in IPMX TR-10-15 Part 2 |

### Bandwidth with JPEG-XS

| Resolution | Frame Rate | Compression | Approximate Bandwidth |
|-----------|-----------|-------------|----------------------|
| 1080p60 | 60 | 4:1 | ~750 Mbps (fits on **1G**) |
| 2160p30 (4K) | 30 | 4:1 | ~1.5 Gbps (fits on **1G** barely, needs **10G** safely) |
| 2160p60 (4K) | 60 | 4:1 | **~3 Gbps (10G required)** |
| 2160p60 (4K) | 60 | 10:1 | ~1.2 Gbps (fits on **1G**) |

> **Key exam point:** JPEG-XS at 4:1 compression allows **4K60 on a 1G connection** — this is one of the headline capabilities of IPMX.

### Why Not H.264 / H.265?

- H.264 and H.265 use **temporal compression** (inter-frame prediction) — each frame depends on previous/future frames
- This introduces **hundreds of milliseconds of latency** (not acceptable for live production, interactive AV, or gaming)
- H.264/H.265 also have high encode complexity and require powerful hardware
- IPMX includes H.264/H.265 options (TR-10-15) for bandwidth-constrained applications where latency is tolerable, but JPEG-XS is the primary codec

---

## 8. HDCP in IPMX

### Why HDCP?

- **HDCP (High-bandwidth Digital Content Protection)** prevents unauthorised copying of protected content (streaming services, Blu-ray, etc.)
- Traditional HDMI/DisplayPort already use HDCP
- IPMX adds **HDCP over IP** — defined in VSF TR-10-5

### How HDCP Works in IPMX

1. The sender (encoder) and receiver (decoder) perform a **key exchange** (HKEP — HDCP Key Exchange Protocol)
2. If both devices are authorised HDCP devices, encryption keys are exchanged
3. The media stream is **encrypted at the sender** and **decrypted at the receiver**
4. Unauthorised devices cannot decrypt the stream even if they receive the IP packets

### HDCP Compliance

- Not all IPMX devices need to support HDCP — it is required only when transporting **HDCP-protected content**
- Devices that process only non-protected content (cameras, production gear) may not implement HDCP
- The IPMX standard requires that devices that **handle HDCP** implement TR-10-5 correctly

### HDCP vs. Network Security

- HDCP protects **content** from unauthorised copying
- It does **not** secure the network or prevent interception of unprotected streams
- Network security (VLANs, ACLs, 802.1X) is separate from HDCP and must be implemented independently

---

## 9. VSF TR-10 — The IPMX Technical Recommendations

The VSF **TR-10 series** is the normative document series that defines IPMX. These are freely downloadable from vsf.tv.

| Document | Status | Topic |
|----------|--------|-------|
| **TR-10-0** | Final | General organisation; overview of the IPMX system |
| **TR-10-1** | Final | System timing and definitions (PTP, clock domains) |
| **TR-10-2** | Final | Uncompressed active video (ST 2110-20 requirements) |
| **TR-10-3** | Final | PCM digital audio (ST 2110-30 / AES67 requirements) |
| **TR-10-4** | Draft | Ancillary data (SMPTE ST 291-1 / ST 2110-40) |
| **TR-10-5** | Final | HDCP key exchange protocol |
| **TR-10-6** | Draft | Forward Error Correction (FEC) |
| **TR-10-7** | Draft | Compressed video (JPEG-XS in ST 2110-22 wrapper) |
| **TR-10-8** | Final | NMOS requirements (IS-04, IS-05, IS-10) |
| **TR-10-9** | Draft | System environments and device behaviour |
| **TR-10-10** | Draft | HDMI InfoFrame packet transport |
| **TR-10-11** | Final | Constant bit-rate compressed video |
| **TR-10-12** | Draft | AES3 transparent transport |
| **TR-10-13** | Final | Privacy Encryption Protocol (PEP) |
| **TR-10-14** | Draft | IPMX USB transport |
| **TR-10-15 Part 1** | Draft | JPEG-XS codec requirements |
| **TR-10-15 Part 2** | Draft | H.265 codec requirements |
| **TR-10-15 Part 3** | Draft | H.264 codec requirements |
| **TR-10-16** | Draft | HDR info block |

> **Exam note:** You don't need to memorise every document — but know TR-10-0 (overview), TR-10-2 (video), TR-10-3 (audio), TR-10-5 (HDCP), TR-10-7 (JPEG-XS), and TR-10-8 (NMOS).

---

## 10. Network Requirements for IPMX

### Summary Table

| Requirement | Minimum | Recommended |
|-------------|---------|------------|
| **Link speed (compressed JPEG-XS 4K)** | 1 Gbps | 10 Gbps |
| **Link speed (uncompressed HD)** | 10 Gbps | 10 Gbps |
| **Link speed (uncompressed 4K)** | 25 Gbps | 25 Gbps |
| **Jumbo frames** | 1500 byte MTU (compressed) | 9000 byte MTU (uncompressed) |
| **IGMP snooping / IGMP Plus** | Required | Required |
| **PTP Transparent Clock** | Required | Required |
| **QoS / DSCP** | Recommended | Required in mixed networks |
| **EEE** | Disabled | Disabled |
| **Multicast routing (PIM)** | Required if cross-VLAN/subnet | Required |

### DSCP Markings for IPMX

| Traffic | DSCP | Value |
|---------|------|-------|
| Video streams (ST 2110-20/22) | AF41 | 34 |
| Audio streams (ST 2110-30) | EF | 46 |
| Ancillary data (ST 2110-40) | CS1 | 8 |
| NMOS control (IS-04/IS-05) | CS1 or BE | 8 or 0 |
| PTP (IEEE 1588) | CS6 | 48 |

### PTP-Specific Network Requirements

- Every switch in the PTP path must support **PTP Transparent Clock** or be a **PTP Boundary Clock**
- PTP uses multicast to the address `224.0.1.129` (default) — ensure this is not blocked by IGMP configuration
- PTP domain must be consistent across all devices (IPMX uses domain 127)

### NMOS-Specific Network Requirements

- The NMOS Registry server must be reachable by all IPMX devices
- DNS must resolve the Registry service (`_nmos-register._tcp`)
- Port **TCP 80 or 443** for NMOS REST API access
- If using mDNS fallback: mDNS must work on the VLAN (link-local, not routed)

### Multicast Group Management

- IPMX streams are multicast — IGMP snooping (or IGMP Plus) is required on all switches in the path
- Each IPMX stream has a unique multicast group address
- In large systems, hundreds or thousands of multicast groups may be active — verify the switch's multicast group table capacity (NETGEAR M4350: supports 4K+ multicast groups)

### COTS (Commercial Off-The-Shelf) Network

- IPMX is explicitly designed to run on **standard enterprise Ethernet infrastructure** — no specialised hardware required
- Contrast with SDI (coax, frame synchronisers) or proprietary AV systems (specialist cables/switches)
- This is a core IPMX value proposition: deploy on the same managed switches used for IT

---

## 11. IPMX vs. Other AV-over-IP Protocols

| Feature | IPMX | NDI | SDVoE | Dante | HDBaseT |
|---------|------|-----|-------|-------|---------|
| **Open standard** | Yes | No (Vizrt) | No (Alliance) | No (Audinate) | No (HDBaseT Alliance) |
| **Interoperable** | Yes (any IPMX device) | Somewhat (royalty model) | Only Alliance members | Only Audinate | Only certified devices |
| **Video** | Yes | Yes | Yes | No | Yes |
| **Audio** | Yes (AES67) | Yes | Yes | Yes | Yes |
| **Min bandwidth (1080p)** | ~750 Mbps (JPEG-XS 4:1) | ~125 Mbps | ~3 Gbps | N/A | Fixed (no IP) |
| **4K on 1G** | Yes (JPEG-XS) | Possible (HX) | No (needs 10G) | N/A | No |
| **Latency** | Sub-frame (JPEG-XS) | 1–3 frames | Sub-frame | 1–10 ms | Sub-frame |
| **HDCP** | Yes (TR-10-5) | No | No | No | Yes |
| **Discovery** | NMOS (open) | mDNS + proprietary | Proprietary API | Proprietary | N/A |
| **Timing/sync** | PTP (IEEE 1588) | Internal | Internal | PTP v1 | Clock reference |
| **Compression** | JPEG-XS + uncompressed | Proprietary | None (uncompressed) | None (PCM) | None |
| **USB** | Yes (TR-10-14) | No | No | No | Yes |
| **Primary market** | Pro AV + Broadcast | Pro AV / Broadcast | Pro AV / Display walls | Pro Audio | Installed AV |

### Why IPMX Over NDI?

- IPMX is a true open standard — no royalty, no vendor lock-in
- IPMX uses proven, standards-based components (SMPTE, AES, AMWA)
- NMOS discovery is open and integrates with any control system
- JPEG-XS provides lower latency than NDI's codec at comparable bandwidth

### Why IPMX Over SDVoE?

- SDVoE requires 10G everywhere — expensive for large deployments
- IPMX with JPEG-XS works on 1G — uses existing infrastructure
- IPMX is open; SDVoE is controlled by the SDVoE Alliance (Semtech)

### IPMX and ST 2110 Relationship

- IPMX **is** ST 2110 for the most part — it adds ProAV features on top of a broadcast foundation
- Broadcast-only installations may use pure ST 2110 without the IPMX additions (no HDCP, no NMOS required)
- IPMX-compliant devices are (by definition) ST 2110-compliant, but not vice versa

---

## 12. NETGEAR Switch Configuration for IPMX

### NS Series Switches (Netgear AV / IPMX)

- **NETGEAR NS Series (Gen 2)** — branded for AV and IPMX deployments
- Key features for IPMX:
  - **PTP Transparent Clock** — compensates for switch latency in PTP messages
  - **IGMP Plus** — efficient multicast for IPMX streams
  - **10G and 25G ports** — required for uncompressed IPMX streams
  - **Engage IPMX profile** — pre-configured port settings for IPMX deployments

### Engage IPMX Profile Configuration

What the IPMX Engage profile sets automatically:

| Setting | Value | Reason |
|---------|-------|--------|
| **IGMP Plus** | Enabled on AV VLANs | Efficient multicast delivery |
| **QoS** | EF (46) for audio, AF41 (34) for video | Proper traffic prioritisation |
| **EEE** | Disabled | Prevents latency jitter |
| **PTP pass-through** | Enabled | PTP messages not blocked |
| **Jumbo frames** | 9000 MTU (optional, for uncompressed) | Prevents fragmentation |
| **Storm control** | Configured | Prevents multicast flooding |

### PTP Configuration on NETGEAR

1. Enable PTP on the switch: **System → PTP → Enable**
2. Set PTP mode: **End-to-End Transparent Clock** (most common for IPMX)
3. Set PTP domain: **127** (IPMX/ST 2110 default)
4. Verify PTP status: check that PTP messages are passing through without being dropped
5. Test with a PTP analyser or check device sync status on endpoints

### NMOS on NETGEAR Networks

- The NMOS Registry server can run on:
  - A dedicated server on the network
  - A VM on an existing server
  - Embedded in one of the IPMX endpoint devices
- NETGEAR switches don't run the NMOS Registry — they just need to pass the NMOS traffic
- Ensure TCP ports 80/443 are not blocked between devices and the Registry server
- Configure the DNS server to advertise the NMOS Registry service, or use mDNS

### Bandwidth Planning for IPMX

| Number of Streams | Resolution | Codec | Total Bandwidth | Recommended Uplink |
|------------------|-----------|-------|----------------|-------------------|
| 4× | 1080p60 | JPEG-XS 4:1 | ~3 Gbps | 10G |
| 8× | 1080p60 | JPEG-XS 4:1 | ~6 Gbps | 10G (or LAG) |
| 4× | 4K60 | JPEG-XS 4:1 | ~12 Gbps | 25G or 2× 10G LAG |
| 1× | 4K60 | Uncompressed | ~12 Gbps | 25G |

---

## 13. Exam Tips — IPMX

- Know the **acronym**: IPMX = Internet Protocol Media Experience; originated from **AIMS**
- Know the **three "Plug and ___" pillars**: Present, Produce, Play
- Know the **standards stack**: SMPTE ST 2110 (transport) + AMWA NMOS (discovery/control) + AES67 (audio) + VSF TR-10 (IPMX spec) + IEEE 1588 (PTP)
- Know the **standards bodies**: AIMS, VSF, AMWA, SMPTE, AES, EBU, JT-NM
- Know **what IPMX adds to ST 2110**: HDCP, USB, NMOS requirement, JPEG-XS
- Know **JPEG-XS**: sub-frame latency, visually lossless, intra-frame only, enables 4K60 on 1G at 10:1 compression
- Know **NMOS IS-04** (discovery/registration) vs. **IS-05** (connection management)
- Know **PTP roles**: Grandmaster Clock, Transparent Clock, Boundary Clock
- Know **PTP domain 127** for IPMX/ST 2110, **domain 0** for AES67
- Know **why Transparent Clock** is needed on switches (compensates for variable queuing delay in switches)
- Know the **bandwidth requirements**: uncompressed 4K60 = ~12 Gbps; JPEG-XS 4:1 4K60 = ~3 Gbps; JPEG-XS 10:1 4K60 = ~1.2 Gbps
- Know how **HDCP** works in IPMX — key exchange between sender and receiver (TR-10-5)
- Know how **IPMX compares to NDI, SDVoE, and ST 2110** — open vs. proprietary, bandwidth, latency
- Know **NS Series Gen 2** supports PTP Transparent Clock — key differentiator for IPMX
- Know **IGMP Plus** is required for efficient IPMX multicast delivery on NETGEAR switches

---

## Key Terms Glossary — IPMX

| Term | Definition |
|------|-----------|
| **IPMX** | Internet Protocol Media Experience — open AV-over-IP standard from AIMS |
| **AIMS** | Alliance for IP Media Solutions — trade org that originated IPMX |
| **VSF** | Video Services Forum — publishes TR-10 IPMX technical recommendations |
| **AMWA** | Advanced Media Workflow Association — defines NMOS specifications |
| **ST 2110** | SMPTE standard for uncompressed media (video, audio, ancillary) over IP |
| **ST 2110-20** | Uncompressed video transport |
| **ST 2110-30** | PCM audio transport (AES67-compatible) |
| **ST 2110-40** | Ancillary data transport |
| **ST 2110-22** | Compressed video (JPEG-XS, HEVC) in ST 2110 |
| **NMOS** | Networked Media Open Specifications (AMWA) — discovery and control |
| **IS-04** | NMOS Discovery and Registration API |
| **IS-05** | NMOS Connection Management API |
| **SDP** | Session Description Protocol — describes a media stream (address, codec, channels) |
| **PTP** | Precision Time Protocol (IEEE 1588) — nanosecond clock synchronisation |
| **Grandmaster Clock** | The authoritative PTP time source on a network |
| **Transparent Clock** | Switch type that corrects for its own processing delay in PTP messages |
| **Boundary Clock** | Switch that terminates PTP from upstream and re-generates downstream |
| **PTP Domain** | Logical PTP network segment; IPMX uses domain 127, AES67 uses domain 0 |
| **JPEG-XS** | ISO/IEC 21122 — ultra-low-latency, visually lossless intra-frame codec |
| **HDCP** | High-bandwidth Digital Content Protection — content encryption |
| **TR-10** | VSF Technical Recommendation series defining the IPMX specification |
| **COTS** | Commercial Off-The-Shelf — standard enterprise networking hardware |
| **NL / WL** | Narrow Linear / Wide Linear — ST 2110-21 traffic shaping modes |
| **JT-NM** | Joint Task Force on Network Media — cross-org coordination group |
