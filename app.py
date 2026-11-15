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

    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)

    ai_message = response['messages'][-1].content
    #adding the response 1st to the message history
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)