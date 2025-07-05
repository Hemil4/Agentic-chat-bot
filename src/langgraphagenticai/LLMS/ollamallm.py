import streamlit as st
from langchain_ollama import ChatOllama
import requests
import json

class OllamaLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input
        self.default_base_url = "http://localhost:11434"

    def check_ollama_connection(self, base_url):
        """Check if Ollama server is running and accessible"""
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_available_models(self, base_url):
        """Get list of available models from Ollama server"""
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return models
            return []
        except requests.exceptions.RequestException:
            return []

    def get_llm_model(self):
        """Initialize and return Ollama LLM model"""
        try:
            base_url = self.user_controls_input.get("ollama_base_url", self.default_base_url)
            selected_model = self.user_controls_input.get("selected_ollama_model")
            
            # Check if Ollama server is running
            if not self.check_ollama_connection(base_url):
                st.error(f"Cannot connect to Ollama server at {base_url}. Please make sure Ollama is running.")
                return None
            
            # Check if model is selected
            if not selected_model:
                st.error("Please select an Ollama model")
                return None
            
            # Initialize ChatOllama (preferred for chat applications)
            llm = ChatOllama(
                model=selected_model,
                base_url=base_url,
                temperature=self.user_controls_input.get("ollama_temperature", 0.7)
            )
            
            return llm
            
        except Exception as e:
            st.error(f"Error occurred while initializing Ollama LLM: {e}")
            return None