from src.models import ResearchState
from langsmith import traceable

@traceable(run_type="chain", name="assembly")
def assembly_node(state: ResearchState):
    print("=" * 50)
    print("FINAL RESEARCH OUTPUT")
    print("=" * 50)
    print(f"\n## {state.query}\n")
    
    for s in state.outline.sections:
        print(f"### {s.title}")
        for p in s.points:
            print(f"  - {p}")
        print()
    
    print("## SOURCES")
    for src in state.sources:
        print(f"[{src.id}] [{src.title}]({src.url}) (score: {src.credibility_score})")
    
    print("\n## EVALUATION")
    for key in ["Intent Match", "Engagement", "Accuracy", "Readability", "Structure", "SEO", "CTA", "Overall"]:
        print(f"  {key}: {state.evaluation.get(key, 'N/A')}")
    print(f"\n  Recommendation: {state.evaluation.get('Recommendation', 'None')}")
    
    return state