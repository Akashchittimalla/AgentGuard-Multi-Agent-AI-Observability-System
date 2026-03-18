from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, AIMessage
import operator

# 1. Define the State (how data moves between nodes)
class AgentState(TypedDict):
    # This 'operator.add' allows us to append new messages to the history
    messages: Annotated[List[BaseMessage], operator.add]

# 2. Define the Router (The Decision Maker)
def should_continue(state: AgentState):
    """
    Checks the last message from the Guard. 
    If 'RISK DETECTED' is found, we route to 'sanitize'.
    """
    last_message = state["messages"][-1].content
    if "RISK DETECTED" in last_message.upper():
        return "sanitize"
    return END

# 3. Define the Sanitize Node
def sanitize_response(state: AgentState):
    """
    Replaces a risky response with a professional compliance disclaimer.
    """
    disclaimer = (
        "⚠️ **Compliance Notice:** The previous response was intercepted. "
        "AgentGuard has detected high-risk financial advice that violates "
        "regulatory safety guidelines (e.g., 'Get Rich Quick' or 'Stock Tipping'). "
        "\n\n*Please consult a licensed financial advisor for investment decisions.*"
    )
    return {"messages": [AIMessage(content=disclaimer)]}

# 4. Build the Workflow
workflow = StateGraph(AgentState)

# Add our nodes from agents.py and the new sanitize node
from core.agents import call_worker, call_guard

workflow.add_node("worker", call_worker)
workflow.add_node("guard", call_guard)
workflow.add_node("sanitize", sanitize_response)

# Connect the nodes
workflow.set_entry_point("worker")
workflow.add_edge("worker", "guard")

# Logic: After Guard, check if we need to sanitize or finish
workflow.add_conditional_edges(
    "guard",
    should_continue,
    {
        "sanitize": "sanitize",
        END: END
    }
)

# Compile the graph
agent_app = workflow.compile()