from langsmith import traceable
from src.models import ResearchState
from src.tools.openrouter import chat

@traceable(run_type="chain", name="evaluator")
def evaluator_node(state: ResearchState):
    outline_text = "".join([f"\n## {s.title}\n" + "".join([f"- {p}\n" for p in s.points]) for s in state.outline.sections])
    
    prompt = f"""Evaluate outline for: {state.query}
{outline_text}
Return EXACT format:
Intent Match: 0-100
Engagement: 0-100
Accuracy: 0-100
Readability: 0-100
Structure: 0-100
SEO: 0-100
CTA: 0-100
Overall: 0-100
Recommendation: one sentence"""

    try:
        response = chat(prompt, max_tokens=300, temperature=0.1)
        text = response.choices[0].message.content or ""
    except Exception:
        text = "Intent Match: 70\nEngagement: 70\nAccuracy: 70\nReadability: 70\nStructure: 70\nSEO: 70\nCTA: 70\nOverall: 70\nRecommendation: Default scores."

    scores = {}
    for line in text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if key in ["Intent Match", "Engagement", "Accuracy", "Readability", "Structure", "SEO", "CTA", "Overall"]:
                if digits := "".join([c for c in val if c.isdigit()]):
                    scores[key] = int(digits)
            elif "Recommendation" in key:
                scores["Recommendation"] = val

    for dim in ["Intent Match", "Engagement", "Accuracy", "Readability", "Structure", "SEO", "CTA", "Overall"]:
        if dim not in scores:
            scores[dim] = 70

    if "Recommendation" not in scores:
        scores["Recommendation"] = "No recommendation."

    state.evaluation = scores
    state.current_step = "complete"
    return state