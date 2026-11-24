from Backend.agentic_chatbot import chatbot
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import streamlit as st
import uuid


#generate a unique thread id for each new conversation

def generate_thread_id():
    return str(uuid.uuid4())


#add a new thread id to the conversation list
def add_thread(thread_id):
    #prevent the same thread from being added multiple times
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

# Create a complete new chat conversation
def reset_chat():

    #Generate and assign a new thread
    st.session_state["thread_id"] = generate_thread_id()
    # clear the current chat messages from the UI
    st.session_state["message_history"] = []
    # add the new thread to the conversation list
    add_thread(st.session_state["thread_id"])


#Load a previous conversation from the langGraph checkpointer

def load_conversation(thread_id):
    #Get the saved state for selected thread
    state = chatbot.get_state(
        config = {
            "configurable":{
                "thread_id": thread_id
            }
        }
    )
    #Return saved messages
    #Return an empty list if no messages are available
    return state.values.get("messages",[])

st.title("Agentic Chatbot")


# Create message history when app runs for the first time
if 'message_history' not in st.session_state:
    st.session_state['message_history']  = []

#create a thread ID when app runs for the first time
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

# Create a list for storing all conversation thread_ids

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

#add current thread to the conversation list
add_thread(st.session_state["thread_id"])

#               SIDEBAR FEATURE

#Display the sidebar title
st.sidebar.title("My Conversations")

# create a button for starting a new conversation

if st.sidebar.button("New Chat"):

    #Reset the current chat and create a new thread
    reset_chat()

    #Rerun the streamlit app to update the interface
    st.rerun()


#Display al the conversation threads in reverse order
#This shows the newest conversation first

for thread_id in st.session_state["chat_threads"][::-1]:
    # create one sidebar button fro every conversation
    if st.sidebar.button(
        str(thread_id),
        key=thread_id
    ):
        #set the selected thread as the current thread
        st.session_state["thread_id"]= thread_id

        #Load the messages saved under the selected thread
        messages = load_conversation(thread_id)

        # Temporary list for converting LangChain messages into streamlit's required message format
        temp_messages =[]

        #Loop through all saved messages
        for message in messages:

            #check whether the message was sent by the user
            if isinstance(message,HumanMessage):
                role = "user"

            #check whether the message was sent by AI
            elif isinstance(message,AIMessage):
                role = "assistant"
            #Ignore other message types such as tool message
            else:
                continue

            #convert the Langchain message into a dictionary
            temp_messages.append({
                "role":role,
                "content":message.content
            })     

        #Replace the current UI history with the selected conversation
        st.session_state["message_history"] = temp_messages 

        #Rerun the application to display the loaded messages
        st.rerun()

#Main chat Interface

#Display all messages from the currently selected conversation

for message in st.session_state["message_history"]:
    #create either a user chat bubble or assistant chat bubble
    with st.chat_message(message["role"]):

        #Display the message content
        st.text(message["content"])


#Create the chat input box

user_input = st.chat_input("Type here")

#Run this block after the user submits a message

if user_input:

    # Save the user's message in streamlit session state
    st.session_state["message_history"].append({
        "role":"user",
        "content":user_input
    })

    # Display the user's message in the chat interface
    with st.chat_message("user"):
        st.text(user_input)

    # Pass the current thread ID to the lang graph
    # LangGraph uses this ID to save and retrieve conversation memory

    CONFIG = {
        "configurable":{ "thread_id":st.session_state["thread_id"]}
    }

    # Create the assistant chat-message container
    with st.chat_message("assistant"):
        # stream the assistant response token by token
        ai_message = st.write_stream(
            #Return only the content  of AI message chunks
            message_chunk.content

            #Stream messages from the langGraph chatbot
            for message_chunk, metadata in chatbot.stream(
                {
                    #send the latest user message to the chatbot
                    "messages": [HumanMessage(content=user_input)]
                },

                #Use the curent conversation thread
                config=CONFIG,
                stream_mode="messages"
            )
            if isinstance(message_chunk,AIMessage)
        )

    # Save the complete assistant response in streamlit session state
    st.session_state["message_history"].append({
        "role":"assistant",
        "content": ai_message
    })   
        



