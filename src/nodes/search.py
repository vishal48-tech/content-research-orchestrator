from langsmith import traceable
from src.models import ResearchState, Source
from src.tools.duckduckgo import search as web_search
from src.tools.jina import extract
from src.utils.scoring import score_source

@traceable(run_type="chain", name="search")
def search_node(state: ResearchState):
    angles = state.research_plan.get("angles", ["overview"])
    target = state.research_plan.get("target_sources", 5)
    
    all_sources = []
    for angle in angles:
        results = web_search(f"{state.query} {angle}", max_results=2)
        for r in results:
            extracted = extract(r["url"])
            if extracted["word_count"] > 50:
                all_sources.append(Source(
                    id=f"src_{len(all_sources)+1}",
                    title=extracted["title"] or r["title"],
                    url=r["url"],
                    content=extracted["content"],
                    word_count=extracted["word_count"],
                    credibility_score=score_source(r["url"], extracted["word_count"])
                ))
    
    state.sources = all_sources[:target]
    state.current_step = "checkpoint_sources"
    return state