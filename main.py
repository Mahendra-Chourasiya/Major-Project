# import os
# import streamlit as st
# import pickle
# import time
# from langchain import OpenAI
# from langchain.chains import RetrievalQAWithSourcesChain
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import UnstructuredURLLoader
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# # import os


# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env (especially openai api key)

# st.title("RockyBot: News Research Tool 📈")
# st.sidebar.title("News Article URLs")

# urls = []
# for i in range(3):
#     url = st.sidebar.text_input(f"URL {i+1}")
#     urls.append(url)

# process_url_clicked = st.sidebar.button("Process URLs")
# file_path = "faiss_store_openai.pkl"

# main_placeholder = st.empty()
# os.environ["OPENAI_API_KEY"] = "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"

# llm = OpenAI(temperature=0.9, max_tokens=500, openai_api_key="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")

# if process_url_clicked:
#     # load data
#     loader = UnstructuredURLLoader(urls=urls)
#     main_placeholder.text("Data Loading...Started...✅✅✅")
#     data = loader.load()
#     # split data
#     if data:
#         text_splitter = RecursiveCharacterTextSplitter(
#             separators=['\n\n', '\n', '.', ','],
#             chunk_size=1000
#         )
#         main_placeholder.text("Text Splitter...Started...✅✅✅")
#         docs = text_splitter.split_documents(data)
#         # create embeddings and save it to FAISS index
#         if docs:
#             embeddings = OpenAIEmbeddings()
#             vectorstore_openai = FAISS.from_documents(docs, embeddings)
#             main_placeholder.text("Embedding Vector Started Building...✅✅✅")
#             time.sleep(2)
#             vectorstore_openai.save_local(file_path)
#     else:
#         main_placeholder.text("Text Splitter produced empty documents. Check data.")
# else:
#     main_placeholder.text("Data loading failed. Check URLs or network connection.")

#     # Save the FAISS index to a pickle file
#     # with open(file_path, "wb") as f:
#     #     pickle.dump(vectorstore_openai, f)

# query = main_placeholder.text_input("Question: ")
# if query:
#     if os.path.exists(file_path):
#         with open(file_path, "rb") as f:
#             vectorstore = pickle.load(f)
#             chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
#             result = chain({"question": query}, return_only_outputs=True)
#             # result will be a dictionary of this format --> {"answer": "", "sources": [] }
#             st.header("Answer")
#             st.write(result["answer"])

#             # Display sources, if available
#             sources = result.get("sources", "")
#             if sources:
#                 st.subheader("Sources:")
#                 sources_list = sources.split("\n")  # Split the sources by newline
#                 for source in sources_list:
#                     st.write(source)




import os
import streamlit as st
import pickle
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv  # Optional, for environment variables

# Load environment variables from .env file (optional)
load_dotenv()

# Use environment variable for API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

st.title("RockyBot: News Research Tool ")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()

# Use environment variable for API key (if .env is used)
if os.getenv('OPENAI_API_KEY'):
    llm = OpenAI(temperature=0.9, max_tokens=500, openai_api_key=os.getenv('OPENAI_API_KEY'))
else:
    # Fallback to directly setting the API key (if .env is not used)
    llm = OpenAI(temperature=0.9, max_tokens=500, openai_api_key="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")

if process_url_clicked:
    # Data Loading
    try:
        loader = UnstructuredURLLoader(urls=urls)
        main_placeholder.text("Data Loading...Started...✅✅✅")
        data = loader.load()
    except Exception as e:
        main_placeholder.text(f"Data Loading Failed: {e}")
        # Handle the error more gracefully, maybe display the specific error message to the user

    # Text Splitting (if data is loaded successfully)
    if data:
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '.', ','],
                chunk_size=1000
            )
            main_placeholder.text("Text Splitter...Started...✅✅✅")
            processed_documents = text_splitter.split_documents(data)
        except Exception as e:
            main_placeholder.text(f"Text Splitting Failed: {e}")
            # Handle the error more gracefully

        # Create Embeddings and Save FAISS Index (if documents are processed)
        if processed_documents:
            embeddings = OpenAIEmbeddings()
            vectorstore_openai = FAISS.from_documents(processed_documents, embeddings)
            main_placeholder.text("Embedding Vector Started Building...✅✅✅")
            vectorstore_openai.save_local(file_path)
    else:
        main_placeholder.text("No data loaded. Check URLs or network connection.")

query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)

