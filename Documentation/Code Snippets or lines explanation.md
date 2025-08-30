# Code Snippets and Line-by-Line Explanation

This document breaks down every important part of the code to help you understand exactly how this AI chatbot works. We'll go through both main files: the vector store builder and the chat application.

## File 1: build_vector_store.py - The Data Preparation Engine

This file takes raw text documents and transforms them into a searchable AI database.

### Import Section
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from pathlib import Path
import os
```

**What each line does:**
- **Line 1**: Imports a smart text splitter that breaks documents into chunks while keeping related sentences together
- **Line 2**: Imports the system that converts text into mathematical vectors (embeddings) using HuggingFace models
- **Line 3**: Imports FAISS, a high-performance database for storing and searching through vectors
- **Line 4**: Imports the Document class, which wraps text with metadata
- **Line 5**: Imports Path for easy file handling
- **Line 6**: Imports os for system operations

**What would happen if we used something else:**
- Without RecursiveCharacterTextSplitter, we might break sentences in the middle, making the AI give incomplete answers
- Without HuggingFace embeddings, we'd need to train our own model (extremely expensive and time-consuming)
- Without FAISS, simple keyword search would miss the meaning and context of questions

### Loading the Documents
```python
handbook_text = Path("data/handbook_cleaned_FULL.txt").read_text(encoding="utf-8")
direction_text = Path("data/direction_final.txt").read_text(encoding="utf-8")
```

**What each line does:**
- **Line 1**: Reads the entire GitLab handbook (500,000+ words) into memory as a string
- **Line 2**: Reads GitLab's strategic direction document into memory

**What would happen if we used something else:**
- If we didn't specify `encoding="utf-8"`, special characters might display incorrectly
- If we tried to process the files line by line instead of loading completely, we'd lose the ability to understand context across paragraphs

### Setting Up the Text Splitter
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=750,
    chunk_overlap=150,
    length_function=len,
)
```

**What each line does:**
- **Line 1**: Creates an intelligent text splitter object
- **Line 2**: Sets each chunk to about 750 characters (roughly 150 words)
- **Line 3**: Makes chunks overlap by 150 characters to preserve context between chunks
- **Line 4**: Uses simple character counting to measure length

**What would happen if we used different numbers:**
- **Smaller chunk_size (300)**: More precise retrieval but might lose broader context
- **Larger chunk_size (1500)**: Better context but might include irrelevant information
- **No overlap (0)**: Risk of splitting important information across chunks
- **Too much overlap (400)**: Redundant information, slower search, higher costs

### The Chunking Function with Metadata
```python
def chunk_with_metadata(text, source_label):
    sections = text.split("## SECTION:")
    documents = []

    for section in sections:
        if not section.strip():
            continue
        header, *content = section.strip().split("\n", 1)
        body = content[0] if content else ""
        chunks = splitter.create_documents([body])
        for chunk in chunks:
            chunk.metadata = {
                "source": source_label,
                "section": header.strip()
            }
        documents.extend(chunks)
    return documents
```

**Breaking this down line by line:**

**Line 1**: Defines a function that takes text and a label for where it came from
**Line 2**: Splits the text at "## SECTION:" markers (this is how the documents are organized)
**Line 3**: Creates an empty list to store the processed document chunks

**Line 5**: Starts a loop through each section
**Line 6-7**: Skips empty sections to avoid processing nothing
**Line 8**: Separates the section header from the content using Python's unpacking
**Line 9**: Gets the body text, or empty string if there's no content
**Line 10**: Uses the text splitter to break the section into appropriately-sized chunks
**Line 11-15**: Adds metadata to each chunk so we know where it came from
**Line 16**: Adds all chunks from this section to our master list
**Line 17**: Returns all the processed documents

**What would happen with different approaches:**
- **Without metadata**: The AI couldn't tell users where information came from
- **Without section splitting**: Related information might be scattered across random chunks
- **Different splitting markers**: Would need to match how the source documents are actually formatted

### Creating the Documents
```python
handbook_docs = chunk_with_metadata(handbook_text, "handbook")
direction_docs = chunk_with_metadata(direction_text, "direction")
all_docs = handbook_docs + direction_docs
print(f"✅ Total chunks: {len(all_docs)}")
```

**What each line does:**
- **Line 1**: Processes the handbook text into searchable chunks tagged as "handbook"
- **Line 2**: Processes the direction text into searchable chunks tagged as "direction"
- **Line 3**: Combines both sets of documents into one master collection
- **Line 4**: Prints how many chunks were created (helps verify the process worked)

