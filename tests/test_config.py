import os
import pytest
from unittest.mock import patch

def test_config_loads_without_error():
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "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"}):
        from src import config
        assert config.OPENROUTER_API_KEY == "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"

def test_config_fallbacks():
    with patch.dict(os.environ, {}, clear=True):
        import importlib
        from src import config
        importlib.reload(config)
        assert config.OPENROUTER_BASE_URL == "https://openrouter.ai/api/v1"
        assert config.MODEL == "nvidia/nemotron-3-ultra-550b-a55b:free"
        assert config.OPENROUTER_API_KEY == "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"