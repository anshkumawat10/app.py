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

# Custom Styling: Cute Aesthetic + Compact Mic Widget
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
        padding: 16px 24px;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px rgba(244, 114, 182, 0.15);
    }

    .ai-cute-avatar {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        background: linear-gradient(135deg, #F472B6 0%, #FB923C 50%, #38BDF8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 0 16px rgba(244, 114, 182, 0.5);
        animation: floatCute 3s ease-in-out infinite alternate;
    }

    @keyframes floatCute {
        0% { transform: translateY(0px) rotate(-3deg); }
        100% { transform: translateY(-4px) rotate(3deg); }
    }

    /* COMPACT VOICE RECORDER WIDGET */
    div[data-testid="stAudioInput"] {
        max-width: 130px !important;
        transform: scale(0.85);
        transform-origin: left center;
        margin: 0;
        padding: 0;
    }

    /* Mood Buttons */
    .stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.08);
        color: #F8FAFC;
        font-size: 0.95rem;
        font-weight: 500;
        padding: 8px 12px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #F472B6 0%, #38BDF8 100%);
        color: #0F172A;
        border-color: transparent;
        transform: translateY(-2px);
    }

    /* Soft Chat Bubbles */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        padding: 12px 16px;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.92);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Cute Header Banner
st.markdown("""
<div class="ai-cute-header">
    <div class="ai-cute-avatar">🌸</div>
    <div>
        <h2 style="margin:0; font-size: 1.5rem; color: #F472B6 !important;">MindEase • Your Comfort Companion ✨</h2>
        <p style="margin:0; opacity: 0.85; font-size: 0.9rem;">Always here to listen, support, and help • Created by <b>Ansh Kumawat</b></p>
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
    st.warning("🚨 **Need Immediate Help?**\nContact: **1800-599-0019** (Tele-MANAS)")

# Mood Check-In Section at Top
st.markdown("##### How are you feeling right now? 💖")
col1, col2, col3, col4 = st.columns(4)

if "current_mood" not in st.session_state:
    st.session_state.current_mood = "Neutral"

with col1:
    if st.button("😊 Radiant"):
        st.session_state.current_mood = "Radiant & Happy"
        st.toast("Logged: Radiant! 🌟")

with col2:
    if st.button("🌿 Peaceful"):
        st.session_state.current_mood = "Peaceful & Calm"
        st.toast("Logged: Peaceful. 🍵")

with col3:
    if st.button("😔 Stressed"):
        st.session_state.current_mood = "Tired & Stressed"
        st.toast("Logged: Take it easy today. 🧸")

with col4:
    if st.button("😰 Anxious"):
        st.session_state.current_mood = "Anxious & Uneasy"
        st.toast("Logged: I'm right here with you. 🫁")

st.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hi there! 🌸 I'm MindEase, your cozy companion. How can I help you today?"}
    ]

# 1. RENDER ALL CHAT MESSAGES IN THE MIDDLE BODY
for msg in st.session_state.messages:
    avatar_icon = "🌸" if msg["role"] == "model" else "✨"
    with st.chat_message("assistant" if msg["role"] == "model" else "user", avatar=avatar_icon):
        st.write(msg["text"])

# 2. MEDIA ATTACHMENTS BAR (Voice + Document) JUST ABOVE THE BOTTOM INPUT
with st.expander("🎙️ / 📎 Record Voice or Attach Document", expanded=False):
    col_mic, col_attach = st.columns([1, 3])
    with col_mic:
        voice_input = st.audio_input("Record Voice", key="voice_recorder", label_visibility="collapsed")
    with col_attach:
        uploaded_file = st.file_uploader("Attach file", type=["pdf", "png", "jpg", "jpeg"], key="doc_uploader", label_visibility="collapsed")

# 3. NATIVE BOTTOM CHAT INPUT (Pinned at bottom of page)
user_text = st.chat_input("Tell me what's on your mind... 💭")

# Handle User Input Processing
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

    # Prepare Gemini Request
    sys_instruction = (
        "You are MindEase, a cute, warm, ultra-intelligent, and deeply empathetic AI companion created by Ansh Kumawat. "
        "If asked who built or created you, state explicitly that you were created by Ansh Kumawat. "
        f"CURRENT USER MOOD CONTEXT: '{st.session_state.current_mood}'. "
        "Adapt your tone dynamically: gentle & soothing when stressed, cheerful when happy, clear & practical when solving tasks. "
        "Sprinkle warm, cute emojis (🌸, ✨, 🧸, 🌿) naturally. Keep responses concise (2-4 sentences max per turn)."
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

    st.session_state.messages.append({"role": "model", "text": response.text})
    st.rerun()
