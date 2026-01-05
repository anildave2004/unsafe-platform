"""
Mock LLM client for simulating Anthropic API calls.
This module provides a simple mock implementation for testing and development.
"""
from typing import Dict, Any, List, Optional


class MockAnthropicClient:
    """Mock client simulating Anthropic's Claude API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the mock client.
        
        Args:
            api_key: API key (ignored in mock implementation)
        """
        self.api_key = api_key or "mock_api_key"
        self.messages = MockMessages()
    

class MockMessages:
    """Mock messages API for creating completions."""
    
    def create(
        self,
        model: str,
        max_tokens: int,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> "MockResponse":
        """Create a mock completion.
        
        Args:
            model: Model name (e.g., "claude-3-5-sonnet-20241022")
            max_tokens: Maximum tokens to generate
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional arguments (ignored)
            
        Returns:
            MockResponse object with simulated completion
        """
        # Extract the user's question from messages
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        # Generate mock responses based on context
        response_text = self._generate_mock_response(user_message)
        
        return MockResponse(content=response_text, model=model)
    
    def _generate_mock_response(self, user_message: str) -> str:
        """Generate a contextual mock response based on the user message.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Simulated response text
        """
        lower_msg = user_message.lower()
        
        # Triage/classification responses
        if "classify" in lower_msg or "triage" in lower_msg or "analyze" in lower_msg:
            if "temperature" in lower_msg or "overheat" in lower_msg:
                return "CRITICAL: Temperature anomaly detected. Immediate attention required."
            elif "vibration" in lower_msg or "mechanical" in lower_msg:
                return "HIGH: Abnormal vibration pattern suggests mechanical failure risk."
            elif "network" in lower_msg or "connection" in lower_msg:
                return "MEDIUM: Network connectivity issue detected."
            else:
                return "LOW: Minor anomaly detected, monitoring recommended."
        
        # Risk assessment responses
        if "risk" in lower_msg or "financial" in lower_msg or "exposure" in lower_msg:
            return "Estimated financial exposure: $50,000. Risk score: 0.75. Immediate mitigation recommended."
        
        # Action/resolution responses
        if "action" in lower_msg or "resolve" in lower_msg or "mitigate" in lower_msg:
            return "Recommended actions: 1. Alert maintenance team, 2. Schedule inspection, 3. Enable backup systems."
        
        # Default response
        return "Mock LLM response: Request processed successfully."


class MockResponse:
    """Mock response object from LLM completion."""
    
    def __init__(self, content: str, model: str):
        """Initialize mock response.
        
        Args:
            content: Response text content
            model: Model name used
        """
        self.content = [MockContent(content)]
        self.model = model
        self.stop_reason = "end_turn"
        self.usage = {
            "input_tokens": 100,
            "output_tokens": 50
        }


class MockContent:
    """Mock content block in response."""
    
    def __init__(self, text: str):
        """Initialize mock content.
        
        Args:
            text: Content text
        """
        self.text = text
        self.type = "text"


def get_llm_client(api_key: Optional[str] = None) -> MockAnthropicClient:
    """Factory function to get LLM client.
    
    Args:
        api_key: Optional API key for authentication
        
    Returns:
        MockAnthropicClient instance
    """
    return MockAnthropicClient(api_key=api_key)
