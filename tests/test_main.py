from unittest.mock import patch, MagicMock
from src.main import run_research

def test_run_research():
    def mock_chat(prompt, **kwargs):
        response = MagicMock()
        response.choices = [MagicMock()]
        
        prompt_lower = prompt.lower()
        if "research plan" in prompt_lower:
            content = "search_angles: overview\ntarget_sources: 1\nreasoning: test"
        elif "outline" in prompt_lower:
            content = "## 1. Intro\n- Point 1"
        elif "evaluate" in prompt_lower:
            content = "Intent Match: 80\nOverall: 75\nRecommendation: Good."
        else:
            content = "test"
        
        response.choices[0].message.content = content
        return response

    with patch('src.tools.openrouter.chat', side_effect=mock_chat):
        with patch('src.nodes.search.web_search', return_value=[
            {"title": "Result", "url": "https://example.com"}
        ]):
            with patch('src.nodes.search.extract', return_value={
                "title": "Article", "content": "Words " * 100, "word_count": 200
            }):
                result = run_research("AI agents")
                assert result["current_step"] == "complete"
                assert len(result["sources"]) > 0

def test_run_research_empty_query():
    with patch('src.tools.openrouter.chat', side_effect=Exception("API error")):
        with patch('src.nodes.search.web_search', return_value=[]):
            result = run_research("")
            assert result["current_step"] == "complete"