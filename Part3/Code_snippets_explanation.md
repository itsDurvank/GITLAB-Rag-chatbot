## File 3: streamlit.py - The Interactive Chat Interface

This file creates the web application that users interact with.


### Streamlit Configuration (MUST be first!)
```
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Part2.llm_integration import setup_api_key, build_qa_chain

import streamlit as st
st.set_page_config("GitLab GenAI Chatbot", page_icon="🤖", layout="wide")
```

**What these lines do:**
- **Line 1**: Imports os for system operations
- **Line 2**: Imports sys to access and modify Python’s runtime environment
- **Line 3**: Ensures Python can find and import modules from the project’s parent folder.
- **Line 4**: Imports setup_api_key and build_qa_chain from the Part2 folder.
- **Line 5**: Imports Streamlit, the web framework
- **Line 6**: Configures the web page title, icon, and layout

**Why this MUST be first:**
- Streamlit requires page configuration before any other Streamlit commands
- If you put this after other st. commands, you'll get an error


### API Key Setup with Security
```python
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Google API Key not found. Please add it to Streamlit secrets.")
    st.stop()
```

**What each line does:**
- **Line 1**: Checks if the API key exists in Streamlit's secure secrets
- **Line 2**: If found, sets it as an environment variable for the AI model to use
- **Line 3**: If not found, shows an error message
- **Line 4**: Stops the application from running without the API key

**Why this approach:**
- **Security**: API keys never appear in code that gets shared publicly
- **Flexibility**: Different environments (development, production) can use different keys
- **Error handling**: Clear message if setup is incomplete

### LOAD QA Chain 
qa_chain = build_qa_chain()

**What each line does:**
- **Line 1**: Loads the QA chain from backend(llm_integration.py)


# ------------------------------
# 🖼️ Streamlit UI Setup
# ------------------------------
```
st.title("🤖 GitLab Handbook & Direction AI Chatbot")
st.markdown("""
Welcome! This GenAI assistant helps GitLab team members and future employees learn about:
- 📘 GitLab's Handbook (culture, engineering, async, etc.)
- 🧭 GitLab's Product Direction (strategy, themes, FY25+)

Just ask your question below and the chatbot will find answers from official GitLab docs.
""")
```

**What each line does:**
- **Line 1**: Creates a large title with emoji for visual appeal
- **Lines 2-8**: Creates a welcome message with formatting and bullet points


# Chat session state
```
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.chat_input("Ask me anything about GitLab... ✨")
```
**What each line does:**
- **Line 1**: Checks if chat history exists in browser session
- **Line 2**: Creates empty chat history if this is first visit
- **Line 4**: Creates a chat input box where users type questions

**Why session state:**
- Maintains conversation history across user interactions
- Survives page refreshes and reruns
- Provides persistent user experience

# DDisplaying Previous Messages
```
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_msg)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_msg)
```

**What this loop does:**
- **Line 1**: Goes through each previous conversation turn
- **Lines 2-3**: Shows what the user said with a person avatar
- **Lines 4-5**: Shows what the bot replied with a robot avatar


### Processing New Questions
```python
if user_query:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_query)

    try:
        with st.spinner("🤖 Thinking... generating response..."):
            result = qa_chain({"question": user_query})
            response = result["answer"]

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response)

        # Sources shown in expander
        with st.expander("📚 Sources & Reasoning", expanded=False):
            for doc in result.get("source_documents", []):
                meta = doc.metadata
                st.markdown(f"**{meta.get('source', 'Unknown')} →** `{meta.get('section', 'N/A')}`")
                st.code(doc.page_content.strip()[:700] + "...", language="markdown")

        st.session_state.chat_history.append((user_query, response))

    except Exception as e:
        st.error("⚠️ Something went wrong while generating the answer.")
        st.exception(e)
```

**Breaking down this complex section:**

**Line 1**: Only runs if user typed something
**Lines 2-3**: Immediately shows the user's question in the chat

**Lines 5-8**: The core AI processing
- **Line 6**: Shows a spinner so user knows something is happening
- **Line 7**: Runs the entire AI chain (retrieval + generation)
- **Line 8**: Extracts just the answer text from the result

**Lines 10-11**: Shows the AI's response in the chat

**Lines 13-18**: Shows sources in an expandable section
- **Line 14**: Loops through each source document that was used
- **Line 15**: Gets metadata (source file, section) from each document
- **Line 16**: Shows which file and section the information came from
- **Line 17**: Shows first 700 characters of the source text

**Line 19**: Saves this conversation turn to session state

**Lines 21-23**: Error handling
- Catches any problems (API failures, network issues, etc.)
- Shows user-friendly error message
- Shows technical details for debugging

**What would happen without different parts:**
- **Without try/except**: App would crash on any error
- **Without spinner**: Users wouldn't know if the app is working
- **Without source display**: Users couldn't verify information
- **Without session state**: Conversation history would be lost

This architecture creates a production-ready AI chatbot that handles real-world challenges like error management, user feedback, source attribution, and conversation persistence.
