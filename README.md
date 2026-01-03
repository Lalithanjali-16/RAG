## (Ingestion Pipeline – Step by Step)

### 1️⃣ Imports required libraries

* `os` → For directory existence checks.
* `load_dotenv` → Loads environment variables from `.env`.
* `TextLoader`, `DirectoryLoader` → Load text documents from files.
* `CharacterTextSplitter` → Splits documents into smaller chunks.
* `HuggingFaceEmbeddings` → Generates embeddings locally (no API cost).
* `Chroma` → Vector database to store embeddings.

---

### 2️⃣ Loads environment variables

```python
load_dotenv()
```

* Prepares the environment for future configurations.
* (OpenAI key is no longer required since Hugging Face embeddings are used.)

---

### 3️⃣ `load_documents()` – Load text files

* Checks whether the `docs/` directory exists.
* Loads **all `.txt` files** inside `docs/`.
* Uses UTF-8 encoding to avoid Unicode errors.
* Raises an error if:

  * The directory does not exist.
  * No `.txt` files are found.
* Returns a list of `Document` objects (text + metadata).

---

### 4️⃣ `split_documents()` – Chunking documents

* Uses `CharacterTextSplitter`.
* Splits documents into:

  * **Chunk size:** 1000 characters
  * **Overlap:** 0 characters
* Converts long documents into smaller, searchable chunks.
* Prints how many chunks are created.
* Returns a list of chunked `Document` objects.

---

### 5️⃣ `create_vector_store()` – Create embeddings & store in ChromaDB

* Uses **Hugging Face embeddings**:

  ```python all-MiniLM-L6-v2
  ```
* Generates vector embeddings for each chunk.
* Stores embeddings in **persistent ChromaDB**:

  ```
  db/chroma_db
  ```
* Uses **cosine similarity** for semantic search.
* Saves the vector database to disk so it can be reused later.

---

### 6️⃣ `main()` – Orchestrates the pipeline

* Calls functions in order:

  1. Load documents
  2. Split documents into chunks
  3. Embed and store in ChromaDB

---

### 7️⃣ Script execution entry point

```python
if __name__ == "__main__":
    main()
```

* Ensures the pipeline runs only when the file is executed directly.

---

## ✅ Key Highlights (Important for RAG & Interviews)

* ✔ Uses **local Hugging Face embeddings** (no OpenAI quota issues)
* ✔ Persistent **vector database**
* ✔ Proper document chunking for better retrieval
* ✔ Ready for **RAG-based Question Answering**
* ✔ Clean separation of loading, chunking, and embedding

---

## 🧠 One-line summary (Interview ready)

> This script ingests text documents, splits them into chunks, generates semantic embeddings using Hugging Face models, and stores them persistently in ChromaDB for efficient retrieval in a RAG system.



### Retrieval pipeline

1. **Imports required libraries**

   * `Chroma` → Vector database for storing and searching embeddings.
   * `HuggingFaceEmbeddings` → Generates embeddings using a local Hugging Face model.
   * `load_dotenv` → Loads environment variables from `.env` (not strictly needed here, but fine to keep).

2. **Loads environment variables**

   * Calls `load_dotenv()` so any variables in `.env` are available (e.g., future API keys).

3. **Defines the persistent ChromaDB directory**

   * Uses:

     ```python persistent_directory = "db/chroma_db"
     ```
   * This is where the previously created vector store is stored on disk.

4. **Initializes the embedding model**

   * Uses a **free, local Hugging Face embedding model**:

     ```python sentence-transformers/all-MiniLM-L6-v2
     ```
   * Ensures the same embedding model is used as during ingestion.

5. **Loads the existing Chroma vector store**

   * Connects to the persisted Chroma database.
   * Uses cosine similarity (`hnsw:space = "cosine"`) for vector comparison.

6. **Defines the user query**

   * Query:
     Which island does SpaceX lease for its launches in the Pacific?
    
7. **Creates a retriever from the vector store**

   * Converts Chroma into a retriever interface.
   * Retrieves the **top 5 most similar chunks** (`k=5`).

8. **Performs semantic search**

   * Embeds the query using the Hugging Face model.
   * Finds the most relevant document chunks from ChromaDB.

9. **Prints the query**

   * Displays the user’s question for clarity.

10. **Prints retrieved context**

    * Iterates over the retrieved documents.
    * Prints the text content of each relevant chunk.

---

### ✅ Key Highlights (important for interviews / RAG explanation)

* Uses **local embeddings (no OpenAI, no quota issues)**
* Retrieval embeddings **match ingestion embeddings** (correct RAG practice)
* ChromaDB is **persistent**, not recreated every run
* Implements **semantic search**, not keyword search
* Ready to plug into a **RAG QA chain** with an LLM

