# Notes: Isolated Transformer

## What is an isolated transformer?

- Definition: A transformer whose primary and secondary windings are electrically separate so that there is no direct conductive path between the supply side and the load side. Energy transfers only via magnetic coupling through the transformer's core, not by a shared conductor.
- Achieved by using distinct insulated windings (primary and secondary) wrapped on the core with  inter‑winding clearances and insulation. High end isolation transformers may include an electrostatic (Faraday) shield to reduce capacitive coupling.
- Electrical effect: The secondary is electrically "floating" relative to the primary and earth. This floating condition is what breaks galvanic connections and prevents direct ground-loop currents between interconnected systems.

## Isolated vs Autotransformer

- Autotransformer: uses a single continuous winding with taps; primary and secondary share conductors, so it does NOT provide galvanic isolation. It can be smaller and cheaper but offers no isolation benefit.
- Isolated transformer: uses separate windings and therefore provides galvanic isolation and the ability to break ground loops.

## Typical applications

- Audio systems: isolate mixing consoles, snake boxes, and amplifiers to eliminate hum from power-domain ground loops.
- Can be used to step-up or step-down voltages while keeping circuits isolated.

## Why hum appears

- Ground loops and common‑mode currents: 
    - Ground loop — multiple conductive paths between the same two equipment chassis or circuit reference points. Small voltage differences between earth points (caused by wiring resistance, stray magnetic fields, or nearby loads) produce circulating currents through cable shields and chassis, which show up as 50/60 Hz hum in audio circuits.
- Signal vs power loops: Loops can exist in the signal domain (between audio gear via cable shields and multiple earth references) or in the power domain (different mains earth points between rack locations). 
    - Signal‑domain loops are often the cause, but power‑domain loops can also induce hum through shared chassis and connected equipment.
    - Signal-domain loops will not be solved with an isolated transformer.

## How an isolated transformer helps

- Breaks the conductive path: By providing galvanic isolation (separate primary and secondary windings), an isolation transformer removes the direct conductive path through mains earth that a power‑domain ground loop needs. If the loop is formed through the power earth, floating the secondary will stop that circulating current and the audible hum will disappear.
- Reduces common‑mode injection from mains: Because the secondary is not directly connected to primary earth, mains common‑mode voltages are less likely to be imposed on the equipment chassis via the power connection.
- Limitations and realities:
	- Does not automatically fix signal‑domain loops: If the hum is flowing through signal cables and shield connections between devices, a mains isolation transformer alone often won't help — you need signal isolation (balanced wiring, DI boxes, signal transformers, or lifting ground at the signal interface).
	- Inter‑winding capacitance and shield quality matter: Cheap isolation transformers with high inter‑winding capacitance can still allow some hum via capacitive coupling. Transformers with an electrostatic (Faraday) shield or low inter‑winding capacitance are more effective at stopping common‑mode hum.
	- Safety and bonding: Floating a system with an isolation transformer changes how earth references behave. Either leave the secondary floating with awareness of hazards, or bond the secondary to earth at a single point if a known reference is required — follow local electrical code.

## Pros / Cons

- Pros: effective at eliminating ground-loop hum, provides safety isolation, simple passive device (no active electronics).
- Cons: bulky for high VA values, can be costly, introduces weight and some insertion loss, may saturate if overloaded.
