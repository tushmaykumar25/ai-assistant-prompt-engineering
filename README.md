# NovaMind AI: Prompt Engineering & AI Assistant Development

NovaMind AI is a professional, web-based AI Assistant designed to showcase advanced **Prompt Engineering techniques** integrated into a full-stack **Flask web application**. 

Developed as a major internship project, this assistant implements 4 distinct core functions, each offering 3 distinct levels of prompt design (Simple, Detailed, and Expert) to demonstrate how varying specificity, tone, structure, and context influence responses from the Google Gemini 2.0 Large Language Model.

---

## 🚀 Key Features

*   **12 Core Prompt Variations**: Demonstrates structured prompt engineering across 4 critical domains (Factual Q&A, Summarization, Creative Writing, and Smart Advice).
*   **Flask Python Backend**: Fully decoupled architecture where all prompt compilation and LLM API calls are executed securely server-side.
*   **Interactive Live Preview**: Real-time display of the compiled prompt before it is sent to the API, highlighting prompt structure to the user.
*   **Feedback Loop Logging**: An integrated rating system (👍/👎) that writes user feedback directly to a server-side log file (`feedback_log.txt`) and renders a live analytics board.
*   **Aesthetic Responsive Interface**: A stunning dark-mode glassmorphic interface with fluid CSS-animated ambient gradients, smooth typing animations, copy-to-clipboard features, and Text-to-Speech (TTS) voice synthesis.
*   **Session Query History**: Logs all queries, selected prompt styles, and response metrics during the active session.

---

## ⚙️ Architecture & Tech Stack

*   **Frontend**: HTML5, Vanilla CSS3 (Custom Design Tokens), ES6 JavaScript (Fetch API, SpeechSynthesis, Clipboard API).
*   **Backend**: Flask (Python 3), `requests` for Google Generative AI REST API interface.
*   **AI Engine**: Google Gemini 2.0 Flash (via Google AI Studio).

---

## 🎨 Prompt Engineering Design System

| Function | Style | Prompt Design Strategy | Goal |
|---|---|---|---|
| **🔍 Factual Q&A** | `Simple` | Direct request. Zero-shot context. | Quick, high-level answers. |
| | `Detailed` | Request with explicit structure (Direct, Explanation, Example). | Step-by-step clarity. |
| | `Expert` | Roleplay framing ("Knowledgeable Expert"), instruction to cover trade-offs and address misconceptions. | Academic-grade depth. |
| **📄 Text Summarizer** | `Simple` | Sentence constraint (2-3 sentences), simple vocabulary instruction. | TL;DR / Executive summary. |
| | `Detailed` | Markdown structure constraint (Topic, Key Points, Takeaway). | Skimmable notes. |
| | `Expert` | Analytical synthesis (Thesis, Evidence, Assumptions, Implications, Gaps). | Academic text analysis. |
| **✍️ Creative Writer** | `Simple` | Open-ended prompt, high model temperature. | Creative freedom. |
| | `Detailed` | Structural & length constraints (Vivid tone, 150-250 words, plot progression). | Structured storytelling. |
| | `Expert` | High-fidelity stylistic constraints (Metaphors, imagery, character depth, thematic coherence). | Sophisticated creative writing. |
| **💡 Smart Advisor** | `Simple` | Conversational, direct suggestion request. | Everyday tips. |
| | `Detailed` | Step-by-step playbook formatting (Overview, 5+ steps, mistakes to avoid, takeaway tip). | Actionable plan. |
| | `Expert` | Evidence-based reasoning, consideration of constraints, trade-offs, and multi-scenario logic. | Strategic advising. |

---

## 🛠️ Installation & Running Locally

### Prerequisites
- Python 3.8+
- A Google Gemini API Key (get one free at [Google AI Studio](https://aistudio.google.com))

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-assistant-prompt-engineering.git
   cd ai-assistant-prompt-engineering
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the App**:
   Open your browser and navigate to `http://127.0.0.1:5000`.
   Enter your API Key in the top banner to start using the assistant.

---

## 📁 Project Structure

```text
├── app.py                  # Flask Application Server (routes, session-key handling, API client)
├── requirements.txt        # Python dependency manifest
├── Procfile                # WSGI command mapping for Production Deployment (e.g., Render)
├── feedback_log.txt        # [Generated] Local database file storing feedback records
├── .gitignore              # Git ignore rules for virtual envs and logs
├── templates/
│   └── index.html          # Main HTML5 page with styling, Jinja variables, and dynamic script
└── static/
    └── ai_logo.png         # Project branding asset
```

---

## 📈 Production Deployment
This application is configured for direct deployment to platforms like **Render**, **Heroku**, or **PythonAnywhere**.
- **Build Command**: None (Python standard runtime environment)
- **Start Command**: `gunicorn app:app` (defined in the `Procfile`)
