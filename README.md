# Adaptive Diagnostic Engine

A 1-Dimension Adaptive Testing system that dynamically selects questions based on a student's performance using Item Response Theory (IRT).

---

## Prerequisites

- Python 3.11+
- MongoDB running locally
- A free Groq API key from https://console.groq.com

---

## Setup and Installation

Clone the repository and install dependencies:
```bash
git clone https://github.com/pratyakshagarwal/HighScores_Assignment.git
pip install -r requirements.txt
```

Create a `.env` file in the root directory:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=adaptive_test
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

Seed the database with questions:
```bash
python seed_questions.py
```

Start the FastAPI backend:
```bash
uvicorn app.main:app --reload
```

In a second terminal, start the Streamlit frontend:
```bash
streamlit run frontend.py
```

Open your browser at http://localhost:8501

---

## Project Structure
```
adaptive-diagnostic-engine/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── routes.py        # API endpoints
│   ├── adaptive.py      # IRT algorithm logic
│   ├── insight.py       # Session analysis and LLM study plan
│   ├── database.py      # MongoDB connection
│   └── models.py        # Pydantic models
├── seed_questions.py              # Database seeder (50 questions)
├── frontend.py          # Streamlit UI
├── .env                 # Environment variables (not committed)
└── requirements.txt
```

---

## Adaptive Algorithm Logic

The system uses a 2-Parameter Item Response Theory (2PL IRT) model.

**Starting point:** Every student begins with an ability score of 0.5 (range 0.0 to 1.0).

**Probability of correct answer:** For each question, the probability that a student with a given ability answers correctly is calculated using the logistic function:
```
P(correct) = 1 / (1 + e ^ (-discrimination * (ability - difficulty)))
```

Where difficulty and discrimination are stored per question in MongoDB.

**Ability update after each answer:** After every response, the student's ability is updated using a gradient-based rule:
```
new_ability = ability + learning_rate * discrimination * (result - P(correct))
```

- If the student answers correctly, result = 1, so ability increases.
- If incorrect, result = 0, so ability decreases.
- The learning rate scales down for high-discrimination questions to prevent large jumps.

**Question selection:** Instead of simply picking the nearest difficulty, the system selects the question with the highest Fisher Information at the student's current ability level:
```
Information = discrimination^2 * P * (1 - P)
```

A question is most informative when P is close to 0.5, meaning the difficulty closely matches the student's ability. This is the standard approach used in Computerized Adaptive Testing (CAT).

---

## AI Log

**How AI tools were used:**

Claude was used through the development of this project as a coding assistant. The primary areas where it accelerated development were:

- Generating the initial 50 question seed data with correct difficulty, discrimination, and tags metadata across 6 topics
- Writing the LangChain prompt template and Groq integration to replace the original Ollama setup
- Adding proper error handling across all files — HTTPException usage, PyMongoError catching, and input validation

**What AI could not solve directly:**

- The ability score was always increasing regardless of wrong answers. This was a bug where the discrimination parameter was never being passed to update_ability from routes.py, so the function was silently using a wrong default. Claude identified the root cause only after being shown both files together and asked to compare the function signatures.
- Deciding to swap from Ollama to Groq required a judgment call about what would be practical for an evaluator to set up. Claude provided the options but the decision was made manually.
- Tuning the learning rate formula and the proximity penalty weight in question selection required manual testing against the live API to feel right. Claude provided the formula but the constants were adjusted by hand.

---

## API Documentation

Base URL: `http://localhost:8000/api`

### POST /start-session

Creates a new test session for a student.

Request body: none

Response:
```json
{
  "session_id": "64f1a2b3c4d5e6f7a8b9c0d1"
}
```

---

### GET /next-question/{session_id}

Returns the next best question for the student based on their current ability.

Response:
```json
{
  "question_id": "64f1a2b3c4d5e6f7a8b9c0d2",
  "question": "Solve for x: 3x + 9 = 0",
  "options": {"A": "3", "B": "-3", "C": "0", "D": "-9"},
  "difficulty": 0.2,
  "topic": "Algebra"
}
```

---

### POST /submit-answer

Submits a student's answer and updates their ability score.

Request body:
```json
{
  "session_id": "64f1a2b3c4d5e6f7a8b9c0d1",
  "question_id": "64f1a2b3c4d5e6f7a8b9c0d2",
  "answer": "B"
}
```

Response:
```json
{
  "correct": true,
  "new_ability": 0.573
}
```

---

### GET /finish-test/{session_id}

Ends the test, analyzes performance, and returns a personalized AI study plan.

Response:
```json
{
  "final_ability": 0.68,
  "ability_trajectory": [0.5, 0.53, 0.61, 0.68],
  "ability_variance": 0.004,
  "total_correct": 7,
  "total_attempted": 10,
  "max_streak": 4,
  "avg_difficulty_attempted": 0.55,
  "topic_stats": {},
  "topic_accuracy": {},
  "weak_topics": ["Vocabulary", "Arithmetic"],
  "strong_topics": ["Algebra", "Geometry"],
  "study_plan": "..."
}
```
