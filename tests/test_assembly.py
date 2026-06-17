from unittest.mock import patch
from src.nodes.assembly import assembly_node
from src.models import ResearchState, Source, Outline, OutlineSection

def test_assembly_prints_output(capsys):
    state = ResearchState(
        query="AI agents",
        sources=[Source(id="src_1", title="Test Article", url="https://example.com", credibility_score=0.8)],
        outline=Outline(sections=[OutlineSection(title="Intro", points=["Point 1", "Point 2"])]),
        evaluation={"Intent Match": 80, "Overall": 75, "Recommendation": "Add more."}
    )
    
    result = assembly_node(state)
    
    captured = capsys.readouterr()
    assert "FINAL RESEARCH OUTPUT" in captured.out
    assert "AI agents" in captured.out
    assert "Test Article" in captured.out
    assert "80" in captured.out
    assert "Add more." in captured.out
    assert result.current_step == "planning"

def test_assembly_empty_sources(capsys):
    state = ResearchState(
        query="Empty",
        sources=[],
        outline=Outline(sections=[]),
        evaluation={}
    )
    
    assembly_node(state)
    
    captured = capsys.readouterr()
    assert "FINAL RESEARCH OUTPUT" in captured.out
    assert "Empty" in captured.out

def test_assembly_missing_eval_scores(capsys):
    state = ResearchState(
        query="Test",
        sources=[],
        outline=Outline(sections=[]),
        evaluation={"Recommendation": "Test rec"}
    )
    
    assembly_node(state)
    
    captured = capsys.readouterr()
    assert "N/A" in captured.out
    assert "Test rec" in captured.out