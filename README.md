# 🤖 AI Tutor Chatbot

## 📌 Project Overview

The **AI Tutor Chatbot** is a Generative AI-powered application developed using Python, Tkinter, and the Google Gemini API. It acts as a virtual learning assistant that helps students understand concepts through simple explanations, examples, and interactive conversations.

The application provides a user-friendly chat interface where users can ask questions and receive AI-generated responses in real time.

## ✨ Features

- **AI-Powered Responses:** Generates answers using the Google Gemini API.
- **Interactive Chat Interface:** Provides a simple graphical user interface using Tkinter.
- **Conversation Memory:** Maintains the current conversation history to support contextual follow-up questions.
- **Clear Chat:** Allows users to clear the current conversation and start a new one.
- **Error Handling:** Displays helpful messages when API requests fail.
- **Threaded API Requests:** Runs API calls in a background thread to keep the interface responsive.
- **Secure API Configuration:** Reads the API key from an environment variable instead of hardcoding it in the source code.

## 🛠️ Technologies Used

- Python
- Tkinter
- Google Gemini API
- Google Gen AI Python SDK
- Threading
- Environment Variables

## 📂 Project Structure

```text
Task5_AI_Tutor_Chatbot/
│
├── main.py
├── README.md
└── requirements.txt
```

## ⚙️ Installation and Setup

### 1. Install Python

Install Python 3.10 or a compatible version supported by the Google Gen AI SDK.

### 2. Install the Required Package

Open the terminal in the project directory and run:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the Gemini API Key

Create an API key through [Google AI Studio](https://aistudio.google.com/app/apikey).

In the VS Code PowerShell terminal, set the environment variable:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your valid API key.

**Security:** Never hardcode the API key in the source code or upload it to GitHub.

### 4. Run the Application

```bash
python main.py
```

The AI Tutor Chatbot window will open, allowing you to start asking questions.

## 💬 How to Use

1. Launch the application.
2. Enter a question in the message field.
3. Click **Send** or press Enter.
4. Read the AI-generated explanation.
5. Ask follow-up questions to continue the conversation.
6. Click **Clear Chat** to begin a new conversation.

## 🧠 Conversation Memory

The application stores conversation messages in memory while it is running. Previous messages are sent with new requests so the AI can respond to follow-up questions with relevant context.

Conversation history is temporary and is cleared when the application closes or when the user selects **Clear Chat**.

## ⚠️ Limitations

- An internet connection is required to communicate with the Gemini API.
- Responses depend on model availability, API quotas, and service availability.
- AI-generated answers may occasionally be inaccurate and should be verified when necessary.
- Conversation history is not permanently stored.

## 🚀 Future Enhancements

- Save and restore conversations between sessions.
- Add voice input and text-to-speech.
- Support multiple subjects and learning levels.
- Add quizzes and practice questions.
- Improve formatting for code snippets and mathematical explanations.

## 🎯 Learning Outcomes

This project provides practical experience with Generative AI, API integration, Python GUI development, threading, error handling, and conversation context management.

## 👩‍💻 Project Information

**Project Name:** AI Tutor Chatbot  
**Internship:** TechNova  
**Category:** Generative AI Mini Project

---

*Built as a hands-on project to explore Generative AI and create a more interactive learning experience.*
