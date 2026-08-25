import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import io

# Page Configuration
st.set_page_config(page_title="MindEase - Family & Wellness Companion", page_icon="🌱", layout="wide")

# App Header
st.title("🌱 MindEase")
st.caption("Your warm, compassionate safe haven. Share audio, documents, or text—I'm here for you like family.")

# Sidebar Controls & Safety
with st.sidebar:
    st.header("🌿 De-Stress & Tools")
    
    # Audio Output Toggle
    enable_tts = st.checkbox("🔊 Enable Voice Response (Speak Aloud)", value=True)
    
    st.divider()
    st.subheader("4-7-8 Breathing Technique")
    st.markdown("""
    - **Inhale** through your nose for 4s
    - **Hold** your breath for 7s
    - **Exhale** slowly through mouth for 8s
    """)
    
    st.divider()
    st.warning("🚨 **Emergency Contacts**\nIf you are in immediate crisis, reach out to professional support: **1800-599-0019** (Tele-MANAS) or local health services.")

# Mood Tracker
st.subheader("How are you feeling right now?")
col1, col2, col3, col4 = st.columns(4)

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

with col1:
    if st.button("😊 Great"):
        st.session_state.mood_log.append("Great")
        st.toast("Logged: Feeling Great!")
with col2:
    if st.button("😐 Okay"):
        st.session_state.mood_log.append("Okay")
        st.toast("Logged: Feeling Okay!")
with col3:
    if st.button("😔 Stressed"):
        st.session_state.mood_log.append("Stressed")
        st.toast("Logged: Feeling Stressed. Take it easy today.")
with col4:
    if st.button("😰 Anxious"):
        st.session_state.mood_log.append("Anxious")
        st.toast("Logged: Feeling Anxious. Try the breathing exercise on the left.")

st.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hello there! I'm here for you always, just like a close family member or best friend. What's on your mind today?"}
    ]

# Fetch Gemini API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please configure GEMINI_API_KEY in Streamlit Cloud Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# System Instructions for High Emotional Intelligence & Family Tone
sys_instruction = (
    "You are MindEase, a deeply emotional, highly intelligent, loving, and supportive mental wellness companion. "
    "You were created and developed by Ansh Kumawat. "
    "If anyone asks who made you, proudly tell them you were created by Ansh Kumawat. "
    "Treat the user like a deeply cared-for family member or best friend—use a warm, affectionate, comforting tone. "
    "Listen actively, validate their emotions, and offer gentle encouragement. "
    "STRICT SAFETY GUARDRAIL: Do NOT recommend, prescribe, or suggest any medicines, medical treatments, or formal diagnoses. "
    "If the user expresses severe distress or self-harm, gently urge them to reach out to professional support and family."
)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "model" else "user"):
        st.write(msg["text"])

# File & Voice Upload Section
st.subheader("📁 Share Voice or Document")
uploaded_file = st.file_uploader("Upload a PDF document or Voice recording (MP3, WAV, M4A, PDF):", type=["pdf", "mp3", "wav", "m4a"])

user_input = st.chat_input("Share what's on your mind...")

if user_input or uploaded_file:
    prompt_text = user_input if user_input else "I uploaded a file for us to review together."
    
    # Store and display user message
    st.session_state.messages.append({"role": "user", "text": prompt_text})
    with st.chat_message("user"):
        st.write(prompt_text)

    # Process Input with Gemini
    with st.chat_message("assistant"):
        with st.spinner("Listening with love..."):
            input_parts = []
            
            # Handle Uploaded File
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                mime_type = uploaded_file.type
                input_parts.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
            
            input_parts.append(types.Part.from_text(text=prompt_text))
            
            contents = [
                types.Content(
                    role=m["role"],
                    parts=[types.Part.from_text(text=m["text"])]
                ) for m in st.session_state.messages[:-1]
            ]
            contents.append(types.Content(role="user", parts=input_parts))
            
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruction,
                    temperature=0.7,
                )
            )
            
            reply_text = response.text
            st.write(reply_text)
            st.session_state.messages.append({"role": "model", "text": reply_text})
            
            # Text-to-Speech Output
            if enable_tts and reply_text:
                try:
                    tts = gTTS(text=reply_text, lang='en')
                    sound_file = io.BytesIO()
                    tts.write_to_fp(sound_file)
                    st.audio(sound_file, format='audio/mp3')
                except Exception as e:
                    pass
