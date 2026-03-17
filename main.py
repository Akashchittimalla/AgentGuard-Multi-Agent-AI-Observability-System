import streamlit as st
import logfire
import os
import asyncio
from dotenv import load_dotenv
from utils.helpers import render_stats_sidebar

# Import your graph and helpers
try:
    from core.graph import agent_app
    from utils.helpers import render_stats_sidebar
except ImportError as e:
    st.error(f"Mapping Error: Ensure 'core/graph.py' and 'utils/helpers.py' exist. {e}")

# 1. Initialize Environment & Observability
if os.path.exists(".env"):
    load_dotenv()

# Configure Logfire
logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))
logfire.instrument_pydantic()

# 2. Page Config
st.set_page_config(
    page_title="AgentGuard NOC", 
    page_icon="🛡️", 
    layout="wide"
)

# 3. Session State Initialization
if "history" not in st.session_state:
    st.session_state.history = []

# 4. Sidebar & Stats
render_stats_sidebar()

st.sidebar.markdown("---")
if st.sidebar.button("📊 View Live Traces (Logfire)"):
    st.sidebar.info("Check [logfire.pydantic.dev](https://logfire.pydantic.dev) for real-time spans.")

# 5. UI Header
st.title("🛡️ AgentGuard: Real-Time Observability")
st.caption("Monitoring Multi-Agent Orchestration: Grok-Beta (Worker) + Gemini-3-Flash (Guard)")

# Display previous chat history
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Main Chat Input
user_query = st.chat_input("Ask about financial tasks or risky advice...")

if user_query:
    # Append and show user input
    st.session_state.history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 7. Agent Logic Execution
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        log_container = st.container()
        final_response_text = "Processing..."
        
        initial_state = {"input": user_query, "iterations": 0}
        
        try:
            with logfire.span("agent_workflow", user_query=user_query):
                # Stream the graph updates
                for output in agent_app.stream(initial_state, stream_mode="updates"):
                    for node_name, state_update in output.items():
                        with log_container:
                            if node_name == "worker":
                                worker_out = state_update.get("output", "No response from worker.")
                                final_response_text = worker_out
                                st.info(f"🤖 **Worker (Grok)**: {worker_out}")
                            
                            elif node_name == "guard":
                                feedback = state_update.get("feedback")
                                # Use getattr for Pydantic objects or .get for dicts
                                score = getattr(feedback, 'risk_score', 0)
                                reason = getattr(feedback, 'reasoning', "Safe.")
                                
                                if score > 7:
                                    st.error(f"🚨 **Guard Intercepted!** Risk: {score}/10")
                                    st.write(f"**Reason:** {reason}")
                                    final_response_text = "🛑 **BLOCKED**: This response was flagged for high financial risk."
                                elif score > 3:
                                    st.warning(f"⚠️ **Guard Warning**: {reason}")
                                else:
                                    st.success(f"✅ **Guard Approved**")

            # Final response display
            st.markdown("---")
            st.subheader("Final Verified Response")
            st.write(final_response_text)
            
            # Save to history
            st.session_state.history.append({"role": "assistant", "content": final_response_text})

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
            logfire.error("Workflow failed", error=str(e))