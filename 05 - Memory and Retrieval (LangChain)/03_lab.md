# Module 05: Memory & Retrieval (LangChain)
## Phase 3: Independent Lab - Student Guide

**Module Title:** Memory & Retrieval (LangChain)  
**Target Audience:** Agentic AI Graduate Course  
**Estimated Time:** 90-120 Minutes (Take-Home Assignment)  
**Due Date:** [To be specified by instructor]  
**Goal:** Build a domain-specific RAG-enhanced conversational agent with persistent memory

---

## Lab Overview

In the demonstration, you observed the instructor build a RAG system for a statistical/technical document. Your task is to implement a similar system but for a **different domain** with **additional memory features** not covered in the demo.

**The Twist:** Your RAG system must:
1. Work with a different document type (medical, legal, course materials, research papers, etc.)
2. Implement **hybrid memory**: both conversation buffer (short-term) AND vector store (long-term)
3. Include **metadata filtering** to narrow searches
4. Provide **evaluation metrics** for retrieval quality

This ensures you understand the underlying architecture, not just code replication.

---

## Learning Objectives

By completing this lab, you will demonstrate:
- [ ] Ability to configure and secure API credentials
- [ ] Understanding of document loading and chunking strategies for different content types
- [ ] Implementation of vector store creation and querying
- [ ] Design of hybrid memory systems (buffer + vector store)
- [ ] Application of metadata filtering for precise retrieval
- [ ] Evaluation of RAG system performance with quantitative metrics

---

## Pre-Lab Setup

* Create / edit a `.gitignore` file:

```plaintext
.env
*.db
chromadb/
chroma_db/
vector_store/
__pycache__/
*.pyc
```

Create memory-retrieval-lab.

### Document Collection

Gather 5-10 PDF documents in your chosen domain:

**Suggested Domains:**
- **Academic:** Research papers from your field of study
- **Professional:** Industry whitepapers, technical specifications
- **Educational:** Course syllabi, lecture notes, textbooks
- **Medical:** Clinical guidelines, research articles (public domain only)
- **Legal:** Case law, legal opinions (public domain only)

**Requirements:**
- Minimum 5 documents, each at least 5 pages
- All documents should be on related topics (same domain)
- Ensure you have legal right to use these documents

Create a `documents/` folder and place your PDFs there.

---

## Part 1: Secure Configuration & Setup (15 minutes)

### Task 1.1: Configuration Manager

