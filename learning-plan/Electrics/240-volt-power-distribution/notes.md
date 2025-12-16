# Notes: 240 Volt Power Distribution


- **240 Volt Power Distribution**
    - Two 120 volt out of phase wires are used. The sum of the voltages is 240 volts.
    - For loads that are split back into 120 volts, a neutral wire is also used if the legs are not balanced. 
        - Ex: leg A draws 10 amps, leg B draws 5 amps, neutral carries 5 amps back on the neutral wire

- **Method of Delivery:**
	- In North America, 240V is supplied by two 120V hot wires (out of phase) and a neutral from the main panel. The voltage between the two hots is 240V.
	- In many other countries, 240V is the standard single-phase supply, delivered as one hot and one neutral.
    - Camlocks are often what is used to go from wall pannels to a power distro

- **Breakers and Panel Workings:**
	- 240V circuits use double-pole breakers, which connect to both hot wires in the panel.
	- Each breaker protects the circuit from overcurrent and short circuits.

- **Applications:**
	- Reduces current draw and wire size for the same power compared to 120V circuits.
		- Using Ohm's Law: Power (P) = Voltage (V) × Current (I). For the same power, doubling the voltage (from 120V to 240V) means the current is halved: I = P / V. Lower current means less heat loss and allows for smaller wire size.
        - Watts = Volts x Amps

- **How to wire a 240V Circuit:**
    1. Connect the ground wire (green or bare) to the ground bus bar first.
    2. Connect the neutral wire (white) to the neutral bus bar.
    3. Connect the two hot wires (usually black and red) to the breaker terminals.
    4. Ensure all connections are secure
    5. Enable power and test the circuit

---

## Determining power requirments

- **Confirm supply type:** single-phase 120/240V or three-phase (e.g., 208V, 400/415V, 480V).
- **Total continuous power (P):** sum amplifier/channel RMS power + 20–30% overhead for headroom.
- **Calculate current:**
    - Single-phase: I = P / V
    - Three-phase (line-to-line): I = P / (√3 × V × PF) — use PF ≈ 0.9 if unknown.
- **Design for continuous loads:** multiply current by 1.25 (NEC continuous-load rule) and choose breaker ≥ that value.
- **Inrush management:** stagger amp turn-on, use soft-start or larger breakers if amplifiers have high inrush. (Jason recomended sequencers to help with this)

### Worked Examples

- Single-phase example:
    - P = 5000 W, V = 240 V → I = 5000 / 240 = 20.8 A
    - Design current = 20.8 × 1.25 = 26.0 A → choose 30 A double-pole breaker
- Three-phase example:
    - P = 15,000 W, V = 400 V (line-to-line), PF = 0.9 → I = 15000 / (1.732 × 400 × 0.9) ≈ 24.0 A
    - Design current = 24.0 × 1.25 = 30.0 A → choose appropriate 3‑pole breaker