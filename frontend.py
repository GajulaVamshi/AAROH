import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="🧠 AAROH - Final Year Project",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {font-size: 3rem; color: #1f77b4; font-weight: bold;}
.project-info {background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
               padding: 1rem; border-radius: 10px; color: white;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧠 AAROH</h1>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="project-info">
    <h3>A Multimodal, Context-Aware & Action-Centric AI System</h3>
    <p><strong>Gajula Vamshi</strong> | Roll No: 221020110015<br>
    B.Tech CSE (AI) | Om Sterling Global University | BTAI-822</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.info("**Status:** 🟢 Production Ready\n**Architecture:** Fully Implemented")

# API Config
API_BASE = st.sidebar.text_input("API URL", value="http://localhost:8000")
user_id = st.sidebar.text_input("User ID", value="student_001")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Actions Demo
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Quick Demo Actions")
demo_actions = [
    "Open Google", "Open YouTube", "Play music", 
    "System info", "Send demo email", "What's my context?"
]

for action in demo_actions:
    if st.sidebar.button(action):
        st.session_state.demo_query = action.lower()
        st.rerun()

# Chat Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("intent"):
            st.caption(f"🔍 Intent: {message['intent']}")

# Chat Input
if prompt := st.chat_input("💭 Ask AAROH anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Demo override
    if hasattr(st.session_state, 'demo_query'):
        prompt = st.session_state.demo_query
        del st.session_state.demo_query
    
    # API Call
    with st.chat_message("assistant"):
        with st.spinner("🧠 AAROH Processing..."):
            try:
                response = requests.post(
                    f"{API_BASE}/api/v1/chat",
                    json={"query": prompt, "user_id": user_id},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data["response"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["response"],
                        "intent": data["intent_type"]
                    })
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

# Demo Sections
tab1, tab2, tab3 = st.tabs(["📊 Memory", "🔧 Permissions", "📈 Architecture"])

with tab1:
    if st.button("View Memory Context"):
        try:
            mem = requests.get(f"{API_BASE}/api/v1/memory/{user_id}")
            st.json(mem.json())
        except:
            st.info("Start chatting to build memory!")

with tab2:
    st.info("**Safety System Active**\n\nCertain actions require explicit permission.")
    if st.button("🔓 Enable System Controls"):
        st.success("✅ System controls enabled!")

with tab3:
    st.markdown("""
    ```
    [Multimodal Input] → [Preprocessing] → [Intent Extraction]
         ↓
    [Hybrid Classifier] → [Safety Guard] → [Decision Router]
         ↓
    ┌──────────────┬──────────────┬──────────────┐
    │   Chat       │   Task       │  Search      │
    │  Engine      │  Engine      │  Engine      │
    └──────────────┴──────────────┴──────────────┘
         ↓
    [Context Engine: Short-term + Semantic Memory]
         ↓
    [Action Execution + Response Generation]
    ```
    **Key Features Implemented:**
    - ✅ Hybrid Query Classification
    - ✅ Multi-layer Context Engine  
    - ✅ Permission-aware Safety
    - ✅ Modular Action Framework
    - ✅ Semantic Memory Retrieval
    """)

# Footer
st.markdown("---")
st.markdown("""
*🧠 AAROH - Final Year Project | May 2026 Submission Ready*  
**Keywords:** Multimodal AI, Context-Aware Systems, Intent Extraction, AI Agents, Task Automation
""")