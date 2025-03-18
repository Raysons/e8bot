from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/")
async def root():
    return {"message": "Read AI Webhook is running!"}

@app.post("/read-ai-webhook")
async def read_ai_webhook(payload: dict):
    if not DISCORD_WEBHOOK_URL:
        return {"error": "DISCORD_WEBHOOK_URL is not set"}

    # Extract data
    meeting_title = payload.get("meeting_title")
    meeting_time = payload.get("meeting_time")
    meeting_link = payload.get("meeting_link")

    if not all([meeting_title, meeting_time, meeting_link]):
        return {"error": "Missing required fields"}

    # Send to Discord
    data = {
        "content": f"📅 **New Meeting:** {meeting_title}\n🕒 {meeting_time}\n🔗 [Join Here]({meeting_link})"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        return {"status": "success", "message": "Notification sent to Discord"}
    return {"error": "Failed to send to Discord", "details": response.text}
