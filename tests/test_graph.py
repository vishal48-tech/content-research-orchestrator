from unittest.mock import patch, MagicMock
from src.graph import graph
from src.models import ResearchState

def test_full_graph_runs():
    def mock_chat(prompt, **kwargs):
        print(f"DEBUG: {prompt[:80]}...")
        response = MagicMock()
        response.choices = [MagicMock()]
        
        prompt_lower = prompt.lower()
        
        if "research plan" in prompt_lower:
            content = "search_angles: overview, comparison\ntarget_sources: 2\nreasoning: test"
        elif "create outline" in prompt_lower:
            content = "## 1. Intro\n- Point 1\n## 2. Details\n- Point 2"
        elif "evaluate outline" in prompt_lower:
            content = "Intent Match: 80\nEngagement: 70\nAccuracy: 75\nReadability: 80\nStructure: 70\nSEO: 60\nCTA: 50\nOverall: 70\nRecommendation: Good."
        else:
            content = "test"
        
        response.choices[0].message.content = content
        return response

    # Patch at the source module where chat is defined
    with patch('src.tools.openrouter.chat', side_effect=mock_chat):
        with patch('src.nodes.search.web_search', return_value=[
            {"title": "Result", "url": "https://example.com"}
        ]):
            with patch('src.nodes.search.extract', return_value={
                "title": "Article", "content": "Words " * 100, "word_count": 200
            }):
                state = ResearchState(query="AI agents")
                result = graph.invoke(state)
                
                assert result["current_step"] == "complete"
                assert len(result["sources"]) > 0
                assert len(result["outline"].sections) > 0
                assert "Overall" in result["evaluation"]

def test_graph_with_empty_query():
    with patch('src.tools.openrouter.chat', side_effect=Exception("API error")):
        with patch('src.nodes.search.web_search', return_value=[]):
            state = ResearchState(query="")
            result = graph.invoke(state)
            assert result["current_step"] == "complete"

def test_graph_state_preserved():
    with patch('src.tools.openrouter.chat', side_effect=Exception("API error")):
        with patch('src.nodes.search.web_search', return_value=[]):
            state = ResearchState(query="test", research_plan={"angles": ["a"], "target_sources": 1})
            result = graph.invoke(state)
            assert result["query"] == "test"