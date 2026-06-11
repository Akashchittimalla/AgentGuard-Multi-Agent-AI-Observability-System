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

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing conversation history first
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask about financial tasks...")

if user_input:
    # Show user message immediately without waiting for the model
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run the LangGraph workflow
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = agent_app.invoke({"messages": [HumanMessage(content=user_input)]})

        # Only extract AIMessages — the result also contains the input HumanMessage
        # which would cause the prompt to appear twice if we iterated all messages
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                st.markdown(msg.content)
                st.session_state.messages.append({"role": "assistant", "content": msg.content})
