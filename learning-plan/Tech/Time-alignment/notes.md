# Notes: Time Alignment of Speakers

## What Is Time Alignment?

- Time alignment is the process of ensuring that sound from multiple speakers arrives at the listener (or measurement point) at the same time
- When speakers are at different distances from the listener, their sound arrives at different times — this causes phase cancellation, comb filtering, and a loss of clarity
- Time alignment is achieved by adding **delay** to the closer speaker so it "waits" for the sound from the farther speaker to catch up

### Why Does Sound Arrive at Different Times?

- Sound is a pressure wave that moves through air at a finite speed (~343 m/s)
- If you have two speakers — one 10 metres from the listener and one 20 metres away — the sound from the closer speaker arrives roughly 29 ms before the farther one
- During those 29 ms, the listener hears only the close speaker. When the far speaker's sound finally arrives, the two signals overlap — but they are offset in time
- That time offset means the peaks and troughs of the two sound waves no longer line up. At some frequencies they reinforce each other; at others they cancel. This is the core problem time alignment solves
- By adding a digital delay to the closer speaker's signal chain, you hold its sound back so both speakers' sound arrives at the listener simultaneously, and the peaks and troughs line up again

## Why It Matters

- Without time alignment, overlapping frequencies from multiple sources will interfere destructively
- This results in:
  - Loss of low-frequency energy (especially with subwoofers)
  - Comb filtering — a series of notches and peaks in the frequency response
  - Poor intelligibility and inconsistent coverage
- Proper alignment ensures **coherent summation** — when two sources are in phase, they add constructively

### Constructive and Destructive Interference

