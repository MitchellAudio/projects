"""
Web-based Quiz GUI using Python's built-in http.server.

Serves a single-page application that handles all quiz interaction
in the browser. Communicates with the Python backend via JSON API endpoints.
"""

import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from question_generator import QuestionGenerator


# ─── HTML/CSS/JS Single-Page App ─────────────────────────

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Notes Quiz Tool</title>
<style>
  :root {
    --bg: #F5F6FA; --card: #FFFFFF; --primary: #2C3E50;
    --accent: #3498DB; --success: #27AE60; --error: #E74C3C;
    --warning: #E67E22; --text: #2C3E50; --text-light: #7F8C8D;
    --border: #DCE1E8; --highlight: #EBF5FB;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
         background: var(--bg); color: var(--text); min-height: 100vh; }

  .container { max-width: 780px; margin: 0 auto; padding: 32px 24px; }

  /* ── Home Screen ── */
  .home { text-align: center; padding-top: 80px; }
  .home h1 { font-size: 2.2rem; color: var(--primary); margin-bottom: 6px; }
  .home .subtitle { color: var(--text-light); font-size: 1rem; margin-bottom: 32px; }

  .count-select { display: flex; justify-content: center; align-items: center;
                  gap: 10px; margin-bottom: 32px; flex-wrap: wrap; }
  .count-select label { color: var(--text); font-size: 0.95rem; }
  .count-select input[type="radio"] { display: none; }
  .count-select .chip { padding: 6px 16px; border-radius: 20px; cursor: pointer;
    background: var(--card); border: 2px solid var(--border); font-size: 0.95rem;
    transition: all 0.15s; }
  .count-select input:checked + .chip { background: var(--accent); color: white;
    border-color: var(--accent); }

  .btn { display: inline-block; width: 100%; max-width: 320px; padding: 14px 24px;
    border: none; border-radius: 8px; font-size: 1.05rem; font-weight: 600;
    cursor: pointer; transition: opacity 0.15s; margin: 5px auto; }
  .btn:hover { opacity: 0.88; }
  .btn-accent { background: var(--accent); color: white; }
  .btn-primary { background: var(--primary); color: white; }
  .btn-success { background: var(--success); color: white; }
  .btn-error { background: var(--error); color: white; }
  .btn-small { max-width: 180px; padding: 10px 20px; font-size: 0.95rem; }
  .btn-ghost { background: none; color: var(--accent); font-size: 0.9rem;
    padding: 8px; max-width: none; width: auto; border: none; cursor: pointer; }

  .stats { color: var(--text-light); font-size: 0.85rem; margin-top: 28px; }
  .btn-stack { display: flex; flex-direction: column; align-items: center; }

  /* ── Selection Screen ── */
  .sel-header { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
  .sel-header h2 { font-size: 1.4rem; color: var(--primary); }
  .sel-list { background: var(--card); border: 1px solid var(--border);
    border-radius: 8px; max-height: 440px; overflow-y: auto; margin-bottom: 16px; }
  .sel-group { font-size: 0.85rem; font-weight: 700; color: var(--text-light);
    padding: 14px 20px 4px; }
  .sel-item { display: flex; align-items: center; padding: 12px 20px;
    border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.1s; }
  .sel-item:hover { background: var(--highlight); }
  .sel-item:last-child { border-bottom: none; }
  .sel-item input { margin-right: 14px; width: 18px; height: 18px; accent-color: var(--accent); }
  .sel-item label { cursor: pointer; flex: 1; font-size: 1rem; }
  .sel-item .count { color: var(--text-light); font-size: 0.85rem; }

  /* ── Quiz Screen ── */
  .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
  .top-bar .progress-text { color: var(--text-light); font-size: 0.9rem; }
  .top-bar .score { font-weight: 700; font-size: 0.95rem; color: var(--primary); }
  .progress-bar { width: 100%; height: 6px; background: var(--border); border-radius: 3px;
    margin-bottom: 16px; overflow: hidden; }
  .progress-bar .fill { height: 100%; background: var(--accent); border-radius: 3px;
    transition: width 0.3s ease; }

  .badge { display: inline-block; padding: 4px 12px; border-radius: 4px; font-size: 0.75rem;
    font-weight: 700; color: white; text-transform: uppercase; letter-spacing: 0.5px; }
  .badge-recall { background: var(--warning); }
  .badge-fill { background: var(--accent); }
  .badge-mc { background: var(--primary); }

  .source { color: var(--text-light); font-size: 0.8rem; margin: 6px 0 12px; }
  .q-card { background: var(--card); border: 1px solid var(--border); border-radius: 8px;
    padding: 20px 24px; margin-bottom: 16px; white-space: pre-wrap; line-height: 1.6;
    font-size: 1.05rem; }

  .answer-area { margin-bottom: 14px; }

  /* Fill-in-blank input */
  .fb-row { display: flex; gap: 10px; }
  .fb-input { flex: 1; padding: 12px 16px; font-size: 1.05rem; border: 2px solid var(--border);
    border-radius: 8px; outline: none; transition: border 0.15s; font-family: inherit; }
  .fb-input:focus { border-color: var(--accent); }
  .fb-input:disabled { background: #f8f8f8; }
  .fb-input.correct { border-color: var(--success); background: #E8F8F5; }
  .fb-input.wrong { border-color: var(--error); background: #FDEDEC; }

  /* Multiple choice */
  .mc-option { display: block; width: 100%; text-align: left; padding: 14px 20px;
    background: var(--card); border: 2px solid var(--border); border-radius: 8px;
    font-size: 1rem; cursor: pointer; margin-bottom: 8px; transition: all 0.15s;
    font-family: inherit; }
  .mc-option:hover:not(:disabled) { border-color: var(--accent); background: var(--highlight); }
  .mc-option:disabled { cursor: default; }
  .mc-option.correct { border-color: var(--success); background: #E8F8F5; color: var(--success);
    font-weight: 600; }
  .mc-option.wrong { border-color: var(--error); background: #FDEDEC; color: var(--error); }

  /* Flashcard */
  .fc-reveal { width: 100%; padding: 14px; background: var(--card); border: 2px solid var(--border);
    border-radius: 8px; cursor: pointer; font-size: 1rem; color: var(--accent);
    font-weight: 600; transition: all 0.15s; font-family: inherit; }
  .fc-reveal:hover { border-color: var(--accent); background: var(--highlight); }
  .fc-answer { background: var(--highlight); border: 1px solid var(--border); border-radius: 8px;
    padding: 16px 20px; white-space: pre-wrap; line-height: 1.5; font-size: 0.95rem;
    margin-bottom: 14px; max-height: 250px; overflow-y: auto; }
  .fc-rate { display: flex; justify-content: center; gap: 14px; }

  /* Feedback */
  .feedback { padding: 12px 16px; border-radius: 8px; font-weight: 600;
    font-size: 0.95rem; margin-bottom: 14px; display: none; white-space: pre-wrap; }
  .feedback.correct { display: block; background: #E8F8F5; color: var(--success); }
  .feedback.wrong { display: block; background: #FDEDEC; color: var(--error); }
  .feedback.info { display: block; background: #FEF5E7; color: var(--warning); }

  .bottom-bar { display: flex; justify-content: space-between; align-items: center; }

  /* ── Results Screen ── */
  .results { text-align: center; padding-top: 60px; }
  .results .emoji { font-size: 3.5rem; margin-bottom: 10px; }
  .results h1 { font-size: 2rem; color: var(--primary); margin-bottom: 14px; }
  .results .final-score { font-size: 1.15rem; color: var(--text); margin-bottom: 4px; }
  .results .percent { font-size: 3.2rem; font-weight: 800; margin-bottom: 6px; }
  .results .message { color: var(--text-light); margin-bottom: 36px; font-size: 1rem; }
  .results .btn-row { display: flex; justify-content: center; gap: 14px; }

  .screen { display: none; }
  .screen.active { display: block; }
</style>
</head>
<body>
<div class="container">

  <!-- HOME -->
  <div id="home" class="screen active home">
    <h1>Notes Quiz Tool</h1>
    <p class="subtitle">Test your knowledge from your learning notes</p>

    <div class="count-select">
      <label>Questions:</label>
      <input type="radio" name="qcount" id="q5" value="5"><label for="q5" class="chip">5</label>
      <input type="radio" name="qcount" id="q10" value="10"><label for="q10" class="chip">10</label>
      <input type="radio" name="qcount" id="q15" value="15" checked><label for="q15" class="chip">15</label>
      <input type="radio" name="qcount" id="q20" value="20"><label for="q20" class="chip">20</label>
    </div>

    <div class="btn-stack">
      <button class="btn btn-accent" onclick="startAll()">Quiz All Notes</button>
      <button class="btn btn-primary" onclick="showSelection('topic')">Quiz by Topic</button>
      <button class="btn btn-primary" onclick="showSelection('section')">Quiz by Section</button>
    </div>
    <p class="stats" id="stats"></p>
  </div>

  <!-- SELECTION -->
  <div id="selection" class="screen selection">
    <div class="sel-header">
      <button class="btn-ghost" onclick="showScreen('home')">&larr; Back</button>
      <h2 id="sel-title">Select Topics</h2>
    </div>
    <div class="sel-list" id="sel-list"></div>
    <button class="btn btn-accent" onclick="startSelected()">Start Quiz &rarr;</button>
  </div>

  <!-- QUIZ -->
  <div id="quiz" class="screen quiz">
    <div class="top-bar">
      <span class="progress-text" id="prog-text">Question 1 / 15</span>
      <span class="score" id="score-text">Score: 0 / 0</span>
    </div>
    <div class="progress-bar"><div class="fill" id="prog-fill"></div></div>

    <span class="badge" id="q-badge">RECALL</span>
    <p class="source" id="q-source"></p>
    <div class="q-card" id="q-text"></div>
    <div class="answer-area" id="answer-area"></div>
    <div class="feedback" id="feedback"></div>
    <div class="bottom-bar">
      <button class="btn-ghost" onclick="showScreen('home')">&larr; Quit</button>
      <button class="btn btn-accent btn-small" id="next-btn" style="display:none"
              onclick="nextQuestion()">Next &rarr;</button>
    </div>
  </div>

  <!-- RESULTS -->
  <div id="results" class="screen results">
    <div class="emoji" id="res-emoji"></div>
    <h1>Quiz Complete!</h1>
    <p class="final-score" id="res-score"></p>
    <p class="percent" id="res-percent"></p>
    <p class="message" id="res-msg"></p>
    <div class="btn-row">
      <button class="btn btn-accent btn-small" onclick="retryQuiz()">Try Again</button>
      <button class="btn btn-primary btn-small" onclick="showScreen('home')">Home</button>
    </div>
  </div>

</div>

<script>
/* State */
let quizData = null;
let questions = [];
let currentIdx = 0;
let score = 0;
let answered = 0;
let selMode = '';
let answeredCurrent = false;

/* Init */
fetch('/api/info').then(r => r.json()).then(d => {
  quizData = d;
  document.getElementById('stats').textContent =
    d.total_files + ' note files across ' + d.total_topics + ' topics';
});

/* Screens */
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

/* Home */
function getCount() {
  const r = document.querySelector('input[name="qcount"]:checked');
  return r ? parseInt(r.value) : 15;
}

function startAll() {
  fetch('/api/quiz?mode=all&count=' + getCount())
    .then(r => r.json()).then(qs => beginQuiz(qs));
}

/* Selection */
function showSelection(mode) {
  selMode = mode;
  document.getElementById('sel-title').textContent =
    mode === 'topic' ? 'Select Topics' : 'Select Sections';

  const list = document.getElementById('sel-list');
  list.innerHTML = '';

  if (mode === 'topic') {
    quizData.topics.forEach(t => {
      list.innerHTML += selItem(t.name, t.name, t.count + ' note files');
    });
  } else {
    let curTopic = '';
    quizData.subtopics.forEach(s => {
      if (s.topic !== curTopic) {
        curTopic = s.topic;
        list.innerHTML += '<div class="sel-group">' + escHtml(curTopic) + '</div>';
      }
      list.innerHTML += selItem(s.topic + '|' + s.subtopic, s.subtopic, '');
    });
  }
  showScreen('selection');
}

function selItem(value, label, extra) {
  return '<div class="sel-item" onclick="this.querySelector(\'input\').click()">' +
    '<input type="checkbox" value="' + escAttr(value) + '" onclick="event.stopPropagation()">' +
    '<label>' + escHtml(label) + '</label>' +
    (extra ? '<span class="count">' + escHtml(extra) + '</span>' : '') + '</div>';
}

function startSelected() {
  const checked = [...document.querySelectorAll('#sel-list input:checked')].map(i => i.value);
  if (!checked.length) return;
  const params = 'mode=' + selMode + '&count=' + getCount() +
    '&selected=' + encodeURIComponent(checked.join(','));
  fetch('/api/quiz?' + params).then(r => r.json()).then(qs => beginQuiz(qs));
}

/* Quiz */
function beginQuiz(qs) {
  questions = qs;
  currentIdx = 0;
  score = 0;
  answered = 0;
  if (!questions.length) { alert('No questions could be generated from the selected notes.'); return; }
  displayQuestion();
  showScreen('quiz');
}

function displayQuestion() {
  answeredCurrent = false;
  const q = questions[currentIdx];
  const total = questions.length;

  document.getElementById('prog-text').textContent =
    'Question ' + (currentIdx + 1) + ' / ' + total;
  document.getElementById('prog-fill').style.width =
    ((currentIdx / total) * 100) + '%';
  document.getElementById('score-text').textContent =
    'Score: ' + score + ' / ' + answered;

  const badge = document.getElementById('q-badge');
  if (q.type === 'flashcard')      { badge.textContent = 'RECALL';           badge.className = 'badge badge-recall'; }
  else if (q.type === 'fill_blank') { badge.textContent = 'FILL IN THE BLANK'; badge.className = 'badge badge-fill'; }
  else                              { badge.textContent = 'MULTIPLE CHOICE';  badge.className = 'badge badge-mc'; }

  document.getElementById('q-source').textContent =
    q.source_topic + '  /  ' + q.source_subtopic;
  document.getElementById('q-text').textContent = q.question;
  document.getElementById('feedback').className = 'feedback';
  document.getElementById('feedback').textContent = '';
  document.getElementById('next-btn').style.display = 'none';

  const area = document.getElementById('answer-area');
  area.innerHTML = '';

  if (q.type === 'flashcard')       buildFlashcard(q, area);
  else if (q.type === 'fill_blank') buildFillBlank(q, area);
  else if (q.type === 'multiple_choice') buildMC(q, area);
}

/* Flashcard */
function buildFlashcard(q, area) {
  const btn = document.createElement('button');
  btn.className = 'fc-reveal';
  btn.textContent = 'Show Answer';
  btn.onclick = function() { revealFlashcard(q, area); };
  area.appendChild(btn);
}

function revealFlashcard(q, area) {
  area.innerHTML = '';
  const ans = document.createElement('div');
  ans.className = 'fc-answer';
  ans.textContent = q.answer;
  area.appendChild(ans);

  const rate = document.createElement('div');
  rate.className = 'fc-rate';

  const gotBtn = document.createElement('button');
  gotBtn.className = 'btn btn-success btn-small';
  gotBtn.textContent = 'I Got It';
  gotBtn.onclick = function() { rateFC(true); };

  const missBtn = document.createElement('button');
  missBtn.className = 'btn btn-error btn-small';
  missBtn.textContent = 'I Missed It';
  missBtn.onclick = function() { rateFC(false); };

  rate.appendChild(gotBtn);
  rate.appendChild(missBtn);
  area.appendChild(rate);
}

function rateFC(got) {
  if (answeredCurrent) return;
  answeredCurrent = true;
  answered++;
  if (got) { score++; showFeedback('Nice one!', 'correct'); }
  else { showFeedback('Keep studying this one!', 'info'); }
  updateScore();
  document.getElementById('next-btn').style.display = '';
}

/* Fill in the Blank */
function buildFillBlank(q, area) {
  const row = document.createElement('div');
  row.className = 'fb-row';

  const inp = document.createElement('input');
  inp.className = 'fb-input';
  inp.id = 'fb-input';
  inp.placeholder = 'Type your answer...';

  const btn = document.createElement('button');
  btn.className = 'btn btn-accent btn-small';
  btn.textContent = 'Submit';
  btn.onclick = function() { checkFB(q); };

  inp.addEventListener('keydown', function(e) { if (e.key === 'Enter') checkFB(q); });

  row.appendChild(inp);
  row.appendChild(btn);
  area.appendChild(row);

  setTimeout(function() { inp.focus(); }, 100);
}

function checkFB(q) {
  if (answeredCurrent) return;
  const inp = document.getElementById('fb-input');
  const val = inp.value.trim();
  if (!val) return;
  answeredCurrent = true;
  answered++;
  inp.disabled = true;

  fetch('/api/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_answer: val, correct_answer: q.answer })
  }).then(r => r.json()).then(res => {
    if (res.correct) {
      score++;
      inp.classList.add('correct');
      showFeedback(res.message, 'correct');
    } else {
      inp.classList.add('wrong');
      showFeedback(res.message, 'wrong');
    }
    if (q.context) {
      const fb = document.getElementById('feedback');
      fb.textContent += '\n' + q.context;
    }
    updateScore();
    document.getElementById('next-btn').style.display = '';
  });
}

/* Multiple Choice */
function buildMC(q, area) {
  q.options.forEach(function(opt, i) {
    const btn = document.createElement('button');
    btn.className = 'mc-option';
    btn.textContent = opt;
    btn.onclick = function() { checkMC(q, i); };
    area.appendChild(btn);
  });
}

function checkMC(q, idx) {
  if (answeredCurrent) return;
  answeredCurrent = true;
  answered++;
  const btns = document.querySelectorAll('.mc-option');
  btns.forEach(function(b, i) {
    b.disabled = true;
    if (q.options[i] === q.answer) b.classList.add('correct');
    else if (i === idx) b.classList.add('wrong');
  });
  if (q.options[idx] === q.answer) {
    score++;
    showFeedback('Correct!', 'correct');
  } else {
    showFeedback('The correct answer was: ' + q.answer, 'wrong');
  }
  updateScore();
  document.getElementById('next-btn').style.display = '';
}

/* Navigation */
function nextQuestion() {
  currentIdx++;
  if (currentIdx >= questions.length) showResults();
  else displayQuestion();
}

/* Results */
function showResults() {
  const pct = answered > 0 ? Math.round((score / answered) * 100) : 0;
  document.getElementById('res-score').textContent = 'Score: ' + score + ' / ' + answered;
  document.getElementById('res-percent').textContent = pct + '%';

  let emoji, color, msg;
  if (pct >= 90)      { emoji = '\u2B50'; color = 'var(--success)'; msg = 'Outstanding! You really know your stuff!'; }
  else if (pct >= 70) { emoji = '\uD83C\uDF89'; color = 'var(--success)'; msg = 'Great job! Keep it up!'; }
  else if (pct >= 50) { emoji = '\uD83D\uDCAA'; color = 'var(--warning)'; msg = 'Good effort! Review the topics you missed.'; }
  else                { emoji = '\uD83D\uDCDA'; color = 'var(--error)'; msg = 'Keep studying \u2014 you\'ll get there!'; }

  document.getElementById('res-emoji').textContent = emoji;
  document.getElementById('res-percent').style.color = color;
  document.getElementById('res-msg').textContent = msg;
  showScreen('results');
}

function retryQuiz() {
  questions.sort(function() { return Math.random() - 0.5; });
  currentIdx = 0; score = 0; answered = 0;
  displayQuestion();
  showScreen('quiz');
}

/* Helpers */
function showFeedback(text, cls) {
  const fb = document.getElementById('feedback');
  fb.textContent = text;
  fb.className = 'feedback ' + cls;
}
function updateScore() {
  document.getElementById('score-text').textContent = 'Score: ' + score + ' / ' + answered;
}
function escHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
function escAttr(s) {
  return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
}
</script>
</body>
</html>
"""


class QuizHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the quiz API and page."""

    notes_data = None
    generator = None

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == '/' or path == '/index.html':
            self._serve_page()
        elif path == '/api/info':
            self._serve_info()
        elif path == '/api/quiz':
            self._serve_quiz(params)
        else:
            self._send_json({'error': 'not found'}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/check':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            self._check_answer(body)
        else:
            self._send_json({'error': 'not found'}, 404)

    # ── Page ──

    def _serve_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(PAGE_HTML.encode('utf-8'))

    # ── API: Info ──

    def _serve_info(self):
        notes = self.notes_data
        topics = {}
        subtopics = []
        seen = set()

        for n in notes:
            topics[n.topic] = topics.get(n.topic, 0) + 1
            key = (n.topic, n.subtopic)
            if key not in seen:
                seen.add(key)
                subtopics.append({'topic': n.topic, 'subtopic': n.subtopic})

        self._send_json({
            'total_files': len(notes),
            'total_topics': len(topics),
            'topics': [{'name': k, 'count': v} for k, v in sorted(topics.items())],
            'subtopics': sorted(subtopics, key=lambda x: (x['topic'], x['subtopic'])),
        })

    # ── API: Generate Quiz ──

    def _serve_quiz(self, params):
        mode = params.get('mode', ['all'])[0]
        count = int(params.get('count', ['15'])[0])
        selected = params.get('selected', [''])[0].split(',')
        selected = [s.strip() for s in selected if s.strip()]

        gen = self.generator

        if mode == 'all':
            questions = gen.generate_all(count)
        elif mode == 'topic':
            sections = []
            for note in self.notes_data:
                if note.topic in selected:
                    sections.extend(note.sections)
            questions = gen.generate_from_sections(sections, count)
        elif mode == 'section':
            sections = []
            for key in selected:
                parts = key.split('|', 1)
                if len(parts) == 2:
                    topic, subtopic = parts
                    for note in self.notes_data:
                        if note.topic == topic and note.subtopic == subtopic:
                            sections.extend(note.sections)
            questions = gen.generate_from_sections(sections, count)
        else:
            questions = []

        self._send_json([{
            'type': q.type,
            'question': q.question,
            'answer': q.answer,
            'options': q.options,
            'source_topic': q.source_topic,
            'source_subtopic': q.source_subtopic,
            'context': q.context,
        } for q in questions])

    # ── API: Check Answer ──

    def _check_answer(self, body):
        correct, message = QuestionGenerator.check_answer(
            body.get('user_answer', ''),
            body.get('correct_answer', ''))
        self._send_json({'correct': correct, 'message': message})

    # ── Helpers ──

    def _send_json(self, data, code=200):
        payload = json.dumps(data).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        """Suppress request logging to keep terminal clean."""
        pass


def run_server(notes_data, port=8787):
    """Start the quiz web server and return the server instance."""
    generator = QuestionGenerator(notes_data)

    QuizHandler.notes_data = notes_data
    QuizHandler.generator = generator

    server = HTTPServer(('127.0.0.1', port), QuizHandler)
    return server
