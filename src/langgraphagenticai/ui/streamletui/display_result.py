import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        if usecase == "Basic Chatbot":
            # Create the input with proper message format
            input_messages = [HumanMessage(content=user_message)]
            
            try:
                # Display user message first
                with st.chat_message("user"):
                    st.write(user_message)
                
                # Stream the graph execution
                for event in graph.stream({'messages': input_messages}):
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
                st.error(f"Error during graph execution: {e}")
                print(f"Debug - Error details: {e}")
                print(f"Debug - User message: {user_message}")
                print(f"Debug - Graph type: {type(graph)}")

        elif usecase=="Chatbot With Web":
             # Prepare state and invoke the graph
            initial_state = {"messages": [user_message]}
            res = graph.invoke(initial_state)
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message)==ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif type(message)==AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)