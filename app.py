import random
import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(
    page_title="MindEase - Your Gentle AI Buddy",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cute, Soft Ambient Glassmorphism Theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1A1C3B 40%, #2A1B3D 100%);
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Adorable Mascot Header Frame */
    .ai-cute-header {
        display: flex;
        align-items: center;
        gap: 18px;
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(244, 114, 182, 0.3);
        border-radius: 24px;
        padding: 18px 24px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(244, 114, 182, 0.15);
    }

    .ai-cute-avatar {
        width: 68px;
        height: 68px;
        border-radius: 50%;
        background: linear-gradient(135deg, #F472B6 0%, #FB923C 50%, #38BDF8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        box-shadow: 0 0 20px rgba(244, 114, 182, 0.5);
        animation: floatCute 3s ease-in-out infinite alternate;
    }

    @keyframes floatCute {
        0% { transform: translateY(0px) rotate(-3deg); box-shadow: 0 0 16px rgba(244, 114, 182, 0.4); }
        100% { transform: translateY(-6px) rotate(3deg); box-shadow: 0 0 26px rgba(56, 189, 248, 0.6); }
    }

    /* Warm Interactive Buttons */
    .stButton > button {
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.08);
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 500;
        padding: 12px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #F472B6 0%, #38BDF8 100%);
        color: #0F172A;
        border-color: transparent;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(244, 114, 182, 0.35);
    }

    /* Soft Chat Bubbles */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        padding: 14px 18px;
        margin-bottom: 12px;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.92);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    h1, h2, h3 { color: #F8FAFC !important; }
</style>
""", unsafe_allow_html=True)

# Cute Mascot Header
st.markdown("""
<div class="ai-cute-header">
    <div class="ai-cute-avatar">🌸</div>
    <div>
        <h2 style="margin:0; font-size: 1.6rem; color: #F472B6 !important;">MindEase • Your Comfort Companion ✨</h2>
        <p style="margin:0; opacity: 0.85; font-size: 0.95rem;">Always here to listen, support, and help • Created with ❤️ by <b>Ansh Kumawat</b></p>
    </div>
</div>
""", unsafe_allow_html=True)

# API Key Validation
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing! Please configure GEMINI_API_KEY in Streamlit Cloud Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Sidebar Options
with st.sidebar:
    st.markdown("### 🐾 Companion Settings")
    selected_model = st.selectbox(
        "Select Engine Speed:",
        options=["gemini-3.6-flash", "gemini-3.1-pro"],
        format_func=lambda x: "⚡ Flash (Ultra Fast)" if "flash" in x else "🧠 Pro (Deep Empathy)"
    )
    st.divider()
    st.header("🌿 De-Stress Corner")
    st.subheader("4-7-8 Comfort Breathing")
    st.markdown("""
    * **Inhale** gently (4s) 🌸
    * **Hold** softly (7s) 🌿
    * **Exhale** completely (8s) ✨
    """)
    st.divider()
    st.warning("🚨 **Need Immediate Help?**\nIf you are in severe distress, reach out: **1800-599-0019** (Tele-MANAS)")

# Cute Mood Check-In Section
st.subheader("How are you feeling right now? 💖")
col1, col2, col3, col4 = st.columns(4)

if "current_mood" not in st.session_state:
    st.session_state.current_mood = "Neutral"

with col1:
    if st.button("😊 Radiant & Happy"):
        st.session_state.current_mood = "Radiant & Happy"
        st.toast("Logged: Feeling radiant! Let's celebrate! 🌟")

with col2:
    if st.button("🌿 Peaceful & Calm"):
        st.session_state.current_mood = "Peaceful & Calm"
        st.toast("Logged: A peaceful mind is a gift. 🍵")

with col3:
    if st.button("😔 Tired & Stressed"):
        st.session_state.current_mood = "Tired & Stressed"
        st.toast("Logged: Sending warm hugs. Take it easy today. 🧸")

with col4:
    if st.button("😰 Anxious & Uneasy"):
        st.session_state.current_mood = "Anxious & Uneasy"
        st.toast("Logged: I'm right here with you. Take a slow breath. 🫁")

st.divider()

# Session Chat Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hi there! 🌸 I'm MindEase, your cozy companion. Whether you want to share how your day went, vent, talk through a problem, or ask a question—I'm listening with all my heart!"}
    ]

# Render Messages with Cute Icons
for msg in st.session_state.messages:
    avatar_icon = "🌸" if msg["role"] == "model" else "✨"
    with st.chat_message("assistant" if msg["role"] == "model" else "user", avatar=avatar_icon):
        st.write(msg["text"])

# Multi-Input Bar
col_mic, col_attach, col_input = st.columns([2, 1, 9])

with col_mic:
    voice_input = st.audio_input("Record Voice", key="voice_recorder", label_visibility="collapsed")

with col_attach:
    with st.popover("📎"):
        uploaded_file = st.file_uploader("Share document or image", type=["pdf", "png", "jpg", "jpeg"], key="doc_uploader")

with col_input:
    user_text = st.chat_input("Tell me what's on your mind... 💭")

# Build Inputs
user_prompt = user_text
input_parts = []
has_attachment = False

if voice_input:
    input_parts.append(types.Part.from_bytes(data=voice_input.read(), mime_type="audio/wav"))
    user_prompt = user_prompt or "🎤 Sent a voice message."
    has_attachment = True

if uploaded_file:
    input_parts.append(types.Part.from_bytes(data=uploaded_file.read(), mime_type=uploaded_file.type))
    user_prompt = user_prompt or f"📄 Uploaded document: {uploaded_file.name}"
    has_attachment = True

if user_text:
    input_parts.append(types.Part.from_text(text=user_text))

# Execute Response
if user_prompt or has_attachment:
    st.session_state.messages.append({"role": "user", "text": user_prompt})
    with st.chat_message("user", avatar="✨"):
        st.write(user_prompt)

    with st.chat_message("assistant", avatar="🌸"):
        with st.spinner("Listening with care... ✨"):
            # System Prompt explicitly engineered for deep empathy & tone matching
            sys_instruction = (
                "You are MindEase, a cute, warm, ultra-intelligent, and deeply empathetic AI companion created by Ansh Kumawat. "
                "If asked who built or created you, state explicitly that you were created by Ansh Kumawat. "
                f"CURRENT USER MOOD CONTEXT: '{st.session_state.current_mood}'. "
                "TONE RULES: "
                "1. Read the user's emotional state carefully from their words, voice note, or mood check-in. "
                "2. Adapt your tone dynamically: use soft, gentle, and comforting words when they feel anxious or stressed; use cheerful, warm, and uplifting energy when they are happy; use clear, encouraging guidance when they need practical help. "
                "3. Always validate their feelings first before offering solutions or insights. "
                "4. Sprinkle warm, cute emojis (like 🌸, ✨, 🧸, 🌿, ☕, 🐾) naturally—do not overdo it, but keep the vibe cozy and inviting. "
                "5. Keep responses concise, supportive, and human-like (2-4 sentences per turn unless analyzing a document)."
            )

            contents = [
                types.Content(
                    role=m["role"],
                    parts=[types.Part.from_text(text=m["text"])]
                ) for m in st.session_state.messages[:-1]
            ]
            
            if user_text and not has_attachment:
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_text)]))
            else:
                contents.append(types.Content(role="user", parts=input_parts))

            response = client.models.generate_content(
                model=selected_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruction,
                    temperature=0.7,
                )
            )

            reply_text = response.text
            st.write(reply_text)
            st.session_state.messages.append({"role": "model", "text": reply_text})
