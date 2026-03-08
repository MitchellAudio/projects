# Quiz Tool

A GUI quiz application that generates questions from your markdown learning notes and tests your knowledge with instant feedback.

## Features

- **Three quiz modes:**
  - **All Notes** — pulls questions from every note file
  - **By Topic** — select one or more topics (e.g., Tech, Electrics, Software)
  - **By Section** — select specific subtopics (e.g., Time alignment, Impedance)
- **Three question types:**
  - **Definition Match** — given a description, pick the correct term
  - **Complete the Statement** — pick the missing key term from a statement
  - **Which is Correct?** — pick the true fact about a given topic
- **Browser-based GUI** — opens automatically in your default browser (no install required)
- **Instant feedback** with colour-coded correct/incorrect indicators
- **Score tracking** throughout the quiz with a results summary at the end
- **Configurable question count** (5, 10, 15, or 20 per quiz)

## Usage

```bash
# From the project root
python3 quiz-tool/src/quiz.py

# Or from inside the quiz-tool directory
cd quiz-tool
python3 src/quiz.py

# Or specify a custom notes path
python3 src/quiz.py /path/to/learning-plan

# Stop the server (works from any terminal window)
pkill -f "quiz-tool/src/quiz.py"
```

## Requirements

- Python 3.8+

No external dependencies — the tool uses only the Python standard library and serves a browser-based UI on `http://127.0.0.1:8787`.

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
    ├── quiz.py                 # Entry point — starts server and opens browser
    ├── notes_parser.py         # Finds and parses markdown notes
    ├── question_generator.py   # Generates questions from parsed content
    └── quiz_app.py             # Web server (browser-based SPA via http.server)
```

id like to add a bit of question tracking if wrong or if i want to flag something 