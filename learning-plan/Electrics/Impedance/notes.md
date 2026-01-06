# Notes: Impedance


## Core concepts

- Impedance (Z): the complex opposition a circuit element presents to alternating current; Z = R + jX where R is resistance and X is reactance (positive for inductance, negative for capacitance). Magnitude |Z| and phase angle describe how voltage and current relate at a given frequency.
- Frequency dependence: reactive elements (L and C) make impedance frequency-dependent — speaker impedance varies strongly with frequency due to voice-coil inductance and cabinet/driver resonances.

## Input and output impedance (audio relevance)

- Source (output) impedance: the low impedance the signal source presents. Low output impedance is generally desirable because it drives the load with minimal voltage drop and provides good damping of the connected speakers (lowers output impedance of the amplifier relative to speaker impedance increases damping factor).
- Input impedance: the impedance the receiving device presents to the source. It should be significantly higher than the source impedance to avoid loading and level loss (rule of thumb: input impedance at least 10× source impedance for negligible loading).
- Bridging vs matching: modern audio typically uses bridging (voltage transfer) where amplifiers have low output impedance and speakers are treated as loads; classic impedance matching (for maximum power transfer) using equal source/load impedances is less common in audio line-level gear but still relevant in legacy telephone or RF systems.

## Speakers and nominal impedance

- Nominal speaker impedance (4 Ω, 8 Ω, etc.) is a simplified number; the real impedance varies with frequency and often has peaks at resonance. Amplifier stability and thermal limits depend on actual load behavior.

## Reactive behaviour and its effects

- Capacitive loading: long cables into high‑impedance inputs create capacitive load, which can roll off highs and create instability in some circuits.
- Inductive loading: speaker voice coils are inductive, leading to increasing impedance with frequency and phase shifts that affect amplifier load and frequency response.

## Damping factor and control of speakers

- Damping factor = Z_speaker / Z_output (often quoted as amplifier output impedance relative to speaker). Higher damping factors (lower amplifier output impedance) give better control of cone motion around resonance, improving transient performance and bass control.

## Practical measurement tips

- To estimate source impedance: measure open-circuit voltage V_oc, then measure voltage V_load with a known load R_load. Z_source ≈ R_load * (V_oc/V_load - 1).
- To check speaker impedance: use a low-frequency sine sweep and measure impedance magnitude vs frequency (or use an LCR meter at diagnostic points). DC resistance (DCR) is not equal to nominal impedance but gives voice-coil resistance.

## Practical rules of thumb for audio

- Keep source impedance low relative to input impedance to avoid level loss and tonal change.
- Use balanced connections and low source impedance for long runs to reject noise and maintain signal integrity.
- Avoid driving reactive loads that push an amplifier beyond its thermal or stability limits; check amplifier ratings and conservative headroom.

## When matching matters

- Microphone connections: many passive transformers or matching transformers are used to interface low-impedance mics to preamps or to balance/unbalance signals — choose transformers for the frequency range and impedance ratio required.
- Speaker lines and long cable runs: consider cable resistance and impedance at the power levels involved; for very long runs, higher voltage distribution (line matching) or larger conductor gauge reduces loss.
