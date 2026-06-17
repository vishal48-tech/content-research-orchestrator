from langsmith import traceable
from src.tools.openrouter import chat
from src.models import ResearchState

@traceable(run_type="chain", name="coordinator")
def coordinator_node(state: ResearchState):
    prompt = f"""You are a research coordinator. Create a research plan for: {state.query}

CRITICAL: Return ONLY this exact format. No markdown. No bold. No bullet points. No explanations.

search_angles: angle1, angle2, angle3
target_sources: 5
reasoning: brief strategy

Example response:
search_angles: latest releases, performance benchmarks, enterprise use cases
target_sources: 6
reasoning: Need current data plus real-world validation"""

    try:
        response = chat(prompt, max_tokens=200, temperature=0.2)
        text = response.choices[0].message.content or ""
    except Exception as e:
        # API error — log it, use query-aware fallback
        print(f"API error: {e}")
        text = f"search_angles: {state.query} overview, {state.query} latest, {state.query} comparison\ntarget_sources: 5\nreasoning: API fallback for {state.query}"

    # Now parse — if parsing fails, we still have the fallback from above
    angles = []
    target = 5
    reasoning = ""

    for line in text.split("\n"):
        line = line.strip().replace("**", "").replace("*", "")
        if line.startswith("search_angles:"):
            content = line.replace("search_angles:", "").strip()
            angles = [a.strip() for a in content.split(",") if a.strip()]
        elif line.startswith("target_sources:"):
            val = line.replace("target_sources:", "").strip()
            if val.isdigit():
                target = int(val)
        elif line.startswith("reasoning:"):
            reasoning = line.replace("reasoning:", "").strip()

    # If still no angles, use query-aware fallback
    if not angles:
        angles = [f"{state.query} overview", f"{state.query} trends", f"{state.query} comparison"]
        reasoning = f"Parsing fallback for {state.query}"
    
    state.research_plan = {"angles": angles, "target_sources": target, "reasoning": reasoning}
    state.current_step = "searching"
    return state