Create `config.py` to centralize all configuration:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration for the RAG system"""
    
    # API Keys
    HF_TOKEN = os.getenv('HF_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Embedding Configuration
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION = 384
    
    # Chunking Configuration
    CHUNK_SIZE = 400  # Tokens - adjust based on your domain
    CHUNK_OVERLAP = 100  # Tokens
    
    # Vector Store Configuration
    PERSIST_DIRECTORY = "./vector_store"
    COLLECTION_NAME = "documents"
    
    # Retrieval Configuration
    DEFAULT_K = 4  # Number of chunks to retrieve
    SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score
    
    # Memory Configuration
    BUFFER_SIZE = 10  # Number of recent messages to keep in buffer
    
    # LLM Configuration (choose one)
    LLM_PROVIDER = "ollama"  # Options: "ollama", "openai"
    LLM_MODEL = "llama3.2"  # Or "gpt-4o-mini" for OpenAI
    LLM_TEMPERATURE = 0.0  # Lower = more deterministic
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.HF_TOKEN:
            errors.append("HF_TOKEN not found in .env file")
        
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not found in .env file (required for OpenAI)")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
        
        print("✓ Configuration validated successfully")

# Validate configuration on import
Config.validate()
```

**Deliverable 1:** Screenshot showing successful configuration validation

---

## Part 2: Document Processing Pipeline (30 minutes)

### Task 2.1: Advanced Document Loader

Create `document_processor.py`:

```python
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
import tiktoken
from config import Config

class DocumentProcessor:
    """Handles document loading, chunking, and metadata enrichment"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=self._tiktoken_len,
            separators=["\n\n", "\n", " ", ""]  # Try these in order
        )
    
    @staticmethod
    def _tiktoken_len(text: str) -> int:
        """Calculate token count using tiktoken"""
        tokenizer = tiktoken.get_encoding('cl100k_base')
        tokens = tokenizer.encode(text, disallowed_special=())
        return len(tokens)
    
    def load_documents(self, directory: str = "documents") -> List[Document]:
        """Load all PDFs from directory"""
        loader = DirectoryLoader(
            directory,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        
        print(f"Loading documents from {directory}...")
        documents = loader.load()
        print(f"✓ Loaded {len(documents)} pages from PDFs")
        
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks with metadata enrichment"""
        print("Chunking documents...")
        
        chunks = self.text_splitter.split_documents(documents)
        
        # Enrich metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = i
            chunk.metadata['chunk_size'] = len(chunk.page_content)
            chunk.metadata['domain'] = Config.COLLECTION_NAME
            
            # TODO: Add domain-specific metadata
            # Example for medical: chunk.metadata['document_type'] = 'clinical_guideline'
            # Example for legal: chunk.metadata['jurisdiction'] = 'federal'
            # Example for academic: chunk.metadata['year'] = 2024
        
        print(f"✓ Created {len(chunks)} chunks")
        print(f"   Average chunk size: {sum(c.metadata['chunk_size'] for c in chunks) / len(chunks):.0f} chars")
        
        return chunks
    
    def display_sample_chunks(self, chunks: List[Document], n: int = 3):
        """Display sample chunks for verification"""
        print(f"\nSample of first {n} chunks:")
        for i, chunk in enumerate(chunks[:n]):
            print(f"\n--- Chunk {i} ---")
            print(f"Content: {chunk.page_content[:200]}...")
            print(f"Metadata: {chunk.metadata}")

# Usage example
if __name__ == "__main__":
    processor = DocumentProcessor()
    docs = processor.load_documents()
    chunks = processor.chunk_documents(docs)
    processor.display_sample_chunks(chunks)
```

**YOUR TASK:**
1. Modify the `chunk_documents` method to add **domain-specific metadata** relevant to your chosen domain
2. Experiment with different chunk sizes (200, 400, 800) and document which works best for your domain
3. Add error handling for corrupted or unreadable PDFs

**Deliverable 2:** 
- Complete `document_processor.py` with domain-specific metadata
- Brief write-up (200 words) explaining your chunking strategy choice
- Screenshot of sample chunks with metadata

---

## Part 3: Vector Store Implementation (25 minutes)

### Task 3.1: Vector Store Manager with Metadata Filtering

Create `vector_store_manager.py`:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List, Dict, Any
from langchain.schema import Document
from config import Config
import os

class VectorStoreManager:
    """Manages vector store creation, querying, and metadata filtering"""
    
    def __init__(self):
        print("Initializing embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        self.db = None
    
    def create_vector_store(self, chunks: List[Document]) -> None:
        """Create and persist vector store from document chunks"""
        print("Creating vector store...")
        print(f"   Embedding {len(chunks)} chunks...")
        print(f"   This may take 1-2 minutes...")
        
        self.db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=Config.PERSIST_DIRECTORY,
            collection_name=Config.COLLECTION_NAME
        )
        
        print(f"✓ Vector store created and persisted to {Config.PERSIST_DIRECTORY}")
    
    def load_vector_store(self) -> None:
        """Load existing vector store from disk"""
        if not os.path.exists(Config.PERSIST_DIRECTORY):
            raise FileNotFoundError(f"No vector store found at {Config.PERSIST_DIRECTORY}")
        
        print("Loading existing vector store...")
        self.db = Chroma(
            persist_directory=Config.PERSIST_DIRECTORY,
            embedding_function=self.embeddings,
            collection_name=Config.COLLECTION_NAME
        )
        print("✓ Vector store loaded")
    
    def search(
        self, 
        query: str, 
        k: int = None,
        metadata_filter: Dict[str, Any] = None
    ) -> List[tuple]:
        """
        Search vector store with optional metadata filtering
        
        Args:
            query: Search query string
            k: Number of results to return (default from config)
            metadata_filter: Dict of metadata key-value pairs to filter on
        
        Returns:
            List of (Document, score) tuples
        """
        if self.db is None:
            raise ValueError("Vector store not loaded. Call create_vector_store or load_vector_store first.")
        
        k = k or Config.DEFAULT_K
        
        # TODO: Implement metadata filtering
        # Hint: Chroma supports metadata filtering with where clauses
        # Example: where={"year": {"$gte": 2020}}
        
        results = self.db.similarity_search_with_score(
            query,
            k=k,
            # filter=metadata_filter  # Add this parameter
        )
        
        return results
    
    def display_search_results(self, query: str, results: List[tuple]) -> None:
        """Pretty print search results"""
        print("=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n[{i}] Score: {score:.4f}")
            print(f"    Content: {doc.page_content[:200]}...")
            print(f"    Metadata: {doc.metadata}")
        
        print("\n")

# Usage example
if __name__ == "__main__":
    from document_processor import DocumentProcessor
    
    # Process documents
    processor = DocumentProcessor()
    docs = processor.load_documents()
    chunks = processor.chunk_documents(docs)
    
    # Create vector store
    vs_manager = VectorStoreManager()
    vs_manager.create_vector_store(chunks)
    
    # Test search
    results = vs_manager.search("your test query here", k=3)
    vs_manager.display_search_results("your test query here", results)
```

**YOUR TASK:**
1. Implement metadata filtering in the `search` method (see Chroma documentation for `where` clause syntax)
2. Add a method `search_with_threshold` that only returns results above a certain similarity score
3. Create 5 test queries relevant to your domain and document retrieval quality

**Deliverable 3:**
- Complete `vector_store_manager.py` with metadata filtering
- Test results for 5 domain-specific queries
- Example of metadata filtering in action (e.g., "only search documents from 2023")

---

## Part 4: Hybrid Memory System (30 minutes)

### Task 4.1: Conversation Buffer + Vector Store Memory

Create `memory_manager.py`:

```python
from typing import List, Dict, Tuple
from collections import deque
from config import Config

class HybridMemory:
    """
    Implements hybrid memory:
    - Short-term: Conversation buffer (last N turns)
    - Long-term: Vector store (all conversations, searchable)
    """
    
    def __init__(self, vector_store_manager):
        self.vector_store = vector_store_manager
        
        # Short-term memory: FIFO buffer
        self.buffer = deque(maxlen=Config.BUFFER_SIZE)
        
        # Track conversation metadata
        self.turn_count = 0
        self.session_id = self._generate_session_id()
    
    @staticmethod
    def _generate_session_id() -> str:
        """Generate unique session identifier"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def add_turn(self, user_message: str, agent_response: str) -> None:
        """Add a conversation turn to both short and long-term memory"""
        self.turn_count += 1
        
        # Add to short-term buffer
        turn = {
            'turn_id': self.turn_count,
            'user': user_message,
            'agent': agent_response,
            'session_id': self.session_id
        }
        self.buffer.append(turn)
        
        # TODO: Add to long-term vector store
        # Hint: Create a Document with the conversation turn and metadata
        # Store it in the vector store for future semantic search
        
        print(f"✓ Turn {self.turn_count} added to memory")
    
    def get_recent_context(self, n: int = None) -> List[Dict]:
        """Retrieve recent conversation turns from buffer"""
        n = n or Config.BUFFER_SIZE
        return list(self.buffer)[-n:]
    
    def search_history(self, query: str, k: int = 3) -> List[Dict]:
        """Search past conversations semantically using vector store"""
        # TODO: Implement semantic search over past conversations
        # Hint: Use vector_store_manager.search with appropriate metadata filter
        # Filter: only search chunks that are conversation history, not documents
        
        pass
    
    def format_context_for_prompt(self) -> str:
        """Format recent context as a string for LLM prompt injection"""
        recent = self.get_recent_context()
        
        if not recent:
            return ""
        
        context = "Recent conversation history:\n"
        for turn in recent:
            context += f"User: {turn['user']}\n"
            context += f"Agent: {turn['agent']}\n\n"
        
        return context
    
    def display_buffer(self) -> None:
        """Display current buffer contents"""
        print(f"\nCurrent Buffer ({len(self.buffer)} turns):")
        for turn in self.buffer:
            print(f"  Turn {turn['turn_id']}:")
            print(f"    User: {turn['user'][:100]}...")
            print(f"    Agent: {turn['agent'][:100]}...")
```

**YOUR TASK:**
1. Complete the `add_turn` method to store conversations in the vector store
2. Implement the `search_history` method for semantic search over past conversations
3. Add metadata to distinguish document chunks from conversation chunks
4. Test the hybrid memory system with a multi-turn conversation

**Deliverable 4:**
- Complete `memory_manager.py`
- Demonstration of a 10-turn conversation showing both buffer memory and vector store memory
- Example of searching past conversation history semantically

---

## Part 5: RAG Agent with Hybrid Memory (20 minutes)

### Task 5.1: Complete Agent Implementation

Create `rag_agent.py`:

```python
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from vector_store_manager import VectorStoreManager
from memory_manager import HybridMemory
from config import Config
from typing import Optional

class RAGAgent:
    """RAG-enhanced conversational agent with hybrid memory"""
    
    def __init__(self):
        # Initialize vector store
        self.vs_manager = VectorStoreManager()
        self.vs_manager.load_vector_store()
        
        # Initialize memory
        self.memory = HybridMemory(self.vs_manager)
        
        # Initialize LLM
        if Config.LLM_PROVIDER == "ollama":
            self.llm = Ollama(
                model=Config.LLM_MODEL,
                temperature=Config.LLM_TEMPERATURE
            )
        elif Config.LLM_PROVIDER == "openai":
            self.llm = ChatOpenAI(
                model=Config.LLM_MODEL,
                temperature=Config.LLM_TEMPERATURE
            )
        
        # Create RAG chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vs_manager.db.as_retriever(
                search_kwargs={"k": Config.DEFAULT_K}
            ),
            return_source_documents=True
        )
    
    def query(
        self, 
        question: str, 
        use_memory: bool = True,
        metadata_filter: Optional[dict] = None
    ) -> dict:
        """
        Query the RAG system with optional memory context
        
        Args:
            question: User's question
            use_memory: Whether to include conversation history
            metadata_filter: Optional metadata filter for retrieval
        
        Returns:
            Dict with 'answer', 'sources', and 'memory_context'
        """
        # Build prompt with memory context if requested
        if use_memory:
            memory_context = self.memory.format_context_for_prompt()
            enhanced_question = f"{memory_context}\nCurrent question: {question}"
        else:
            enhanced_question = question
        
        # Get answer from RAG chain
        result = self.qa_chain.invoke({"query": enhanced_question})
        
        # Store in memory
        self.memory.add_turn(question, result['result'])
        
        return {
            'answer': result['result'],
            'sources': result['source_documents'],
            'memory_used': use_memory,
            'turn_count': self.memory.turn_count
        }
    
    def interactive_session(self):
        """Run an interactive Q&A session"""
        print("=" * 70)
        print("RAG Agent - Interactive Session")
        print("=" * 70)
        print("Type 'quit' to exit, 'history' to see past questions, 'buffer' to see recent context")
        print()
        
        while True:
            question = input("You: ").strip()
            
            if question.lower() == 'quit':
                print("Goodbye!")
                break
            
            elif question.lower() == 'history':
                # TODO: Implement history search
                print("Searching history...")
                pass
            
            elif question.lower() == 'buffer':
                self.memory.display_buffer()
                continue
            
            elif not question:
                continue
            
            # Get response
            result = self.query(question)
            
            print(f"\nAgent: {result['answer']}\n")
            print(f"Sources used: {len(result['sources'])}")
            print(f"Memory context: {'Yes' if result['memory_used'] else 'No'}")
            print(f"Turn: {result['turn_count']}\n")
            print("-" * 70 + "\n")

