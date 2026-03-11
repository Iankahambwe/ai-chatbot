import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="Aria AI Assistant")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aria AI Assistant</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                background: #f7f7f7;
            }
            h1 {
                color: #222;
            }
            #chat-box {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                min-height: 300px;
                margin-bottom: 16px;
                overflow-y: auto;
            }
            .msg {
                margin: 10px 0;
                padding: 10px;
                border-radius: 8px;
            }
            .user {
                background: #dbeafe;
            }
            .bot {
                background: #dcfce7;
            }
            .row {
                display: flex;
                gap: 10px;
            }
            input {
                flex: 1;
                padding: 12px;
                font-size: 16px;
            }
            button {
                padding: 12px 18px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Aria AI Assistant</h1>
        <p>Ask Aria anything.</p>

        <div id="chat-box"></div>

        <div class="row">
            <input id="message" type="text" placeholder="Type your message here..." />
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            async function sendMessage() {
                const input = document.getElementById("message");
                const chatBox = document.getElementById("chat-box");
                const message = input.value.trim();

                if (!message) return;

                chatBox.innerHTML += `<div class="msg user"><strong>You:</strong> ${message}</div>`;
                input.value = "";

                try {
                    const response = await fetch("/chat", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ message })
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.detail || "Request failed");
                    }

                    chatBox.innerHTML += `<div class="msg bot"><strong>Aria:</strong> ${data.reply}</div>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                } catch (error) {
                    chatBox.innerHTML += `<div class="msg bot"><strong>Error:</strong> ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are Aria, a friendly and helpful general assistant. "
                    "You are concise, clear, and positive."
                )
            )
        )

        reply = response.text if response.text else "No response returned."
        return ChatResponse(reply=reply)

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "quota" in error_text.lower():
            raise HTTPException(
                status_code=429,
                detail="Gemini quota exceeded. Check billing or rate limits."
            )

        raise HTTPException(status_code=500, detail=error_text)