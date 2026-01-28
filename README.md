# MCQ Checker - Medical Imaging Question Bank

A Flask-based web application for managing and testing multiple-choice questions and free-form answer questions on medical imaging topics. Features a dark mode UI with local storage support for saving answers.

## Features

- 🌙 **Dark Mode Interface** - Modern, comfortable dark theme for extended studying sessions
- 📚 **Multiple Themes** - Organize questions by topics (CT, MRI, PET, Ultrasound, etc.)
- ✅ **Instant Feedback** - Get immediate correctness indicators for multiple-choice questions
- 💾 **Local Storage** - Automatically saves your answers in the browser
- 📝 **Free-form Answers** - Support for both multiple-choice and short-answer questions
- 🎯 **Answer Explanations** - Detailed explanations for each question
- 📊 **Answer Management** - Delete and modify your answers easily

## Project Structure

```
CAMP1-TUM-MCQ/
├── flaskapp.py              # Main Flask application
├── themes/                  # Question theme files (JSON format)
│   ├── 2_xrays.json
│   ├── 3_ct.json
│   ├── 6_MRI.json
│   ├── 9_us.json
│   └── simulation.json      # Medical imaging questions
├── README.md               # This file
└── requirements.txt        # Python dependencies (optional)
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project**
   ```bash
   cd CAMP1-TUM-MCQ
   ```

2. **Install Flask**
   ```bash
   pip install flask
   ```

3. **Create a requirements.txt (optional)**
   ```bash
   echo flask > requirements.txt
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python flaskapp.py
   ```

2. **Open your browser**
   - Navigate to `http://127.0.0.1` (or `http://localhost`)
   - The app will run on port 80

3. **Select a theme** and start answering questions

## Usage Guide

### Selecting a Theme
- Click on any theme button at the top to load questions from that theme
- Themes correspond to different medical imaging topics

### Answering Questions

**Multiple Choice Questions:**
- Select an answer option (A, B, C, D, etc.)
- Click "Check answer" to submit
- Get instant feedback with correct/incorrect indicator
- View the explanation if available

**Free-form Answer Questions:**
- Click "Show Answer" to reveal the correct answer
- The answer is displayed in a blue information box

### Managing Answers
- Your answers are automatically saved locally in your browser
- Click "Delete answer" to clear a specific answer
- Answers persist across page refreshes (within the same theme)

## JSON Theme Format

Each theme file should follow this structure:

```json
{
  "questions": [
    {
      "id": "unique_id",
      "text": "Question text here?",
      "options": {
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      },
      "correct": "A",
      "explanation": "Explanation for why A is correct..."
    },
    {
      "id": "free_form_id",
      "text": "Free-form question?",
      "answer": "Expected answer or explanation"
    }
  ]
}
```

### Question Types

1. **Multiple Choice** (with `options` field)
   - Must have: `id`, `text`, `options`, `correct`
   - Optional: `explanation`

2. **Free-form/Short Answer** (without `options` field)
   - Must have: `id`, `text`, `answer`

## Features in Detail

### Dark Mode
- Eye-friendly dark background (#0f0f0f)
- High contrast text for readability
- Color-coded feedback:
  - 🟢 Green for correct answers
  - 🔴 Red for incorrect answers
  - 🔵 Blue for explanations and information

### Local Storage
- Answers are saved automatically when you select them
- Viewed free-form answers are remembered
- Storage is theme-specific (answers for different themes don't mix)

### Answer Explanations
- Detailed explanations appear after answering multiple-choice questions
- Helps understand the reasoning behind correct answers

## Development

### Modifying the App

**Add a new theme:**
1. Create a new JSON file in the `themes/` directory
2. Follow the JSON format above
3. The app will automatically detect it

**Customize styling:**
- Edit the CSS in the `<style>` section of the HTML template in `flaskapp.py`
- Dark mode colors can be adjusted there

## Troubleshooting

**Port 80 is already in use:**
- Edit `flaskapp.py` and change the port number:
  ```python
  app.run(host="127.0.0.1", port=5000, debug=True)  # Use port 5000 instead
  ```

**Questions not loading:**
- Ensure JSON files are in the `themes/` directory
- Validate JSON format with a JSON validator
- Check the Flask console for error messages

**Answers not saving:**
- Check if browser allows localStorage (may need to enable in privacy settings)
- Try a different browser
- Clear browser cache and try again

## Browser Compatibility

- Chrome/Chromium: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Edge: ✅ Full support
- IE11: ⚠️ Limited support (dark mode may not work)

## Tips for Best Experience

1. **Use a modern browser** for optimal dark mode rendering
2. **Keep the window open** while studying to prevent losing unsaved changes
3. **Review explanations** even for correct answers to deepen understanding
4. **Delete wrong answers** and retry to test your learning
5. **Take screenshots** of explanations if you want to review later

## Future Enhancements

Potential features for future versions:
- ☐ Progress tracking and statistics
- ☐ Multiple-choice answer shuffling
- ☐ Bookmarking difficult questions
- ☐ Export answers as PDF
- ☐ User authentication and cloud sync
- ☐ Time limits for exams
- ☐ Question search and filtering

## License

This project is for educational purposes.

## Support

For issues or questions, check the Flask console output for error messages or review the JSON theme files for proper formatting.

---

**Last Updated:** January 2026
