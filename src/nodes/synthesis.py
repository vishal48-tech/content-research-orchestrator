from langsmith import traceable
from src.models import ResearchState, Outline, OutlineSection
from src.tools.openrouter import chat

@traceable(run_type="chain", name="synthesis")
def synthesis_node(state: ResearchState):
    source_text = "".join([f"\nSource {i+1}: {s.title}\n{s.content[:400]}..." for i, s in enumerate(state.sources)])
    
    prompt = f"""Create outline for: {state.query}
Sources:{source_text}
Format:
## 1. Title
- Point
## 2. Title
- Point"""

    try:
        response = chat(prompt, max_tokens=1000, temperature=0.3)
        text = response.choices[0].message.content or ""
    except Exception:
        text = f"## 1. Introduction\n- Overview of {state.query}\n## 2. Key Points\n- Main findings"

    outline = Outline(sections=[], raw=text)
    current = None
    
    for line in text.split("\n"):
        if line.startswith("## "):
            current = OutlineSection(title=line.replace("## ", "").strip())
            outline.sections.append(current)
        elif line.startswith("- ") and current:
            current.points.append(line.replace("- ", "").strip())
    
    if not outline.sections:
        outline.sections.append(OutlineSection(title="Overview", points=[f"Research on {state.query}"]))
    
    state.outline = outline
    state.current_step = "checkpoint_outline"
    return state