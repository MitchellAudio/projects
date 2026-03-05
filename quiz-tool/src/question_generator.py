"""
Generate quiz questions from parsed note sections.

Extracts multiple choice questions from markdown content:
- Definition matching: term ↔ description
- Fact questions: key statements with the bold term as the answer
- Formula questions: complete the formula from options
- Statement questions: true/false style from bullet point facts
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

            # Clean markdown from description and make sure it doesn't contain the answer
            desc_clean = self._clean_markdown(desc)
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

                # Build display line with blank
                clean_line = line_stripped.lstrip('-*0123456789. ')
                display_line = clean_line.replace(f'**{term}**', '_____', 1)
                display_line = self._clean_markdown(display_line)

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
        Multiple choice: ask about facts stated in the notes using
        the section header as context.

        Uses bullet points that state a clear fact and turns them into
        "According to the notes on [topic], which of the following is true?"
        """
        questions = []

        if section.level < 2 or len(section.content) < 3:
            return []

        # Collect clean bullet-point facts from this section
        facts = []
        for line in section.content:
            stripped = line.strip()
            if not re.match(r'^[-*]', stripped):
                continue
            cleaned = stripped.lstrip('-* ')
            cleaned = self._clean_markdown(cleaned)
            if len(cleaned) < 30 or len(cleaned) > 200:
                continue
            if ':' in cleaned[:15]:
                continue
            if cleaned.startswith(('[ ]', '[x]', 'http', 'www')):
                continue
            if '**' in cleaned:
                continue
            facts.append(cleaned)

        if len(facts) < 2:
            return []

        # Pick facts from this section and pair with wrong facts from other sections
        header = self._clean_markdown(section.header)

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
        """Collect bullet-point facts from all notes, grouped by section key."""
        facts_by_section = {}
        all_terms = set()
        bold_pattern = re.compile(r'\*\*([^*]+)\*\*')

        for note in self.notes:
            for section in note.sections:
                key = f"{note.topic}|{note.subtopic}|{section.header}"
                section_facts = []

                for line in section.content:
                    stripped = line.strip()
                    if re.match(r'^[-*]', stripped):
                        cleaned = stripped.lstrip('-* ')
                        cleaned = self._clean_markdown(cleaned)
                        if len(cleaned) < 30 or len(cleaned) > 200:
                            pass
                        elif ':' in cleaned[:15]:
                            pass
                        elif cleaned.startswith(('[ ]', '[x]', 'http', 'www')):
                            pass
                        elif '**' in cleaned:
                            pass
                        else:
                            section_facts.append(cleaned)

                    # Collect bold terms
                    for m in bold_pattern.finditer(line):
                        t = m.group(1).strip()
                        if self._is_good_term(t):
                            all_terms.add(t)

                if section_facts:
                    facts_by_section[key] = section_facts

        self._all_terms = sorted(all_terms)
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
        """Get distractor terms from the collected bold terms."""
        candidates = [
            t for t in self._all_terms
            if t.lower() != correct_term.lower()
            and correct_term.lower() not in t.lower()
            and t.lower() not in correct_term.lower()
        ]
        if len(candidates) < count:
            return candidates
        return random.sample(candidates, count)

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
        """Get facts from other sections to use as wrong answers."""
        current_key = f"{section.topic}|{section.subtopic}|{section.header}"
        candidates = []

        for key, facts in self.all_facts.items():
            if key == current_key:
                continue
            for fact in facts:
                # Make sure it's different enough from the correct answer
                if fact.lower() == correct_fact.lower():
                    continue
                # Check word overlap isn't too high (would be confusing)
                correct_words = set(correct_fact.lower().split())
                fact_words = set(fact.lower().split())
                if correct_words and fact_words:
                    overlap = len(correct_words & fact_words) / max(len(correct_words), len(fact_words))
                    if overlap > 0.5:
                        continue
                candidates.append(fact)

        if len(candidates) < count:
            return candidates
        return random.sample(candidates, count)

    @staticmethod
    def _clean_markdown(text: str) -> str:
        """Remove markdown formatting from text."""
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        return text.strip()

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
