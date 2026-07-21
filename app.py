from flask import Flask, request, jsonify, render_template, session
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'novamind-secret-key-2024'

FEEDBACK_LOG = 'feedback_log.txt'

# ============================================================
# PROMPT TEMPLATES — 3 styles per function (as per guidelines)
# ============================================================
PROMPTS = {
    'qa': [
        {
            'label': 'Simple',
            'desc': 'Short and direct. Good for quick answers.',
            'template': 'Answer this question clearly and concisely:\n\n{input}'
        },
        {
            'label': 'Detailed',
            'desc': 'Structured explanation with examples and context.',
            'template': (
                'Please provide a comprehensive answer to the following question. '
                'Include a clear explanation, relevant examples, and any important context.\n\n'
                'Question: {input}\n\n'
                'Format your response with:\n'
                '1. Direct answer\n'
                '2. Detailed explanation\n'
                '3. Relevant example(s)'
            )
        },
        {
            'label': 'Expert',
            'desc': 'Academic-level analysis with multiple perspectives.',
            'template': (
                'You are a knowledgeable expert. Provide a thorough, academic-level response '
                'to the following question. Discuss multiple perspectives, include nuanced analysis, '
                'address common misconceptions, and reference key concepts.\n\n'
                'Question: {input}\n\n'
                'Demonstrate depth of knowledge and insight in your response.'
            )
        },
    ],
    'summary': [
        {
            'label': 'Simple',
            'desc': 'Short 2-3 sentence plain-language summary.',
            'template': 'Summarize the following text in 2 to 3 simple sentences:\n\n{input}'
        },
        {
            'label': 'Detailed',
            'desc': 'Structured key points and one key takeaway.',
            'template': (
                'Provide a structured summary of the following text:\n'
                '- Main topic in one sentence\n'
                '- 4 to 6 key points as bullet points\n'
                '- One key takeaway\n\n'
                'Text:\n{input}'
            )
        },
        {
            'label': 'Expert',
            'desc': 'Critical analysis covering thesis and implications.',
            'template': (
                'Critically analyze and summarize the following text. Cover:\n'
                '1. Central argument or thesis\n'
                '2. Key evidence or supporting points\n'
                '3. Assumptions made by the author\n'
                '4. Implications or significance\n'
                '5. Any limitations or gaps\n\n'
                'Text:\n{input}'
            )
        },
    ],
    'creative': [
        {
            'label': 'Simple',
            'desc': 'Free-form. Let the AI be fully creative.',
            'template': 'Write a short creative piece about: {input}'
        },
        {
            'label': 'Detailed',
            'desc': 'Specified tone, mood, and structure.',
            'template': (
                'Write a creative piece about the following topic:\n'
                '- Topic: {input}\n'
                '- Tone: Engaging and vivid\n'
                '- Include a clear beginning, middle, and end\n'
                '- Use descriptive language and sensory imagery\n'
                '- Target length: 150 to 250 words'
            )
        },
        {
            'label': 'Expert',
            'desc': 'Literary craft with techniques, depth, and themes.',
            'template': (
                'Write a high-quality literary piece on the following theme. '
                'Employ literary devices such as metaphor, imagery, foreshadowing, and symbolism. '
                'Develop nuanced characters if applicable, build tension or emotional resonance, '
                'and ensure a clear thematic statement.\n\n'
                'Theme or Topic: {input}\n\n'
                'Target length: 200 to 350 words. Prioritize craft and literary excellence.'
            )
        },
    ],
    'advice': [
        {
            'label': 'Simple',
            'desc': 'Casual, friendly tips in everyday language.',
            'template': 'Give me some helpful tips about: {input}'
        },
        {
            'label': 'Detailed',
            'desc': 'Step-by-step plan with reasoning and caveats.',
            'template': (
                'Provide detailed, actionable advice on the following topic:\n'
                '1. Brief overview of why this matters\n'
                '2. Step-by-step recommendations (at least 5 steps)\n'
                '3. Common mistakes to avoid\n'
                '4. One key summary tip\n\n'
                'Topic: {input}'
            )
        },
        {
            'label': 'Expert',
            'desc': 'Evidence-based, considers trade-offs and context.',
            'template': (
                'As an expert advisor, provide comprehensive, evidence-based guidance on the following topic. '
                'Consider multiple perspectives and approaches, relevant trade-offs and context-dependent factors, '
                'research-backed or well-established best practices, potential challenges and how to navigate them, '
                'and tailored recommendations for different scenarios.\n\n'
                'Topic: {input}'
            )
        },
    ],
}

# ============================================================
# ROUTES
# ============================================================

@app.route('/', methods=['GET'])
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/set-key', methods=['POST'])
def set_key():
    """Save the Gemini API key to the server session."""
    data = request.get_json()
    api_key = data.get('api_key', '').strip()
    if not api_key:
        return jsonify({'error': 'No API key provided'}), 400
    session['api_key'] = api_key
    return jsonify({'status': 'ok', 'message': 'API key saved successfully'})


@app.route('/generate', methods=['POST'])
def generate():
    """
    Handle AI generation requests.
    Expects JSON: { function, style, input }
    Returns JSON: { response, prompt_used, style, function }
    """
    api_key = session.get('api_key', '')
    if not api_key:
        return jsonify({'error': 'API key not set. Please save your Gemini API key first.'}), 400

    data = request.get_json()
    fn = data.get('function', '')
    style_idx = int(data.get('style', 0))
    user_input = data.get('input', '').strip()

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    if fn not in PROMPTS:
        return jsonify({'error': 'Invalid function selected'}), 400

    if style_idx not in range(len(PROMPTS[fn])):
        style_idx = 0

    style = PROMPTS[fn][style_idx]
    prompt = style['template'].replace('{input}', user_input)

    # Call Gemini API from the Python backend
    url = (
        'https://generativelanguage.googleapis.com/v1beta/'
        'models/gemini-2.0-flash:generateContent?key=' + api_key
    )
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'temperature': 0.8, 'maxOutputTokens': 1024}
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 500

    if not resp.ok:
        try:
            err_msg = resp.json().get('error', {}).get('message', f'HTTP {resp.status_code}')
        except Exception:
            err_msg = f'HTTP {resp.status_code}'
        return jsonify({'error': err_msg}), 400

    try:
        result = resp.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        return jsonify({'error': 'Unexpected response format from Gemini API'}), 500

    return jsonify({
        'response': text,
        'prompt_used': prompt,
        'style': style['label'],
        'function': fn
    })


@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Store user feedback to feedback_log.txt.
    Expects JSON: { function, style, query, helpful }
    """
    data = request.get_json()
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'function': data.get('function', ''),
        'style': data.get('style', ''),
        'query': data.get('query', '')[:150],   # store first 150 chars
        'helpful': data.get('helpful')           # True / False
    }
    with open(FEEDBACK_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')

    return jsonify({'status': 'ok', 'message': 'Feedback saved'})


@app.route('/feedback-log', methods=['GET'])
def get_feedback_log():
    """Return all feedback entries from the log file."""
    logs = []
    if os.path.exists(FEEDBACK_LOG):
        with open(FEEDBACK_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return jsonify({'logs': logs, 'total': len(logs)})


# ============================================================
# RUN
# ============================================================
if __name__ == '__main__':
    print('\n  NovaMind AI Assistant — Flask Server')
    print('  Open your browser at: http://127.0.0.1:5000\n')
    app.run(debug=True)
