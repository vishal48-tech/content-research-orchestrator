# tests/test_coordinator_parsing.py

import pytest
from src.models import ResearchState
from src.nodes.coordinator import coordinator_node
from unittest.mock import patch, MagicMock

def test_coordinator_parses_strict_format():
    """Test parsing when model returns exact format."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = (
        "search_angles: latest frameworks, benchmark comparison, enterprise adoption\n"
        "target_sources: 6\n"
        "reasoning: Need current data plus real-world validation"
    )
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="AI agent frameworks 2026")
        result = coordinator_node(state)
        
        assert result.research_plan["angles"] == ["latest frameworks", "benchmark comparison", "enterprise adoption"]
        assert result.research_plan["target_sources"] == 6
        assert result.research_plan["reasoning"] == "Need current data plus real-world validation"
        assert result.current_step == "searching"

def test_coordinator_parses_markdown_format():
    """Test parsing when model returns markdown (bold, bullets, etc.)."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = (
        "**search_angles:**  \n"
        "1. **State‑of‑the‑art frameworks** – Identify recent platforms  \n"
        "2. **Architectural patterns** – Examine design principles  \n"
        "target_sources: 8\n"
        "reasoning: Complex topic needs deep dive"
    )
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="AI agent frameworks 2026")
        result = coordinator_node(state)
        
        # Should extract angles even with markdown
        assert len(result.research_plan["angles"]) > 0
        assert result.research_plan["target_sources"] == 8
        assert result.current_step == "searching"

def test_coordinator_api_error_fallback():
    """Test fallback when API fails."""
    with patch('src.nodes.coordinator.chat', side_effect=Exception("Rate limit")):
        state = ResearchState(query="fusion energy")
        result = coordinator_node(state)
        
        # Fallback should include query
        assert any("fusion energy" in a for a in result.research_plan["angles"])
        assert result.research_plan["target_sources"] == 5
        assert result.current_step == "searching"

def test_coordinator_empty_response_fallback():
    """Test fallback when model returns empty/invalid."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = ""
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="quantum computing")
        result = coordinator_node(state)
        
        # Fallback should include query
        assert any("quantum computing" in a for a in result.research_plan["angles"])
        assert result.current_step == "searching"

def test_coordinator_malformed_no_angles():
    """Test fallback when no angles found in response."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Here is my plan: I will search for things"
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="climate tech")
        result = coordinator_node(state)
        
        # Fallback should include query
        assert any("climate tech" in a for a in result.research_plan["angles"])
        assert result.current_step == "searching"

def test_coordinator_invalid_target_sources():
    """Test that invalid target_sources defaults to 5."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = (
        "search_angles: test1, test2\n"
        "target_sources: abc\n"
        "reasoning: test"
    )
    
    with patch('src.nodes.coordinator.chat', return_value=mock_response):
        state = ResearchState(query="test")
        result = coordinator_node(state)
        
        assert result.research_plan["target_sources"] == 5

def test_coordinator_query_aware_fallback():
    """Test that fallback angles are specific to query, not generic."""
    with patch('src.nodes.coordinator.chat', side_effect=Exception("API down")):
        state = ResearchState(query="cryptocurrency regulation 2026")
        result = coordinator_node(state)
        
        angles = result.research_plan["angles"]
        assert any("cryptocurrency" in a or "regulation" in a for a in angles)
        assert "overview" not in angles  # Should NOT be generic
        assert "comparison" not in angles  # Should NOT be generic