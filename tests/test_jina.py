from unittest.mock import patch, MagicMock
from src.tools.jina import extract

def test_extract_success():
    mock_text = "Article Title\nThis is the content.\nMore content here."
    
    with patch('requests.get', return_value=MagicMock(text=mock_text)):
        result = extract("https://example.com")
        assert result["title"] == "Article Title"
        assert result["content"] == "This is the content.\nMore content here."
        assert result["word_count"] == 7

def test_extract_empty():
    with patch('requests.get', return_value=MagicMock(text="")):
        result = extract("https://example.com")
        assert result["title"] == ""
        assert result["content"] == ""
        assert result["word_count"] == 0

def test_extract_error():
    with patch('requests.get', side_effect=Exception("timeout")):
        result = extract("https://example.com")
        assert result["word_count"] == 0
        assert result["title"] == ""