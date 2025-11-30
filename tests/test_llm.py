import pytest
from unittest.mock import patch, MagicMock
from core.llm_service import create_llm_service

@pytest.fixture
def llm_service():
    # Mock the API key environment variable if needed
    with patch.dict('os.environ', {'GOOGLE_API_KEY': 'dummy'}):
        return create_llm_service(provider="gemini")

def test_llm_service_init(llm_service):
    assert llm_service.provider == "gemini"

@patch('core.llm_service.LLMService.generate')
def test_generate(mock_generate, llm_service):
    mock_generate.return_value = "Test response"
    result = llm_service.generate([{"role": "user", "content": "test"}])
    assert isinstance(result, str)
    assert len(result) > 0
