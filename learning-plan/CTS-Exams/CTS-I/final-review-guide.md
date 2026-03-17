# CTS-I Final Review Guide (Last Few Days)

Use this as a rapid, high-yield pass before exam day. It is based on your CTS-I notes and focuses on what is most testable.

---

## 1) Highest-Yield Domains (Priority Order)

1. Safety, rigging, and code compliance
2. Installation standards (mounting, pathways, cable handling)
3. Setup, verification, and troubleshooting workflow
4. Project coordination, documentation, closeout, and client training
5. AVIXA standards, terminology, and job-task framing

If time is tight, master #1-#3 first.

---

## 2) Must-Memorize Numbers and Rules

### Rigging and Safety

- WLL formula: `WLL = MBS / Design Factor`
- Design factors:
  - Permanent standing rigging: `5:1`
  - Running/moving loads: `8:1`
  - Over people/life safety contexts: `10:1`
- Bridle rule: as included angle increases, leg tension increases.
- Critical limit: do not exceed `120 degrees` included angle.
- Secondary safety required for overhead equipment and must be independent of primary mount.

### OSHA / Height Work

- Fall protection thresholds:
  - Construction: `6 ft`
  - General industry: `4 ft`
- Ladder: 4:1 ratio and 3-point contact.

### Cable Pathways and Handling

- NEC conduit fill:
  - 1 conductor: `53%`
  - 2 conductors: `31%`
  - 3+ conductors: `40%`
- Max bends between pull points: `360 degrees`.
- Pulling tension for Cat6/Cat6A: `25 lbs` max.
- Power crossing best practice: cross signal and power at `90 degrees`.
- UTP minimum bend radius: typically `4x cable diameter`.

### Separation from Power (Parallel Runs)

- Unshielded data: `12 in`
- Shielded data: `6 in`
- Coax: `6 in`
- Speaker level: `3 in`
- Fiber: no separation requirement

### Rack and Thermal

- 1U = `1.75 in`
- Rack width between rails = `19 in`
- BTU conversion: `BTU/hr = Watts x 3.412`
- Heavy devices low, maintain service clearance, avoid hot-air recirculation.

### Display / Projection

- Throw ratio: `Throw Distance / Screen Width`
- Use lens shift before keystone.
- Keystone is quality loss; avoid in permanent pro installs.
- Verify mount load capacity with safety margin and use independent safety cable.

### Fire / Code

- Plenum spaces require correct cable rating.
- Cable hierarchy (higher can substitute lower): `CMP -> CMR -> CM/CMG -> CMX`
- Penetrations in rated assemblies require listed fire-stopping systems.

### ADA / Usability

- Operable controls generally should be reachable at max `48 in` height (context dependent).
- Maintain required clear floor space for access.

---

## 3) Exam-Style Thinking Patterns

Use this order on scenario questions:

1. Safety first (personnel, overhead, electrical, code)
2. Code/compliance second (NEC, fire-stop, plenum, ADA)
3. Manufacturer instructions and rated hardware
4. Signal integrity (distance, bend, separation, termination)
5. Verification with measurable test evidence
6. Documentation and communication trail (RFI, CO, as-builts)

If two options both work technically, choose the one that is safer, code-compliant, and documented.

---

## 4) Setup and Verification: What to Say to Yourself

### Cable test logic

- Cat cable: wiremap first, then cert metrics (NEXT, return loss, insertion loss).
- Fiber: inspect/clean -> continuity/VFL -> loss test -> OTDR when needed.
- Coax: continuity + short + attenuation/return loss as required.

### System verification logic

- Component test first.
- End-to-end route test second.
- Scenario test third (presentation, VC, recording, wireless).
- Edge-case/control behavior fourth (startup, rapid commands, recovery after failures).

### Evidence

- Record test methods, tool model/calibration, pass/fail, and location/cable ID.

---

## 5) Project Process You Should Be Fluent In

- Construction phase awareness: rough-in timing matters.
- Coordinate with electrical, HVAC, IT, architecture early.
- Use RFIs for conflicts/ambiguity.
- Use change orders when scope shifts.
- Closeout package: as-builts, O&M, test reports, warranties, training records.
- Punch list is normal; track, assign, verify closure.

---

## 6) 3-Day Final Plan (Adjust if Exam Is Sooner)

### Day -3: Safety + Installation Core

- Drill rigging/WLL/bridle + overhead safety rules.
- Drill conduit fill, bends, cable separation, bend radius, pull tension.
- Drill fire/plenum/fire-stop rules.
- End with 30 minutes of formula recall from memory.

### Day -2: Projection + Verification + Troubleshooting

- Throw ratio, zoom range, offset/shift logic.
- Keystone vs lens shift decisions.
- Audio/video/control/fiber test workflows.
- Run timed scenario practice: choose best next action and why.

### Day -1: Closeout + Terminology + Light Review

- RFI/change order/coordination/meeting/documentation flow.
- O&M and training deliverables.
- AVIXA standards/terms and JTA domains.
- Finish with one 60-90 minute mixed recall session, then stop early.

### Exam Morning (30-45 min max)

- Review only your one-page numbers/formulas list.
- Do not learn new topics.
- Run mental checklist: Safety -> Code -> Install -> Verify -> Document.

---

## 7) Rapid Formula Sheet

- `W = V x A`
- `V = I x R`
- `dB (voltage) = 20 log(V1/V2)`
- `dB (power) = 10 log(P1/P2)`
- `SPL distance change = 20 log(d2/d1)`
- `Throw Ratio = Throw Distance / Screen Width`
- `WLL = MBS / Design Factor`
- `Bridle leg tension = Load / (2 x cos(angle/2))`
- `BTU/hr = Watts x 3.412`

---

## 8) 20 Quick-Check Prompts (No Notes)

1. What is the first priority in any installation scenario?
2. What design factor is minimum for standing rigging?
3. What happens to bridle leg tension as angle increases?
4. Why is 120 degrees included angle a red flag?
5. What are NEC conduit fill percentages for 1, 2, and 3+ conductors?
6. Why should power and signal cross at 90 degrees?
7. Which is preferred in permanent installs: lens shift or keystone?
8. What does CMP mean and where is it required?
9. What must be done at penetrations through rated walls/floors?
10. What is the Cat6 max pulling tension value from your notes?
11. What is 1U in inches?
12. How do you estimate rack heat from watts?
13. What is your default order for cable testing and certification?
14. What are the core steps of integration testing?
15. What belongs in closeout documentation?
16. When do you submit an RFI?
17. What triggers a change order?
18. What should a training handoff include?
19. In a tie between answers, what principle usually wins?
20. Recite the 4 CTS-I JTA domains.

---

## 9) Last-Minute Confidence Strategy

- Answer the question that is asked, not the one you expected.
- Eliminate unsafe and non-compliant options first.
- Watch absolute words like "always" and "never" unless code/safety truly demands it.
- Mark and move if stuck; return with fresh context.
- Keep a steady pace and trust your process.

You have already done the hard part by building broad notes. This guide is your short path to sharp recall under exam pressure.
