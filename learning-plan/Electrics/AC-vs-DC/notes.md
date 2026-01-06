# Notes: AC vs DC

## Quick definitions

- DC (Direct Current): current and voltage that are constant (time-invariant). DC provides bias rails for active circuits, phantom power, and battery operation.
- AC (Alternating Current): voltage and current that vary periodically (sinusoids are most common in power and audio). Audio signals are AC (bipolar waveforms centered on a reference), and mains power is AC (60 Hz in the USA).

## How AC and DC appear in audio systems

- Audio signal: an AC waveform (typically within 20 Hz–20 kHz) that represents sound. It is usually small amplitude (millivolts to volts) and rides on circuit reference (ground).
- Power rails: active audio electronics (preamps, ADCs, amps) require DC rails (e.g., ±12 V, +48 V phantom, or single-supply rails). Those DC rails are produced from AC mains internally.
- Mains power: AC at 60 Hz distributed for powering equipment in the USA. Transformers interact with mains frequency and are the reason we often experience 60 Hz hum.

## Practical implications for audio gear

### Transformers in audio and buildings

- Audio transformers (signal DI, line isolation): pass the AC audio, convert balanced↔unbalanced, and perform impedance transformation. They can break signal‑domain ground loops when used in the signal path.
- Power transformers (mains & isolation): step voltages (distribution) and provide mains isolation. Isolation transformers create a floating secondary to break power‑domain ground loops; autotransformers change voltage without isolation.
- Shielding and capacitance: transformers have inter‑winding capacitance; high‑quality isolation transformers include an electrostatic/Faraday shield to reduce capacitive coupling of mains into the secondary and lower common‑mode noise.
- Limitations: transformers cannot pass DC — applying DC bias to a transformer will saturate the core and distort or damage it.

### Power supplies: linear vs switching

These power supplies are the internal component that switches the incoming ac from main power into dc for the electronics.
- Linear power supplies (Linear PSU):
	- How they work: mains → transformer → rectifier → large smoothing capacitors → linear regulator.
	- Noise profile: low high‑frequency noise; residual low‑frequency ripple (120 Hz after rectification of 60 Hz mains) can remain if filtering is inadequate.
	- Pros: excellent for sensitive analog circuits (mic pres, phono), predictable PSRR, simple EMI behavior.
	- Cons: heavy, less efficient, generate heat (transformer and regulator dissipation).

- Switch‑Mode Power Supplies (SMPS):
	- How they work: mains → rectifier → high‑frequency switching stage → filtering and regulation.
	- Noise profile: efficient but can introduce high‑frequency switching noise (tens of kHz to MHz) that can couple into analog stages if not filtered/shielded.
	- Pros: compact, efficient, lower weight, multiple rails easier to implement.
	- Cons: require careful design (layout, filtering, common‑mode chokes, snubbers); poorly designed SMPSs are common sources of audible interference.

- Practical mitigations for SMPS noise:
	- Add LC/π input/output filters, common‑mode chokes, and ferrites on cables.
	- Use metal enclosures tied to earth to shield radiated noise.
	- Locally regulate sensitive analog rails with low‑noise linear regulators or LDOs downstream of a SMPS.
	- Keep analog and digital grounds separated and join at a single point where practical.

### Hum, ripple and how they manifest

- Low‑frequency hum: mains fundamental (60 Hz) and rectified ripple (120 Hz) appear as tone-like hum in audio. Causes include poor filtering on DC rails or mains coupling into signal paths.
- High‑frequency artifacts: switching noise from SMPS or digital clocks can show as hiss, intermodulation products, or ultrasonic noise that demodulates into the audible band.

### Practical checklist

- If you hear a 60 Hz tone: check for 120 Hz ripple on DC rails (scope) and poor PS filtering.
- If you hear broadband/hissing artifacts: suspect SMPS switching or digital circuit noise coupling; check for poor filtering or radiated HF.
- To isolate a problem quickly: temporarily power a suspect rack from a known clean linear supply or use an isolation transformer to see if hum changes 
- For signal‑path hum: try a passive transformer DI or ground‑lift on a DI box to break the signal ground loop.

## Special cases in audio

- Phantom power (+48 V DC): a DC supply delivered over balanced microphone cables; it must be quiet, well regulated, and protected because it biases condenser microphone electronics.
- Headphone/line outputs and DC: output stages must avoid DC on loudspeaker or headphone outputs (DC can damage drivers and cause offset). Output coupling caps or servo circuits are used to eliminate DC at the speaker.

## Troubleshooting tips

- If you hear mains‑frequency hum, check for 60 Hz (and 120 Hz ripple after rectification) on DC rails with an oscilloscope and inspect power supply filtering.
- Use an isolation transformer to test whether the hum is power‑earth related (do not remove protective earths).
- For high‑frequency hiss or switching noise, suspect SMPS or digital switching stages and look for poor layout, inadequate filtering, or common‑mode paths into analog stages.
