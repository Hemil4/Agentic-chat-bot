import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json
import traceback


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        print(f"Debug - Usecase: '{usecase}'")
        print(f"Debug - User message: '{user_message}'")
        
        try:
            if usecase == "Basic Chatbot":
                self._handle_basic_chatbot()
            elif usecase in ["chatbot with webserch", "Chatbot With Web"]:
                self._handle_chatbot_with_websearch()
            else:
                st.error(f"Unknown usecase: '{usecase}'")
                print(f"Debug - Unknown usecase: '{usecase}'")
                
        except Exception as e:
            st.error(f"Error in display_result_on_ui: {e}")
            print(f"Debug - Full error: {traceback.format_exc()}")

    def _handle_basic_chatbot(self):
        """Handle basic chatbot functionality"""
        try:
            # Create the input with proper message format
            input_messages = [HumanMessage(content=self.user_message)]
            
            # Display user message first
            with st.chat_message("user"):
                st.write(self.user_message)
            
            # Stream the graph execution
            for event in self.graph.stream({'messages': input_messages}):
                print(f"Debug - Event: {event}")
                for value in event.values():
                    print(f"Debug - Value: {value}")
                    if 'messages' in value:
                        messages = value['messages']
                        print(f"Debug - Messages: {messages}")
                        print(f"Debug - Messages type: {type(messages)}")
                        
                        # Handle the messages (should be a list of message objects)
                        if isinstance(messages, list) and len(messages) > 0:
                            # Get the last message (should be the AI response)
                            last_message = messages[-1]
                            print(f"Debug - Last message: {last_message}")
                            print(f"Debug - Last message type: {type(last_message)}")
                            
                            # Check if it's an AI message and extract content
                            if hasattr(last_message, 'content'):
                                response_content = last_message.content
                                print(f"Debug - Response content: {response_content}")
                                
                                # Display assistant response
                                with st.chat_message("assistant"):
                                    st.write(response_content)
                            else:
                                print(f"Debug - Message has no content attribute: {last_message}")
                                with st.chat_message("assistant"):
                                    st.write(str(last_message))
                        else:
                            print(f"Debug - Messages is not a proper list: {messages}")
                            
        except Exception as e:
            st.error(f"Error during basic chatbot execution: {e}")
            print(f"Debug - Basic chatbot error: {traceback.format_exc()}")

    def _handle_chatbot_with_websearch(self):
        """Handle chatbot with web search functionality"""
        try:
            # Display user message first
            with st.chat_message("user"):
                st.write(self.user_message)
            
            # Prepare state and invoke the graph
            initial_state = {"messages": [HumanMessage(content=self.user_message)]}
            print(f"Debug - Initial state: {initial_state}")
            
            # Check if graph is valid
            if not self.graph:
                st.error("Graph is not initialized properly")
                return
            
            # Invoke the graph
            print("Debug - Invoking graph...")
            res = self.graph.invoke(initial_state)
            print(f"Debug - Graph response: {res}")
            
            if not res:
                st.error("No response from graph")
                return
            
            if 'messages' not in res:
                st.error("Invalid response format from graph")
                print(f"Debug - Response keys: {res.keys() if hasattr(res, 'keys') else 'No keys'}")
                return
            
            # Process messages
            messages = res['messages']
            print(f"Debug - Processing {len(messages)} messages")
            
            # Track if we've shown search indicator
            search_indicated = False
            
            for i, message in enumerate(messages):
                print(f"Debug - Message {i}: {type(message)} - {message}")
                
                if isinstance(message, HumanMessage):
                    # Skip user message as we already displayed it
                    continue
                    
                elif isinstance(message, AIMessage):
                    # Check if this is a tool-calling message
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        if not search_indicated:
                            with st.chat_message("assistant"):
                                st.write("🔍 **Searching the web...**")
                            search_indicated = True
                    elif hasattr(message, 'content') and message.content:
                        # This is the final AI response
                        with st.chat_message("assistant"):
                            st.write(message.content)
                    else:
                        print(f"Debug - AI message with no content: {message}")
                        
                elif isinstance(message, ToolMessage):
                    # Don't display raw tool messages, they're processed into the final AI response
                    print(f"Debug - Tool message received (not displayed): {message}")
                    continue
                    
                else:
                    print(f"Debug - Unknown message type: {type(message)}")
                        
        except Exception as e:
            st.error(f"Error during web search chatbot execution: {e}")
            print(f"Debug - Web search error: {traceback.format_exc()}")
            
            # Additional debugging info
            print(f"Debug - Graph type: {type(self.graph)}")
            print(f"Debug - Graph methods: {dir(self.graph)}")
            
            # Try to get more info about the error
            try:
                if hasattr(self.graph, '__dict__'):
                    print(f"Debug - Graph attributes: {self.graph.__dict__.keys()}")
            except:
                pass