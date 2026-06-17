from src.models import Source, OutlineSection, Outline, ResearchState

def test_source_defaults():
    s = Source()
    assert s.id == ""
    assert s.credibility_score == 0.5

def test_source_custom():
    s = Source(id="src_1", title="Test", url="https://example.com", content="Hello", word_count=2, credibility_score=0.9)
    assert s.title == "Test"
    assert s.word_count == 2

def test_outline_section():
    sec = OutlineSection(title="Intro", points=["Point 1", "Point 2"])
    assert len(sec.points) == 2

def test_research_state_defaults():
    state = ResearchState()
    assert state.current_step == "planning"
    assert state.sources == []

def test_research_state_full():
    state = ResearchState(
        query="AI agents",
        sources=[Source(id="src_1", title="Test")],
        outline=Outline(sections=[OutlineSection(title="Intro", points=["P1"])]),
        evaluation={"Overall": 80}
    )
    assert state.query == "AI agents"
    assert state.outline.sections[0].title == "Intro"

def test_state_serialization():
    state = ResearchState(query="test")
    data = state.model_dump()
    assert data["query"] == "test"
    assert "sources" in data