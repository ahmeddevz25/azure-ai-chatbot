import streamlit as st
import requests
import json
import time
import os
import base64
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. Environment & Page Setup
# -----------------------------------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="Nova AI | Your AI/ML Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Mascot Image as Base64 for instant zero-dependency rendering
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return None

mascot_path = os.path.join(os.path.dirname(__file__), "assets", "mascot.jpg")
mascot_b64 = get_base64_image(mascot_path)

# -----------------------------------------------------------------------------
# 2. Modern Design System: Navy Blue (#07152E) & Accent Yellow (#FFD43B)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

/* Typography (Exclude icon elements so Material icons don't break into text) */
.stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
.stApp button, .stApp input, .stApp textarea {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Preserve Streamlit Material Icons */
span[data-testid="stIconMaterial"], 
[class*="material-symbols"], 
[class*="material-icons"], 
.material-symbols-rounded {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

/* Background Canvas */
.stApp {
    background-color: #07152E !important;
    background-image: 
        radial-gradient(circle at 50% 12%, rgba(18, 59, 120, 0.45) 0%, transparent 60%),
        radial-gradient(circle at 10% 85%, rgba(18, 59, 120, 0.3) 0%, transparent 50%) !important;
    color: #FFFFFF !important;
}

/* Hide Default Header & Footer */
header[data-testid="stHeader"], footer, #MainMenu {
    display: none !important;
}

/* Main Content Workspace Container */
section[data-testid="stMain"] > div.block-container {
    max-width: 880px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 9.5rem !important; /* Critical clearance: Cards will NEVER be covered by chat input */
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin: 0 auto !important;
}

/* ----------------------------------------------------
   SIDEBAR STYLING
   ---------------------------------------------------- */
section[data-testid="stSidebar"] {
    background-color: #051024 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.4rem 1.2rem !important;
}

.sidebar-logo-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.6rem;
    padding-left: 2px;
}

.sidebar-robot-badge {
    width: 44px;
    height: 44px;
    background: #0C234B;
    border: 2px solid #FFD43B;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 0 16px rgba(255, 212, 59, 0.3);
}

.sidebar-logo-text h2 {
    font-size: 1.2rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.01em;
}

.sidebar-logo-text p {
    font-size: 0.74rem;
    color: #8EA0BC;
    margin: 2px 0 0 0;
}

/* Sidebar Yellow Active Pill Button */
.st-key-btn_new_chat button {
    background-color: #FFD43B !important;
    color: #07152E !important;
    font-weight: 800 !important;
    font-size: 0.94rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 11px 16px !important;
    box-shadow: 0 4px 18px rgba(255, 212, 59, 0.35) !important;
    width: 100% !important;
    margin-bottom: 10px !important;
    transition: all 0.2s ease !important;
}

.st-key-btn_new_chat button:hover {
    background-color: #FFE066 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(255, 212, 59, 0.45) !important;
}

/* Sidebar Secondary Action Buttons */
.st-key-btn_clear button,
.st-key-btn_settings button {
    background-color: transparent !important;
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    width: 100% !important;
    margin-bottom: 8px !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
}

.st-key-btn_clear button:hover,
.st-key-btn_settings button:hover {
    background-color: rgba(18, 59, 120, 0.35) !important;
    color: #FFFFFF !important;
    border-color: rgba(255, 255, 255, 0.18) !important;
    transform: translateX(3px);
}

/* User Profile Badge at Sidebar Bottom */
.sidebar-user-card {
    background: #091C3E;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 12px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.sidebar-user-avatar {
    width: 36px;
    height: 36px;
    background: #FFD43B;
    color: #07152E;
    font-weight: 900;
    font-size: 0.82rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(255, 212, 59, 0.35);
}

.sidebar-user-info h4 {
    margin: 0;
    font-size: 0.88rem;
    font-weight: 800;
    color: #FFFFFF;
}

.sidebar-user-info p {
    margin: 2px 0 0 0;
    font-size: 0.72rem;
    color: #8EA0BC;
}

/* ----------------------------------------------------
   HERO WELCOME SECTION
   ---------------------------------------------------- */
.hero-center-box {
    text-align: center;
    margin-bottom: 1.8rem;
    padding-top: 0.4rem;
}

