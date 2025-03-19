from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/")
async def root():
    return {"message": "Read AI Webhook is running!"}

@app.post("/read-ai-webhook")
async def read_ai_webhook(request: Request):
    payload = await request.json()

    print("Received payload:", payload)  # Debugging
    print("Payload keys:", list(payload.keys()))  # View available keys

    if not DISCORD_WEBHOOK_URL:
        return {"error": "DISCORD_WEBHOOK_URL is not set"}

    # Ensure the webhook is triggered by a meeting ending
    if payload.get("trigger") != "meeting_end":
        return {"error": "Unsupported event type"}

    # Extract essential details
    meeting_title = payload.get("title", "Untitled Meeting")
    start_time = payload.get("start_time", "Unknown Start Time")
    end_time = payload.get("end_time", "Unknown End Time")
    summary = payload.get("summary", "No summary available.")
    report_url = payload.get("report_url", "#")

    # Participants
    participants = payload.get("participants", [])
    participant_names = ", ".join([p["name"] for p in participants]) or "No participants listed"

    # Action Items
    action_items = payload.get("action_items", [])
    action_list = "\n".join([f"- {item['text']}" for item in action_items]) or "No action items."

    # Key Questions
    key_questions = payload.get("key_questions", [])
    question_list = "\n".join([f"- {q['text']}" for q in key_questions]) or "No key questions."

    # Format the message for Discord
    message = {
        "content": (
            f"📅 **Meeting Summary: {meeting_title}**\n"
            f"🕒 **Start:** {start_time}\n"
            f"🕒 **End:** {end_time}\n"
            f"👥 **Participants:** {participant_names}\n\n"
            f"📝 **Summary:**\n{summary}\n\n"
            f"✅ **Action Items:**\n{action_list}\n\n"
            f"❓ **Key Questions:**\n{question_list}\n\n"
            f"🔗 **[Full Report]({report_url})**"
        )
    }

    # Send the message to Discord
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)

    if response.status_code == 204:
        return {"status": "success", "message": "Notification sent to Discord"}

    return {"error": "Failed to send to Discord", "details": response.text}
