import requests
import json
from typing import Optional, Dict, Any

class ModelClient:
    """Client to call LLM endpoints (OpenAI-compatible, vLLM, etc.)"""
    
    def __init__(self, endpoint: str, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key
        self.model_name = model_name
        
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.0) -> str:
        """Generate response from model endpoint."""
        # OpenAI-compatible endpoint
        if "openai" in self.endpoint.lower() or self.endpoint.endswith("/v1/chat/completions"):
            return self._call_openai(prompt, max_tokens, temperature)
        # vLLM endpoint (OpenAI-compatible)
        elif "vllm" in self.endpoint.lower() or ":8000" in self.endpoint:
            return self._call_vllm(prompt, max_tokens, temperature)
        # Generic endpoint
        else:
            return self._call_generic(prompt, max_tokens, temperature)
    
    def _call_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "model": self.model_name or "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            resp = requests.post(
                f"{self.endpoint}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise Exception(f"OpenAI call failed: {str(e)}")
    
    def _call_vllm(self, prompt: str, max_tokens: int, temperature: float) -> str:
        # vLLM uses OpenAI-compatible API
        if not self.endpoint.endswith("/v1"):
            self.endpoint += "/v1"
        return self._call_openai(prompt, max_tokens, temperature)
    
    def _call_generic(self, prompt: str, max_tokens: int, temperature: float) -> str:
        # Try generic completion endpoint
        headers = {"Content-Type": "application/json"}
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            resp = requests.post(
                f"{self.endpoint}/generate",
                headers=headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            return result.get("text", result.get("response", "")).strip()
        except Exception as e:
            raise Exception(f"Generic endpoint call failed: {str(e)}")

def get_model_response(model_endpoint: str, prompt: str, api_key: Optional[str] = None, model_name: Optional[str] = None) -> str:
    """Convenience function to get model response."""
    client = ModelClient(endpoint=model_endpoint, api_key=api_key, model_name=model_name)
    return client.generate(prompt)
