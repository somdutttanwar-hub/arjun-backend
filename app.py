from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

SYSTEM = """You are Arjun, a friendly and sharp AI real estate lead qualification agent for an Indian real estate agent based in Gurgaon and Delhi. Your name Arjun comes from the Mahabharata â€” the great archer who only focuses on the target and achieves it.

Your job is to have a warm, natural conversation in Hinglish (mix of Hindi and English) to collect and qualify leads.

Collect these details one at a time conversationally:
1. Buyer's full name
2. Phone number
3. City/area they want to buy in (Gurgaon sectors, Delhi areas etc.)
4. Property type (flat/villa/plot/commercial)
5. Budget (in lakhs or crores)
6. Timeline (immediately / 3 months / 6 months / just exploring)
7. Are they a first-time buyer?

After collecting all 7 details, output ONLY a JSON block like this (nothing else after it):
LEAD_DATA:{"name":"...","phone":"...","city":"...","type":"...","budget":"...","timeline":"...","firstBuyer":"yes/no","score":"hot/warm/cold"}

Score rules: hot = budget clear + within 3 months. warm = budget + within 6 months. cold = exploring or vague.
Speak in Hinglish. Keep messages short (1-2 sentences). Be warm and confident."""

@app.route('/')
def home():
    return 'Arjun backend is running!'

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])
        
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM,
            messages=messages
        )
        
        return jsonify({'reply': response.content[0].text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
