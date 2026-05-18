import streamlit as st
from openai import OpenAI

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroStudy AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CYBERPUNK CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top left, #1a0033, #090016, #000000);
    color: white;
    overflow-x: hidden;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Layout */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

/* Neon Title */
.neon-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 800;
    color: white;
    text-shadow:
        0 0 5px #ff00ff,
        0 0 10px #ff00ff,
        0 0 20px #00ffff,
        0 0 40px #00ffff;
    margin-bottom: 10px;
}

/* Subtitle */
.neon-subtitle {
    text-align: center;
    color: #d8b4fe;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

/* Glow Line */
.glow-line {
    height: 2px;
    width: 100%;
    background: linear-gradient(90deg, #ff00ff, #00ffff);
    margin-top: 20px;
    margin-bottom: 30px;
    box-shadow: 0 0 20px #00ffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15, 15, 35, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Cards */
.cyber-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(14px);
    padding: 22px;
    border-radius: 20px;
    transition: 0.3s;
    margin-bottom: 20px;
}

.cyber-card:hover {
    transform: translateY(-5px);
    border: 1px solid #ff00ff;
    box-shadow: 0 0 25px rgba(255,0,255,0.5);
}

/* Chat Messages */
.stChatMessage {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}

/* User Message */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    border-left: 4px solid #00ffff;
}

/* Assistant Message */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    border-left: 4px solid #ff00ff;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 14px;
    height: 48px;
    border: none;
    font-weight: bold;
    color: white;
    background: linear-gradient(90deg, #ff00ff, #7c3aed, #00ffff);
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(255,0,255,0.6);
}

/* Inputs */
textarea,
input {
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Chat Input */
.stChatInput input {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.05);
    border-radius: 12px;
}

/* Success Alert */
.stSuccess {
    border-radius: 12px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #7c3aed;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
You are NeuroStudy AI, a futuristic AI study assistant.

Your tasks:
- Explain concepts clearly
- Help students understand difficult topics
- Summarize notes
- Give examples
- Provide step-by-step answers
- Keep responses beginner friendly

Use headings and bullet points.
"""

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    st.title("⚙️ Settings")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_..."
    )

    st.divider()

    model_name = st.selectbox(
        "Choose AI Model",
        [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ]
    )

    st.divider()

    st.subheader("📝 Notes Summarizer")

    notes = st.text_area(
        "Paste your notes",
        height=200,
        placeholder="Paste lecture notes or textbook content..."
    )

    if st.button("✨ Summarize Notes"):

        if not api_key:
            st.error("Please enter API key")

        elif not notes.strip():
            st.warning("Please paste notes")

        else:
            try:

                with st.spinner("Summarizing..."):

                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://api.groq.com/openai/v1"
                    )

                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {
                                "role": "system",
                                "content": """
                                Summarize clearly using:
                                - Bullet points
                                - Simple explanations
                                - Important concepts
                                """
                            },
                            {
                                "role": "user",
                                "content": notes
                            }
                        ],
                        temperature=0.3
                    )

                    summary = response.choices[0].message.content

                    st.success("Summary Generated")

                    st.markdown(summary)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="neon-title">
        ⚡ NeuroStudy AI
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="neon-subtitle">
        Futuristic AI-Powered Study Assistant
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="glow-line"></div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# FEATURE CARDS
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="cyber-card">
    <h3>🧠 Smart Learning</h3>
    <p>Understand difficult topics instantly using AI.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="cyber-card">
    <h3>⚡ Instant Summaries</h3>
    <p>Convert long notes into quick revision points.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="cyber-card">
    <h3>🚀 Exam Booster</h3>
    <p>Prepare smarter with AI-powered explanations.</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────
prompt = st.chat_input(
    "Ask anything about studies..."
)

if prompt:

    if not api_key:
        st.error("Please enter your Groq API key.")
        st.stop()

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # RECENT MEMORY
    recent_messages = st.session_state.messages[-6:]

    full_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + recent_messages

    # ASSISTANT MESSAGE
    with st.chat_message("assistant"):

        try:

            with st.spinner("Thinking..."):

                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )

                stream = client.chat.completions.create(
                    model=model_name,
                    messages=full_messages,
                    temperature=0.5,
                    stream=True
                )

                response = st.write_stream(
                    chunk.choices[0].delta.content or ""
                    for chunk in stream
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)

st.caption("⚡ Built with Streamlit + Groq AI")