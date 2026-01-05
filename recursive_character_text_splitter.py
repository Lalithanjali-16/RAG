# 🔹 Character Text Splitter
#     →Uses only one separator (e.g., \n, \n\n, etc.).
#     →Attempts to split text only at that separator.
#     →If the separator is not found, the text will not be split, even if the chunk size limit is exceeded.
#     →Best suited for simple, well-structured text with consistent separators.

# 🔹 Recursive Character Text Splitter
#     →Uses multiple separators (e.g., \n\n, \n, " ", etc.).
#     →Tries splitting with the largest separator first.
#     →If a chunk still exceeds the chunk size, it recursively falls back to smaller separators.
#     →Ensures chunks are created even when ideal separators are missing.
#     →Best suited for complex or unstructured text.

from langchain_text_splitters import (CharacterTextSplitter,RecursiveCharacterTextSplitter)

tesla_text = """Tesla's Q3 Results

Tesla reported record revenue of $25.2B in Q3 2024.

Model Y Performance

The Model Y became the best-selling vehicle globally, with 350,000 units sold.

Production Challenges

Supply chain issues caused a 12% increase in production costs.

This is one very long paragraph that definitely exceeds our 100 character limit and has no double newlines inside it whatsoever making it impossible to split properly."""


character_splitter = CharacterTextSplitter(
    separator=' ', #Default separator. Other options include ["\n\n", "\n", ". ", " ", ""]
    chunk_size=100,
    chunk_overlap=0
)
chunks1 = character_splitter.split_text(tesla_text)
for i,chunk in enumerate(chunks1,1):
    print(f"Chunk {i}: ({len(chunk)} chars)")
    print(f'"{chunk}"')
    print()

recursive_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", " ", ""],  # Multiple separators
    chunk_size=100,
    chunk_overlap=0
)
chunks2 = recursive_splitter.split_text(tesla_text)
print(f"With RecursiveCharacterTextSplitter:")
for i,chunk in enumerate(chunks2,1):
    print(f"Chunk {i}: ({len(chunk)} chars)")
    print(f'"{chunk}"')
    print()