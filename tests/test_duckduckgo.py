import pytest
from unittest.mock import patch, MagicMock
from src.tools.duckduckgo import search

def test_search_extracts_real_url():
    mock_html = '''
    <div class="result">
        <a class="result__a" href="/l/?uddg=https%3A%2F%2Fexample.com%2Farticle">Test Title</a>
    </div>
    '''
    
    with patch('requests.post', return_value=MagicMock(text=mock_html)):
        with patch('requests.head', return_value=MagicMock(url="https://example.com/article")):
            results = search("test", max_results=1)
            assert len(results) == 1
            assert results[0]["url"] == "https://example.com/article"
            assert results[0]["title"] == "Test Title"

def test_search_empty_results():
    with patch('requests.post', return_value=MagicMock(text="<html></html>")):
        results = search("test")
        assert results == []

def test_search_no_redirect():
    mock_html = '''
    <div class="result">
        <a class="result__a" href="https://example.com/page">Direct Link</a>
    </div>
    '''
    
    with patch('requests.post', return_value=MagicMock(text=mock_html)):
        with patch('requests.head', return_value=MagicMock(url="https://example.com/page")):
            results = search("test", max_results=1)
            assert results[0]["url"] == "https://example.com/page"

def test_search_head_request_fails():
    mock_html = '''
    <div class="result">
        <a class="result__a" href="/l/?uddg=https%3A%2F%2Fexample.com">Title</a>
    </div>
    '''
    
    with patch('requests.post', return_value=MagicMock(text=mock_html)):
        with patch('requests.head', side_effect=Exception("timeout")):
            results = search("test", max_results=1)
            assert results[0]["url"] == "https://example.com"