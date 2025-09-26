
# Brothers Website (Full)
Private educational Flask app for cybersecurity practice between brothers.

## Run locally
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
Open http://127.0.0.1:5000

## Deploy to Render
- Create new Web Service on Render (not Blueprint)
- Connect GitHub repo
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