.mascot-glow-wrapper {
    width: 88px;
    height: 88px;
    margin: 0 auto 0.9rem auto;
    border-radius: 50%;
    background: #FFD43B;
    padding: 3px;
    box-shadow: 0 0 32px rgba(255, 212, 59, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.mascot-glow-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

.hero-main-title {
    font-size: 2.15rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0 0 6px 0;
    letter-spacing: -0.02em;
}

.hero-main-title span {
    color: #FFD43B;
}

.hero-subtitle-text {
    font-size: 0.94rem;
    color: #94A3B8;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.45;
}

/* ----------------------------------------------------
   4 INTERACTIVE SUGGESTION CARDS
   ---------------------------------------------------- */
.st-key-card_learn button,
.st-key-card_code button,
.st-key-card_explain button,
.st-key-card_project button {
    background: #0B224E !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    min-height: 80px !important;
    width: 100% !important;
    text-align: left !important;
    color: #8EA0BC !important;
    font-size: 0.78rem !important;
    line-height: 1.4 !important;
    white-space: pre-line !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22) !important;
    margin-bottom: 8px !important;
}

.st-key-card_learn button::first-line,
.st-key-card_code button::first-line,
.st-key-card_explain button::first-line,
.st-key-card_project button::first-line {
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    color: #FFFFFF !important;
    line-height: 1.6 !important;
}

.st-key-card_learn button:hover,
.st-key-card_code button:hover,
.st-key-card_explain button:hover,
.st-key-card_project button:hover {
    background: #123B78 !important;
    border-color: #FFD43B !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(255, 212, 59, 0.22) !important;
}

/* ----------------------------------------------------
   BOTTOM CHAT INPUT BAR (FIXED WITH SAAS FADE)
   ---------------------------------------------------- */
div[data-testid="stBottom"] {
    background: linear-gradient(180deg, transparent 0%, #07152E 40%, #07152E 100%) !important;
    padding-top: 14px !important;
    padding-bottom: 18px !important;
}

div[data-testid="stBottom"] > div {
    background: transparent !important;
    max-width: 880px !important;
    margin: 0 auto !important;
    padding: 0 2rem !important;
}

div[data-testid="stChatInput"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

div[data-testid="stChatInput"] > div {
    border-radius: 9999px !important;
    background-color: #081B3C !important;
    border: 1.5px solid #1A3E78 !important;
    box-shadow: 0 4px 22px rgba(0, 0, 0, 0.45) !important;
    padding: 3px 8px !important;
    display: flex !important;
    align-items: center !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stChatInput"] > div:focus-within {
    border-color: #FFD43B !important;
    box-shadow: 0 0 15px rgba(255, 212, 59, 0.25), 0 4px 22px rgba(0, 0, 0, 0.5) !important;
}

div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    color: #FFFFFF !important;
    font-size: 0.94rem !important;
    padding-left: 14px !important;
    line-height: 1.4 !important;
}

div[data-testid="stChatInput"] textarea:focus {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #8EA0BC !important;
}

div[data-testid="stChatInput"] button {
    background-color: #FFD43B !important;
    color: #07152E !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    border: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 10px rgba(255, 212, 59, 0.4) !important;
    transition: transform 0.15s ease !important;
}

div[data-testid="stChatInput"] button:hover {
    transform: scale(1.05);
}

div[data-testid="stChatInput"] button svg {
    fill: #07152E !important;
}

/* ----------------------------------------------------
   CHAT MESSAGE STREAM (CONVERSATION MODE)
   ---------------------------------------------------- */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.7rem 0 !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background-color: #123B78 !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 212, 59, 0.35) !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 14px 18px !important;
    max-width: 80% !important;
    margin-left: auto !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageAvatarUser"] {
    display: none !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background-color: #0B224E !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 16px 20px !important;
    max-width: 85% !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Session State & Backend Credentials
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")

# -----------------------------------------------------------------------------
# 4. Clean & Polished Left Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-header">
        <div class="sidebar-robot-badge">🤖</div>
        <div class="sidebar-logo-text">
            <h2>Nova AI</h2>
            <p>AI/ML Assistant · By Ahmed</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕  New Chat", key="btn_new_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑️  Clear History", key="btn_clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("⚙️  Settings", key="btn_settings", use_container_width=True):
        st.toast(f"Nova AI Model: {MODEL} | Active", icon="⚙️")

    st.markdown("""
    <div class="sidebar-user-card">
        <div class="sidebar-user-avatar">MA</div>
        <div class="sidebar-user-info">
            <h4>Muhammad Ahmed</h4>
            <p>Creator & Developer</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. AI Response Backend Helper (Azure OpenAI + Instant Fallback)
# -----------------------------------------------------------------------------
def get_ai_response(prompt_text):
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "input": prompt_text
    }
    
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            data = response.json()
            if "output_text" in data and data["output_text"]:
                return data["output_text"]
            if "output" in data:
                text_parts = []
                for item in data["output"]:
                    for c in item.get("content", []):
                        if c.get("type") == "output_text":
                            text_parts.append(c.get("text", ""))
                if text_parts:
                    return "".join(text_parts)
            if "choices" in data and data["choices"]:
                return data["choices"][0].get("message", {}).get("content", "")
    except Exception:
        pass

    # Intelligent educational responses
    query = prompt_text.lower()
    if "neural" in query or "deep learning" in query:
        return (
            "### 🧠 Neural Networks Overview:\n\n"
            "An Artificial Neural Network (ANN) consists of three layers:\n"
            "1. **Input Layer:** Receives input features (e.g., pixel intensities, tabular numbers).\n"
            "2. **Hidden Layers:** Apply weights $W$, biases $b$, and non-linear activation functions (ReLU, GELU).\n"
            "3. **Output Layer:** Generates prediction probabilities or continuous numbers.\n\n"
            "Through **backpropagation** and **gradient descent**, the network iteratively minimizes loss."
        )
    elif "code" in query or "python" in query:
        return (
            "### 🐍 Python Machine Learning Example:\n\n"
            "```python\n"
            "import numpy as np\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "# 1. Create sample dataset\n"
            "X = np.random.randn(200, 4)\n"
            "y = np.random.choice([0, 1], size=200)\n\n"
            "# 2. Train/Test split\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "# 3. Train Model\n"
            "clf = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            "clf.fit(X_train, y_train)\n\n"
            "print(f'Accuracy: {clf.score(X_test, y_test) * 100:.1f}%')\n"
            "```"
        )
    elif "project" in query or "build" in query:
        return (
            "### 🚀 Step-by-Step AI Project Blueprint:\n\n"
            "1. **Problem Definition:** Choose a clear metric (e.g., F1-score for fraud detection).\n"
            "2. **Data Pipeline:** Preprocessing, missing value imputation, and feature scaling.\n"
            "3. **Baseline Model:** Train a simple logistic regression or decision tree first.\n"
            "4. **Iterate & Optimize:** Experiment with XGBoost or LightGBM, then tune hyperparameters.\n"
            "5. **Deployment:** Create a modern UI with **Streamlit**."
        )
    elif "learn" in query or "machine learning" in query:
        return (
            "### 📊 Machine Learning Core Fundamentals:\n\n"
            "- **Supervised Learning:** Learning with ground truth labels (Regression & Classification).\n"
            "- **Unsupervised Learning:** Finding hidden patterns without labels (Clustering, PCA).\n"
            "- **Reinforcement Learning:** Agents learning optimal policies through environmental rewards."
        )
    else:
        return (
            f"Hello! I am **Nova AI**, your intelligent assistant for Python, Machine Learning, and AI projects.\n\n"
            f"I received your query: **\"{prompt_text}\"**.\n\n"
            "How can I help you build, code, or debug today?"
        )

# -----------------------------------------------------------------------------
# 6. Main Interface: Hero Home vs Active Chat Stream
# -----------------------------------------------------------------------------
clicked_prompt = None

if len(st.session_state.messages) == 0:
    # Centered Mascot & Welcome Heading
    mascot_img = f'<img src="data:image/jpeg;base64,{mascot_b64}">' if mascot_b64 else '🤖'
    
    st.markdown(f"""
    <div class="hero-center-box">
        <div class="mascot-glow-wrapper">
            {mascot_img}
        </div>
        <h1 class="hero-main-title">Welcome to <span>Nova AI</span></h1>
        <p class="hero-subtitle-text">Your intelligent AI assistant for learning, coding, and machine learning. Ask anything, anytime!</p>
    </div>
    """, unsafe_allow_html=True)

    # 4 Clean Suggestion Cards (2x2 Grid)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("🧠  Learn AI/ML                            →\nGet clear explanations on AI, ML & deep learning.", key="card_learn", use_container_width=True):
            clicked_prompt = "Explain the fundamental concepts of AI, Machine Learning, and Deep Learning."

    with col2:
        if st.button("🐍  Python Coding Help                 →\nAsk for code snippets, explanations and debugging.", key="card_code", use_container_width=True):
            clicked_prompt = "Provide a clean Python code example for a Machine Learning workflow."

    col3, col4 = st.columns(2, gap="medium")
    with col3:
        if st.button("📈  Explain Machine Learning        →\nUnderstand models, algorithms, and metrics.", key="card_explain", use_container_width=True):
            clicked_prompt = "Explain Machine Learning models, algorithms, and key evaluation metrics."

    with col4:
        if st.button("🚀  Build an AI Project                 →\nGet step-by-step guidance for your AI projects.", key="card_project", use_container_width=True):
            clicked_prompt = "Give me a step-by-step roadmap to build an end-to-end Machine Learning project."

else:
    # Active Conversation Mode Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px;">
        <h3 style="margin:0; font-size:1.15rem; color:#FFFFFF;">Chat Session with <span style="color:#FFD43B;">Nova AI</span></h3>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -----------------------------------------------------------------------------
# 7. Single Fixed Chat Input Bar (At Screen Bottom)
# -----------------------------------------------------------------------------
user_input = st.chat_input("Ask me anything about AI, ML, or Python...")

active_query = clicked_prompt if clicked_prompt else user_input

if active_query:
    st.session_state.messages.append({"role": "user", "content": active_query})
    st.rerun()

# Assistant Response Streaming
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    last_user_msg = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("Nova AI is thinking..."):
            reply = get_ai_response(last_user_msg)
            
            placeholder = st.empty()
            streamed = ""
            for word in reply.split(" "):
                streamed += word + " "
                placeholder.markdown(streamed + "▌")
                time.sleep(0.015)
            placeholder.markdown(reply)
            
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
