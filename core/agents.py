import os
from langchain_xai import ChatXAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

# 1. Environment Variable Retrieval
# We wrap these in SecretStr to satisfy Pydantic validation in LangChain
xai_key = os.getenv("XAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

# 2. Worker LLM (Grok/xAI)
# If the key is missing, ChatXAI throws a ValidationError. 
# We pass it explicitly to ensure Cloud Run picks it up correctly.
if not xai_key:
    raise ValueError("XAI_API_KEY not found in environment variables.")

worker_llm = ChatXAI(
    model="grok-2-1212",
    xai_api_key=SecretStr(xai_key),
    temperature=0
)

# 3. Guard LLM (Gemini/Google)
# Used for auditing the worker's output
if not google_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

guard_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=SecretStr(google_key),
    temperature=0
)

# 4. Agent Logic Functions
def call_worker(state):
    """
    The Worker Agent analyzes the financial data using Grok.
    """
    messages = state["messages"]
    response = worker_llm.invoke(messages)
    return {"messages": [response]}

def call_guard(state):
    """
    The Guard Agent audits the Worker's response for accuracy and compliance.
    """
    messages = state["messages"]
    # Logic to evaluate the last message in the thread
    response = guard_llm.invoke(messages)
    return {"messages": [response]}