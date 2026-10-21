# 🤖 Azure AI Chatbot

A modern, fast, and beautifully designed AI Chatbot powered by **Azure OpenAI (`gpt-4.1-mini`)** and built with **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=flat-square&logo=streamlit)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-gpt--4.1--mini-0078D4?style=flat-square&logo=microsoftazure)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- ⚡ **Real-Time Token Streaming**: Fast word-by-word streaming using Azure OpenAI Chat Completions SSE API.
- 🎨 **Modern SaaS UI**: Clean, human-crafted conversational layout inspired by ChatGPT and Claude.
- 💬 **Conversational Memory**: Full multi-turn session chat history with one-click clear button.
- ⚙️ **Configurable Parameters**: Interactive sidebar with real-time temperature slider and customizable system prompts.
- 🔒 **Secure Environment**: API credentials managed cleanly through `.env` environment variables.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ahmeddevz25/azure-ai-chatbot.git
cd azure-ai-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure credentials
Copy the example environment file and add your Azure credentials:
```bash
cp .env.example .env
```
Inside `.env`, configure:
```env
AZURE_OPENAI_ENDPOINT=https://<your-resource>.services.ai.azure.com/openai/v1/chat/completions
AZURE_OPENAI_API_KEY=your_azure_api_key_here
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini
```

### 4. Run the chatbot
```bash
streamlit run chatbot.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
├── .streamlit/
│   └── config.toml        # Streamlit theme and UI configurations
├── chatbot.py             # Main Streamlit web application
├── chatbot.ipynb          # Jupyter Notebook exploration and API test suite
├── requirements.txt       # Python dependencies
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore configuration
└── README.md              # Project documentation
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
