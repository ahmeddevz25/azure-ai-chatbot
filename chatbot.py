import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# ==========================================
# Azure AI Configuration
# ==========================================
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://testing26.services.ai.azure.com/openai/v1/chat/completions")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")

# ==========================================
# Streamlit Page Setup
# ==========================================
st.set_page_config(
    page_title="AI Workspace Chat",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# ChatGPT / Claude Style Clean Architecture CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* Global Reset */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    color: #0F172A;
    background-color: #F8FAFC !important;
}

/* Hide Default Streamlit Chrome */
header[data-testid="stHeader"], 
#MainMenu, 
footer, 
[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}

/* Chat Canvas Reading Width */
.block-container {
    max-width: 760px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 7.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    margin: 0 auto !important;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
    padding-top: 1.25rem !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}

/* Clean Top Navigation Bar */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #E2E8F0;
}

.brand-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-logo {
    width: 32px;
    height: 32px;
    background: #0F172A;
    color: #FFFFFF;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 700;
}

.brand-title {
    font-size: 0.98rem;
    font-weight: 600;
    color: #0F172A;
    letter-spacing: -0.015em;
    line-height: 1.2;
}

.brand-subtitle {
    font-size: 0.78rem;
    color: #64748B;
}

.model-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #FFFFFF;
    color: #334155;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.74rem;
    font-weight: 500;
    border: 1px solid #E2E8F0;
}

.status-dot-active {
    width: 7px;
    height: 7px;
    background-color: #10B981;
    border-radius: 50%;
    display: inline-block;
}

/* ========================================================
   CONVERSATIONAL MESSAGES (ChatGPT / Claude Style)
   ======================================================== */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.35rem 0 !important;
    margin-bottom: 1.5rem !important;
    display: flex !important;
    width: 100% !important;
    align-items: flex-start !important;
}

/* --- 1. USER MESSAGE (Natural Speech Bubble on Right, NO TEXT CLIPPING) --- */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    justify-content: flex-end !important;
}

/* Hide default user icon to make it a clean modern floating bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageAvatarUser"] {
    display: none !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    flex: 0 1 auto !important;
    width: fit-content !important;
    max-width: 75% !important;
    background-color: #0F172A !important;
    color: #FFFFFF !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 10px 18px 12px 18px !important;
    margin-left: auto !important;
    margin-right: 0 !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
    overflow: visible !important;
    word-break: break-word !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] * {
    color: #FFFFFF !important;
    overflow: visible !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] div {
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] p {
    color: #FFFFFF !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.5 !important;
    font-size: 0.95rem !important;
    display: inline-block !important;
}

/* --- 2. ASSISTANT MESSAGE (Clean text on canvas, NO huge box) --- */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    justify-content: flex-start !important;
    align-items: flex-start !important;
}

/* Minimalist round assistant monogram */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageAvatarAssistant"] {
    width: 28px !important;
    height: 28px !important;
    min-width: 28px !important;
    border-radius: 50% !important;
    background-color: #0F172A !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-right: 12px !important;
    margin-top: 3px !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageAvatarAssistant"] svg {
    filter: invert(1) brightness(2) !important;
    width: 15px !important;
    height: 15px !important;
}

/* Clean text container without box borders */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background-color: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding: 0 !important;
    width: 100% !important;
    color: #0F172A !important;
    overflow: visible !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] p {
    color: #1E293B !important;
    line-height: 1.7 !important;
    font-size: 0.98rem !important;
    margin-bottom: 0.75rem !important;
}

/* Typography Inside Assistant Responses */
[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3,
[data-testid="stChatMessageContent"] h4 {
    font-weight: 600 !important;
    color: #0F172A !important;
    letter-spacing: -0.02em !important;
    margin-top: 1.1rem !important;
    margin-bottom: 0.4rem !important;
}

[data-testid="stChatMessageContent"] strong {
    font-weight: 600 !important;
    color: #0F172A !important;
}

[data-testid="stChatMessageContent"] ul, 
[data-testid="stChatMessageContent"] ol {
    margin-top: 0.4rem !important;
    margin-bottom: 0.8rem !important;
    padding-left: 1.4rem !important;
}

[data-testid="stChatMessageContent"] li {
    margin-bottom: 0.4rem !important;
    line-height: 1.6 !important;
}

[data-testid="stChatMessageContent"] pre {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    border: 1px solid #1E293B !important;
    margin: 0.8rem 0 !important;
}

/* ========================================================
   BOTTOM CHAT INPUT BAR
   ======================================================== */
[data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(248, 250, 252, 0) 0%, rgba(248, 250, 252, 0.92) 30%, #F8FAFC 100%) !important;
    padding-top: 1.25rem !important;
}

[data-testid="stChatInput"] {
    max-width: 760px !important;
    margin: 0 auto !important;
    padding-bottom: 1.25rem !important;
}

[data-testid="stChatInput"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.06), 0 2px 6px -1px rgba(15, 23, 42, 0.02) !important;
    transition: all 0.2s ease !important;
    padding: 4px 8px !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: #0F172A !important;
    box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.1), 0 4px 20px -2px rgba(15, 23, 42, 0.08) !important;
}

[data-testid="stChatInput"] textarea {
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    color: #0F172A !important;
}

/* ========================================================
   EMPTY STATE (Clean & Minimalist)
   ======================================================== */
