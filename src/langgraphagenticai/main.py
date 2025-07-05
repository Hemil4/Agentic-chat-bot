from email import message
import streamlit as st
from src.langgraphagenticai.ui.streamletui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.LLMS.ollamallm import OllamaLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamletui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness.
    """

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    user_message = st.chat_input("Enter your message:")

    if user_message: 
        try:
            # Initialize the appropriate LLM based on user selection
            selected_llm = user_input.get("selected_llm")
            
            if selected_llm == "Groq":
                obj_llm_config = GroqLLM(user_controls_input=user_input)
                model = obj_llm_config.get_llm_model()
            elif selected_llm == "Ollama":
                obj_llm_config = OllamaLLM(user_controls_input=user_input)
                model = obj_llm_config.get_llm_model()
            else:
                st.error(f"Error: Unsupported LLM selected: {selected_llm}")
                return

            if not model:
                st.error("Error: LLM model could not be initialized")
                return

            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No use case selected.")
                return
            
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                if graph:
                    display_result = DisplayResultStreamlit(usecase, graph, user_message)
                    display_result.display_result_on_ui()
                else:
                    st.error("Error: Failed to create graph")
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                print(f"Debug - Graph setup error: {e}")

        except Exception as e:
            st.error(f"Error: {e}")
            print(f"Debug - Main error: {e}")