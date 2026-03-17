from typing import TypedDict
from langgraph.graph import StateGraph, END
from .agents import call_worker, call_guard

class AgentState(TypedDict):
    input: str
    output: str
    feedback: dict

def worker_node(state: AgentState):
    response = call_worker(state["input"])
    return {"output": response, "iterations": state.get("iterations", 0) + 1}

def guard_node(state: AgentState):
    feedback = call_guard(state["output"])
    return {"feedback": feedback.dict()}

def should_continue(state: AgentState):
    if state["feedback"]["recommended_action"] == "continue" or state["iterations"] > 2:
        return END
    return "worker"

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("worker", worker_node)
workflow.add_node("guard", guard_node)
workflow.set_entry_point("worker")
workflow.add_edge("worker", "guard")
workflow.add_conditional_edges("guard", should_continue)

agent_app = workflow.compile()