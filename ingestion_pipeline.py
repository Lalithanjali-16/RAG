import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

def load_documents(docs_path='docs'):
    print(f"Loading docs from {docs_path}")
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The directory {docs_path} does not exist")

    #Load all .txt files from the docs directory
    loader = DirectoryLoader(
    path=docs_path,
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)


    documents = loader.load()
    if len(documents)==0:
        raise FileNotFoundError(f"No .txt file in {docs_path}")
    
    # for i,doc in enumerate(documents[:2]):
    #     print(f"\nDocument {i+1} : ")
    #     print(f" Source: {doc.metadata['source']}")
    #     print(f" Content length: {len(doc.page_content)} characters")
    #     print(f" Content preview: {doc.page_content[:100]}")
    #     print(f" metadata: {doc.metadata}")

    return documents

def split_documents(documents,chunk_size=1000, chunk_overlap=0):
    # Split documents into smaller chunks with overlap
    print("Splitting documents into chunks")
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    if chunks:
        # for i,chunk in enumerate(chunks[:5]):
        #     print(f"\n---Chunk {i+1}")
        #     print(f"Sourcs: {chunk.metadata['source']}")
        #     print(f"Length: {len(chunk.page_content)} characters")
        #     print(f"Content: ")
        #     print(chunk.page_content)

        if len(chunks)>5:
            print(f"\n and {len(chunks)-5} more chunks")

    return chunks 

# def create_vector_store(chunks,persist_directory = "db/chroma_db"):
#     print("Creating and embeddings and store in ChromaDB ")
#     embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')
#     print("Creating vector store")
#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=embedding_model,
#         persist_directory=persist_directory,
#         collection_metadata={"hnsw:space" : "cosine"}
#     )
#     print("Finished creating vector store")
#     print(f"Vector store created and saved to {persist_directory}")
#     return vectorstore

def create_vector_store(chunks, persist_directory="db/chroma_db"):
    print("Creating embeddings and storing in ChromaDB")

    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"}
    )

    print(f"Vector store created and saved to {persist_directory}")
    return vectorstore


def main():
    # 1. Loading the files
    documents = load_documents(docs_path='docs')
    # 2. Chunking the files
    chunks = split_documents(documents)
    # 3. Embeddings and storing in vector DB
    vectorstore=create_vector_store(chunks)

if __name__ == "__main__" :
    main()