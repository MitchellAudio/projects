# Notes: Single Vs Three Phase Power
## Overview

- Single-phase (split-phase) is common for residential power in North America (120/240V).
- Three-phase is used for higher-power distribution in commercial and industrial settings (examples: 208V, 400/415V, 480V systems depending on region and connection).

## Split-phase (120/240V) — how it works

- The transformer at the service splits the secondary into two 120V legs that are 180° out of phase.
- Between either hot leg and neutral = 120V. Between the two hot legs = 240V.
- 240V loads connect across both hot legs; 120V loads connect between a hot leg and neutral.

## Three-phase basics

- Three-phase systems have three sinusoidal voltages, each 120° apart.
- Common wiring:
	- Wye (star): line-to-line voltage = √3 × line-to-neutral voltage. Neutral available.
        - Wye is a wiring topology (an internal connection of windings), not a single physical connector — the neutral may be brought out to a terminal (neutral lug/bushing), but the Wye itself describes how windings are arranged.
	- Delta: line voltages between phases; neutral may not be present unless a center-tapped winding is used.


## Power calculations

- Single-phase: P (W) = V × I × PF (power factor). For purely resistive loads PF = 1.
- Three-phase (balanced): P (W) = √3 × V_line × I_line × PF.

## Why use three-phase?

- More efficient transmission of power for motors and heavy loads.
- Motors run smoother and with less vibration on three-phase.
- For the same power, three-phase requires less conductor material than multiple single-phase circuits.

## Phase rotation and balancing

- Phase rotation (A-B-C order) matters for three-phase motors — reversing rotation changes motor spin direction.
- Balance loads across phases to minimize neutral current and avoid overheating conductors.

## Neutral & grounding

- Neutral is the current return for unbalanced single-phase loads; ground is a safety conductor used only for fault currents.
- In a balanced three-phase system with purely three-phase loads, neutral current can be zero.

## Motor starting and inrush

- Motors draw high inrush currents when starting
- Soft-starts, VFDs (variable frequency drives), or star-delta starters can reduce inrush and mechanical stress.
