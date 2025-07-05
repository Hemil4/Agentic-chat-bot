from logging import config
import streamlit as st
import os
import requests

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def get_ollama_models(self, base_url):
        """Fetch available models from Ollama server"""
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return models
            return self.config.get_ollama_default_models()
        except requests.exceptions.RequestException:
            return self.config.get_ollama_default_models()

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API KEY", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your Groq API key to proceed.")

            elif self.user_controls["selected_llm"] == "Ollama":
                # Ollama configuration
                st.subheader("Ollama Configuration")
                
                # Base URL configuration
                default_url = "http://localhost:11434"
                self.user_controls["ollama_base_url"] = st.text_input(
                    "Ollama Server URL", 
                    value=default_url,
                    help="URL where Ollama server is running"
                )
                
                # Check connection status
                try:
                    response = requests.get(f"{self.user_controls['ollama_base_url']}/api/tags", timeout=3)
                    if response.status_code == 200:
                        st.success("✅ Connected to Ollama server")
                        # Get available models
                        available_models = self.get_ollama_models(self.user_controls["ollama_base_url"])
                        if available_models:
                            self.user_controls["selected_ollama_model"] = st.selectbox(
                                "Select Model", 
                                available_models
                            )
                        else:
                            st.warning("No models found. Please pull a model first using 'ollama pull <model_name>'")
                    else:
                        st.error("❌ Cannot connect to Ollama server")
                except requests.exceptions.RequestException:
                    st.error("❌ Cannot connect to Ollama server. Make sure Ollama is running.")
                    # Show default models as fallback
                    default_models = self.config.get_ollama_default_models()
                    self.user_controls["selected_ollama_model"] = st.selectbox(
                        "Select Model (Default List)", 
                        default_models
                    )
                
                # Temperature setting
                self.user_controls["ollama_temperature"] = st.slider(
                    "Temperature", 
                    min_value=0.0, 
                    max_value=2.0, 
                    value=0.7, 
                    step=0.1,
                    help="Controls randomness in responses. Lower values make output more focused and deterministic."
                )
                
                # Instructions for setup
                with st.expander("🔧 Ollama Setup Instructions"):
                    st.markdown("""
                    **To use Ollama locally:**
                    1. Install Ollama from https://ollama.ai
                    2. Start Ollama server: `ollama serve`
                    3. Pull a model: `ollama pull llama3.2`
                    4. The server runs on http://localhost:11434 by default
                    
                    **Popular models to try:**
                    - `ollama pull llama3.2` - Latest Llama model
                    - `ollama pull mistral` - Mistral 7B model
                    - `ollama pull codellama` - Code-focused model
                    """)

            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)

            if self.user_controls["selected_usecase"]=="chatbot with webserch":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY API KEY",type="password")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app/tavily.com/home")
            
        return self.user_controls