import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_chat():
    """Fixture for mocking OpenRouter chat calls."""
    def _mock_chat(prompt, **kwargs):
        response = MagicMock()
        response.choices = [MagicMock()]
        
        prompt_lower = prompt.lower()
        if "research plan" in prompt_lower:
            content = "search_angles: overview, comparison\ntarget_sources: 2\nreasoning: test"
        elif "create outline" in prompt_lower:
            content = "## 1. Introduction\n- Point 1\n## 2. Details\n- Point 2"
        elif "evaluate outline" in prompt_lower:
            content = "Intent Match: 85\nEngagement: 70\nAccuracy: 80\nReadability: 75\nStructure: 60\nSEO: 50\nCTA: 40\nOverall: 65\nRecommendation: Good."
        else:
            content = "test"
        
        response.choices[0].message.content = content
        return response
    
    return _mock_chat

@pytest.fixture
def mock_search_results():
    """Fixture for mock search results."""
    return [
        {"title": "LangGraph Guide", "url": "https://example.com/1"},
        {"title": "CrewAI Overview", "url": "https://example.com/2"}
    ]

@pytest.fixture
def mock_extracted_content():
    """Fixture for mock extracted content."""
    return {
        "title": "LangGraph Guide",
        "content": "LangGraph is a stateful framework for building multi-agent systems.",
        "word_count": 150
    }