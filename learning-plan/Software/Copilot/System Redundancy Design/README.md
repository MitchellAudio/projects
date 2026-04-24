# Redundant Theatrical Sound System Design

A comprehensive system design project for a fully redundant sound system for a musical with immersive sound, 32 wireless lavaliers, 16 pit inputs, 8 output zones, and snapshot-driven mixing.

## Project Goal

Design a theatrical sound system with **complete redundancy** — covering console failover, network redundancy, playback backup, and amplifier interfacing — with the fastest possible switchover time and minimal operator intervention.

## System Requirements

| Requirement | Specification |
|---|---|
| Show type | Musical with immersive sound |
| Wireless mics | 32× Sennheiser (Dante-enabled) |
| Pit inputs | 16 channels (band/orchestra) |
| Playback | Dual Mac QLab systems |
| Output zones | 8 |
| Amplifiers | d&b D20 (no built-in Dante) |
| Network | Dante Primary + Secondary |
| Redundancy goal | Automatic or near-automatic failover |
| Operator positions | A1 (FOH) + A2 (backstage) |

## Documents

| # | File | Description |
|---|---|---|
| 1 | [01-system-architecture-primary.md](01-system-architecture-primary.md) | Allen & Heath dLive + SQ-5 complete system architecture — the baseline design |
| 2 | [02-automation-approaches.md](02-automation-approaches.md) | Five approaches to automating Dante switchover and amp control (OSC, conmon, DDM, OCA, Genius.lab) |
| 3 | [03-variation-yamaha-rivage.md](03-variation-yamaha-rivage.md) | Yamaha RIVAGE PM5 alternative — native DSP mirroring, Genius.lab macros, Theatre Mode |
| 4 | [04-variation-digico-quantum.md](04-variation-digico-quantum.md) | DiGiCo Quantum 338 alternative — show file portability, Optocore fiber, dual DMI slots |
| 5 | [05-variation-hybrid-automation.md](05-variation-hybrid-automation.md) | Hybrid A&H dLive + Python failover controller — automated switchover with existing gear |
| 6 | [06-comparison-matrix.md](06-comparison-matrix.md) | Decision matrix comparing all four architectures across 14 criteria |
| 7 | [07-failover-procedures.md](07-failover-procedures.md) | Step-by-step failover procedures for every failure mode in each architecture |
| 8 | [08-dlive-foh-sq5-monitor-architecture.md](08-dlive-foh-sq5-monitor-architecture.md) | dLive FOH (with Waves) + SQ-5 monitor/backup + ME-500 pit system + RSTP ring network |

## Quick Recommendation

1. **Best overall**: Yamaha RIVAGE PM5 — native automatic DSP failover, Genius.lab single-button automation, Theatre Mode, DaNSe noise suppression, show file portability
2. **Best if DiGiCo available**: Quantum 338 + SD9T — show file compatibility, Optocore fiber redundancy, Dante + Waves simultaneously
3. **Best with existing A&H gear**: dLive + SQ + Python Automation — ~3 second automated switchover via custom scripting

## Key Limitations Identified

- Allen & Heath dLive and SQ-5 show files are **completely incompatible** — no conversion tool exists
- SQ-5 has only **one option card slot** — must choose Dante OR Waves, not both
- d&b D20 amplifiers have **no built-in Dante** — require DS10 bridge
- True automatic seamless DSP failover only exists natively on Yamaha RIVAGE PM (DSP Mirroring) and DiGiCo Quantum 7 (dual engines)

## Related Workspace Resources

- `learning-plan/Software/Theatre-mix/` — TheatreMix dual-console automation
- `learning-plan/Software/R1/` — d&b R1 remote control software
- `learning-plan/Tech/Vlans/` — VLAN configuration (Dante Primary/Secondary)
- `learning-plan/Tech/Qos/` — QoS settings for Dante traffic
- `learning-plan/Paperwork/System-flow-diagram/` — USITT system diagram conventions
- `learning-plan/Paperwork/Rack-diagrams/` — Rack layout templates
- `class-projects/Sound-System-Documentation/` — USITT documentation standards
