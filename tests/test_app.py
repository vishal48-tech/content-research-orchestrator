import sys
from unittest.mock import MagicMock, patch

def test_app_runs():
    # Create mock streamlit module
    mock_st = MagicMock()
    mock_st.text_input = MagicMock(return_value="test topic")
    mock_st.button = MagicMock(return_value=True)
    
    # Inject before import
    sys.modules['streamlit'] = mock_st
    
    # Also mock graph and other dependencies
    with patch('src.graph.graph') as mock_graph:
        mock_graph.invoke.return_value = {
            'query': 'test topic',
            'sources': [{'title': 'Test', 'url': 'https://example.com', 'credibility_score': 0.8}],
            'outline': type('obj', (object,), {
                'sections': [type('obj', (object,), {'title': 'Intro', 'points': ['Point 1']})()]
            })(),
            'evaluation': {'Overall': 75, 'Recommendation': 'Good'},
            'current_step': 'complete'
        }
        
        import importlib
        import app
        importlib.reload(app)
        
        assert hasattr(app, 'st')