# Usage
if __name__ == "__main__":
    agent = RAGAgent()
    agent.interactive_session()
```

**YOUR TASK:**
1. Complete the `interactive_session` method to handle the 'history' command
2. Add error handling for failed LLM calls or retrieval errors
3. Implement a `clear_memory` method to reset the conversation
4. Add optional citation display showing which source documents were used

**Deliverable 5:**
- Complete `rag_agent.py`
- Recording or transcript of an interactive session (10+ turns)
- Demonstration of memory persistence across multiple questions

---

## Part 6: Evaluation & Analysis (15 minutes)

### Task 6.1: Retrieval Quality Metrics

Create `evaluation.py`:

```python
from typing import List, Tuple
from vector_store_manager import VectorStoreManager
import numpy as np

class RAGEvaluator:
    """Evaluate RAG system performance"""
    
    def __init__(self, vs_manager: VectorStoreManager):
        self.vs_manager = vs_manager
    
    def evaluate_retrieval_relevance(
        self,
        test_queries: List[Tuple[str, List[str]]]
    ) -> dict:
        """
        Evaluate retrieval quality using test queries with known relevant docs
        
        Args:
            test_queries: List of (query, list_of_relevant_doc_ids) tuples
        
        Returns:
            Dict with precision, recall, and F1 scores
        """
        precisions = []
        recalls = []
        
        for query, relevant_ids in test_queries:
            # Get retrieval results
            results = self.vs_manager.search(query, k=5)
            retrieved_ids = [doc.metadata.get('chunk_id') for doc, _ in results]
            
            # Calculate metrics
            relevant_set = set(relevant_ids)
            retrieved_set = set(retrieved_ids)
            
            true_positives = len(relevant_set & retrieved_set)
            
            precision = true_positives / len(retrieved_set) if retrieved_set else 0
            recall = true_positives / len(relevant_set) if relevant_set else 0
            
            precisions.append(precision)
            recalls.append(recall)
        
        avg_precision = np.mean(precisions)
        avg_recall = np.mean(recalls)
        f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0
        
        return {
            'precision': avg_precision,
            'recall': avg_recall,
            'f1_score': f1,
            'num_queries': len(test_queries)
        }
    
    def analyze_chunk_size_impact(self, chunk_sizes: List[int]) -> dict:
        """
        Analyze how chunk size affects retrieval quality
        
        YOUR TASK: Implement this method
        - Re-chunk documents with different sizes
        - Compare retrieval quality metrics
        - Return analysis results
        """
        pass
    
    def generate_report(self) -> str:
        """Generate evaluation report"""
        report = "# RAG System Evaluation Report\n\n"
        
        # TODO: Add sections:
        # - System configuration
        # - Document statistics (count, avg size, domain)
        # - Retrieval quality metrics
        # - Recommendations for improvements
        
        return report

