"""
Generate quiz questions from parsed note sections.

Extracts multiple choice questions from markdown content:
- Definition matching: term ↔ description
- Fact questions: key statements with the bold term as the answer
- Formula questions: complete the formula from options
- Statement questions: which fact about a topic is correct (same-topic distractors)
"""

import re
import random
from dataclasses import dataclass, field


@dataclass
class Question:
    """A single quiz question with its metadata."""
    type: str               # 'multiple_choice'
    question: str            # The question text
    answer: str              # The correct answer
    options: list = field(default_factory=list)   # For multiple choice
    source_topic: str = ""   # e.g., "Tech"
    source_subtopic: str = ""  # e.g., "Time alignment"
    context: str = ""        # Extra info shown after answering


class QuestionGenerator:
    """Generates quiz questions from parsed note data."""

    # Terms that are labels/headers, not real answers
    SKIP_TERMS = {
        'note', 'important', 'key', 'example', 'tip', 'warning',
        'the problem', 'the basic fix', 'the haas trick',
        'key takeaway', 'key details and boundaries',
        'constructive interference', 'destructive interference',
        'the core principle', 'the fusion window',
        'the compound problem', 'level matters too',
        'signal type matters', 'best of both worlds',
        'still used', 'key concept', 'why',
    }

    # Words that suggest a line is an instruction, not a concept
    _INSTRUCTION_WORDS = {
        'click', 'press', 'select', 'open', 'close', 'drag', 'tap',
        'go to', 'navigate', 'use the', 'run the', 'type the',
    }

    # Unicode symbols to strip from display text
    _SYMBOLS = re.compile(r'[✓✗✘✔★☆→←↑↓►▶▷●○◆◇■□▪▫•·‣⬆⬇⬅➡⚡⚠️📌🔑💡🎯]')

    def __init__(self, notes: list):
        self.notes = notes
        self.all_facts = self._collect_all_facts()

    # ─── Public Methods ───────────────────────────────────

    def generate_from_sections(self, sections: list, count: int = 15) -> list:
        """Generate up to `count` questions from a list of NoteSection objects."""
        questions = []

        for section in sections:
            if not section.content:
                continue
            content_text = ' '.join(section.content)
            if 'Add your notes' in content_text:
                continue

            questions.extend(self._extract_definition_mc(section))
            questions.extend(self._extract_fact_mc(section))
            questions.extend(self._extract_formula_mc(section))
            questions.extend(self._extract_statement_mc(section))

        # Deduplicate by question text
        seen = set()
        unique = []
        for q in questions:
            if q.question not in seen:
                seen.add(q.question)
                unique.append(q)

        random.shuffle(unique)
        return unique[:count]

    def generate_for_topic(self, topic: str, count: int = 15) -> list:
        """Generate questions from all notes within a topic."""
        sections = []
        for note in self.notes:
            if note.topic == topic:
                sections.extend(note.sections)
        return self.generate_from_sections(sections, count)

    def generate_for_subtopic(self, topic: str, subtopic: str, count: int = 15) -> list:
        """Generate questions from a specific subtopic."""
        sections = []
        for note in self.notes:
            if note.topic == topic and note.subtopic == subtopic:
                sections.extend(note.sections)
        return self.generate_from_sections(sections, count)

    def generate_all(self, count: int = 15) -> list:
        """Generate questions from all available notes."""
        sections = []
        for note in self.notes:
            sections.extend(note.sections)
        return self.generate_from_sections(sections, count)

    # ─── Question Extraction ─────────────────────────────

    def _extract_definition_mc(self, section) -> list:
        """
        Multiple choice: given a description, pick the correct term.

        Matches lines like:
          - **SMAART** — dual-FFT transfer function measurement...
          - **Term** (extra info) — description
          - **Term**: description of the term
        """
        questions = []
        pattern = re.compile(
            r'^[\s\-*]*\*\*([^*]+)\*\*\s*(?:\([^)]*\)\s*)?[—\-:]+\s*(.+)$')

        for line in section.content:
            match = pattern.match(line.strip())
            if not match:
                continue

            term = match.group(1).strip()
            desc = match.group(2).strip()

            if not self._is_good_term(term) or len(desc) < 20:
                continue

            # Clean markdown + symbols from description; reject if it contains the answer
            desc_clean = self._clean_display(desc)
            if term.lower() in desc_clean.lower():
                continue

            distractors = self._get_distractors(term, 3, section)
            if len(distractors) < 3:
                continue

            options = distractors + [term]
            random.shuffle(options)
            questions.append(Question(
                type='multiple_choice',
                question=f"Which term matches this description?\n\n\"{desc_clean}\"",
                answer=term,
                options=options,
                source_topic=section.topic,
                source_subtopic=section.subtopic,
            ))

        return questions

    def _extract_fact_mc(self, section) -> list:
        """
        Multiple choice: given a statement with a key term blanked out, pick the term.

        Takes: "Sound travels at approximately **343 m/s**"
        Creates: "Sound travels at approximately _____" with 4 options
        """
        questions = []
        bold_pattern = re.compile(r'\*\*([^*]+)\*\*')

        for line in section.content:
            line_stripped = line.strip()

            # Only bullet points and numbered items
            if not re.match(r'^[-*\d]', line_stripped):
                continue

            matches = list(bold_pattern.finditer(line_stripped))
            if not matches:
                continue

            for match in matches:
                term = match.group(1).strip()

                if not self._is_good_term(term):
                    continue

                # Skip very short terms — they make trivial fill-in-the-blank
                if len(term) < 5:
                    continue

                # Build display line with blank
                clean_line = line_stripped.lstrip('-*0123456789. ')
                display_line = clean_line.replace(f'**{term}**', '_____', 1)
                display_line = self._clean_display(display_line)

                # Make sure the answer isn't still visible in the question
                if term.lower() in display_line.lower():
                    continue

                if len(display_line) < 25:
                    continue

                # Get distractors of similar type
                distractors = self._get_similar_distractors(term, 3, section)
                if len(distractors) < 3:
                    continue

                options = distractors + [term]
                random.shuffle(options)
                questions.append(Question(
                    type='multiple_choice',
                    question=f"Complete the statement:\n\n{display_line}",
                    answer=term,
                    options=options,
                    source_topic=section.topic,
                    source_subtopic=section.subtopic,
                ))
                break  # One question per line

        return questions

    def _extract_formula_mc(self, section) -> list:
        """
        Multiple choice: given one side of a formula, pick the other side.
        """
        questions = []
        formula_pattern = re.compile(r'\*\*(.+?=.+?)\*\*')

        for line in section.content:
            match = formula_pattern.search(line)
            if not match:
                continue

            formula = match.group(1).strip()
            parts = formula.split('=', 1)
            if len(parts) != 2:
                continue

            lhs = parts[0].strip()
            rhs = parts[1].strip()

            if len(rhs) < 3 or len(lhs) < 3:
                continue

            # Generate plausible wrong formulas
            distractors = self._get_formula_distractors(rhs, 3)
            if len(distractors) < 3:
                continue

            options = distractors + [rhs]
            random.shuffle(options)
            questions.append(Question(
                type='multiple_choice',
                question=f"Complete the formula:\n\n{lhs} = ?",
                answer=rhs,
                options=options,
                source_topic=section.topic,
                source_subtopic=section.subtopic,
                context=f"Full formula: {formula}",
            ))

        return questions

    def _extract_statement_mc(self, section) -> list:
        """
        Multiple choice: given a topic/section header, pick the correct fact.

        Distractors come from the SAME TOPIC first so they're plausible.
        Facts must pass _is_good_fact quality gate.
        """
        questions = []

        if section.level < 2 or len(section.content) < 3:
            return []

        # Collect quality-filtered facts from this section
        facts = []
        for line in section.content:
            stripped = line.strip()
            if not re.match(r'^[-*]', stripped):
                continue
            cleaned = self._clean_display(stripped)
            if self._is_good_fact(cleaned):
                facts.append(cleaned)

        if len(facts) < 2:
            return []

        header = self._clean_display(section.header)

        for fact in facts[:3]:  # Limit per section
            wrong_facts = self._get_wrong_facts(fact, section, 3)
            if len(wrong_facts) < 3:
                continue

            def truncate(s):
                return s[:117] + '...' if len(s) > 120 else s

            display_answer = truncate(fact)
            display_wrong = [truncate(w) for w in wrong_facts]

            display_options = display_wrong + [display_answer]
            random.shuffle(display_options)

            questions.append(Question(
                type='multiple_choice',
                question=f"Regarding \"{header}\", which of the following is correct?",
                answer=display_answer,
                options=display_options,
                source_topic=section.topic,
                source_subtopic=section.subtopic,
            ))

        return questions

    # ─── Helpers ──────────────────────────────────────────

    def _collect_all_facts(self) -> dict:
        """Collect quality-scored bullet-point facts, grouped by section key.

        Also builds:
          self._all_terms       — set of bold terms across all notes
          self._facts_by_topic  — {topic: [facts]} for same-topic distractors
        """
        facts_by_section = {}
        facts_by_topic = {}      # topic -> list of cleaned facts
        all_terms = set()
        bold_pattern = re.compile(r'\*\*([^*]+)\*\*')

        for note in self.notes:
            topic_facts = facts_by_topic.setdefault(note.topic, [])

            for section in note.sections:
                key = f"{note.topic}|{note.subtopic}|{section.header}"
                section_facts = []

                for line in section.content:
                    stripped = line.strip()
                    if re.match(r'^[-*]', stripped):
                        cleaned = self._clean_display(stripped)
                        if self._is_good_fact(cleaned):
                            section_facts.append(cleaned)
                            topic_facts.append(cleaned)

                    # Collect bold terms
                    for m in bold_pattern.finditer(line):
                        t = m.group(1).strip()
                        if self._is_good_term(t):
                            all_terms.add(t)

                if section_facts:
                    facts_by_section[key] = section_facts

        self._all_terms = sorted(all_terms)
        self._facts_by_topic = facts_by_topic
        return facts_by_section

    def _is_good_term(self, term: str) -> bool:
        """Check if a bold term is suitable as a quiz answer."""
        if len(term) < 3 or len(term) > 50:
            return False
        if '=' in term or '÷' in term:
            return False
        # Strip trailing colons/punctuation for matching
        check = term.rstrip(':').strip().lower()
        if check in self.SKIP_TERMS:
            return False
        # Reject terms that look like headers or labels (end with colon)
        if term.endswith(':'):
            return False
        # Reject checkbox items
        if term.startswith('[ ]') or term.startswith('[x]'):
            return False
        # Reject terms that still contain markdown
        if '**' in term or '__' in term:
            return False
        return True

    def _get_distractors(self, correct_term: str, count: int, section) -> list:
        """Get distractor terms, preferring same-topic terms for plausibility."""
        def is_valid(t):
            return (
                t.lower() != correct_term.lower()
                and correct_term.lower() not in t.lower()
                and t.lower() not in correct_term.lower()
                and len(t) >= 3
            )

        all_valid = [t for t in self._all_terms if is_valid(t)]
        if len(all_valid) < count:
            return all_valid
        return random.sample(all_valid, count)

    def _get_similar_distractors(self, correct_term: str, count: int, section) -> list:
        """
        Get distractors that are somewhat similar in nature to the correct term.
        Numbers get number distractors, text gets text distractors.
        """
        is_numeric = bool(re.search(r'\d', correct_term))

        candidates = [
            t for t in self._all_terms
            if t.lower() != correct_term.lower()
            and correct_term.lower() not in t.lower()
            and t.lower() not in correct_term.lower()
            and bool(re.search(r'\d', t)) == is_numeric
        ]

        # Fall back to all terms if not enough similar ones
        if len(candidates) < count:
            candidates = [
                t for t in self._all_terms
                if t.lower() != correct_term.lower()
                and correct_term.lower() not in t.lower()
                and t.lower() not in correct_term.lower()
            ]

        if len(candidates) < count:
            return candidates
        return random.sample(candidates, count)

    def _get_formula_distractors(self, correct_rhs: str, count: int) -> list:
        """Generate plausible wrong formula completions."""
        # Collect all formula RHS values from notes
        formula_pattern = re.compile(r'\*\*(.+?=.+?)\*\*')
        all_rhs = set()

        for note in self.notes:
            for section in note.sections:
                for line in section.content:
                    match = formula_pattern.search(line)
                    if match:
                        parts = match.group(1).split('=', 1)
                        if len(parts) == 2:
                            rhs = parts[1].strip()
                            if rhs.lower() != correct_rhs.lower() and len(rhs) >= 3:
                                all_rhs.add(rhs)

        candidates = list(all_rhs)
        if len(candidates) >= count:
            return random.sample(candidates, count)

        # If not enough real formulas, fall back to general terms
        extra = self._get_distractors(correct_rhs, count - len(candidates),
                                       None)
        return candidates + extra[:count - len(candidates)]

    def _get_wrong_facts(self, correct_fact: str, section, count: int) -> list:
        """Get plausible wrong facts, preferring the SAME TOPIC.

        This makes questions harder because the distractors are
        about related subjects rather than completely different domains.
        """
        current_key = f"{section.topic}|{section.subtopic}|{section.header}"
        correct_words = set(correct_fact.lower().split())

        def is_different_enough(fact):
            if fact.lower() == correct_fact.lower():
                return False
            fact_words = set(fact.lower().split())
            if correct_words and fact_words:
                overlap = len(correct_words & fact_words) / max(len(correct_words), len(fact_words))
                if overlap > 0.5:
                    return False
            return True

        # 1. Try same-topic, different-section facts first
        same_topic = []
        for key, facts in self.all_facts.items():
            if key == current_key:
                continue
            # Same topic?
            if key.startswith(f"{section.topic}|"):
                for fact in facts:
                    if is_different_enough(fact):
                        same_topic.append(fact)

        if len(same_topic) >= count:
            return random.sample(same_topic, count)

        # 2. Not enough same-topic — supplement with other topics
        other_topic = []
        for key, facts in self.all_facts.items():
            if key == current_key:
                continue
            if key.startswith(f"{section.topic}|"):
                continue  # already collected
            for fact in facts:
                if is_different_enough(fact):
                    other_topic.append(fact)

        combined = same_topic + other_topic
        if len(combined) < count:
            return combined
        # Prefer same-topic candidates
        if same_topic:
            n_same = min(len(same_topic), max(1, count - 1))
            n_other = count - n_same
            result = random.sample(same_topic, n_same)
            if other_topic and n_other > 0:
                result += random.sample(other_topic, min(n_other, len(other_topic)))
            return result[:count]
        return random.sample(combined, count)

    @classmethod
    def _clean_markdown(cls, text: str) -> str:
        """Remove markdown formatting and symbols from text."""
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Remove lingering markdown artefacts like  Important:**
        text = text.replace('**', '')
        return text.strip()

    @classmethod
    def _clean_display(cls, text: str) -> str:
        """Clean text for display: remove markdown, symbols, leading bullets."""
        text = cls._clean_markdown(text)
        text = cls._SYMBOLS.sub('', text)
        text = text.lstrip('-*0123456789. ')
        # Collapse double spaces left by symbol removal
        text = re.sub(r'  +', ' ', text).strip()
        return text

    @classmethod
    def _is_good_fact(cls, text: str) -> bool:
        """
        Score a cleaned fact line for quiz-worthiness.

        Good facts:
          - Are complete sentences or clauses (contain a verb-like word)
          - Contain technical terms, numbers, or comparisons
          - Are not just instructions ("click", "open", "use the")
          - Are not just titles, lists of names, or fragments
        """
        lower = text.lower()

        # Too short or too long
        if len(text) < 35 or len(text) > 200:
            return False

        # Starts with a label or header pattern  (e.g. "Note:" "Key:")
        if ':' in text[:18]:
            return False

        # Checkbox / task items
        if text.startswith(('[ ]', '[x]', '[X]')):
            return False

        # URLs
        if lower.startswith(('http', 'www')):
            return False

        # Residual markdown
        if '**' in text or '__' in text:
            return False

        # Ends with colon — it's a label/header fragment, not a complete fact
        if text.rstrip().endswith(':'):
            return False

        # Instruction-style lines ("Click File > Save", "Use the slider")
        for phrase in cls._INSTRUCTION_WORDS:
            if lower.startswith(phrase):
                return False

        # Sentence quality: should contain at least one verb-like word
        verb_indicators = (
            ' is ', ' are ', ' was ', ' were ', ' has ', ' have ',
            ' can ', ' will ', ' does ', ' do ', ' uses ', ' allows ',
            ' means ', ' provides ', ' creates ', ' requires ', ' carries ',
            ' sends ', ' receives ', ' supports ', ' ensures ', ' prevents ',
            ' determines ', ' defines ', ' enables ', ' converts ', ' measures ',
            ' occurs ', ' happens ', ' travels ', ' operates ', ' connects ',
        )
        has_verb = any(v in lower for v in verb_indicators)

        # Also accept lines with numbers/units (quantitative facts)
        has_numbers = bool(re.search(r'\d+\s*(?:ms|hz|khz|mhz|db|v|mv|m/s|ft|gbps|mbps|w|ohm|°|%)', lower))

        if not has_verb and not has_numbers:
            return False

        return True

    @staticmethod
    def check_answer(user_answer: str, correct_answer: str) -> tuple:
        """
        Evaluate a text answer with flexible matching.
        Returns (is_correct: bool, feedback_message: str)
        """
        user = user_answer.strip().lower()
        correct = correct_answer.strip().lower()
        user = re.sub(r'[*_~`]', '', user)
        correct = re.sub(r'[*_~`]', '', correct)

        if user == correct:
            return True, "Correct!"
        if len(user) > 2 and (user in correct or correct in user):
            return True, f"Correct! (Full answer: {correct_answer})"

        correct_words = set(re.split(r'\W+', correct))
        user_words = set(re.split(r'\W+', user))
        correct_words.discard('')
        user_words.discard('')

        if correct_words and user_words:
            overlap = correct_words & user_words
            ratio = len(overlap) / len(correct_words)
            if ratio >= 0.6:
                return True, f"Close enough! (Full answer: {correct_answer})"

        return False, f"The correct answer was: {correct_answer}"
