from langsmith import traceable
from langgraph.graph import StateGraph, END
from src.models import ResearchState
from src.nodes.coordinator import coordinator_node
from src.nodes.search import search_node
from src.nodes.synthesis import synthesis_node
from src.nodes.evaluator import evaluator_node
from src.nodes.assembly import assembly_node

@traceable(run_type="chain", name="build_graph")
def build_graph():
    builder = StateGraph(ResearchState)
    
    builder.add_node("coordinator", coordinator_node)
    builder.add_node("search", search_node)
    builder.add_node("synthesis", synthesis_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("assembly", assembly_node)
    
    builder.set_entry_point("coordinator")
    builder.add_edge("coordinator", "search")
    builder.add_edge("search", "synthesis")
    builder.add_edge("synthesis", "evaluator")
    builder.add_edge("evaluator", "assembly")
    builder.add_edge("assembly", END)
    
    return builder.compile()

graph = build_graph()