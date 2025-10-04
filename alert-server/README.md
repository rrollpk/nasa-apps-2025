Alert server

Run:

Set environment variables:
- ALERT_SMTP_HOST
- ALERT_SMTP_PORT
- ALERT_SMTP_USER
- ALERT_SMTP_PASS
- ALERT_FROM

Install deps: pip install -r requirements.txt
Run: uvicorn main:app --reload --port 8000

Endpoints:
- POST /subscribe {"email": "user@example.com"}
  - validates email, saves to subscriptions.json and sends a confirmation email
