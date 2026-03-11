# Aria AI Assistant

Aria AI Assistant is a simple AI chatbot web application built with FastAPI and Google's Gemini API.

The app provides a web interface where users can ask questions and receive AI-generated responses.

## Features

- FastAPI backend
- Gemini AI integration
- Simple browser-based chat interface
- Deployable on Railway
- Environment variable support for API keys

## Technologies

- Python
- FastAPI
- Uvicorn
- Google Gemini API
- HTML + JavaScript

## Installation

Clone the repository:

git clone https://github.com/Iankahambwe/ai-chatbot.git

Navigate to the project:

cd ai-chatbot

Install dependencies:

pip install -r requirements.txt

## Environment Variable

Set your Gemini API key:

Windows PowerShell

$env:GEMINI_API_KEY="your_api_key_here"

Linux / Mac

export GEMINI_API_KEY="your_api_key_here"

## Run the App

Start the FastAPI server:

python -m uvicorn main:app --reload

Open the app in your browser:

http://127.0.0.1:8000

## Deployment

The project can be deployed on Railway using:

- requirements.txt
- railway.json

## Author

Ian Kahambwe