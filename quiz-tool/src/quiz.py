#!/usr/bin/env python3
"""
Notes Quiz Tool — Entry Point

Finds the learning-plan directory, parses all notes, and launches the quiz GUI.

Usage:
    python3 quiz.py                          # Auto-detect notes path
    python3 quiz.py /path/to/learning-plan   # Specify notes path
"""

import sys
import os
import webbrowser
from pathlib import Path

# Ensure the src directory is on the import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notes_parser import NotesParser
from quiz_app import run_server


def find_notes_directory():
    """Auto-detect the learning-plan directory relative to this script."""
    script_dir = Path(__file__).resolve().parent

    # Try: quiz-tool/src/ → quiz-tool/ → projects/ → projects/learning-plan
    search_paths = [
        script_dir.parent / "learning-plan",          # from src/
        script_dir.parent.parent / "learning-plan",   # from quiz-tool/src/
        Path.cwd() / "learning-plan",                 # from cwd
    ]

    for path in search_paths:
        if path.exists() and path.is_dir():
            return str(path)

    return None


def main():
    # Accept an optional path argument
    if len(sys.argv) > 1:
        notes_dir = sys.argv[1]
    else:
        notes_dir = find_notes_directory()

    if not notes_dir or not Path(notes_dir).exists():
        print("Error: Could not find the learning-plan directory.")
        print()
        print("Usage:")
        print("  python quiz.py                          # auto-detect")
        print("  python quiz.py /path/to/learning-plan   # manual path")
        sys.exit(1)

    # Parse all notes
    parser = NotesParser(notes_dir)
    notes_data = parser.parse_all()

    if not notes_data:
        print(f"Error: No notes with content found in {notes_dir}")
        sys.exit(1)

    total_sections = sum(len(n.sections) for n in notes_data)
    print(f"Loaded {len(notes_data)} note files ({total_sections} sections)")

    # Launch the web server
    port = 8787
    server = run_server(notes_data, port)
    url = f"http://127.0.0.1:{port}"

    print(f"Quiz running at {url}")
    print("Press Ctrl+C to stop\n")

    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
