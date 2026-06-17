from unittest.mock import patch, MagicMock
from src.nodes.coordinator import coordinator_node
from src.models import ResearchState

def test_coordinator_parses_angles():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "search_angles: comparison, benchmarks, use cases\ntarget_sources: 8\nreasoning: test"
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="AI agents")
        result = coordinator_node(state)
        assert result.research_plan["angles"] == ["comparison", "benchmarks", "use cases"]
        assert result.research_plan["target_sources"] == 8
        assert result.current_step == "searching"

def test_coordinator_fallback_empty_angles():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "target_sources: 3\nreasoning: missing angles"
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="AI agents")
        result = coordinator_node(state)
        assert result.research_plan["angles"] == ["overview", "comparison", "trends"]

def test_coordinator_fallback_api_error():
    with patch('src.nodes.coordinator.chat', side_effect=Exception("API down")):
        state = ResearchState(query="AI agents")
        result = coordinator_node(state)
        assert result.research_plan["angles"] == ["overview", "comparison", "trends"]
        assert result.research_plan["target_sources"] == 5
        assert result.current_step == "searching"

def test_coordinator_invalid_target():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "search_angles: test\ntarget_sources: abc\nreasoning: test"
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="AI agents")
        result = coordinator_node(state)
        assert result.research_plan["target_sources"] == 5