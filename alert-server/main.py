import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
from typing import List

app = FastAPI()

# Allow CORS for local development (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUBS_FILE = os.path.join(os.path.dirname(__file__), 'subscriptions.json')

class SubscribeRequest(BaseModel):
    email: EmailStr


def save_subscription(email: str):
    subs = []
    if os.path.exists(SUBS_FILE):
        with open(SUBS_FILE, 'r', encoding='utf-8') as f:
            try:
                subs = json.load(f)
            except Exception:
                subs = []
    if email not in subs:
        subs.append(email)
        with open(SUBS_FILE, 'w', encoding='utf-8') as f:
            json.dump(subs, f, indent=2)


def send_confirmation_email(to_email: str):
    host = os.getenv('ALERT_SMTP_HOST')
    port = int(os.getenv('ALERT_SMTP_PORT', '587'))
    user = os.getenv('ALERT_SMTP_USER')
    password = os.getenv('ALERT_SMTP_PASS')
    from_addr = os.getenv('ALERT_FROM')

    if not (host and user and password and from_addr):
        raise RuntimeError('SMTP credentials are not fully set in environment variables')

    msg = EmailMessage()
    msg['Subject'] = 'Subscription confirmed'
    msg['From'] = from_addr
    msg['To'] = to_email
    msg.set_content(f"You have been subscribed to the alert system. We'll send alerts to {to_email}.")

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)


@app.post('/subscribe')
async def subscribe(req: SubscribeRequest):
    email = req.email
    try:
        save_subscription(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # If ALERT_DEV is set, skip sending emails (useful for local development)
    if os.getenv('ALERT_DEV'):
        return {"status": "ok", "email": email, "note": "dev mode - email not sent"}

    try:
        send_confirmation_email(email)
    except Exception as e:
        # don't fail if email sending fails, but report it
        raise HTTPException(status_code=500, detail=f"Saved but failed to send email: {e}")

    return {"status": "ok", "email": email}
