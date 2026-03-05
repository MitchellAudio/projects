"""
Parse markdown notes files into structured data for quiz generation.

Scans the learning-plan directory, finds all notes.md files, and parses
them into sections with metadata (topic, subtopic, headers, content).
"""

import re
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class NoteSection:
    """A section within a note file, defined by a markdown header."""
    header: str
    level: int
    content: list = field(default_factory=list)
    file_path: str = ""
    topic: str = ""
    subtopic: str = ""


@dataclass
class NoteFile:
    """A parsed note file with its metadata and sections."""
    file_path: str
    topic: str
    subtopic: str
    sections: list = field(default_factory=list)


class NotesParser:
    """Finds and parses markdown note files from the learning-plan directory."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def find_note_files(self) -> list:
        """Recursively find all notes.md files and extract topic/subtopic metadata."""
        note_files = []

        for notes_path in sorted(self.base_path.rglob("notes.md")):
            rel = notes_path.relative_to(self.base_path)
            parts = rel.parts

            # Extract topic (parent category) and subtopic (specific subject)
            # e.g., Tech/Time-alignment/notes.md → topic="Tech", subtopic="Time alignment"
            if len(parts) >= 3:
                topic = parts[0]
                subtopic = parts[1].replace('-', ' ').replace('_', ' ')
            elif len(parts) >= 2:
                topic = parts[0].replace('-', ' ').replace('_', ' ')
                subtopic = topic
            else:
                topic = "General"
                subtopic = "General"

            note_files.append({
                'path': str(notes_path),
                'topic': topic,
                'subtopic': subtopic,
            })

        return note_files

    def parse_file(self, file_path: str, topic: str, subtopic: str) -> NoteFile:
        """Parse a single markdown file into a NoteFile with sections."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except (IOError, UnicodeDecodeError):
            return NoteFile(file_path=file_path, topic=topic, subtopic=subtopic)

        sections = []
        current_section = None
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

        for line in lines:
            line = line.rstrip('\n')
            match = header_pattern.match(line)

            if match:
                level = len(match.group(1))
                header_text = match.group(2).strip()
                current_section = NoteSection(
                    header=header_text,
                    level=level,
                    content=[],
                    file_path=file_path,
                    topic=topic,
                    subtopic=subtopic,
                )
                sections.append(current_section)
            elif current_section is not None:
                # Add content lines, skipping leading blank lines
                if line.strip() or current_section.content:
                    current_section.content.append(line)

        # Remove trailing blank lines from each section
        for section in sections:
            while section.content and not section.content[-1].strip():
                section.content.pop()

        return NoteFile(
            file_path=file_path,
            topic=topic,
            subtopic=subtopic,
            sections=sections,
        )

    def parse_all(self) -> list:
        """Find and parse all note files. Returns only files with actual content."""
        note_files = self.find_note_files()
        parsed = []

        for nf in note_files:
            note = self.parse_file(nf['path'], nf['topic'], nf['subtopic'])

            # Skip files with no content or only placeholder text
            has_content = False
            for section in note.sections:
                content_text = ' '.join(section.content)
                if section.content and 'Add your notes' not in content_text:
                    has_content = True
                    break

            if has_content:
                parsed.append(note)

        return parsed

    @staticmethod
    def get_topics(notes: list) -> list:
        """Get sorted list of unique topic names."""
        return sorted(set(n.topic for n in notes))

    @staticmethod
    def get_subtopics(notes: list) -> list:
        """Get list of unique (topic, subtopic) pairs with file paths."""
        subtopics = []
        seen = set()

        for n in notes:
            key = (n.topic, n.subtopic)
            if key not in seen:
                seen.add(key)
                subtopics.append({
                    'topic': n.topic,
                    'subtopic': n.subtopic,
                    'path': n.file_path,
                })

        return sorted(subtopics, key=lambda x: (x['topic'], x['subtopic']))