# YOUR TEST QUERIES
# Create at least 10 test queries for your domain
TEST_QUERIES = [
    # Example format: ("query", [list of relevant chunk IDs])
    # ("What is maximum likelihood?", [45, 46, 47]),
    # ("Explain binomial distribution", [120, 121]),
]
```

**YOUR TASK:**
1. Create at least 10 test queries for your domain with manually identified relevant chunks
2. Run the evaluation and achieve at least 60% precision and 40% recall
3. Implement the `analyze_chunk_size_impact` method
4. Generate a comprehensive evaluation report

**Deliverable 6:**
- Complete `evaluation.py` with domain-specific test queries
- Evaluation metrics report showing precision, recall, and F1 scores
- Analysis of chunk size impact on retrieval quality
- Recommendations for system improvements

---

## Part 7: Reflection & Analysis (Required Written Component)

### Task 7.1: Engineering Judgment Questions

Answer the following questions in a separate document (`lab_reflection.md`):

1. **Cost Analysis (200 words)**
   - Calculate the cost of processing your documents if you used OpenAI embeddings instead of HuggingFace
   - Estimate the cost per query if using OpenAI's GPT-4 instead of local Ollama
   - At what scale would the free/local approach become more expensive than cloud services?

2. **Architecture Trade-offs (250 words)**
   - Explain your chunk size choice and why it's optimal for your domain
   - Compare your hybrid memory system to using only conversation buffer
   - Discuss when you would choose to use metadata filtering vs. pure semantic search

3. **Ethical & Safety Considerations (200 words)**
   - What data privacy concerns exist with your chosen domain (medical, legal, etc.)?
   - How would you prevent prompt injection attacks via retrieved documents?
   - What happens if the source documents contain biased or incorrect information?

4. **Production Readiness (250 words)**
   - List 3 things you would change before deploying this to production
   - How would you handle document updates (new versions, corrections)?
   - What monitoring and logging would you implement?

5. **Domain-Specific Insights (200 words)**
   - What makes your domain uniquely challenging for RAG?
   - Did you discover any failure modes specific to your document type?
   - What domain-specific preprocessing would improve results?

**Deliverable 7:** Complete `lab_reflection.md` with thoughtful answers (minimum 1100 words total)

---

## Submission Requirements

### Required Files Structure

```
memory-retrieval-lab/
├── config.py
├── document_processor.py
├── vector_store_manager.py
├── memory_manager.py
├── rag_agent.py
├── evaluation.py
├── documents/                # Your source PDFs
│   ├── doc1.pdf
│   ├── doc2.pdf
│   └── ...
├── vector_store/             # Generated (not committed)
├── outputs/                  # Screenshots, results
│   ├── config_validation.png
│   ├── sample_chunks.png
│   ├── search_results.png
│   ├── interactive_session.txt
│   └── evaluation_report.md
└── lab_reflection.md         # Your written analysis
```

### Submission Checklist

- [ ] All Python files are properly documented with docstrings
- [ ] Code runs without errors on instructor's machine (with proper .env setup)
- [ ] `.env.example` file included (with dummy values)
- [ ] All deliverables (1-7) are complete
- [ ] Evaluation report shows at least 60% precision
- [ ] Lab reflection document is at least 1100 words
- [ ] README.md explains domain choice and how to run the code
- [ ] No hardcoded API keys or sensitive information
- [ ] Code follows PEP 8 style guidelines

---

## Assessment Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Code Quality** | 20 | Clean, documented, follows best practices |
| **Security** | 10 | Proper API key management, no hardcoded secrets |
| **Functionality** | 25 | All required features implemented and working |
| **Memory System** | 15 | Hybrid memory correctly implemented |
| **Evaluation** | 15 | Comprehensive evaluation with good metrics |
| **Reflection** | 15 | Thoughtful analysis of trade-offs and decisions |
| **Total** | **100** | |

### Grading Notes

**Pass Criteria (70/100):**
- Environment is reproducible (code runs)
- Keys are secured (not hardcoded)
- All 7 deliverables attempted
- Reflection questions answered with reasoning

**Fail Criteria (Automatic 0):**
- Hardcoded API keys in submitted code
- Code crashes due to missing dependencies
- Exact copy of demo code without required variations
- Plagiarism or use of unauthorized AI assistance beyond coding help

---

## Tips for Success

1. **Start Early:** Vector store creation can take time for large document sets
2. **Test Incrementally:** Don't write all code at once - test each component
3. **Document Your Choices:** Explain why you made specific architecture decisions
4. **Ask Questions:** If stuck, post in class discussion forum (but don't share complete solutions)
5. **Commit Often:** Use git to track your progress and enable rollback
6. **Read Error Messages:** Most errors have clear solutions - read tracebacks carefully

---

## Common Pitfalls to Avoid

❌ **Don't:**
- Hardcode API keys
- Use the exact same test queries as the demo
- Skip the chunking strategy analysis
- Ignore retrieval quality metrics
- Submit without testing on a fresh environment

✅ **Do:**
- Use `.env` for all secrets
- Create domain-specific test queries
- Experiment with different chunk sizes
- Analyze and iterate on retrieval quality
- Test your submission in a clean virtual environment

---

## Office Hours & Support

If you encounter issues:
1. Check the demo code for reference patterns
2. Review the glossary for concept clarification
3. Search LangChain documentation for API details
4. Post specific error messages in discussion forum
5. Attend office hours for debugging help

**Remember:** The goal is understanding, not perfection. Document what you tried, even if it didn't work as expected.

---

## Extra Credit Opportunities (+10 points each, max 20)

1. **Advanced Evaluation (+10 points)**
   - Implement RAGAS (RAG Assessment) metrics
   - Use LLM-as-judge to evaluate answer quality
   - Create a benchmark dataset for your domain

2. **Production Features (+10 points)**
   - Implement caching for frequent queries
   - Add rate limiting and error recovery
   - Create a simple web interface with Streamlit or Gradio

3. **Multi-Modal RAG (+10 points)**
   - Extract and index images from PDFs
   - Implement vision-based retrieval for diagrams/charts
   - Handle tables and structured data

---

**Good luck! Remember: this lab is about building intuition for RAG systems, not just completing a checklist. Focus on understanding the "why" behind each architectural choice.**
