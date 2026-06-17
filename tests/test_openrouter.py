import pytest
from unittest.mock import patch, MagicMock
from src.tools import openrouter

def test_chat_success():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test response"
    
    with patch.object(openrouter.client.chat.completions, 'create', return_value=mock_response):
        result = openrouter.chat("Hello", max_tokens=100)
        assert result.choices[0].message.content == "Test response"

def test_chat_error():
    with patch.object(openrouter.client.chat.completions, 'create', side_effect=Exception("Rate limit")):
        with pytest.raises(RuntimeError, match="OpenRouter API error"):
            openrouter.chat("Hello")

def test_chat_empty_response():
    mock_response = MagicMock()
    mock_response.choices = []
    
    with patch.object(openrouter.client.chat.completions, 'create', return_value=mock_response):
        result = openrouter.chat("Hello")
        assert result.choices == []