# Module 05: Memory & Retrieval (LangChain)
## Phase 2: Instructor-Led Demonstration - Live Analysis

**Module Title:** Memory & Retrieval (LangChain)  
**Target Audience:** Agentic AI Graduate Course  
**Phase Duration:** 45-60 Minutes  
**Goal:** Live coding session where students observe the RAG workflow, debug errors with the instructor, and analyze results in real-time using Predict-Observe-Explain methodology.

**Source Material:** This demo adapts concepts from `Text_Embedding_with_LangChain_and_HuggingFace.ipynb`

---

## Pre-Demo Setup (5 minutes)

### Environment Check

Before we begin, let's verify our environment is properly configured. Open your terminal and confirm:

```bash
# Verify Python environment
python --version  # Should be 3.10+

# Check that required packages will be available
pip list | grep -E "langchain|chromadb|sentence-transformers"
```

**Expected Output Discussion:**
- If packages are missing, we'll install them together
- Discuss why we're using specific versions (compatibility, stability)

### Install Dependencies (If Needed)

```bash
# Create a new uv project for this module
uv init memory-retrieval-demo
cd memory-retrieval-demo

# Add required packages
uv add langchain langchain-community langchain-openai
uv add chromadb
uv add sentence-transformers
uv add pypdf
uv add python-dotenv
```

**POE Moment 1:**  
**PREDICT:** "What do you think will happen if we forget to install sentence-transformers but try to use HuggingFace embeddings?"  
**Expected Answer:** Runtime error when trying to load the model  
**Teaching Point:** Explicit dependencies vs. implicit dependencies

---

## Part 1: Environment & Safety Check (10 minutes)

### The "Wrong" Way First (Intentional Error)

Let's start by doing something that students commonly do wrong - hardcoding API keys.

**Instructor:** Create a new file `wrong_way.py`:

```python
# ❌ NEVER DO THIS
OPENAI_API_KEY = "sk-1234567890abcdef"  # Hardcoded key

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
```

**POE Moment 2:**  
**PREDICT:** "What are the security risks of this code?"  
**Expected Answers:**
- Gets committed to git
- Visible in logs
- Shared in screenshots
- Exposed if repo is public

**OBSERVE:** Show a git commit history with this file  
**EXPLAIN:** "One accidental commit to GitHub, and your key is compromised. Now let's do it right."

---

### The "Right" Way (Security Best Practice)

**Instructor:** Create `.env` file:

```bash
# .env file (NEVER commit this)
HF_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_key_here
```

**Instructor:** Create `.gitignore`:

```
.env
*.db
chromadb/
emb/
__pycache__/
```