- **Constructive interference** happens when two sound waves arrive in phase — their pressure peaks line up and combine. Two identical sources in phase produce a **+6 dB** increase in level (that's roughly a perceived doubling of loudness from correlated signals like the same audio feed)
- **Destructive interference** happens when two sound waves arrive out of phase — the peak of one wave lines up with the trough of the other, and they cancel each other out. At a perfect 180° offset, two identical signals will cancel to complete silence
- In practice, you rarely get perfect cancellation everywhere because listeners are at different distances from each speaker, so the phase relationship changes with position and frequency — but you still hear significant damage as dips and notches across the frequency response
- The goal of time alignment is to maximise constructive interference and minimise destructive interference across the listening area

---

## Core Concepts

### Speed of Sound

- Sound travels at approximately **343 m/s** (1,125 ft/s) at 20°C at sea level
- This means roughly **1 ms per foot** (more precisely, 1.125 ft/ms or 0.343 m/ms)
- Temperature, humidity, and altitude all affect the speed of sound:
  - Higher temperature → faster speed
  - Rule of thumb: speed increases ~0.6 m/s per °C

### Delay Calculation

- **Delay (ms) = Distance difference (ft) ÷ 1.125**
- Or: **Delay (ms) = Distance difference (m) ÷ 0.343**
- Example: If the main speaker is 30 ft from the listener and a delay fill is 15 ft away:
  - Difference = 15 ft
  - Delay to add to the fill = 15 ÷ 1.125 ≈ **13.3 ms**

### Phase and Wavelength

- **Phase** is the position within one cycle of a waveform, measured in degrees (0°–360°)
  - Think of a single cycle of a sine wave as a circle. 0° is the start, 90° is the positive peak, 180° is the zero crossing going negative, 270° is the negative peak, and 360° brings you back to the start
  - When we say two signals are "90° out of phase," it means one signal is a quarter of a cycle behind the other
- When two identical signals are **0° apart** (in phase), they sum constructively — you get more level
- When **180° apart** (out of phase), they cancel completely — this is total destructive interference
- Anything in between gives partial cancellation or reinforcement:
  - 0°–90° apart: mostly constructive (you get a boost, just not the full +6 dB)
  - 90°–180° apart: increasingly destructive (you start losing energy)
  - The relationship is continuous, not a sudden switch

#### Wavelength

- **Wavelength (λ)** is the physical distance one complete cycle of a sound wave occupies in air
- Formula: **λ = speed of sound ÷ frequency**
  - Example: 1 kHz → λ = 343 ÷ 1000 = 0.343 m (~1.1 ft)
  - Example: 100 Hz → λ = 343 ÷ 100 = 3.43 m (~11.3 ft)
  - Example: 10 kHz → λ = 343 ÷ 10000 = 0.034 m (~1.3 inches)

#### Why This Matters for Alignment

- A timing error of 1 ms means the two signals are offset by about 0.34 m (1.1 ft)
- For a 10 kHz signal (wavelength 0.034 m), that 0.34 m offset is **10 full wavelengths** — the signals happen to be back in phase, but any slight change shifts them out again. High frequencies cycle through in-phase and out-of-phase very rapidly with small distance changes
- For a 100 Hz signal (wavelength 3.43 m), that same 0.34 m offset is only **1/10 of a wavelength** — about 36° of phase shift, which is mild and still mostly constructive
- **Key takeaway:** Lower frequencies have longer wavelengths and are more forgiving of small misalignments. Higher frequencies have shorter wavelengths and are very sensitive to alignment errors — even a fraction of a millisecond matters

---

## Comb Filtering

### What Is It?

- Comb filtering occurs when two copies of the same signal arrive at a listening point at slightly different times
- The name comes from what it looks like on a frequency response graph — a repeating pattern of peaks and deep notches that resembles the teeth of a comb
- It creates a repeating pattern of constructive and destructive interference across the frequency spectrum

### How It Works Step by Step

1. Two versions of the same signal arrive at the listener, separated by a small time gap (Δt)
2. At any given frequency, the two copies are at some phase relationship to each other
3. At frequencies where the delay equals a full wavelength (or multiples of it), the signals are back in phase → constructive interference (peak)
4. At frequencies where the delay equals half a wavelength (or odd multiples of half wavelengths), the signals are perfectly out of phase → destructive interference (null/cancellation)
5. This pattern repeats at regular intervals up through the frequency spectrum

### The Maths

- The **nulls** (cancellations) occur at: **f = (2n - 1) ÷ (2 × Δt)** where n = 1, 2, 3, …
  - More simply: the first null is at **f = 1 ÷ (2 × Δt)**, and subsequent nulls are at odd multiples of that frequency
- The **peaks** (reinforcements) occur at: **f = n ÷ Δt** where n = 1, 2, 3, …
- Example with a 1 ms delay:
  - Nulls at: 500 Hz, 1500 Hz, 2500 Hz, 3500 Hz, …
  - Peaks at: 1000 Hz, 2000 Hz, 3000 Hz, 4000 Hz, …
- Example with a 2 ms delay:
  - Nulls at: 250 Hz, 750 Hz, 1250 Hz, 1750 Hz, …
  - Peaks at: 500 Hz, 1000 Hz, 1500 Hz, 2000 Hz, …
- Notice: a **longer** delay means the nulls and peaks are **closer together** in frequency — more teeth on the comb, more damage across the spectrum

### What It Sounds Like

- Comb filtering sounds hollow, thin, or "phasey" — like speaking into a tube or a metallic, tinny quality
- If you've ever spoken into a microphone while standing near a hard reflective wall, you've probably heard mild comb filtering
- It reduces speech intelligibility because it carves out chunks of the frequency range that carry important consonant and vowel information

### Common Causes

- **Misaligned speakers** — two speakers playing the same content with a time offset
- **Reflections off surfaces** — sound from a speaker bounces off a wall, floor, or ceiling and arrives at the listener slightly after the direct sound
- **Poorly aimed arrays** — two array elements covering the same area with different path lengths
- **Microphone placement** — a mic picking up both direct sound and a reflection (e.g., a lavalier mic near a hard chest plate, or a podium mic near a reflective lectern surface)

---

## Speaker Placement and Time Alignment

### Main + Fill / Delay Speakers

- Delay fills (e.g., under-balcony fills, front fills, outfills) must be delayed to match the arrival of the main system
- The goal is for the listener to perceive one coherent source, not separate arrivals
- Without delay, the fill speaker is closer to the listener than the main system, so its sound arrives first. The listener's brain locks onto the fill as the perceived source direction — pulling the sound image away from the stage

### The Haas Effect (Precedence Effect) — In Depth

- The Haas Effect is a psychoacoustic phenomenon discovered by Helmut Haas in 1949
- **The core principle:** When two sounds arrive within about 1–40 ms of each other, the brain perceives them as a single event and attributes the direction to whichever sound arrived first. The second arrival is not heard as a separate sound — it is fused with the first
- This is how your brain works in everyday life. When someone speaks to you in a room, you hear direct sound and reflections off every surface. The reflections arrive a few milliseconds later, but you don't hear them as echoes — your brain fuses them with the direct sound and uses the earliest arrival to determine where the person is standing

#### How It Applies to Sound Reinforcement

1. **The problem:** A front fill speaker is 3 metres from a front-row listener. The main PA is 20 metres away. The fill's sound arrives ~50 ms earlier. The listener perceives the sound as coming from the fill speaker at their feet, not from the stage — this breaks the illusion
2. **The basic fix:** Add delay to the fill speaker equal to the distance difference divided by the speed of sound. This makes both arrivals hit the listener at the same time. But now the listener hears equal arrivals from two directions, which can feel unfocused
3. **The Haas trick:** Add a few extra milliseconds of delay (typically 5–20 ms) to the fill beyond what physical alignment requires. Now the main PA's sound arrives first. The brain locks onto the main PA as the source direction, and the fill speaker's sound is perceptually fused — it adds level and clarity without the listener being aware of it as a separate source

#### Key Details and Boundaries

- The fusion window is roughly **1–40 ms** for most signals:
  - Below ~1 ms: the brain hears phase effects, not a direction change
  - 1–5 ms: strong fusion, very hard to perceive the second arrival at all
  - 5–20 ms: fusion still holds, second arrival adds a sense of spaciousness
  - 20–40 ms: fusion begins to weaken; the second arrival may start to be perceived as a distinct echo depending on the signal (transient-heavy signals like speech break down sooner)
  - Above ~40 ms: the second arrival is perceived as a separate echo
- **Level matters too:** If the delayed sound is significantly louder than the first arrival, the brain may switch to localising on the louder source. The general guideline is to keep the fill speaker at or below the level of the main system at the listening position
- **Signal type matters:** Transient, percussive, or speech signals are more sensitive to the Haas effect than sustained, reverberant sounds. A snare drum hit will reveal a poorly delayed fill much more than a sustained pad

#### Practical Guidelines

- Start by calculating the physical delay (distance ÷ speed of sound)
- Add 5–10 ms of extra Haas delay as a starting point
- Listen from the audience position — the sound should feel like it's coming from the stage, not from the fill
- If you add too much extra delay, you'll start to hear the fill as a distinct echo — pull it back
- Use measurement tools to verify the physical delay is correct, then add the Haas offset by ear

### Subwoofer Alignment

- Subwoofers are often physically separated from the main system (e.g., on the floor vs. flown mains)
- Because sub frequencies have long wavelengths, even small timing offsets affect phase coherence in the crossover region
- Alignment in the **crossover frequency range** (typically 80–120 Hz) is critical

#### What Is the Crossover Region and Why Does It Matter Here?

- The crossover is the frequency range where the subwoofer hands off to the main speaker (or vice versa). Below the crossover, the sub is doing the work. Above it, the main speaker takes over
- In the crossover region, **both the sub and the main are producing sound at the same frequencies** — this is where they overlap and where time alignment is most critical
- If they're out of time in this overlap region, you get destructive interference right in the crossover band — this shows up as a dip or hole in the frequency response, often around 80–120 Hz, which makes the system sound thin and weak in the low-mids
- Even a 2–3 ms misalignment at 100 Hz (wavelength = 3.43 m) creates a noticeable phase offset

#### What Is an Impulse Response?

- An **impulse response** is the measurement of how a system responds to a very short, sharp signal (an impulse — like a click or a mathematically perfect spike)
- When you measure a speaker's impulse response, you see a spike showing when the sound arrived at the microphone, followed by reflections and decay
- By comparing the impulse responses of the sub and the main, you can see exactly how many milliseconds apart their arrivals are — this tells you how much delay to add
- Measurement tools like SMAART and REW can calculate and display this automatically

#### What Is a Transfer Function?

- A **transfer function** compares the input signal (what you sent to the speaker) to the output signal (what the microphone picked up)
- It shows you magnitude (level at each frequency) and phase (timing relationship at each frequency) across the entire spectrum
- When aligning subs, you look at the transfer function with both the sub and main playing together. If they're well-aligned, the magnitude trace should be smooth through the crossover region. If they're misaligned, you'll see a dip (cancellation) in the crossover band

#### Methods to Align Subs

1. Measure the impulse response of both the main and the sub at the crossover point — note the arrival time difference
2. Adjust sub delay until the impulse responses align (add delay to whichever is arriving first)
3. Verify using a transfer function measurement (SMAART, REW, etc.) — look for smooth summation through the crossover
4. Check polarity — sometimes inverting the polarity of the sub gives a better result:
   - Try the sub with normal polarity and with inverted polarity
   - Pick whichever gives a smoother, stronger response through the crossover
   - If inverting polarity helps, it usually means the sub's phase response through its filters has flipped relative to the main — this is common and not a wiring error
5. Fine-tune by adjusting delay in small increments (0.1–0.5 ms) while watching the transfer function — look for the highest level and smoothest response in the crossover band

### Arrays (Line Arrays, Point Source)

#### Line Arrays

- A line array is a column of speaker cabinets hung vertically, each angled slightly differently to cover a different section of the audience
- The bottom boxes typically have wider splay angles to cover the far seats, while the top boxes have tighter angles for the near audience (or vice versa depending on the hang)
- Because each box is at a slightly different distance from any given listener, they arrive at slightly different times. Without correction, this causes interference — particularly at high frequencies where the wavelengths are short
- **Array processing software** (e.g., d&b ArrayCalc, L-Acoustics Soundvision, Meyer GALAXY) models the geometry of the array and calculates:
  - **Per-box delay** — small delay adjustments (fractions of a millisecond) to align each cabinet's output so they arrive coherently at the target coverage zone
  - **Per-box EQ** — compensating for the fact that some boxes are further from their target area and need different equalisation
  - **Per-box level** — adjusting the drive level to each cabinet for even coverage
- This processing is what makes a modern line array work as a coherent sound source rather than a stack of individual speakers fighting each other

#### Point Source Arrays

- Point source speakers (like a d&b Y series or JBL VTX) radiate from a single point rather than forming a line
- When multiple point source boxes are splayed apart to cover a wide area, each cabinet covers a different zone with minimal overlap
- Where coverage zones do overlap, time alignment between the cabinets becomes important — you may need to add manual delay per cabinet based on the geometry
- Point source arrays generally have less overlap between cabinets than line arrays, so alignment is simpler but still matters at the crossover zones between adjacent cabinets

---

## Room Nodes and Standing Waves

### What Are Room Nodes (Room Modes)?

- Room modes are resonant frequencies determined by the dimensions of a room
- They occur when a sound's wavelength fits evenly into a room dimension, causing the sound wave to bounce back and forth between surfaces and reinforce itself
- The result is a **standing wave** — a pattern where some positions in the room have very high sound pressure (antinodes) and others have very low sound pressure (nodes), and these positions don't move

#### Types of Room Modes

- **Axial modes** (between two parallel surfaces) — the strongest and most problematic
  - These involve sound bouncing between just two surfaces (e.g., front wall to back wall, floor to ceiling, left wall to right wall)
  - A room has three sets of axial modes — one for each pair of parallel surfaces
- **Tangential modes** — involve reflections between four surfaces (e.g., all four walls). These are weaker than axial modes (roughly half the energy)
- **Oblique modes** — involve reflections off all six surfaces. These are the weakest (roughly quarter the energy of axial modes)
- In practice, **axial modes cause the most audible problems** and are the ones you most need to be aware of

#### Calculating Axial Modes

- Formula: **f = (n × speed of sound) ÷ (2 × room dimension)**
  - Where n = 1, 2, 3, … (each value of n gives a higher harmonic of the mode)
  - Example: Room length = 10 m
    - n=1: (1 × 343) ÷ (2 × 10) = **17.15 Hz** (the fundamental mode)
    - n=2: (2 × 343) ÷ (2 × 10) = **34.3 Hz** (second harmonic)
    - n=3: (3 × 343) ÷ (2 × 10) = **51.45 Hz** (third harmonic)
  - These modes exist for each room dimension (length, width, height), so a room has many overlapping modes

#### What This Sounds and Feels Like

- At a mode's antinode (high pressure point), you hear that frequency booming and unnaturally loud
- At a mode's node (low pressure point), that same frequency nearly disappears
- Walk across a room playing a low sine tone and you'll hear the level rise and fall dramatically — that's you walking through nodes and antinodes
- This is why bass sounds different depending on where you stand in a room, and why some seats in a venue sound boomy while others sound thin

### How Nodes Interact with Time Alignment

- Standing waves create areas of high pressure (antinodes) and low pressure (nodes) at fixed positions in the room
- Speaker placement relative to room boundaries affects which modes are excited:
  - A speaker placed in a **corner** excites the most modes — it's at the intersection of three sets of axial modes (length, width, and height). This is why a subwoofer in a corner sounds louder but also boomier
  - A speaker placed at the **centre of a wall** excites the modes for that wall's dimension but sits at the null point for the other two dimensions, exciting fewer modes overall
  - A speaker placed in the **centre of a room** sits at the null of the fundamental mode for all three dimensions — it excites the fewest modes but also has the least low-frequency output
- **Subwoofer placement is especially critical** because sub frequencies (20–120 Hz) have wavelengths of 2.8–17 metres — directly comparable to room dimensions. This means subs interact strongly with room modes in ways that mid and high frequency speakers do not

#### The Compound Problem

- Room modes create their own pattern of peaks and nulls that are fixed in space and frequency
- Misaligned speakers create comb filtering — another pattern of peaks and nulls based on the time offset
- When you combine these two effects, you get an even more uneven frequency response — the comb filtering peaks and nulls stack on top of the modal peaks and nulls, creating a chaotic and unpredictable sound field
- Time alignment cannot fix room modes (only room treatment and speaker placement can address those), but **getting alignment right removes one layer of the problem** and gives you a cleaner baseline to work from

### Mitigating Room Nodes

- **Speaker/sub repositioning** — Move speakers or subwoofers to positions that reduce excitation of problematic modes. Even shifting a sub by a metre can make a significant difference. In practice, try multiple positions and measure at several listener locations to find the best compromise
- **Distributed subwoofer arrays** — Using multiple subwoofers spread across the stage or room averages out the modal response. Instead of one sub exciting modes from one position, several subs excite modes differently and the peaks and nulls partially cancel each other. Common configurations:
  - **Spaced array:** Subs spread evenly across the front of the stage
  - **Cardioid sub array:** Subs arranged with rear-facing cancellation to reduce energy going back into the room (and into microphones on stage)
  - **Distributed placement:** Subs placed at different positions along the walls (common in installed systems)
- **Parametric EQ** — Use narrow parametric notch filters to reduce the most problematic resonant peaks. Be careful: EQ changes the level at that frequency everywhere, but the mode only exists at certain positions. Cutting a mode's frequency at the mix position might make other seats sound thin at that frequency
- **Acoustic treatment** — Bass traps (porous absorbers, membrane absorbers, Helmholtz resonators) placed in corners and at mode pressure maxima physically absorb low-frequency energy. This is the most effective solution but only practical for permanent installations
- **Important:** No amount of EQ or DSP processing can eliminate a standing wave — it can only reduce the peak at certain positions. Physical treatment and smart placement are always the primary tools for mode control

---

## Practical Measurement and Adjustment

### Tools

- **SMAART** (by Rational Acoustics) — the industry standard for live sound system measurement
  - Uses **dual-FFT transfer function** analysis: it compares the electrical signal you're sending to the speakers (the reference) with what the microphone picks up in the room (the measurement). This lets you see exactly how the room and the speaker are changing the sound
  - Shows you magnitude (level at each frequency) and phase (timing relationship at each frequency) in real time
  - Has a built-in **delay finder** that calculates the time offset between two signals — essential for determining how much delay to add
  - You can use it to align mains to subs, fills to mains, and verify array processing

- **REW (Room EQ Wizard)** — free, powerful room acoustics measurement software
  - Measures impulse response, frequency response, RT60 (reverb time), and more
  - Excellent for analysing room modes — it can show you exactly where your room's resonant frequencies are
  - More commonly used for installed systems and studio tuning than live events, but the principles are the same

- **System processor delay** — the DSP (Digital Signal Processing) built into speaker management systems where you actually apply the delay
  - Examples: d&b R1, Lake LM series, Meyer GALAXY, L-Acoustics LA Network Manager
  - These processors let you set delay in milliseconds (or sometimes in distance units like metres/feet, and they calculate the ms for you)
  - They also handle crossover filters, EQ, limiting, and other processing

- **Measurement microphone** — a microphone designed to pick up sound as accurately and neutrally as possible
  - Must have a **flat frequency response** — it shouldn't colour the sound, or your measurements will be wrong
  - Examples: Earthworks M30 (high quality), Behringer ECM8000 (budget-friendly)
  - These are not for recording music — they're specifically for measurement. They typically come with a calibration file that corrects for any small deviations in their response

### Alignment Workflow

1. **Set up measurement mic** at the point of interest
   - For main-to-sub alignment: place the mic where the coverage of both systems overlaps — typically the front rows or the mix position
   - For main-to-fill alignment: place the mic in the fill speaker's coverage area where it overlaps with the main system
   - Use a stand at ear height, away from reflective surfaces if possible

2. **Measure each source individually** — mute everything except the source you're measuring. Capture its impulse response and magnitude/phase response. This gives you a clean baseline for each system on its own

3. **Compare arrival times** — look at the impulse response of each source. The spike in the impulse response shows you when the sound arrived at the mic. The difference in arrival times between the two sources is the delay you need to correct. SMAART's delay finder automates this calculation

4. **Add delay to the closer source** — in your system processor, add delay (in ms) to the source that arrived first. This holds it back so both sources arrive at the mic at the same time. Always delay the closer/earlier source — you can't make sound travel faster, only slower

5. **Check polarity** — with both sources still measured individually, look at their phase traces in the crossover region. If they're roughly 180° apart, try inverting the polarity of one source (usually the sub). This is a simple flip that can make a dramatic improvement

6. **Verify with both sources on** — unmute both sources and look at the transfer function. A well-aligned system will show smooth, continuous magnitude through the crossover region. If you see a dip at crossover, your timing or polarity may still be off — go back and fine-tune

7. **Walk the room** — alignment at one mic position doesn't guarantee alignment everywhere. Move the mic to several positions across the audience area and check that the alignment holds reasonably well. You may need to compromise — optimise for the largest number of seats rather than perfection at one spot

### Common Pitfalls

- **Aligning at only one position** — The mix position is important, but it's one seat in a room of hundreds. If you only optimise for FOH, the front rows or balcony might be badly misaligned. Measure at multiple positions and find the best compromise

- **Forgetting processing latency** — Every piece of digital equipment in the signal chain (console, DSP, amplifier) adds a small amount of latency (typically 1–5 ms each). If the main PA and the fills go through different signal paths with different amounts of processing, you have a built-in time offset before the sound even leaves the speakers. Account for this in your delay calculations

- **Not checking polarity** — Polarity is a simple 180° flip of the signal. If two sources are close to 180° out of phase at crossover, a polarity inversion on one source instantly improves summation. This is the single most impactful and easiest fix — always try it before spending time on fine delay adjustments

- **Over-relying on Haas delay** — Adding extra delay to a fill for the Haas effect is a valid technique, but it should come after physical time alignment is correct. If you're using Haas delay to mask the fact that the fill sounds like a separate source, the underlying alignment is probably wrong

- **Ignoring temperature changes** — The speed of sound changes with temperature (~0.6 m/s per °C). On an outdoor show where the temperature drops 10°C from soundcheck to showtime, the speed of sound decreases by ~6 m/s. For a speaker 30 m away, that's roughly a 0.5 ms shift — enough to affect high-frequency alignment. Re-check alignment if conditions change significantly

- **Chasing perfection at every seat** — In any multi-source system, there is no single delay setting that perfectly aligns everywhere. You are always making compromises. The goal is to find the setting that works best for the most people, not to achieve perfection at one position

---

## Related Concepts

| Concept | Relevance |
|---|---|
| Comb filtering | The primary artefact of misaligned sources — repeating peaks and nulls across the spectrum |
| Haas effect / precedence effect | Psychoacoustic phenomenon used to control perceived source direction with delay fills |
| Crossover alignment | The frequency region where two systems overlap — time alignment is most critical here |
| Phase coherence | The goal of time alignment — ensuring all sources are in phase so they sum constructively |
| Inverse square law | Sound level drops by 6 dB every time you double the distance. This affects how much the misaligned sources interact — if one is much quieter due to distance, the interference is less severe |
| Polarity vs phase | **Polarity** is a fixed 180° inversion of the entire signal (a wiring or DSP switch). **Phase** is frequency-dependent — a time delay causes different amounts of phase shift at different frequencies. They are not the same thing, but both affect how sources sum |
| Array processing | Software-calculated per-box delay, EQ, and level within a line array to maintain a coherent wavefront |
| Inverse square law detail | The law states that intensity is proportional to 1/r². In practice: every doubling of distance = -6 dB. This is why a fill speaker 3 m away can easily overpower a main PA 25 m away if not level-matched |

---

## Resources

- _Sound Systems: Design and Optimization_ — Bob McCarthy (the definitive reference for system alignment)
- _The SynAudCon Newsletter_ — Pat Brown's articles on alignment and measurement
- SMAART documentation and tutorials
- d&b audiotechnik ArrayCalc and R1 guides
- Rational Acoustics blog and webinars

---

## Key Takeaways

1. Time alignment ensures multiple speakers sum constructively rather than causing cancellation
2. The fundamental calculation is distance difference ÷ speed of sound = delay
3. Always align at the **crossover frequency range** between systems
4. Room modes are fixed by the room dimensions — alignment can't fix them, but poor alignment makes them worse
5. Measure, adjust, verify — use transfer function tools like SMAART to confirm alignment
6. Check polarity before fine-tuning delay — it's the most common and impactful fix
