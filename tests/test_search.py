from unittest.mock import patch, MagicMock
from src.nodes.search import search_node
from src.models import ResearchState

def test_search_finds_sources():
    with patch('src.nodes.search.web_search', return_value=[
        {"title": "Result 1", "url": "https://example.com/1"},
        {"title": "Result 2", "url": "https://example.com/2"}
    ]):
        with patch('src.nodes.search.extract', side_effect=[
            {"title": "Article 1", "content": "This is a long article with many words here.", "word_count": 100},
            {"title": "Article 2", "content": "Short.", "word_count": 10}
        ]):
            state = ResearchState(
                query="AI agents",
                research_plan={"angles": ["overview"], "target_sources": 5}
            )
            result = search_node(state)
            assert len(result.sources) == 1
            assert result.sources[0].title == "Article 1"
            assert result.current_step == "checkpoint_sources"

def test_search_no_results():
    with patch('src.nodes.search.web_search', return_value=[]):
        state = ResearchState(
            query="AI agents",
            research_plan={"angles": ["overview"], "target_sources": 5}
        )
        result = search_node(state)
        assert result.sources == []
        assert result.current_step == "checkpoint_sources"

def test_search_filters_low_content():
    with patch('src.nodes.search.web_search', return_value=[
        {"title": "Thin", "url": "https://example.com"}
    ]):
        with patch('src.nodes.search.extract', return_value={
            "title": "Thin", "content": "Hi.", "word_count": 30
        }):
            state = ResearchState(
                query="AI agents",
                research_plan={"angles": ["overview"], "target_sources": 5}
            )
            result = search_node(state)
            assert result.sources == []

def test_search_respects_target():
    with patch('src.nodes.search.web_search', return_value=[
        {"title": f"Result {i}", "url": f"https://example.com/{i}"}
        for i in range(10)
    ]):
        with patch('src.nodes.search.extract', return_value={
            "title": "Article", "content": "Words " * 100, "word_count": 200
        }):
            state = ResearchState(
                query="AI agents",
                research_plan={"angles": ["overview"], "target_sources": 3}
            )
            result = search_node(state)
            assert len(result.sources) == 3