# Quiz Tool

A GUI quiz application that generates questions from your markdown learning notes and tests your knowledge with instant feedback.

## Features

- **Three quiz modes:**
  - **All Notes** — pulls questions from every note file
  - **By Topic** — select one or more topics (e.g., Tech, Electrics, Software)
  - **By Section** — select specific subtopics (e.g., Time alignment, Impedance)
- **Three question types:**
  - **Recall (Flashcard)** — read a concept prompt, try to recall the answer, then reveal and self-rate
  - **Fill in the Blank** — type the missing key term from a statement
  - **Multiple Choice** — pick the correct term from four options
- **Instant feedback** with colour-coded correct/incorrect indicators
- **Score tracking** throughout the quiz with a results summary at the end
- **Configurable question count** (5, 10, 15, or 20 per quiz)
- **Flexible answer checking** — case-insensitive, partial matches accepted

## Usage

```bash
# From the project root
python quiz-tool/src/quiz.py

# Or from inside the quiz-tool directory
cd quiz-tool
python src/quiz.py

# Or specify a custom notes path
python src/quiz.py /path/to/learning-plan

pkill -f "python3 quiz-tool/src/quiz.py"
```

## Requirements

- Python 3.8+
- Tkinter (included with Python on macOS and most Linux distributions)

No external dependencies — the tool uses only the Python standard library.

## How It Works

1. **Parses** all `notes.md` files found recursively in the `learning-plan/` directory
2. **Extracts** questions from markdown patterns:
   - Bold terms with definitions (`**Term** — description`)
   - Bold terms in context (creates fill-in-the-blank)
   - Section headers with content (creates recall/flashcard prompts)
   - Formulas (`**X = Y**` creates formula completion questions)
3. **Presents** shuffled questions in a clean GUI with instant feedback
4. **Scores** your performance and gives a summary at the end

## Project Structure

```
quiz-tool/
├── README.md
├── requirements.txt
└── src/
    ├── quiz.py                 # Entry point
    ├── notes_parser.py         # Finds and parses markdown notes
    ├── question_generator.py   # Generates questions from parsed content
    └── quiz_app.py             # Tkinter GUI application
```
