import streamlit as st
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import pyttsx3
import threading
import speech_recognition as sr

# --- 1. SETUP TEXT-TO-SPEECH ---
def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Audio error: {e}")

# --- 2. SETUP THE AI MODEL ---
try:
    base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=1
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)
except Exception as e:
    st.error(f"Error loading model. Did you put the 'gesture_recognizer.task' file in this folder? Error: {e}")
    st.stop()

GESTURE_MAP = {
    "Thumb_Up": "Yes",
    "Open_Palm": "Hello",
    "Victory": "Peace",
    "Closed_Fist": "Stop",
    "Pointing_Up": "One",
    "ILoveYou": "I Love You"
}

TRANSLATIONS = {
    "Yes": "Haan",
    "Hello": "Namaste",
    "Peace": "Shanti",
    "Stop": "Ruko",
    "One": "Ek",
    "I Love You": "Main tumse pyar karta hoon"
}

# --- 3. BUILD THE WEBSITE ---
st.title("🤟 AI Sign Language Translator")
st.write("**Supported Sign Language:** Indian Sign Language (ISL)")

# Sidebar (TC1)
with st.sidebar:
    st.header("Supported Signs")
    for sign in GESTURE_MAP.values():
        st.write(f"- {sign}")

# --- FORWARD ROUTE (Sign to Speech - TC2) ---
st.header("1. Sign to Text & Speech")
consent = st.checkbox("I consent to being filmed for this demonstration.")
if not consent:
    st.warning("⚠️ You must provide consent to use the camera.")
else:
    img_file = st.camera_input("Show your hand to the camera")
    if img_file is not None:
        bytes_data = img_file.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
        
        result = recognizer.recognize(mp_image)
        
        if result.gestures:
            gesture_name = result.gestures[0][0].category_name
            confidence = result.gestures[0][0].score
            
            if confidence < 0.60:
                st.error("❌ UNRECOGNIZED SIGN (TC4)")
            else:
                friendly_name = GESTURE_MAP.get(gesture_name, gesture_name)
                st.success(f"✅ Recognized: **{friendly_name}**")
                
                hindi_text = TRANSLATIONS.get(friendly_name, friendly_name)
                st.write(f"**English:** {friendly_name}")
                st.write(f"**Hindi:** {hindi_text}")
                
                if st.button("🔊 Speak English"):
                    threading.Thread(target=speak_text, args=(friendly_name,)).start()
                if st.button("🔊 Speak Hindi"):
                    threading.Thread(target=speak_text, args=(hindi_text,)).start()
        else:
            st.error("❌ UNRECOGNIZED SIGN (No hand detected)")

# --- REVERSE ROUTE (Speech to Text - TC3) ---
st.header("2. Speech to Text")
st.write("Upload a short audio clip (e.g., saying 'Hello'), and we will transcribe it.")
audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

if audio_file is not None:
    st.write("⏳ Transcribing audio...")
    
    # Save the uploaded file temporarily so the recognizer can read it
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())
        
    r = sr.Recognizer()
    try:
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = r.record(source)
            # Use Google's free STT engine to read the file
            text = r.recognize_google(audio_data)
            st.success(f"✅ Transcribed Text: **{text}**")
    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio.")
    except Exception as e:
        st.error(f"Error: {e}")