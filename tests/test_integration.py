import pytest
from unittest.mock import patch, MagicMock
from src.models import ResearchState
from src.graph import build_graph

import src.nodes.coordinator as coord_module
import src.nodes.synthesis as synth_module
import src.nodes.evaluator as eval_module
import src.nodes.search as search_module

def test_end_to_end_pipeline(mock_chat, mock_search_results, mock_extracted_content):
    with patch.object(coord_module, 'chat', side_effect=mock_chat):
        with patch.object(synth_module, 'chat', side_effect=mock_chat):
            with patch.object(eval_module, 'chat', side_effect=mock_chat):
                with patch.object(search_module, 'web_search', return_value=mock_search_results):
                    with patch.object(search_module, 'extract', return_value=mock_extracted_content):
                        graph = build_graph()
                        state = ResearchState(query="AI agent frameworks 2026")
                        result = graph.invoke(state)
                        
                        assert result["current_step"] == "complete"
                        assert len(result["sources"]) == 2
                        assert len(result["outline"].sections) == 2
                        assert result["evaluation"]["Overall"] == 65

def test_pipeline_with_api_failure():
    with patch.object(coord_module, 'chat', side_effect=Exception("API down")):
        with patch.object(synth_module, 'chat', side_effect=Exception("API down")):
            with patch.object(eval_module, 'chat', side_effect=Exception("API down")):
                with patch.object(search_module, 'web_search', return_value=[]):
                    graph = build_graph()
                    state = ResearchState(query="test topic")
                    result = graph.invoke(state)
                    assert result["current_step"] == "complete"
                    assert result["sources"] == []

def test_pipeline_respects_source_limit(mock_chat, mock_extracted_content):
    def limited_chat(prompt, **kwargs):
        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message.content = "search_angles: overview\ntarget_sources: 3\nreasoning: test"
        return response

    with patch.object(coord_module, 'chat', side_effect=limited_chat):
        with patch.object(synth_module, 'chat', side_effect=mock_chat):
            with patch.object(eval_module, 'chat', side_effect=mock_chat):
                with patch.object(search_module, 'web_search', return_value=[
                    {"title": f"Result {i}", "url": f"https://example.com/{i}"}
                    for i in range(10)
                ]):
                    with patch.object(search_module, 'extract', return_value=mock_extracted_content):
                        graph = build_graph()
                        state = ResearchState(query="AI agents")
                        result = graph.invoke(state)
                        
                        assert len(result["sources"]) <= 3, f"Got {len(result['sources'])} sources"
                        assert result["research_plan"]["target_sources"] == 3