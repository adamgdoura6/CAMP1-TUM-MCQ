from flask import Flask, request, render_template_string, make_response, redirect
import json
import os
from pathlib import Path
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = 'your-secret-key'

THEMES_DIR = Path(__file__).parent / "themes"

def get_available_themes():
    """Get list of available themes from JSON files"""
    if not THEMES_DIR.exists():
        return []
    return sorted([f.stem for f in THEMES_DIR.glob("*.json")])

def load_theme_questions(theme_name):
    """Load questions from a theme JSON file"""
    theme_file = THEMES_DIR / f"{theme_name}.json"
    if not theme_file.exists():
        return []
    try:
        with open(theme_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("questions", [])
    except Exception as e:
        print(f"Error loading theme {theme_name}: {e}")
        return []

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>MCQ Checker</title>
  <style>
    * {
      color-scheme: dark;
    }
    body { 
      font-family: system-ui, Arial, sans-serif; 
      margin: 24px; 
      max-width: 900px;
      background: #0f0f0f;
      color: #e0e0e0;
    }
    h1 { color: #ffffff; }
    p { color: #b0b0b0; }
    b { color: #e0e0e0; }
    .theme-nav { 
      margin-bottom: 20px; 
      padding: 14px; 
      background: #1a1a1a; 
      border-radius: 12px;
      border: 1px solid #2d2d2d;
    }
    .theme-nav p { margin: 0 0 10px 0; }
    .theme-nav a { display: inline-block; margin-right: 8px; text-decoration: none; }
    .theme-nav button { 
      padding: 10px 16px; 
      border: 2px solid #3d3d3d; 
      border-radius: 6px; 
      background: #1f1f1f; 
      color: #e0e0e0; 
      cursor: pointer; 
      font-size: 14px; 
      transition: all 0.2s; 
    }
    .theme-nav button:hover { 
      border-color: #e0e0e0; 
      background: #2a2a2a; 
    }
    .theme-nav button.active { 
      background: #0066cc; 
      color: #fff; 
      border-color: #0066cc; 
    }
    .q { 
      padding: 14px; 
      border: 1px solid #2d2d2d; 
      border-radius: 12px; 
      margin-bottom: 14px;
      background: #1a1a1a;
    }
    .title { font-weight: 700; margin-bottom: 10px; color: #ffffff; }
    .opt { margin: 6px 0; }
    .opt label { color: #c0c0c0; }
    .opt input[type="radio"] { accent-color: #0066cc; }
    .result { margin-top: 10px; font-weight: 700; }
    .ok { color: #4ade80; }
    .bad { color: #ff6b6b; }
    .explanation { 
      margin-top: 12px; 
      padding: 10px; 
      background: #1a3a52; 
      border-left: 4px solid #0066cc; 
      color: #b0d9ff; 
      border-radius: 4px; 
      font-size: 14px; 
    }
    .score { 
      padding: 12px; 
      border-radius: 12px; 
      background: #1a1a1a; 
      margin-bottom: 18px;
      border: 1px solid #2d2d2d;
    }
    button { 
      padding: 10px 14px; 
      border: 0; 
      border-radius: 10px; 
      background: #0066cc; 
      color: #fff; 
      cursor: pointer; 
      margin-right: 8px; 
    }
    button:hover { opacity: .8; background: #0052a3; }
    .btn-delete { 
      background: #dc2626; 
      padding: 8px 12px; 
      font-size: 13px; 
      margin-left: 8px; 
    }
    .btn-delete:hover { opacity: .8; background: #b91c1c; }
    .no-questions { 
      padding: 20px; 
      background: #2d2416; 
      border-radius: 12px; 
      border: 1px solid #6b4423;
      color: #e8d5b7;
    }
    .free-answer { 
      background: #1a3a52 !important; 
      color: #b0d9ff !important; 
      border-left: 4px solid #0066cc !important; 
    }
    input[type="hidden"] { display: none; }
  </style>
</head>
<body>
  <h1>MCQ Checker</h1>
  
  <div class="theme-nav">
    <p><b>Themes:</b></p>
    {% for t in available_themes %}
      <a href="/?theme={{ t }}">
        <button type="button" class="{% if current_theme == t %}active{% endif %}">{{ t }}</button>
      </a>
    {% endfor %}
  </div>

  {% if questions %}
    <p>Select answers and submit. You'll see correctness per question.</p>

    {% for q in questions %}
      <form method="post" onsubmit="captureAllAnswers(this, '{{ current_theme }}');">
        <input type="hidden" name="theme" value="{{ current_theme }}">
        <input type="hidden" name="question_id" value="{{ q.id }}">
        <div class="q" id="{{ q.id }}">
          <div class="title">{{ loop.index }}. {{ q.text }}</div>
          
          {% if q.get('options') %}
            {# Multiple choice format #}
            {% for letter, text in q.options.items() %}
              <div class="opt">
                <label>
                  <input type="radio" name="{{ q.id }}" value="{{ letter }}"
                    {% if selected.get(q.id) == letter %}checked{% endif %}>
                  <b>{{ letter }}.</b> {{ text }}
                </label>
              </div>
            {% endfor %}

            {% if graded and selected.get(q.id) %}
              {% set user = selected.get(q.id) %}
              {% if user == q.correct %}
                <div class="result ok">✅ Correct ({{ q.correct }})</div>
              {% else %}
                <div class="result bad">❌ Wrong{% if user %} (you chose {{ user }}){% endif %}. Correct: {{ q.correct }}</div>
              {% endif %}
              {% if q.explanation %}
                <div class="explanation">{{ q.explanation }}</div>
              {% endif %}
              <form method="post" style="display: inline;">
                <input type="hidden" name="theme" value="{{ current_theme }}">
                <input type="hidden" name="delete_answer" value="{{ q.id }}">
                <input type="hidden" name="question_id" value="{{ q.id }}">
                <button type="submit" class="btn-delete">Delete answer</button>
              </form>
            {% else %}
              <button type="submit" style="margin-top: 10px;">Check answer</button>
            {% endif %}
          
          {% else %}
            {# Free-form answer format #}
            <div style="margin-top: 10px;">
              <button type="button" class="show-answer-btn" onclick="toggleAnswer('{{ q.id }}', this); saveAnswerViewed('{{ current_theme }}', '{{ q.id }}');" style="background: #0066cc;">Show Answer</button>
              <div id="ans-{{ q.id }}" class="free-answer" style="display: none; margin-top: 12px; padding: 10px; background: #f0f8ff; border-left: 4px solid #0066cc; color: #333; border-radius: 4px; font-size: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                  <div style="flex: 1;">{{ q.answer }}</div>
                  <div class="result ok" style="margin-left: 12px; white-space: nowrap;">✅ Reviewed</div>
                </div>
              </div>
            </div>
          {% endif %}
        </div>
      </form>
    {% endfor %}
  {% else %}
    <div class="no-questions">
      {% if current_theme %}
        <p>No questions found for theme "{{ current_theme }}". Please select another theme.</p>
      {% else %}
        <p>Please select a theme to get started.</p>
      {% endif %}
    </div>
  {% endif %}

  <script>
    const THEME = "{{ current_theme }}";
    const STORAGE_KEY_PREFIX = `answers_${THEME}_`;
    const VIEWED_KEY_PREFIX = `viewed_${THEME}_`;
    
    // Toggle answer visibility and hide button
    function toggleAnswer(questionId, button) {
      const ansDiv = document.getElementById(`ans-${questionId}`);
      if (ansDiv.style.display === 'none') {
        ansDiv.style.display = 'block';
        button.style.display = 'none';
      } else {
        ansDiv.style.display = 'none';
        button.style.display = 'block';
      }
    }
    
    // Save that this answer has been viewed
    function saveAnswerViewed(theme, questionId) {
      const storageKey = VIEWED_KEY_PREFIX + questionId;
      localStorage.setItem(storageKey, 'true');
    }
    
    // Capture all answers from localStorage and add them as hidden inputs before submitting
    function captureAllAnswers(form, theme) {
      // Find all radio inputs to identify all question IDs
      document.querySelectorAll('input[type="radio"]').forEach(input => {
        const storageKey = STORAGE_KEY_PREFIX + input.name;
        const savedValue = localStorage.getItem(storageKey);
        if (savedValue) {
          // Check if this input is already in the form
          let hiddenInput = form.querySelector(`input[type="hidden"][name="saved_${input.name}"]`);
          if (!hiddenInput) {
            hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = `saved_${input.name}`;
            hiddenInput.value = savedValue;
            form.appendChild(hiddenInput);
          }
        }
      });
    }
    
    // Load answers from localStorage on page load
    window.addEventListener('load', function() {
      // Restore radio button selections
      document.querySelectorAll('input[type="radio"]').forEach(input => {
        const storageKey = STORAGE_KEY_PREFIX + input.name;
        const savedValue = localStorage.getItem(storageKey);
        if (savedValue === input.value) {
          input.checked = true;
        }
      });
      
      // Restore viewed answers for free-form questions
      document.querySelectorAll('.free-answer').forEach(ansDiv => {
        const questionId = ansDiv.id.replace('ans-', '');
        const viewedKey = VIEWED_KEY_PREFIX + questionId;
        if (localStorage.getItem(viewedKey)) {
          ansDiv.style.display = 'block';
          const button = ansDiv.parentElement.querySelector('.show-answer-btn');
          if (button) {
            button.style.display = 'none';
          }
        }
      });
      
      // Find the first checked answer and scroll to it
      const checked = document.querySelector('input[type="radio"]:checked');
      if (checked) {
        const questionDiv = checked.closest('.q');
        if (questionDiv) {
          questionDiv.scrollIntoView({behavior: 'smooth', block: 'center'});
        }
      }
    });
    
    // Save answer to localStorage when radio button is selected
    document.addEventListener('change', function(e) {
      if (e.target.type === 'radio') {
        const storageKey = STORAGE_KEY_PREFIX + e.target.name;
        localStorage.setItem(storageKey, e.target.value);
      }
    });
    
    // Clear answer from localStorage when delete button is clicked
    document.addEventListener('submit', function(e) {
      const deleteAnswerInput = e.target.querySelector('input[name="delete_answer"]');
      if (deleteAnswerInput) {
        const questionId = deleteAnswerInput.value;
        const storageKey = STORAGE_KEY_PREFIX + questionId;
        const viewedKey = VIEWED_KEY_PREFIX + questionId;
        localStorage.removeItem(storageKey);
        localStorage.removeItem(viewedKey);
      }
    });
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    current_theme = request.args.get("theme", "") or request.form.get("theme", "")
    available_themes = get_available_themes()
    
    questions = []
    if current_theme:
        questions = load_theme_questions(current_theme)
    
    selected = {}
    graded = False
    response = None
    
    if request.method == "POST":
        # Check if deleting an answer
        delete_answer = request.form.get("delete_answer")
        if delete_answer:
            # Get theme from form or URL
            theme = request.form.get("theme") or request.args.get("theme", "")
            if not theme:
                theme = current_theme
            # Redirect to refresh the page without the deleted answer
            response = make_response(redirect(f"/?theme={theme}"))
            return response
        
        # Load all saved answers from the form (sent from localStorage)
        for key, value in request.form.items():
            if key.startswith('saved_'):
                q_id = key.replace('saved_', '')
                selected[q_id] = value
        
        # Check if this question was just submitted
        question_id = request.form.get("question_id")
        if question_id:
            user_choice = request.form.get(question_id)
            if user_choice:
                user_choice = user_choice.strip().upper()
                selected[question_id] = user_choice
                graded = True

    response_data = render_template_string(
        TEMPLATE,
        questions=questions,
        available_themes=available_themes,
        current_theme=current_theme,
        graded=graded,
        selected=selected,
        score=0,
        total=len(questions),
    )
    
    return response_data

if __name__ == "__main__":
    # Run: python flaskapp.py
    # For local development, use port 5000 (port 80 requires admin privileges)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