**Instructor:** Create `secure_way.py`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify keys exist (but don't print them!)
hf_token = os.getenv('HF_TOKEN')
if hf_token:
    print("✓ HuggingFace token loaded")
else:
    print("✗ HuggingFace token missing - add to .env file")

openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    print("✓ OpenAI API key loaded")
else:
    print("✗ OpenAI API key missing - add to .env file")
```

**POE Moment 3:**  
**OBSERVE:** Run the script together  
**DISCUSS:** "Why do we check if keys exist but never print their values?"  
**Teaching Point:** Defense in depth - even in trusted environments, minimize key exposure

---

## Part 2: The Core RAG Implementation (25 minutes)

### Step 1: Setting Up Embeddings

**Instructor:** Create `01_embeddings_comparison.py`:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import numpy as np

load_dotenv()

# Initialize embedding models
print("Loading embedding models...")

# Local (Free) - HuggingFace
hf_embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2',
    model_kwargs={'device': 'cpu'}
)

# Cloud (Paid) - OpenAI (Optional)
# openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

print("✓ Models loaded successfully\n")

# Test embedding generation
test_texts = [
    "The dog ran through the park",
    "A puppy played in the garden",
    "The computer crashed unexpectedly"
]

print("Generating embeddings for test texts...")
for text in test_texts:
    embedding = hf_embeddings.embed_query(text)
    print(f"Text: '{text}'")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print()
```

**POE Moment 4:**  
**PREDICT:** "Before we run this, what do you expect the embedding dimension to be for 'all-MiniLM-L6-v2'?"  
**Answer:** 384 (students should reference the glossary)

**OBSERVE:** Run the code together  
**Key Observations:**
- Loading time for the model (first time downloads ~100MB)
- Embedding dimension is consistent across different texts
- Embedding values are floats between -1 and 1

**POE Moment 5:**  
**PREDICT:** "Which two texts should have more similar embeddings - the dog/puppy texts or dog/computer?"  
**OBSERVE:** Let's calculate cosine similarity to confirm:

```python
def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Embed all texts
embeddings_list = [hf_embeddings.embed_query(text) for text in test_texts]

# Calculate similarities
sim_dog_puppy = cosine_similarity(embeddings_list[0], embeddings_list[1])
sim_dog_computer = cosine_similarity(embeddings_list[0], embeddings_list[2])

print(f"Similarity (dog ↔ puppy): {sim_dog_puppy:.4f}")
print(f"Similarity (dog ↔ computer): {sim_dog_computer:.4f}")
```

**EXPLAIN:** "See how semantic similarity is captured numerically? This is the foundation of RAG."

---

### Step 2: Loading and Chunking Documents

**Instructor:** Create `langchain` project directory. Place `sample.pdf` in the project directory (use the one from project files)

Create `document_loading.py`:

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Load PDF
print("Loading PDF document...")
pdf_path = "sample.pdf"
loader = PyPDFLoader(pdf_path)

# Initial load (no splitting)
raw_docs = loader.load()
print(f"✓ Loaded {len(raw_docs)} pages")
print(f"First page has {len(raw_docs[0].page_content)} characters\n")

# Show first 500 characters
print("Preview of first page:")
print(raw_docs[0].page_content[:500])
print("...\n")
```

**POE Moment 6:**  
**PREDICT:** "If we embed entire pages, what problems might we encounter?"  
**Expected Answers:**
- Pages too long (exceed embedding model limits)
- Retrieval too coarse (whole page when we need one paragraph)
- Context noise (irrelevant sections included)

**OBSERVE:** Now let's add chunking:

```python
# Create text splitter
text_splitter = CharacterTextSplitter(
    separator="\n",      # Split on newlines
    chunk_size=200,      # Target 200 tokens per chunk
    chunk_overlap=100    # 100 token overlap between chunks
)

# Split documents
chunks = loader.load_and_split(text_splitter=text_splitter)

print(f"✓ Split into {len(chunks)} chunks")
print(f"First chunk: {len(chunks[0].page_content)} characters")
print(f"Last chunk: {len(chunks[-1].page_content)} characters\n")

# Show first few chunks
print("First 3 chunks:")
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i} ---")
    print(chunk.page_content[:200] + "...")
    print(f"Metadata: {chunk.metadata}")
```

**POE Moment 7:**  
**OBSERVE:** The chunking output  
**DISCUSS:** 
- "Notice the overlap - why is this important?"
- "Look at the metadata - what information is preserved?"
- "Are any chunks incomplete sentences? What does that tell us about our separator choice?"

**EXPLAIN:** "The overlap ensures we don't lose context at boundaries. Metadata helps us trace back to the source."

---

### Step 3: Building the Vector Store

Create `03_vector_store.py`:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

print("Step 1: Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

print("Step 2: Loading and chunking document...")
loader = PyPDFLoader("sample.pdf")
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=100
)
chunks = loader.load_and_split(text_splitter=text_splitter)

# Add PDF filename to metadata (important for multi-document systems)
for chunk in chunks:
    chunk.metadata["source"] = "sample.pdf"

print(f"✓ Prepared {len(chunks)} chunks for embedding\n")

print("Step 3: Creating vector store...")
print("(This may take 30-60 seconds to embed all chunks)")

# Create Chroma vector store
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # Saves to disk
)

print(f"✓ Vector store created with {len(chunks)} chunks")
print("✓ Database persisted to ./chroma_db")
```

**POE Moment 8:**  
**PREDICT:** "What's happening during those 30-60 seconds?"  
**Answer:** Each chunk is being passed through the embedding model

**OBSERVE:** Run the code and watch timing  
**Common Error Simulation:** "Let's see what happens if we try to use the database before it's finished building..."

```python
# Intentional error example (comment this out after demonstrating)
# db.similarity_search("test query")  # May fail if not persisted
```

**EXPLAIN:** "Always wait for confirmation that the database is persisted before querying."

---

### Step 4: Semantic Search in Action

Create `semantic_search.py`:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

print("Loading existing vector store...")
embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

# Load the persisted database
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

print("✓ Vector store loaded\n")