.empty-hero {
    text-align: center;
    padding: 3rem 1rem 1.5rem 1rem;
    max-width: 580px;
    margin: 0 auto;
}

.empty-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.025em;
    margin-bottom: 0.4rem;
}

.empty-desc {
    font-size: 0.92rem;
    color: #64748B;
    line-height: 1.5;
    margin-bottom: 2rem;
}

/* Clean Starter Buttons */
.stButton > button {
    border-radius: 12px !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    border: 1px solid #E2E8F0 !important;
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    padding: 0.75rem 1rem !important;
    white-space: pre-wrap !important;
    text-align: left !important;
    line-height: 1.4 !important;
    min-height: 60px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.02) !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background-color: #F8FAFC !important;
    border-color: #94A3B8 !important;
    color: #0F172A !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# Application Header Bar
# ==========================================
st.markdown("""
<div class="app-header">
    <div class="brand-wrapper">
        <div class="brand-logo">✦</div>
        <div>
            <div class="brand-title">Workspace Chat</div>
            <div class="brand-subtitle">Powered by Azure OpenAI</div>
        </div>
    </div>
    <div class="model-pill">
        <span class="status-dot-active"></span>
        <span>gpt-4.1-mini</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# Sidebar (Configuration)
# ==========================================
with st.sidebar:
    st.markdown("**System Status**")
    st.markdown(f"""
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px 12px; margin-bottom:1.2rem;">
        <div style="display:flex; align-items:center; gap:8px; font-weight:600; font-size:0.85rem;">
            <span class="status-dot-active"></span>
            <span>Azure Cloud Connected</span>
        </div>
        <div style="font-size:0.75rem; color:#64748B; margin-top:4px;">
            Deployment: <code>{DEPLOYMENT_NAME}</code><br>
            Status: Active Streaming
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Parameters**")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Higher values make responses more creative, lower values make them focused."
    )
    
    with st.expander("System Prompt", expanded=False):
        system_prompt = st.text_area(
            "Instructions",
            value="You are a helpful, polite, and intelligent AI assistant. Provide concise, clear, and well-structured answers. You can converse naturally in English, Urdu, or Roman Urdu as requested by the user.",
            height=90,
            label_visibility="collapsed"
        )
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

# ==========================================
# Check for Missing API Key
# ==========================================
if not API_KEY:
    st.warning("⚠️ Azure OpenAI API Key is missing. Please add your `AZURE_OPENAI_API_KEY` to `.env` file.")

# ==========================================
# Session State Initialization
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input at bottom
user_prompt = st.chat_input("Message Workspace Chat... (Press Enter to send)")

# Check for pending prompt from buttons
pending_input = None
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    pending_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# Current active user prompt
active_prompt = pending_input or user_prompt

# If active prompt submitted, immediately record to session state
if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})

# ==========================================
# Empty State: Welcome Hero & Starter Prompts
# ==========================================
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="empty-hero">
        <div class="empty-title">How can I help you today?</div>
        <div class="empty-desc">Send a message to start, or pick a starter prompt below.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 Explain Concept\nHow does RAG work in machine learning?", use_container_width=True):
            st.session_state.pending_prompt = "Explain Retrieval-Augmented Generation (RAG) in machine learning with a simple real-world example."
            st.rerun()
            
        if st.button("📝 Draft Message\nHelp me write a concise status update", use_container_width=True):
            st.session_state.pending_prompt = "Write a professional, concise project status update email for my team."
            st.rerun()

    with col2:
        if st.button("⚡ Python Helper\nWrite a clean error-handled API caller", use_container_width=True):
            st.session_state.pending_prompt = "Write a clean Python function using requests with timeout and error handling."
            st.rerun()
            
        if st.button("🌐 Roman Urdu\nAI seekhny ky basic steps batao", use_container_width=True):
            st.session_state.pending_prompt = "Mujhy Artificial Intelligence aur Python seekhny ky aasan steps Roman Urdu may batao."
            st.rerun()

# ==========================================
# Azure AI Streaming Response Generator
# ==========================================
def stream_azure_response(messages_list):
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEPLOYMENT_NAME,
        "messages": [{"role": "system", "content": system_prompt}] + messages_list,
        "temperature": temperature,
        "stream": True
    }
    
    try:
        response = requests.post(
            AZURE_ENDPOINT,
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code != 200:
            yield f"⚠️ API Error ({response.status_code}): {response.text}"
            return
            
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data: ") and decoded_line.strip() != "data: [DONE]":
                    try:
                        chunk = json.loads(decoded_line[6:])
                        choices = chunk.get("choices", [])
                        if choices:
                            delta_content = choices[0].get("delta", {}).get("content", "")
                            if delta_content:
                                yield delta_content
                    except Exception:
                        pass
    except requests.exceptions.RequestException as e:
        yield f"⚠️ Connection Error: {str(e)}"

# ==========================================
# Display Chat Messages
# ==========================================
needs_streaming = (active_prompt is not None)
history_to_display = st.session_state.messages[:-1] if needs_streaming else st.session_state.messages

for message in history_to_display:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Stream reply for the newest message
if needs_streaming:
    with st.chat_message("user"):
        st.markdown(st.session_state.messages[-1]["content"])
    
    with st.chat_message("assistant"):
        response_stream = stream_azure_response(st.session_state.messages)
        completed_response = st.write_stream(response_stream)
        
    st.session_state.messages.append({"role": "assistant", "content": completed_response})
