import streamlit as st
import os

# Inject Streamlit secrets into env vars so core modules can use os.getenv()
try:
    for _k, _v in st.secrets.items():
        os.environ.setdefault(_k, str(_v))
except Exception:
    pass  # local .env file used instead

from langchain_core.messages import HumanMessage, AIMessage
from core.graph import agent_app

st.title("🛡️ AgentGuard: Real-Time Observability")

# Initialize Session State for Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask about financial tasks...")

if user_input:
    # 1. Add User message to state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Run the LangGraph Agentic Workflow
    inputs = {"messages": [HumanMessage(content=user_input)]}
    result = agent_app.invoke(inputs)
    
    # 3. SAFELY extract content to avoid "string indices" error
    # Result["messages"] contains LangChain objects (AIMessage)
    for msg in result["messages"]:
        # Extract the text content safely
        if hasattr(msg, 'content'):
            content_text = msg.content
        elif isinstance(msg, dict):
            content_text = msg.get("content", str(msg))
        else:
            content_text = str(msg)
            
        # Update UI state
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        st.session_state.messages.append({"role": role, "content": content_text})

# 4. Display Logic (The part that was crashing)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])