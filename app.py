import streamlit as st
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# Page configuration
st.set_page_config(
    page_title="AIT Placement Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load env variables
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_FAISS_PATH = 'vectorstore/db_faiss'
HUGGINGFACE_REPO_ID = 'mistralai/Mistral-7B-Instruct-v0.3'
HF_TOKEN = os.getenv("HF_TOKEN")

# MongoDB
client = MongoClient(MONGODB_URI)
db = client['ait_db']
users_col = db['users']
logins_col = db['logins']

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'username' not in st.session_state:
    st.session_state.username = ""

# Dark theme & animation styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A; /* dark blue background */
        color: #E2E8F0;
    }
    .main-header {
        font-size: 2.5rem;
        color: #60A5FA;
        text-align: center;
        margin-bottom: 1.5rem;
        animation: fadeInDown 1s ease-in-out;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #93C5FD;
        margin-bottom: 1rem;
        animation: fadeInLeft 1s ease-in-out;
    }
    input, select, textarea {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
    }
    .metric-label {
        color: #60A5FA;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">AIT Placement Assistant</h1>', unsafe_allow_html=True)


# Query processing function
def process_query(query):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db_faiss = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

        llm = HuggingFaceEndpoint(
            repo_id=HUGGINGFACE_REPO_ID,
            task="text-generation",
            huggingfacehub_api_token=HF_TOKEN,
            max_new_tokens=512,
            temperature=0.5
        )

        custom_prompt = PromptTemplate(
            template="""
            Use the context below to answer the question about AIT placements.
            Context: {context}
            Question: {question}
            Answer concisely and accurately. If the information is not in the context, say you don't know.
            """,
            input_variables=["context", "question"]
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=db_faiss.as_retriever(search_kwargs={'k': 4}),
            chain_type='stuff',
            return_source_documents=True,
            chain_type_kwargs={"prompt": custom_prompt}
        )

        result = qa_chain.invoke({'query': query})
        return result['result']

    except Exception as e:
        return f"Error occurred: {str(e)}"


# Login/Register UI
if not st.session_state.logged_in:
    st.markdown('<h2 class="sub-header">Login / Register</h2>', unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        regno = st.text_input("Registration Number")
        year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        submit = st.form_submit_button("Login / Register")

        if submit and username and email and regno:
            users_col.insert_one({
                "username": username,
                "email": email,
                "regno": regno,
                "year": year
            })
            logins_col.insert_one({"username": username})

            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()

    st.markdown("### Sample Questions You Can Ask:")
    st.markdown("- What companies visited AIT for Mechanical placements?")
    st.markdown("- What is the average package?")
    st.markdown("- How to prepare for core roles?")

# Main Chat Interface
else:
    with st.sidebar:
        st.markdown('<h3 class="sub-header">Dashboard</h3>', unsafe_allow_html=True)
        st.markdown(f"**User:** {st.session_state.username}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Users", users_col.count_documents({}))
        with col2:
            st.metric("Logins", logins_col.count_documents({}))

        st.markdown("### Quick Topics")
        topics = [
            "Companies hiring Mechanical Engineers",
            "Highest paying companies",
            "Skills required for core roles",
            "How to prepare for placements"
        ]
        for topic in topics:
            if st.button(topic):
                response = process_query(topic)
                st.session_state.messages.append({"role": "user", "content": topic})
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.rerun()

    st.markdown('<h2 class="sub-header">Ask Me Anything About AIT Placements</h2>', unsafe_allow_html=True)

    for message in st.session_state.messages:
        role = message["role"]
        with st.chat_message(role):
            st.write(message["content"])

    if prompt := st.chat_input("Ask about AIT placements..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = process_query(prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")
st.markdown("AIT Placement Assistant © 2025 | Powered by LangChain & Streamlit")
