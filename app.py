# app.py

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from openai import OpenAI
import os
from dotenv import load_dotenv

from summarizer import summarize_text

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY environment variable not set.")

# Retrieve the API key from environment variables.
# Ensure you set OPENAI_API_KEY in your environment before running.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Initialize the client
client = OpenAI(api_key=api_key)

# Rate limiter to prevent abuse (example: 10 requests/minute per IP)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

load_dotenv()  # This loads the .env file

@app.route('/')
def home():
    # Render a template called 'index.html' located in the 'templates' folder
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
@limiter.limit("5 per minute")  # Additional limit for this endpoint
def summarize():
    text_content = request.form.get('text_content', '').strip()

    if not text_content:
        flash('Please enter text to summarize.', 'error')
        return redirect(url_for('home'))

    try:
        summary = summarize_text(text_content, client)
        flash('Text summarized successfully!', 'success')
        return jsonify({"summary": summary})
    except Exception as e:
        flash('Error while summarizing text: {}'.format(str(e)), 'error')
        return jsonify({"error": str(e)}), 500

    
# For local testing with `python app.py`, you can uncomment the block below.
# Otherwise, Gunicorn will automatically detect 'app' as the WSGI callable.
# kick update3

# if __name__ == "__main__":
#    # Debug mode for development. Disable in production.
#    app.run(debug=True)


