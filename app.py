import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import io

# Page Configuration
st.set_page_config(
    page_title="MindEase - Warm Wellness Companion",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern CSS Theme
st.markdown("""
<style>
    /* Main Background & Font Styling */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Glassmorphism Cards */
    div[data-testid="stMetricValue"], .css-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Modern Buttons */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.08);
        color: #F8FAFC;
        font-weight: 500;
        transition: all 0.3s ease;
        padding: 10px 20px;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #38BDF8;
        color: #0F172A;
        border-color: #38BDF8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
    }

    /* Chat Message Bubbles */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px 16px;
        margin-bottom: 12px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Custom Headers */
    h1, h2, h3 {
        color: #F1F5F9 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🌱 MindEase")
st.caption("A warm, human safe-space to share, pause, and talk through life.")

# Sidebar Controls & Safety
with st.sidebar:
    st.header("🌿 De-Stress Zone")
    enable_tts = st.checkbox("🔊 Voice Response (Speak Aloud)", value=True)
    
    st.divider()
    st.subheader("4-7-8 Breathing Technique")
    st.markdown("""
    * **Inhale** through nose (4s)
    * **Hold** breath (7s)
    * **Exhale** through mouth (8s)
    """)
    
    st.divider()
    st.warning("🚨 **Emergency Contacts**\nIf in immediate distress: **1800-599-0019** (Tele-MANAS) or local emergency services.")

# Mood Check-In Section
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
        st.toast("Logged: Feeling Stressed.")
with col4:
    if st.button("😰 Anxious"):
        st.session_state.mood_log.append("Anxious")
        st.toast("Logged: Feeling Anxious.")

st.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hey there... I'm really glad you stopped by. How are you holding up today?"}
    ]

# Fetch Gemini API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Cloud Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Humanlike System Instructions
sys_instruction = (
    "You are MindEase, a warm, genuine human friend and supportive listening companion. "
    "You were created by Ansh Kumawat. If asked who built or created you, proudly credit Ansh Kumawat. "
    "CONVERSATIONAL STYLE: Speak like an authentic, highly empathetic human friend. "
    "Use natural, conversational language. Avoid sounding like a formal AI assistant—do not use bullet points or robotic lists in chat. "
    "Keep responses conversational (2-4 sentences max per turn), validating their emotions with care and gentle curiosity. "
    "STRICT SAFETY: Never prescribe medications or offer medical diagnoses. "
    "If the user expresses severe self-harm or crisis, gently offer comforting words and remind them of local emergency care."
)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "model" else "user"):
        st.write(msg["text"])

# Multi-Modal Upload Section
st.subheader("📁 Share Voice or Notes")
uploaded_file = st.file_uploader("Upload audio notes (MP3, WAV, M4A) or documents (PDF):", type=["pdf", "mp3", "wav", "m4a"])

user_input = st.chat_input("Talk to me...")

if user_input or uploaded_file:
    prompt_text = user_input if user_input else "I uploaded something for us to look at together."
    
    st.session_state.messages.append({"role": "user", "text": prompt_text})
    with st.chat_message("user"):
        st.write(prompt_text)

    with st.chat_message("assistant"):
        with st.spinner("Here for you..."):
            input_parts = []
            
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
                    temperature=0.75,
                )
            )
            
            reply_text = response.text
            st.write(reply_text)
            st.session_state.messages.append({"role": "model", "text": reply_text})
            
            if enable_tts and reply_text:
                try:
                    tts = gTTS(text=reply_text, lang='en')
                    sound_file = io.BytesIO()
                    tts.write_to_fp(sound_file)
                    st.audio(sound_file, format='audio/mp3')
                except Exception:
                    pass