### Creating the Embeddings Model
```python
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

**What this line does:**
- Creates an embedding model that converts text into 384-dimensional vectors
- Uses a pre-trained model that's good at understanding sentence meaning
- This specific model is fast, lightweight, and works well for question-answering

**What would happen with different models:**
- **Larger models (all-mpnet-base-v2)**: Better accuracy but slower and more memory-intensive
- **Smaller models**: Faster but might miss subtle meaning differences
- **OpenAI embeddings**: More expensive, requires API calls, but might be more accurate

### Creating and Saving the Vector Database
```python
vectordb = FAISS.from_documents(all_docs, embedding_model)
vectordb.save_local("data/faiss_index")
print("✅ FAISS index saved to: data/faiss_index/")
```

**What each line does:**
- **Line 1**: Creates a FAISS vector database from all documents using the embedding model
- **Line 2**: Saves the database to disk so we don't have to rebuild it every time
- **Line 3**: Confirms the save was successful

**What's happening behind the scenes:**
1. Each text chunk gets converted to a 384-dimensional vector
2. FAISS builds an index that allows fast similarity search
3. The index and metadata get saved as files on disk

---

## File 2: chatApp.py - The Interactive Chat Interface

This file creates the web application that users interact with.

### Streamlit Configuration (MUST be first!)
```python
import streamlit as st
st.set_page_config("GitLab GenAI Chatbot", page_icon="🤖", layout="wide")
```

**What these lines do:**
- **Line 1**: Imports Streamlit, the web framework
- **Line 2**: Configures the web page title, icon, and layout

**Why this MUST be first:**
- Streamlit requires page configuration before any other Streamlit commands
- If you put this after other st. commands, you'll get an error

### Import All Required Libraries
```python
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
```

**What each import provides:**
- **Line 1**: FAISS for loading the vector database we created
- **Line 2**: Same embedding model we used to create the database
- **Line 3**: Document class for handling text with metadata
- **Line 4**: Smart memory that summarizes old conversations to save space
- **Line 5**: Pre-built chain that combines retrieval and conversation
- **Line 6**: Interface to Google's Gemini AI model
- **Line 7**: System for creating custom prompts
- **Line 8**: Operating system interface

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

### Loading the Vector Database with Caching
```python
@st.cache_resource(show_spinner="Loading vector DB...")
def load_vector_store():
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.load_local(
        "data/faiss_index",
        embedding,
        allow_dangerous_deserialization=True
    )

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 18}
    )
    return retriever

retriever = load_vector_store()
```

**Breaking this down:**

**Line 1**: `@st.cache_resource` - Caches this function so it only runs once, even if users refresh the page
**Line 2**: Function definition with descriptive name
**Line 3**: Creates the same embedding model used when building the database
**Line 4-7**: Loads the saved FAISS database from disk
- `allow_dangerous_deserialization=True` is needed because FAISS files contain pickled data

**Line 9-12**: Configures how the database searches for relevant information
- `search_type="mmr"` uses Maximum Marginal Relevance (finds diverse, non-redundant results)
- `k=8` returns 8 most relevant chunks
- `fetch_k=18` initially finds 18 candidates, then picks the 8 most diverse

**Line 14**: Actually calls the function and stores the retriever

**What would happen with different settings:**
- **Without caching**: Database would reload every time someone refreshes, making the app very slow
- **search_type="similarity"**: Might return very similar chunks, giving repetitive answers
- **Lower k (3)**: Faster but might miss important context
- **Higher k (15)**: More context but slower responses and higher AI costs

### Setting Up the AI Model
```python
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    convert_system_message_to_human=True,
)
```

**What each line does:**
- **Line 1**: Creates a connection to Google's Gemini AI model
- **Line 2**: Specifies the "flash" version (faster, cheaper than pro version)
- **Line 3**: Sets temperature to 0.3 (creative enough for natural responses, controlled enough for accuracy)
- **Line 4**: Technical setting needed for compatibility with this version of LangChain

**Why these settings:**
- **gemini-1.5-flash**: Good balance of speed, cost, and quality
- **temperature=0.3**: Low enough for factual accuracy, high enough to avoid robotic responses
- **convert_system_message_to_human=True**: Ensures prompt compatibility

### Conversation Memory Setup
```python
memory = ConversationSummaryBufferMemory(
    llm=gemini_llm,
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)
```

**What each line does:**
- **Line 1**: Creates intelligent memory that summarizes old conversations
- **Line 2**: Uses the same AI model for summarization
- **Line 3**: Names the memory storage "chat_history"
- **Line 4**: Returns messages in a format the conversation chain expects
- **Line 5**: Specifies which part of AI responses to remember (prevents confusion with multiple outputs)

**How this memory works:**
1. Keeps recent conversation turns in full detail
2. Summarizes older conversations to save space
3. Provides relevant context without hitting token limits

### Custom Prompt Template
```python
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert assistant trained on GitLab's official Handbook and Direction documents.

Please:
- Answer with as much useful detail as possible.
- Use bullet points or formatting if appropriate.
- Cite the source section when available.
- Only answer from GitLab materials. Politely decline anything off-topic.

Context:
{context}

Question:
{question}
"""
)
```

**What each part does:**
- **Line 1-2**: Defines a template that takes "context" and "question" as inputs
- **Lines 4-11**: Instructions that guide the AI's behavior
- **Lines 13-16**: Shows where the retrieved context and user question get inserted

**Why this specific prompt:**
- **Clear role definition**: AI knows it's a GitLab expert
- **Specific instructions**: Tells AI how to format responses
- **Safety guardrails**: Prevents off-topic or harmful responses
- **Context integration**: Shows how to use retrieved information

### Creating the Conversation Chain
```python
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=gemini_llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    combine_docs_chain_kwargs={"prompt": prompt},
    output_key="answer",
    verbose=False
)
```

**What each parameter does:**
- **llm**: The AI model that generates responses
- **retriever**: The system that finds relevant document chunks
- **memory**: Remembers conversation history
- **return_source_documents=True**: Includes source citations
- **combine_docs_chain_kwargs**: Uses our custom prompt
- **output_key="answer"**: Prevents confusion when chain returns multiple outputs
- **verbose=False**: Keeps logs clean for production

**What this chain does automatically:**
1. Takes user question
2. Searches vector database for relevant context
3. Combines context with conversation history
4. Generates response using AI model
5. Updates conversation memory
6. Returns answer with sources

### Streamlit User Interface Setup
```python
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

### Chat Session State Management
```python
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

### Displaying Previous Messages
```python
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
