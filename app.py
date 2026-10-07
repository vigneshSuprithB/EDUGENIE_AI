import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="EDUGENIE AI",
    page_icon="🎓",
    layout="wide"
)

# 2. Sidebar for Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input(
        "Gemini API Key", 
        type="password", 
        help="Paste your free key from aistudio.google.com"
    )
    
    st.markdown("---")
    st.markdown("### 🎓 About EDUGENIE AI")
    st.write(
        "An intelligent conversational study assistant built to explain complex academic concepts "
        "and summarize lecture notes using Google Gemini."
    )
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 3. Initialize Conversation State
if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_PROMPT = (
    "You are EDUGENIE AI, an encouraging and expert university academic tutor. "
    "Your mission is to help students grasp difficult concepts by breaking them down into "
    "simple, intuitive explanations with relatable real-world examples. Keep answers structured and clear."
)

# 4. App Header & Tabs
st.title("🎓 EDUGENIE AI — Study Assistant")
tab_chat, tab_summarize = st.tabs(["💬 Concept Tutor", "📝 Notes Summarizer"])

# --- TAB 1: Chatbot Tutor ---
with tab_chat:
    st.caption("Ask questions, test your understanding, or request step-by-step breakdowns.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask a question (e.g., 'Explain the difference between TCP and UDP')..."):
        if not api_key:
            st.warning("⚠️ Please enter your Gemini API key in the sidebar to start.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            try:
                client = genai.Client(api_key=api_key)
                
                # Build context messages from recent history
                recent_history = st.session_state.messages[-5:]
                contents = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                    for m in recent_history
                ]

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT
                            )
                        )
                        st.markdown(response.text)
                
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"Error calling Gemini API: {e}")

# --- TAB 2: Notes Summarizer ---
with tab_summarize:
    st.subheader("Summarize Lecture Notes")
    notes_text = st.text_area("Paste lecture notes or article text here:", height=200)
    
    if st.button("Generate Bullet Summary"):
        if not api_key:
            st.warning("⚠️ Please provide a Gemini API key in the sidebar.")
        elif not notes_text.strip():
            st.info("Please paste some notes first!")
        else:
            try:
                client = genai.Client(api_key=api_key)
                with st.spinner("Summarizing notes..."):
                    summary_resp = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=f"Summarize these lecture notes into clear, high-yield bullet points with bold key terms:\n\n{notes_text}",
                        config=types.GenerateContentConfig(
                            system_instruction="You are an expert academic note summarizer."
                        )
                    )
                    st.success("Summary Generated!")
                    st.markdown(summary_resp.text)
            except Exception as e:
                st.error(f"Error: {e}")