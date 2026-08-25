import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="MindEase - Ultra-Fast AI Companion",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Dark Glassmorphism Design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px 16px;
        margin-bottom: 12px;
    }
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 { color: #F1F5F9 !important; }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🌱 MindEase")
st.caption("Ultra-Fast Voice & Document AI Companion — Created by Ansh Kumawat")

# Sidebar Controls
with st.sidebar:
    st.header("🌿 De-Stress & Emergency")
    st.subheader("4-7-8 Breathing Technique")
    st.markdown("""
    * **Inhale** through nose (4s)
    * **Hold** breath (7s)
    * **Exhale** through mouth (8s)
    """)
    st.divider()
    st.warning("🚨 **Emergency Contacts**\nIf in immediate distress: **1800-599-0019** (Tele-MANAS) or local emergency services.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Hey there! I'm ready. You can type, record a voice command, or attach a document."}
    ]

# Fetch Gemini API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Cloud Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# System Instructions optimized for fast execution
sys_instruction = (
    "You are MindEase, an ultra-intelligent, supportive, and warm AI companion. "
    "You were created and developed by Ansh Kumawat. "
    "If asked who built or created you, explicitly state that you were created by Ansh Kumawat. "
    "Respond quickly and conversationally (2-4 sentences max per turn). "
    "When processing user audio recordings or documents, provide direct, precise, and helpful insights. "
    "STRICT SAFETY: Do NOT prescribe medical treatments or clinical diagnoses. "
    "For severe emotional distress, direct users to emergency services."
)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "model" else "user"):
        st.write(msg["text"])

st.divider()

# Input Bar: Audio Recorder + Popover for File Attachment + Chat Input
col_mic, col_attach, col_input = st.columns([2, 1, 9])

with col_mic:
    voice_input = st.audio_input("Record Voice", key="voice_recorder", label_visibility="collapsed")

with col_attach:
    with st.popover("📎", help="Attach document"):
        uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"], key="doc_uploader")
        if uploaded_file:
            st.success(f"Attached: {uploaded_file.name}")

with col_input:
    user_text = st.chat_input("Type your message...")

# Logic to Handle Input (Text, Voice, or Document)
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

# Process Request through Gemini
if user_prompt or has_attachment:
    st.session_state.messages.append({"role": "user", "text": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking ultra-fast..."):
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
