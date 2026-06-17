from src.graph import graph
from src.models import ResearchState

def run_research(query: str):
    state = ResearchState(query=query)
    return graph.invoke(state)

if __name__ == "__main__":
    result = run_research("AI agent frameworks 2026")
    print(f"\nDone! Step: {result['current_step']}")
    print(f"Sources: {len(result['sources'])}")
    print(f"Sections: {len(result['outline'].sections)}")