# Function to perform search and display results
def search_and_display(query, k=4):
    """Search for a query and display results with scores"""
    print("=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)
    
    # Get results with similarity scores
    results_with_scores = db.similarity_search_with_score(query, k=k)
    
    for i, (doc, score) in enumerate(results_with_scores, 1):
        print(f"\n--- Result {i} (Score: {score:.4f}) ---")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Source: Page {doc.metadata.get('page', 'unknown')}")
    
    print("\n")
    return results_with_scores

# Test queries
query1 = "What is maximum likelihood estimation?"
query2 = "How do you calculate expected value?"
query3 = "Explain the binomial distribution"

# Run searches
results1 = search_and_display(query1)
```

**POE Moment 9:**  
**PREDICT:** "Before we run this, what score range do you expect? Remember cosine similarity ranges from -1 to 1, but Chroma returns distance metrics."  
**Note:** Chroma actually returns L2 distance (lower is better), not cosine similarity directly

**OBSERVE:** Run the search  
**Key Discussion Points:**
- "Notice the scores - lower is more similar in L2 distance"
- "Look at which chunks matched - are they truly relevant?"
- "What if we asked the same question with different wording?"

**POE Moment 10:**  
**PREDICT:** "Will these two queries return the same results?"
- Query A: "What is MLE?"
- Query B: "What is maximum likelihood estimation?"

```python
print("\n\nComparing similar queries:")
resultsA = search_and_display("What is MLE?", k=2)
resultsB = search_and_display("What is maximum likelihood estimation?", k=2)

# Check if top results are the same
if resultsA[0][0].page_content == resultsB[0][0].page_content:
    print("✓ Both queries returned the same top result (semantic matching works!)")
else:
    print("✗ Different top results (interesting - let's discuss why)")
```

**EXPLAIN:** "Semantic search handles abbreviations and synonyms gracefully, but isn't perfect. The embedding model must have seen similar patterns during training."

---

## Part 3: Building a RAG-Enhanced Agent (15 minutes)

### Complete RAG Pipeline

Create `rag_agent.py`:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama  # Free local LLM
from dotenv import load_dotenv

load_dotenv()

print("Step 1: Loading vector store...")
embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

print("Step 2: Initializing LLM...")
# Using Ollama (local, free) - make sure Ollama is running!
# Alternative: Use OpenAI by uncommenting below
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

llm = Ollama(model="llama3.2", temperature=0)

print("Step 3: Creating RAG chain...")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" means inject all retrieved docs into prompt
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("✓ RAG system ready!\n")

# Ask questions
def ask_question(question):
    print("=" * 60)
    print(f"QUESTION: {question}")
    print("=" * 60)
    
    result = qa_chain.invoke({"query": question})
    
    print("\nANSWER:")
    print(result['result'])
    
    print("\nSOURCE DOCUMENTS:")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"\n[{i}] Page {doc.metadata.get('page', '?')}")
        print(f"    {doc.page_content[:150]}...")
    
    print("\n")

# Interactive Q&A
ask_question("What is maximum likelihood estimation?")
ask_question("How does MLE relate to the normal distribution?")
```

**POE Moment 11:**  
**PREDICT:** "What's the difference between asking this question directly to an LLM versus using RAG?"  
**Expected Answer:** RAG grounds the answer in the retrieved documents

**OBSERVE:** Run both versions:

```python
# Direct LLM (no RAG)
print("Without RAG:")
direct_response = llm.invoke("What is maximum likelihood estimation?")
print(direct_response)

print("\n" + "=" * 60 + "\n")

# With RAG
print("With RAG:")
ask_question("What is maximum likelihood estimation?")
```

**DISCUSS:**
- Accuracy differences
- Presence/absence of specific details from the document
- Ability to cite sources
- Hallucination risks

**EXPLAIN:** "RAG doesn't make the LLM smarter - it provides curated context. The LLM still does the reasoning, but now it has relevant reference material."

---

## Part 4: Live Analysis & Debugging (10 minutes)

### Common Error 1: Embedding Model Mismatch

**Instructor:** Intentionally create this error:

```python
# Build database with one embedding model
embeddings_a = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'  # 384 dimensions
)
db = Chroma.from_documents(docs, embeddings_a)

# Try to query with a different embedding model
embeddings_b = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-mpnet-base-v2'  # 768 dimensions
)
db_wrong = Chroma(persist_directory="./chroma_db", embedding_function=embeddings_b)

# This will fail or return garbage results
results = db_wrong.similarity_search("test query")
```

**POE Moment 12:**  
**OBSERVE:** The error or nonsensical results  
**EXPLAIN:** "Dimension mismatch means we're comparing apples (384D) to oranges (768D). ALWAYS use the same embedding model for indexing and retrieval."

**Fix:**
```python
# Always document which embedding model was used
# Consider storing model name in metadata
DB_METADATA = {
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dimension": 384,
    "created_at": "2024-01-15"
}
```

---

### Common Error 2: Forgetting to Persist

```python
# BAD: Doesn't persist
db_temp = Chroma.from_documents(docs, embeddings)  # Lost when script ends!

# GOOD: Persists to disk
db_persist = Chroma.from_documents(
    docs, 
    embeddings, 
    persist_directory="./chroma_db"
)
```

**Teaching Point:** "Always specify persist_directory unless you explicitly want a temporary in-memory database."

---

### Common Error 3: Poor Chunking

**Demonstrate:** Show what happens with bad chunk sizes:

```python
# Too small (loses context)
splitter_tiny = CharacterTextSplitter(chunk_size=10, chunk_overlap=0)
tiny_chunks = splitter_tiny.split_documents(docs)
print(f"Tiny chunks: {tiny_chunks[0].page_content}")  # Incomplete sentences

# Too large (noisy retrieval)
splitter_huge = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
huge_chunks = splitter_huge.split_documents(docs)
print(f"Huge chunks: {len(huge_chunks[0].page_content)} characters")  # Entire sections
```

**DISCUSS:** "Finding the right chunk size is an empirical process. Start with 200-500 tokens and adjust based on retrieval quality."

---

## Part 5: Live Experimentation & Class Discussion (5 minutes)

### Variables to Change & Re-Run

**Instructor:** "Let's experiment together. What happens if we...?"

1. **Change K (number of retrieved documents)**
```python
# retriever=db.as_retriever(search_kwargs={"k": 1})  # vs k=10
```

**PREDICT:** More context = better answers?  
**OBSERVE:** Run with k=1, k=3, k=10  
**DISCUSS:** "There's a sweet spot. Too few = missing info. Too many = noise."

2. **Change LLM Temperature**
```python
# llm = Ollama(model="llama3.2", temperature=0)    # Deterministic
# llm = Ollama(model="llama3.2", temperature=0.7)  # Creative
```

**PREDICT:** How will temperature affect citation accuracy?  
**OBSERVE:** Run same question with different temperatures  
**DISCUSS:** "For RAG, lower temperature is usually better - we want consistency."

3. **Change Chunk Overlap**
```python
# chunk_overlap=0    # No overlap
# chunk_overlap=100  # 50% overlap
# chunk_overlap=190  # 95% overlap (almost duplicates)
```

**PREDICT:** What's the trade-off?  
**DISCUSS:** Storage space vs. context preservation

---

## Summary & Key Observations

**What We Demonstrated:**
1. ✓ Secure API key management with .env files
2. ✓ Embedding generation and semantic similarity
3. ✓ Document loading and chunking strategies
4. ✓ Vector store creation and persistence
5. ✓ Semantic search with similarity scores
6. ✓ Complete RAG pipeline with source citation
7. ✓ Common errors and how to debug them

**Critical Insights from Live Demo:**
- Embedding models must match between indexing and retrieval
- Chunk size dramatically affects retrieval quality
- RAG is only as good as your source documents
- K (number of results) is a hyperparameter that needs tuning
- Always persist your vector store
- Lower scores = more similar (in L2 distance)

**Questions for Students:**
1. "What would you change about our chunking strategy for a different document type (e.g., code, legal docs, chat logs)?"
2. "How would you handle multi-language documents?"
3. "What if your documents update frequently - how would you handle vector store updates?"

---

## Preparation for Independent Lab

You've now seen:
- The complete RAG pipeline in action
- How to debug common errors
- The impact of different hyperparameters

In the independent lab, you'll:
- Build a RAG system for a DIFFERENT domain (e.g., course syllabi, research papers, medical documents)
- Implement conversation memory (buffer + vector store)
- Add metadata filtering
- Evaluate retrieval quality with custom metrics

**Homework Before Next Class:**
1. Ensure Ollama is installed and running on your machine
2. Create a `.env` file with your API keys (if using cloud services)
3. Collect 5-10 PDF documents for your chosen domain
4. Review the glossary terms one more time

---

## Instructor Notes

### Timing Breakdown
- Environment & Security: 10 min
- Embeddings & Chunking: 10 min
- Vector Store & Search: 10 min
- RAG Pipeline: 15 min
- Debugging & Discussion: 10 min

### Common Student Questions to Anticipate
1. **"Why not just put everything in the LLM context window?"**
   - Answer: Cost, latency, and noise. RAG is a filter.

2. **"Can I use this for real-time chat?"**
   - Answer: Yes, but add conversation buffer memory (covered in lab).

3. **"What if I have millions of documents?"**
   - Answer: Production vector databases (Pinecone, Weaviate) with better indexing.

4. **"How do I update documents without rebuilding everything?"**
   - Answer: Incremental updates (delete old chunks, add new ones). Covered in advanced topics.

### Equipment Needed
- Projector for live coding
- Sample PDF (provided)
- Pre-tested code snippets (backup if live coding fails)
- Ollama running locally (or OpenAI API key as backup)

### Fallback Plan
If Ollama isn't working on instructor machine:
- Switch to OpenAI API (have backup key ready)
- Or demonstrate with pre-recorded outputs (screenshots)

The goal is observation and understanding, not perfect execution.
