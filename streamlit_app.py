import streamlit as st
import requests
import os
from dotenv import load_dotenv
import sqlite3

# Load environment variables
load_dotenv()

# Get API endpoint from environment variable
chat_endpoint_template = f"{os.getenv('CHAT_API_ENDPOINT')}?customer_id=2&chat_history=[]&question={{query}}"

# Setup mock database connection
conn = sqlite3.connect('chat_history.db')
cursor = conn.cursor()

# Create a simple table
cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                (id INTEGER PRIMARY KEY, user_input TEXT)''')

# Show title and description.
st.title("Contoso Outdoors 💬 Chatbot")
st.info("This is a simple chatbot built to interface with https://github.com/azure-samples/contoso-chat")
st.write("Hi! I'm Tom Woodsman, your AI assistant. How can I help you today?")

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message.
# This will display automatically at the bottom of the page.
if prompt := st.chat_input("Please enter your message"):
    # Store and display the current prompt as plain text
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    last_message_content = st.session_state.messages[-1]["content"]
    chat_endpoint = chat_endpoint_template.format(query=last_message_content)

    # Call post request to chat endpoint
    response = requests.post(chat_endpoint)
    response_data = response.json()

    # Extract answer and context
    answer = response_data.get("answer")
    context = response_data.get("context", [])

    # Display the answer
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)

    # Display the context
    for item in context:
        st.markdown(f"**{item['title']}**")
        st.markdown(item['content'])
        st.markdown(f"[Learn more]({item['url']})")

    # Append the answer to the chat messages.
    st.session_state.messages.append({"role": "assistant", "content": response_data})