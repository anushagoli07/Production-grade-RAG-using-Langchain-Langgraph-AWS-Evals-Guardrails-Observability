from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from app.agents.nodes.planner import planner_node
from app.agents.nodes.responder import generate_node
from app.agents.nodes.retriever import retrieve_node
from app.agents.state import AgentState


def route_planner(state: AgentState) -> str:
    if state["current_query"] == "CONVERSATIONAL":
        return "responder"
    return "retriever"


workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("retriever", retrieve_node)
workflow.add_node("responder", generate_node)
workflow.set_entry_point("planner")
workflow.add_conditional_edges(
    "planner",
    route_planner,
    {"retriever": "retriever", "responder": "responder"},
)
workflow.add_edge("retriever", "responder")
workflow.add_edge("responder", END)

checkpointer = MemorySaver()
rag_agent = workflow.compile(checkpointer=checkpointer)
