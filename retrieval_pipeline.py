from langchain_chroma import Chroma
#from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

persistent_directory = 'db/chroma_db'
#Load embeddings and vector store
#embedding_model= OpenAIEmbeddings(model='text-embedding-3-small')
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
db= Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space":"cosine"}
)

#Search for relevant documents
query= "Which island does SpaceX lease for its launches in the Pacific?"

retriever= db.as_retriever(search_kwargs={'k':5})
# retriever=db.as_retriever(
#     search_type='similarity_score_threshold',
#     search_kwargs={ "k":5, "score_threshold": 0.3} #Only returns chunks with cosine similarity >= 0.3
# )
relevant_docs=retriever.invoke(query)

print(f"User Query: {query}")
print("---Context---")
for i,doc in enumerate(relevant_docs ,1):
    print(f"Document {i}:\n {doc.page_content}\n")