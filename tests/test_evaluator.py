from unittest.mock import patch, MagicMock
from src.nodes.evaluator import evaluator_node
from src.models import ResearchState, Outline, OutlineSection

def test_evaluator_parses_scores():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Intent Match: 85\nEngagement: 70\nAccuracy: 80\nReadability: 75\nStructure: 60\nSEO: 50\nCTA: 40\nOverall: 65\nRecommendation: Add more details."

    with patch('src.nodes.evaluator.chat', return_value=mock_response):
        state = ResearchState(
            query="AI agents",
            outline=Outline(sections=[OutlineSection(title="Intro", points=["Point 1"])])
        )
        result = evaluator_node(state)
        assert result.evaluation["Intent Match"] == 85
        assert result.evaluation["Overall"] == 65
        assert result.evaluation["Recommendation"] == "Add more details."
        assert result.current_step == "complete"

def test_evaluator_fallback_api_error():
    with patch('src.nodes.evaluator.chat', side_effect=Exception("timeout")):
        state = ResearchState(
            query="AI agents",
            outline=Outline(sections=[OutlineSection(title="Intro", points=["Point 1"])])
        )
        result = evaluator_node(state)
        assert result.evaluation["Overall"] == 70
        assert result.evaluation["Recommendation"] == "Default scores."

def test_evaluator_missing_some_scores():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Intent Match: 90\nOverall: 80\nRecommendation: Good."

    with patch('src.nodes.evaluator.chat', return_value=mock_response):
        state = ResearchState(
            query="AI agents",
            outline=Outline(sections=[])
        )
        result = evaluator_node(state)
        assert result.evaluation["Intent Match"] == 90
        assert result.evaluation["Engagement"] == 70
        assert result.evaluation["Overall"] == 80

def test_evaluator_no_recommendation():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Intent Match: 50\nEngagement: 50"

    with patch('src.nodes.evaluator.chat', return_value=mock_response):
        state = ResearchState(query="AI agents", outline=Outline(sections=[]))
        result = evaluator_node(state)
        assert result.evaluation["Recommendation"] == "No recommendation."