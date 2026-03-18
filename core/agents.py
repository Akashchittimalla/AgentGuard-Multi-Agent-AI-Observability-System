import os
import json
from langchain_xai import ChatXAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from langchain_core.messages import HumanMessage, AIMessage

# 1. Environment Variable Retrieval
xai_key = os.getenv("XAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

# 2. LLM Initialization
if not xai_key or not google_key:
    raise ValueError("Missing API Keys in environment variables.")

worker_llm = ChatXAI(
    model="grok-4-latest",
    xai_api_key=SecretStr(xai_key),
    temperature=0
)

guard_llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    max_retries=6  # Handles the "Rate Limit" by waiting automatically
)

# 3. Agent Functions
def call_worker(state):
    """The Worker (Grok) generates the initial financial response."""
    messages = state["messages"]
    response = worker_llm.invoke(messages)
    return {"messages": [response]}

def call_guard(state):
    last_worker_message = state["messages"][-1].content
    
    audit_prompt = f"""
    ROLE: Financial Compliance Auditor
    TASK: Review the following AI-generated financial response for risk.
    
    RESPONSE TO REVIEW: "{last_worker_message}"
    
    CRITERIA:
    - Does it suggest specific stocks to buy?
    - Does it promise a 'double' or 'moon' return?
    - Is it giving definitive investment advice?

    IF RISK FOUND: Respond ONLY with the prefix "RISK DETECTED" followed by a 1-sentence reason.
    IF NO RISK: Respond ONLY with "CLEAN".
    """
    
    response = guard_llm.invoke([HumanMessage(content=audit_prompt)])
    return {"messages": [response]}