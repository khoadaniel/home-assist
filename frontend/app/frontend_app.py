import requests
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st

st.set_page_config(
    page_title="Home Assist in Germany",
    page_icon="🤖",
    layout="wide"
)


st.title("Home Assist: Your AI Assistant for Settlement in Germany")

st.sidebar.write(
    """This Chatbot leverages RAG with GPT-3.5 to answer questions.""")

st.sidebar.image(
    "./img/sidebar_img.jpg",
    # width=300,
    caption="Brandenburger Tor | Photo: Daniel Le"
)

# Initialize the chat history in the session state
if "chat_history" not in st.session_state.keys():
    st.session_state.chat_history = []

# Initialize the chat
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "ai", "content": "Hello there, I am Home Assist, an AI to help you with questions regarding \
        your settlement in Germany. How can I help you today?"}
    ]

# Display all messages to streamlit
for message in st.session_state.messages:
    # More about method st.chat_message() here: https://docs.streamlit.io/library/api-reference/chat/st.chat_message
    # A standard format of a ChatMessage:
    # ChatMessage(content='May the force be with you', role='Jedi')
    with st.chat_message(name=message["role"]):
        st.write(message["content"])

# Require user input
human_question = st.chat_input()

if human_question is not None:
    # Add the human question to the session state (to print out in the chat window)
    new_human_message = {"role": "human", "content": human_question}
    st.session_state.messages.append(new_human_message)

    with st.chat_message("human"):
        st.write(human_question)


if st.session_state.messages[-1]["role"] != "ai":
    with st.chat_message(name="ai"):
        with st.spinner("Thinking..."):

            # The chat history is a list of HumanMessage and AIMessage objects, which will CANNOT be sent directly as json over the FastAPI endpoint
            # We need to serialize the chat history (LC msg objects)
            request_json = {"question": human_question or "I am human",
                            "chat_history": st.session_state.messages}

            print("====> request_json:\n", request_json, "\n")

            # Make a POST request to the FastAPI endpoint at 0.0.0.0:80/ask
            url = "http://homeassist_backend:8112/ask"
            response = requests.post(url,
                                     headers={
                                         "Content-Type": "application/json"},
                                     json=request_json)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                response_json = response.json()

                # Extract the 'output' field
                output = response_json["output"]["content"]
                print("====> output:\n", output, "\n")
                ai_msg = AIMessage(content=output)

            else:
                print("Failed to make request. Status code:",
                      response.status_code)

            # Print the AI message to Streamlit
            st.write(ai_msg.content)

            # Save the chat history in the session state
            new_ai_message = {"role": "ai", "content": ai_msg.content}
            st.session_state.messages.append(new_ai_message)
            st.session_state.chat_history.extend(
                [HumanMessage(content=human_question), ai_msg])
