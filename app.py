from Backend.agentic_chatbot import chatbot
from langchain_core.messages import BaseMessage, HumanMessage
import streamlit as st

CONFIG = {'configurable':{'thread_id': 'thread-1'}}

st.title("Agentic Chatbot")

if 'message_history' not in st.session_state:
    st.session_state['message_history']  = []


# loading the convesation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

st.write('user:', user_input)

if user_input:
    #adding the message 1st to the message history
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    #adding message to the message history
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
            {'messages':[HumanMessage(content=user_input)]},config={'configurable':{'thread_id':'thread-1'}},
            stream_mode='messages' 
            )
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})    