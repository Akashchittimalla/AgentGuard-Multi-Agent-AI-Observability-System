import streamlit as st

def render_stats_sidebar():
    """
    Renders the NOC (Network Operations Center) stats in the sidebar.
    """
    st.sidebar.title("🛡️ System Status")
    
    # Static Stats for the dashboard
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Guard Latency", "1.2s", "-0.1s")
        st.metric("Worker Load", "45%", "5%")
    with col2:
        st.metric("Risk Intercepts", "12", "+2")
        st.metric("Uptime", "99.9%")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Live Logs")
    # This creates a small scrolling log effect in the sidebar
    st.sidebar.code("Worker: Grok-Beta\nGuard: Gemini-3-Flash\nStatus: Monitoring...", language="text")