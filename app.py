import random
import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="MindEase - Warm Personal AI Companion",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-End Warm Ambient Glassmorphism Theme
st.markdown("""
<style>
    /* Warm Ambient Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #172554 40%, #1E1B4B 100%);
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Welcome Card Glow Banner */
    .welcome-card {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(168, 85, 247, 0.12) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    /* Interactive Mood Buttons */
    .stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.07);
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 500;
        padding: 12px 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        color: #0F172A;
        border-color: transparent;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(56, 189, 248, 0.35);
    }

    /* Floating Chat Bubbles */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        padding: 14px 18px;
        margin-bottom: 14px;
    }

    /* Glass Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.88);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    h1, h2, h3 { color: #F8FAFC !important; }
</style>
""", unsafe_allow_html=True)

# Dynamic Inspiring Notes Pool
WELCOME_NOTES = [
    "✨ *\"No matter how heavy today feels, remember: taking a slow breath is already a step forward.\"*",
    "🌟 *\"You don't have to figure everything out right now. Just be here, step by step.\"*",
    "🌿 *\"Give yourself the same warmth and kindness you so freely give to others.\"*",
    "💡 *\"Every small moment of quiet builds your inner strength. Welcome back to your safe space.\"*",
    "☀️ *\"Whatever brought you here today, you are welcomed, heard, and supported.\"*"
]

if "daily_note" not in st.session_state:
    st.session_state.daily_note = random.choice(WELCOME_NOTES)

# Header & Rotating Welcome Banner
st.title("🌱 MindEase")
st.markdown(f"""
<div class="welcome-card">
    <h3 style="margin-top:0; color:#38BDF8 !important;">Welcome back! 💫</h3>
    <p style="font-size: 1.1rem; margin-bottom: 0;">{st.session_state.daily_note}</p>
    <p style="font-size: 0.85rem; opacity: 0.7; margin-top: 8px;">Created & Designed by <b>Ansh Kumawat</b></p>
</div>
""", unsafe_allow_html=True)

# Fetch Gemini API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Cloud Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Sidebar Engine & Breathing Controls
with st.sidebar:
    st.header("⚡ AI Engine Options")
    
    selected_model = st.selectbox(
        "Select AI Speed & Power:",
        options=["gemini-3.6-flash", "gemini-3.1-pro"],
        format_func=lambda x: "⚡ Gemini 3.6 Flash (Ultra Fast)" if "flash" in x else "🧠 Gemini 3.1 Pro (Deep Intelligence)"
    )
    
    st.divider()
    st.header("🌿 De-Stress Zone")
    st.subheader("4-7-8 Breathing Technique")
    st.markdown("""
    * **Inhale** through nose (4s)
    * **Hold** breath (7s)
    * **Exhale** through mouth (8s)
    """)
    st.divider()
    st.warning("🚨 **Emergency Contacts**\nIf in immediate distress: **1800-599-0019** (Tele-MANAS) or local emergency services.")

# Interactive Emoji Mood Check-In
st.subheader("How is your mind feeling right now?")
col1, col2, col3, col4 = st.columns(4)

if "current_mood" not in st.session_state:
    st.session_state.current_mood = "Neutral"

with col1:
    if st.button("😊 Radiant"):
        st.session_state.current_mood = "Radiant & Happy"
        st.session_state.daily_note = random.choice(WELCOME_NOTES)
        st.toast("Logged: Radiant! 🌟")

with col2:
    if st.button("😐 Peaceful"):
        st.session_state.current_mood = "Peaceful & Calm"
        st.session_state.daily_note = random.choice(WELCOME_NOTES)
        st.toast("Logged: Peaceful. 🌿")

with col3:
    if st.button("😔 Overwhelmed"):
        st.session_state.current_mood = "Overwhelmed & Tired"
        st.session_state.daily_note = random.choice(WELCOME_NOTES)
        st.toast("Logged: Sending extra warmth. 💛")

with col4:
    if st.button("😰 Anxious"):
        st.session_state.current_mood = "Anxious & Uneasy"
        st.session_state.daily_note = random.choice(WELCOME_NOTES)
        st.toast("Logged: Take a deep breath with me. 🫁")

st.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hey there... I'm really glad you stopped by today. How are things carrying on in your world right now?"}
    ]

# Adaptive System Instructions
sys_instruction = (
    "You are MindEase, an ultra-intelligent, supportive, and deeply empathetic AI companion. "
    "You were created and developed by Ansh Kumawat. "
    "If asked who built or created you, explicitly state that you were created by Ansh Kumawat. "
    f"CURRENT USER MOOD CONTEXT: The user currently feels '{st.session_state.current_mood}'. Adapt your tone accordingly. "
    "Respond conversationally and warmly (2-4 sentences max per turn). "
    "When processing user audio recordings or documents, provide direct, precise, and helpful insights. "
    "STRICT SAFETY: Do NOT prescribe medical treatments or clinical diagnoses. "
    "For severe emotional distress, direct users to emergency services."
)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "model" else "user"):
        st.write(msg["text"])

# Multi-Input Row: Voice Recording, Document Attachment, Text Input
col_mic, col_attach, col_input = st.columns([2, 1, 9])

with col_mic:
    voice_input = st.audio_input("Record Voice", key="voice_recorder", label_visibility="collapsed")

with col_attach:
    with st.popover("📎", help="Attach document"):
        uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"], key="doc_uploader")
        if uploaded_file:
            st.success(f"Attached: {uploaded_file.name}")

with col_input:
    user_text = st.chat_input("Talk to me...")

# Logic to Process Inputs
user_prompt = user_text
input_parts = []
has_attachment = False

if voice_input:
    voice_bytes = voice_input.read()
    input_parts.append(types.Part.from_bytes(data=voice_bytes, mime_type="audio/wav"))
    user_prompt = user_prompt or "🎤 Sent a voice message."
    has_attachment = True

if uploaded_file:
    file_bytes = uploaded_file.read()
    input_parts.append(types.Part.from_bytes(data=file_bytes, mime_type=uploaded_file.type))
    user_prompt = user_prompt or f"📄 Uploaded document: {uploaded_file.name}"
    has_attachment = True

if user_text:
    input_parts.append(types.Part.from_text(text=user_text))

# Send Request to Gemini API
if user_prompt or has_attachment:
    st.session_state.messages.append({"role": "user", "text": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Connecting with {selected_model}..."):
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
