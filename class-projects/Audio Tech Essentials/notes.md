# Audio Tech Essentials


### Transducers

**Definition:** A transducer is a device that converts one form of energy into another. In audio systems, transducers convert:
- **Acoustic energy → Electrical energy** (input transducers)
- **Electrical energy → Acoustic energy** (output transducers)

---

#### Input Transducers (Microphones)

Microphones convert sound waves (acoustic energy) into electrical signals.

**Common Types:**

- **Dynamic Microphones**
  - Use electromagnetic induction with a moving coil attached to a diaphragm
  - Rugged, reliable, no power required
  - Examples: Shure SM57, SM58

- **Condenser Microphones**
  - Use a capacitor with a movable diaphragm and fixed backplate
  - Require phantom power (+48V)
  - More sensitive and wider frequency response than dynamic mics
  - Examples: Neumann U87, Audio-Technica AT2020
  - Best for: Studio vocals, acoustic instruments, overhead/room mics

- **Ribbon Microphones**
  - Use a thin metal ribbon suspended in a magnetic field
  - Natural, smooth sound with figure-8 polar pattern
  - Fragile, sensitive to wind and phantom power (older models)
  - Examples: Royer R-121, AEA R84

---

#### Output Transducers (Speakers/Loudspeakers)

Speakers convert electrical signals back into sound waves (acoustic energy).

**Components:**

- **Driver** - The actual transducer element
- **Diaphragm/Cone** - Moves air to create sound waves
- **Voice Coil** - Conducts electrical signal in magnetic field
- **Magnet** - Creates magnetic field for voice coil to move within
- **Suspension** - Allows diaphragm to move while keeping it centered

**Key Concepts:**

- **Impedance** - Measured in ohms (Ω), typically 4Ω, 8Ω, or 16Ω
- **Sensitivity** - How efficiently a speaker converts power to sound (dB SPL @ 1W/1m)
- **Frequency Response** - Range of frequencies the speaker can reproduce
- **Power Handling** - Maximum wattage (RMS and peak)

---

#### Signal Flow

```
Sound Source → Microphone (Input Transducer) → Preamp → Mixer → 
Amplifier → Speaker (Output Transducer) → Sound Wave
```

---

### Notes
- Transducers are the beginning and end of every audio signal chain
- Quality of transducers significantly impacts overall system sound
- Proper impedance matching between amplifier and speakers is critical

---

### Microphone Pickup Patterns (Polar Patterns)

Pickup patterns describe the directionality of a microphone—how it responds to sound from different angles.

**Omnidirectional**
- Picks up sound equally from all directions (360°)
- Circular polar pattern
- Best for: Room ambience, group recordings, capturing natural room sound
- More prone to feedback in live settings

**Cardioid**
- Heart-shaped pattern, most sensitive at front, rejects sound from rear
- ~130° pickup angle
- Most common pattern for live sound and studio work
- Best for: Vocals, instruments, reducing stage bleed and feedback
- Exhibits proximity effect (increased bass when close to source)

**Figure-8 (Bidirectional)**
- Picks up equally from front and back, rejects sound from sides
- Two lobes at 0° and 180°
- Common in ribbon microphones
- Best for: Two-person interviews, Blumlein stereo recording, room rejection from sides
- Useful in mid-side (M-S) stereo techniques

**Supercardioid**
- Tighter front pickup than cardioid with narrower angle (~115°)
- Small rear lobe of sensitivity
- Greater side rejection than cardioid
- Best for: Isolating sound sources on stage, reducing monitor feedback
- Requires careful monitor placement (avoid the rear lobe area)

