# 🤟 AI Sign Language Translator (ISL)

An AI-powered, two-way communication bridge designed to translate Indian Sign Language (ISL) gestures into text and multilingual speech, and convert spoken audio back into text.

Built for the **Ziro.Digital Agentic AI Hackathon 2026** (Partner Challenge: VerbX / IvishAI - PS 3).

## 📖 Overview

Communication barriers between the deaf/hard-of-hearing community and the hearing world are significant. This project uses computer vision and speech synthesis to create an accessible, real-time translation tool that works in both directions:
1. **Sign-to-Speech:** Recognizes a hand gesture and speaks it out loud in two languages (English & Hindi).
2. **Speech-to-Text:** Listens to an audio clip and transcribes it into text.

## ✨ Key Features

*   **Real-time Sign Recognition:** Uses Google's **MediaPipe Gesture Recognizer** to detect hand landmarks and classify supported signs.
*   **Multilingual Output:** Translates recognized signs into English and Hindi.
*   **Text-to-Speech (TTS):** Speaks the translated text out loud.
*   **Reverse Route (STT):** Uploads an audio file and transcribes it using the Google Web Speech API.
*   **Safety & Guardrails (Crucial for Hackathon):**
    *   **Consent Checkbox:** The app is locked until the user provides consent to be filmed.
    *   **Unrecognized State:** If the AI is less than 60% confident in a gesture (or sees no hand), it explicitly returns an "UNRECOGNIZED SIGN" error instead of guessing.

## 🛠️ Tech Stack

*   **Frontend:** Streamlit
*   **Computer Vision:** MediaPipe, OpenCV
*   **Speech Processing:** pyttsx3 (TTS), SpeechRecognition (STT)
*   **Language:** Python 3.15+

## 🚀 How to Run Locally

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt