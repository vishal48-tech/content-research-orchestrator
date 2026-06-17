from unittest.mock import patch, MagicMock
from src.nodes.synthesis import synthesis_node
from src.models import ResearchState, Source

def test_synthesis_parses_outline():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "## 1. Introduction\n- AI agents are growing\n- Key frameworks exist\n## 2. LangGraph\n- Stateful graphs\n- Cyclic workflows"
    
    with patch('src.nodes.synthesis.chat', return_value=mock_response):
        state = ResearchState(
            query="AI agents",
            sources=[Source(id="src_1", title="Test", content="Content here", word_count=100)]
        )
        result = synthesis_node(state)
        assert len(result.outline.sections) == 2
        assert result.outline.sections[0].title == "1. Introduction"
        assert len(result.outline.sections[0].points) == 2
        assert result.current_step == "checkpoint_outline"

def test_synthesis_fallback_empty_response():
    with patch('src.nodes.synthesis.chat', side_effect=Exception("API error")):
        state = ResearchState(query="AI agents", sources=[])
        result = synthesis_node(state)
        assert len(result.outline.sections) == 2
        assert result.outline.sections[0].title == "1. Introduction"

def test_synthesis_no_bullet_points():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "## 1. Overview\n## 2. Details"
    
    with patch('src.nodes.synthesis.chat', return_value=mock_response):
        state = ResearchState(query="AI agents", sources=[])
        result = synthesis_node(state)
        assert len(result.outline.sections) == 2
        assert result.outline.sections[0].points == []

def test_synthesis_malformed_no_sections():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Just some text without headers"
    
    with patch('src.nodes.synthesis.chat', return_value=mock_response):
        state = ResearchState(query="AI agents", sources=[])
        result = synthesis_node(state)
        assert len(result.outline.sections) == 1
        assert result.outline.sections[0].title == "Overview"