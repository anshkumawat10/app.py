import streamlit as st
from google import genai
from google.genai import types

# Page setup for soft, soothing layout
st.set_page_config(page_title="MindEase - Wellness Companion", page_icon="🌱", layout="wide")

# App Header
st.title("🌱 MindEase")
st.caption("A safe, calm space to pause, reflect, and unpack your thoughts.")

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

if st.session_state.mood_log:
    st.caption(f"Logged check-ins today: {len(st.session_state.mood_log)} | Latest: {st.session_state.mood_log[-1]}")

st.divider()

# Sidebar for Resources
with st.sidebar:
    st.header("🌿 De-Stress Zone")
    st.subheader("4-7-8 Breathing Technique")
    st.markdown("""
    - **Inhale** through your nose for 4s
    - **Hold** your breath for 7s
    - **Exhale** slowly through mouth for 8s
    """)
    
    st.divider()
    st.warning("🚨 **Emergency Contacts**\nIf you are in immediate crisis, reach out to professional support: **1800-599-0019** (Tele-MANAS) or local health services.")

# ALWAYS INITIALIZE MESSAGES BEFORE THE API KEY CHECK
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hello there. I'm here for you. How are you feeling today?"}
    ]

# REPLACE WITH THIS:
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

if api_key:
    client = genai.Client(api_key=api_key)
    
    sys_instruction = (
        "You are MindEase, a gentle, highly empathetic, and supportive mental wellness listening companion. "
        "You were created and developed by Ansh Kumawat. "
        "If anyone asks who made you, created you, or built you, proudly tell them you were created by Ansh Kumawat. "
        "Your goal is to offer compassionate active listening and non-judgmental guidance. "
        "Do not offer medical diagnoses or prescriptions. Keep your responses comforting, concise, and encouraging."
    )

    # Render existing conversation
    for msg in st.session_state.messages:
        with st.chat_message("assistant" if msg["role"] == "model" else "user"):
            st.write(msg["text"])

    if user_input := st.chat_input("Share what's on your mind..."):
        st.session_state.messages.append({"role": "user", "text": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Listening..."):
                contents = [
                    types.Content(
                        role=m["role"],
                        parts=[types.Part.from_text(text=m["text"])]
                    ) for m in st.session_state.messages
                ]
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_instruction,
                        temperature=0.7,
                    )
                )
                
                st.write(response.text)
                st.session_state.messages.append({"role": "model", "text": response.text})
else:
    st.info("Please enter your Gemini API key above to start using the chatbot.")
