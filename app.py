import random
import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(
    page_title="MindEase - Smart AI Companion",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-End Dark Glassmorphism Theme with Glowing Avatar CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #172554 40%, #1E1B4B 100%);
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Glowing Smart AI Avatar Frame */
    .ai-avatar-container {
        display: flex;
        align-items: center;
        gap: 16px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
    }

    .ai-face-glow {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, #38BDF8, #818CF8, #C084FC);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.6);
        animation: pulseGlow 3s infinite alternate;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 12px rgba(56, 189, 248, 0.4); transform: scale(0.98); }
        100% { box-shadow: 0 0 24px rgba(168, 85, 247, 0.8); transform: scale(1.04); }
    }

    /* Mood Button Styling */
    .stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.07);
        color: #F8FAFC;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        color: #0F172A;
        border-color: transparent;
        transform: translateY(-2px);
    }

    /* Chat Bubbles */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        padding: 14px 18px;
        margin-bottom: 12px;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Smart AI Face Header
st.markdown("""
<div class="ai-avatar-container">
    <div class="ai-face-glow">🤖</div>
    <div>
        <h2 style="margin:0; font-size: 1.6rem; color: #38BDF8 !important;">MindEase AI</h2>
        <p style="margin:0; opacity: 0.8; font-size: 0.95rem;">Smart Multimodal Assistant • Created by <b>Ansh Kumawat</b></p>
    </div>
</div>
""", unsafe_allow_html=True)

# Fetch Gemini API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Cloud Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 AI Status: Online")
    selected_model = st.selectbox(
        "Select Engine:",
        options=["gemini-3.6-flash", "gemini-3.1-pro"],
        format_func=lambda x: "⚡ Gemini 3.6 Flash (Fast)" if "flash" in x else "🧠 Gemini 3.1 Pro (Deep)"
    )
    st.divider()
    st.header("🌿 De-Stress Zone")
    st.subheader("4-7-8 Breathing Technique")
    st.markdown("""
    * **Inhale** (4s)
    * **Hold** (7s)
    * **Exhale** (8s)
    """)
    st.divider()
    st.warning("🚨 **Emergency Contacts**\nIf in immediate distress: **1800-599-0019**")

# Mood Selection
st.subheader("How are you feeling right now?")
c1, c2, c3, c4 = st.columns(4)

if "current_mood" not in st.session_state:
    st.session_state.current_mood = "Neutral"

with c1:
    if st.button("😊 Radiant"):
        st.session_state.current_mood = "Radiant"
        st.toast("Logged: Feeling Radiant! 🌟")
with c2:
    if st.button("😐 Peaceful"):
        st.session_state.current_mood = "Peaceful"
        st.toast("Logged: Feeling Peaceful. 🌿")
with c3:
    if st.button("😔 Overwhelmed"):
        st.session_state.current_mood = "Overwhelmed"
        st.toast("Logged: Take it easy today. 💛")
with c4:
    if st.button("😰 Anxious"):
        st.session_state.current_mood = "Anxious"
        st.toast("Logged: I'm here for you. 🫁")

st.divider()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hello! I am MindEase. How can I assist you today?"}
    ]

# Render Chat with Smart Avatar Icons
for msg in st.session_state.messages:
    avatar_icon = "🤖" if msg["role"] == "model" else "👤"
    with st.chat_message("assistant" if msg["role"] == "model" else "user", avatar=avatar_icon):
        st.write(msg["text"])

# Inputs Row
col_mic, col_attach, col_input = st.columns([2, 1, 9])

with col_mic:
    voice_input = st.audio_input("Record Voice", key="voice_recorder", label_visibility="collapsed")

with col_attach:
    with st.popover("📎"):
        uploaded_file = st.file_uploader("Attach file", type=["pdf", "png", "jpg", "jpeg"], key="doc_uploader")

with col_input:
    user_text = st.chat_input("Ask or command anything...")

# Request Processing
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

if user_prompt or has_attachment:
    st.session_state.messages.append({"role": "user", "text": user_prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(user_prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing..."):
            sys_instruction = (
                "You are MindEase, an ultra-smart, supportive, and sharp AI companion. "
                "You were created and developed by Ansh Kumawat. "
                f"User mood: '{st.session_state.current_mood}'. "
                "Keep answers direct, smart, precise, and supportive."
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
