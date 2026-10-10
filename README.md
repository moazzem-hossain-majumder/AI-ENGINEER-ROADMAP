# 🚀 The AI Engineer Roadmap: Zero to Production

> **A project-first journey to becoming a production-grade AI Engineer.**  
> Every single concept is paired with an atomic, hands-on, runnable project: **Explain Topic ➔ Code Project ➔ Verify Learning Outcome ➔ Next Step.**

---

## 🧭 Philosophy & How This Roadmap Works

Most AI roadmaps are passive lists of videos and articles. **This roadmap is different:**
1. **Ultra-Atomic Steps:** We start with the simplest 20-line scripts to understand the raw mechanics of an LLM call before adding any abstraction.
2. **Concept ➔ Project Pairing:** You never read about a concept without building a working project that demonstrates it.
3. **Progressive Capstones:** After mastering a group of atomic concepts, you synthesize them into a real-world, production-ready capstone project.
4. **Multi-Model & Provider Agnostic:** Leverage **Groq**, **Google Gemini**, **Hugging Face**, and **OpenAI** without vendor lock-in.

---

## 🗺️ The 8 Master Phases & Project Curriculum

```
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 01: LLM Core & Prompt Engineering Foundations (Projects 001-015) │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 02: Embeddings, Vector Search & Math (Projects 016-030)          │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 03: Retrieval-Augmented Generation (RAG) (Projects 031-050)      │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 04: Function Calling, Tools & Structured Actions (Projects 051-070│
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 05: Autonomous Agents & Multi-Agent Systems (Projects 071-090)   │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 06: Evaluation, Guardrails & Production Quality (Projects 091-110)│
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 07: Open-Source Models, Hugging Face & Fine-Tuning (Projects 111-130)
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 08: Full-Stack Capstone AI Applications (Projects 131-150+)      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Comprehensive Syllabus & Project Index

### 🔹 Phase 01: LLM Foundations & Prompt Engineering (Projects 001–015)
*Master the mechanics of API calls, token dynamics, sampling parameters, conversation state, and schemas.*

| # | Project Name | Core Topic | Learning Outcome | Status |
|---|---|---|---|:---:|
| **001** | [001-hello-llm](01-llm-foundations/001-hello-llm/) | Anatomy of an LLM API Call | Connect to Groq/Gemini, send system & user messages, inspect response metadata. | ✅ Ready |
| **002** | [002-sampling-parameters](01-llm-foundations/002-sampling-parameters/) | Temperature & Top-P Sampling | Master determinism vs. creativity, token probabilities, and stopping sequences. | ✅ Ready |
| **003** | [003-multi-turn-chat](01-llm-foundations/003-multi-turn-chat/) | Conversation History & Buffer State | Build a terminal chat loop maintaining context window state manually. | ✅ Ready |
| **004** | [004-structured-outputs](01-llm-foundations/004-structured-outputs/) | JSON Mode & Pydantic Validation | Enforce strict schema validation and parse unstructured text to typed models. | ✅ Ready |
| **005** | [005-streaming-responses](01-llm-foundations/005-streaming-responses/) | Server-Sent Events & Token Streaming | Stream tokens in real time to the CLI for low-latency user experience. | ✅ Ready |
| **006** | [006-token-budget-calculator](01-llm-foundations/006-token-budget-calculator/) | Tokenization & Cost Estimation | Calculate token usage using tiktoken and estimate cost across models. | ✅ Ready |
| **007** | [007-few-shot-prompting](01-llm-foundations/007-few-shot-prompting/) | In-Context Learning (Few-Shot) | Steer LLM behavior and output formats using canonical examples. | ✅ Ready |
| **008** | [008-chain-of-thought](01-llm-foundations/008-chain-of-thought/) | Reasoning Prompts (CoT & Zero-Shot CoT) | Guide the LLM to think step-by-step for complex logic and math. | ✅ Ready |
| **009** | [009-prompt-templates](01-llm-foundations/009-prompt-templates/) | Reusable & Composable Prompt Templates | Build dynamic parameterized prompt builders for real-world use cases. | ✅ Ready |
| **010** | [010-prompt-injection-defense](01-llm-foundations/010-prompt-injection-defense/) | Prompt Security & System Defenses | Implement input sanitization, delimiters, and adversarial prompt detection. | ✅ Ready |
| **011** | `011-role-playing-persona` | Dynamic System Personas & Tone Control | Condition model personality, constraints, and vocabulary. | 🔲 Planned |
| **012** | `012-text-summarizer-cli` | Map-Reduce & Chunked Summarization | Process documents that exceed standard single-prompt limits. | 🔲 Planned |
| **013** | `013-markdown-to-social` | Multi-Format Content Transformation | Transform long-form technical writing into LinkedIn/Twitter threads. | 🔲 Planned |
| **014** | `014-error-handling-retry` | Exponential Backoff & Provider Fallback | Handle rate limits (429), timeouts, and automatic failovers across providers. | 🔲 Planned |
| **015** | `015-phase1-capstone-cli-assistant` | **Phase 1 Capstone: Universal CLI AI Copilot** | Synthesis of Projects 001–014: multi-provider, streaming, memory, structured export. | 🔲 Capstone |

#### ▶️ Quick Run & Verification Commands for Phase 01:
Test and run any project with a single command from the project root:

```powershell
# Project 001: Hello LLM API Call
.\.venv\Scripts\python 01-llm-foundations/001-hello-llm/main.py

# Project 002: Sampling Parameters & Determinism
.\.venv\Scripts\python 01-llm-foundations/002-sampling-parameters/main.py

# Project 003: Multi-Turn Chat (Automated Demo)
.\.venv\Scripts\python 01-llm-foundations/003-multi-turn-chat/main.py

# Project 003: Multi-Turn Chat (Interactive Terminal Chat)
.\.venv\Scripts\python 01-llm-foundations/003-multi-turn-chat/main.py --interactive

# Project 004: Structured JSON & Pydantic Validation
.\.venv\Scripts\python 01-llm-foundations/004-structured-outputs/main.py

# Project 005: Real-Time Token Streaming
.\.venv\Scripts\python 01-llm-foundations/005-streaming-responses/main.py

# Project 006: Token Budgeting & Multi-Model Cost Calculator
.\.venv\Scripts\python 01-llm-foundations/006-token-budget-calculator/main.py

# Project 007: Few-Shot In-Context Classification
.\.venv\Scripts\python 01-llm-foundations/007-few-shot-prompting/main.py

# Project 008: Chain-of-Thought (CoT) Reasoning Engine
.\.venv\Scripts\python 01-llm-foundations/008-chain-of-thought/main.py

# Project 009: Dynamic Validated Prompt Templates
.\.venv\Scripts\python 01-llm-foundations/009-prompt-templates/main.py

# Project 010: Prompt Injection Defense & Input Sanitization
.\.venv\Scripts\python 01-llm-foundations/010-prompt-injection-defense/main.py
```

---

### 🔹 Phase 02: Embeddings, Semantic Search & Vector DBs (Projects 016–030)
*Learn the mathematical bedrock of AI search: vector spaces, similarity metrics, chunking, and indexing.*

| # | Project Name | Core Topic | Learning Outcome | Status |
|---|---|---|---|:---:|
| **016** | `016-first-embeddings` | Text to High-Dimensional Vectors | Generate vector embeddings and inspect dimension shapes. | 🔲 Planned |
| **017** | `017-cosine-similarity-scratch` | Vector Math & Similarity Algorithms | Implement Cosine, Euclidean, and Dot Product distance from scratch in NumPy. | 🔲 Planned |
| **018** | `018-text-chunking-strategies` | Chunking Algorithms (Fixed, Recursive) | Compare character vs recursive vs semantic chunking strategies. | 🔲 Planned |
| **019** | `019-in-memory-vector-store` | Mini Vector Database from Scratch | Build an in-memory indexed vector search engine with zero external DBs. | 🔲 Planned |
| **020** | `020-chromadb-semantic-search` | Embedded Vector Databases (ChromaDB) | Index documents, run k-NN searches, and filter by metadata. | 🔲 Planned |
| **021** | `021-faiss-high-speed-search` | FAISS (Facebook AI Similarity Search) | Quantization, IVF indexing, and scaling to hundreds of thousands of vectors. | 🔲 Planned |
| **022** | `022-multilingual-similarity` | Cross-Language Semantic Search | Match queries across different languages using multilingual embedding models. | 🔲 Planned |
| **023** | `023-document-deduplicator` | Vector Clustering & Near-Duplicate Search | Group similar documents and eliminate semantic duplicates. | 🔲 Planned |
| **024** | `024-semantic-code-search` | Code Search & AST-aware Chunking | Index Python functions and search codebases using natural language. | 🔲 Planned |
| **025** | `025-image-text-clip-search` | Multimodal Embeddings (CLIP) | Search image datasets using text queries. | 🔲 Planned |
| **030** | `030-phase2-capstone-vector-engine` | **Phase 2 Capstone: Personal Semantic Knowledge Engine** | Search across markdown notes, PDFs, and code with metadata filters. | 🔲 Capstone |

---

### 🔹 Phase 03: Retrieval-Augmented Generation (RAG) (Projects 031–050)
*From basic question answering over private text to state-of-the-art hybrid and agentic RAG architectures.*

| # | Project Name | Core Topic | Learning Outcome | Status |
|---|---|---|---|:---:|
| **031** | `031-minimal-rag-scratch` | Naive RAG Architecture | Connect Ingestion ➔ Embeddings ➔ Retrieval ➔ Prompt Augmentation in pure Python. | 🔲 Planned |
| **032** | `032-pdf-document-qa` | PDF Parsing & Table Extraction | Ingest complex multi-page PDFs and answer precise technical questions. | 🔲 Planned |
| **033** | `033-grounded-citations-rag` | Source Attribution & Citation Tracking | Return exact page numbers and quotes backing every claim in the response. | 🔲 Planned |
| **034** | `034-hybrid-search-rrf` | Hybrid Search (BM25 + Semantic) | Combine keyword search with dense vectors using Reciprocal Rank Fusion (RRF). | 🔲 Planned |
| **035** | `035-hyde-query-expansion` | Hypothetical Document Embeddings (HyDE) | Generate hypothetical answers to bridge query-document semantic gaps. | 🔲 Planned |
| **036** | `036-reranking-cross-encoders` | Cross-Encoder Reranking | Re-score top-K vector results using Cohere/BGE cross-encoders for higher precision. | 🔲 Planned |
| **037** | `037-context-compression` | Selective Context Summarization | Compress retrieved chunks to minimize token spend and avoid prompt distraction. | 🔲 Planned |
| **038** | `038-parent-child-retriever` | Multi-Vector & Parent Document Retrieval | Index small semantic chunks but return broad contextual paragraphs to the LLM. | 🔲 Planned |
| **039** | `039-hallucination-detector` | Self-Correction & Verification | Verify generated answers against retrieved context before outputting. | 🔲 Planned |
| **050** | `050-phase3-capstone-production-rag` | **Phase 3 Capstone: Enterprise Documentation RAG System** | Full pipeline: Hybrid search + Reranking + Citations + Fallback answer validation. | 🔲 Capstone |

---

### 🔹 Phase 04: Function Calling, Tools & Structured Actions (Projects 051–070)
*Teach models how to interact with the real world: APIs, databases, filesystems, and code execution.*

| # | Project Name | Core Topic | Learning Outcome | Status |
|---|---|---|---|:---:|
| **051** | `051-first-function-call` | OpenAI / Groq Tool Calling Protocol | Define JSON schemas for Python functions and parse tool call requests. | 🔲 Planned |
| **052** | `052-multi-tool-router` | Multi-Tool Orchestration | Equip model with weather, math, and unit converter tools; handle dispatch loops. | 🔲 Planned |
| **053** | `053-sqlite-database-agent` | Text-to-SQL & Database Querying | Convert natural language questions into safe SQL queries and explain the results. | 🔲 Planned |
| **054** | `054-live-web-search-bot` | Web Scraping & Live Search Tools | Integrate DuckDuckGo/Tavily search tools for up-to-the-minute real-world answers. | 🔲 Planned |
| **055** | `055-filesystem-operator` | Safe Local File I/O Tooling | Allow LLM to read, search, and edit files in a sandboxed directory. | 🔲 Planned |
| **056** | `056-python-code-interpreter` | Dynamic Python Code Execution | Let the LLM generate and run Python code to solve math, plot graphs, and analyze data. | 🔲 Planned |
| **057** | `057-human-in-the-loop-tools` | Approval & Confirmation Gates | Pause execution for sensitive tool calls (e.g. `delete_file`, `send_email`) until confirmed. | 🔲 Planned |
| **070** | `070-phase4-capstone-system-admin-bot` | **Phase 4 Capstone: Autonomous IT Ops & Diagnostics Assistant** | Inspect system metrics, query logs, diagnose errors, and write incident reports. | 🔲 Capstone |

---

### 🔹 Phase 05: Autonomous Agents & Multi-Agent Workflows (Projects 071–090)
*Architect complex multi-step reasoning, self-reflection, and specialized multi-agent teams.*

| # | Project Name | Core Topic | Learning Outcome | Status |
|---|---|---|---|:---:|
| **071** | `071-react-agent-scratch` | ReAct (Reason + Act) Loop from Scratch | Build a thought-action-observation loop without heavy agent frameworks. | 🔲 Planned |
| **072** | `072-plan-and-solve-agent` | Plan-and-Execute Pattern | Decompose complex multi-step problems into a plan before executing sub-tasks. | 🔲 Planned |
| **073** | `073-agent-memory-reflection` | Episodic & Semantic Agent Memory | Store previous interactions, reflect on mistakes, and improve over iterations. | 🔲 Planned |
| **074** | `074-supervisor-worker-team` | Multi-Agent Supervisor Pattern | Coordinator agent delegates subtasks to Researcher, Coder, and Reviewer agents. | 🔲 Planned |
| **075** | `075-hierarchical-debate-agents`| Debate & Peer Review Patterns | Multiple agents argue opposing viewpoints to arrive at balanced, robust answers. | 🔲 Planned |
| **090** | `090-phase5-capstone-devin-mini` | **Phase 5 Capstone: Autonomous Coding & Bug-Fixing Agent** | Inspect a repository, reproduce an issue with a test, write a fix, and verify tests pass. | 🔲 Capstone |

---

### 🔹 Phase 06: Evaluation, Guardrails & Production Observability (Projects 091–110)
*Quantify AI quality, guard against hallucinations, and monitor latency, cost, and toxicity.*

| # | Project Name | Core Topic | Learning Outcome | Status |
|---|---|---|---|:---:|
| **091** | `091-llm-as-a-judge` | Automated LLM Evaluation | Build rubric-based evaluation prompts to score outputs on factual accuracy and clarity. | 🔲 Planned |
| **092** | `092-rag-triad-evaluation` | RAG Triad Metrics | Evaluate Context Relevance, Groundedness, and Answer Relevance with automated metrics. | 🔲 Planned |
| **093** | `093-pii-redactor-guardrails` | Security Guardrails & PII Masking | Detect and redact emails, SSNs, and API keys before sending prompts. | 🔲 Planned |
| **094** | `094-semantic-caching` | Semantic Response Cache | Cache semantically similar queries to reduce API latency to 10ms and costs to $0. | 🔲 Planned |
| **095** | `095-tracing-opentelemetry` | Observability & OpenTelemetry | Trace multi-step LLM calls, spans, latency bottlenecks, and token costs. | 🔲 Planned |
| **110** | `110-phase6-capstone-ci-cd-evals` | **Phase 6 Capstone: Automated AI Evaluation Pipeline** | Run CI/CD test suites verifying that prompt changes don't cause performance regressions. | 🔲 Capstone |

---

### 🔹 Phase 07: Open-Source Models, Hugging Face & Fine-Tuning (Projects 111–130)
*Run and adapt models locally or on open-source infrastructure without proprietary API dependencies.*

| # | Project Name | Core Topic | Learning Outcome | Status |
|---|---|---|---|:---:|
| **111** | `111-huggingface-inference-api` | Hugging Face Serverless API | Run open-source models (Mistral, Llama, Qwen) using the Hugging Face Hub token. | 🔲 Planned |
| **112** | `112-local-quantized-inference` | GGUF & Quantized Local Models | Run 4-bit quantized LLMs on CPU/consumer GPU with llama-cpp-python. | 🔲 Planned |
| **113** | `113-dataset-curation-formatting`| Dataset Engineering & Synthesizing | Format instruction-tuning datasets in ChatML / Alpaca schemas using LLMs. | 🔲 Planned |
| **114** | `114-lora-fine-tuning-prep` | Parameter-Efficient Fine-Tuning (PEFT/LoRA)| Configure Low-Rank Adaptation (LoRA) adapters and understand weight updates. | 🔲 Planned |
| **115** | `115-model-quantization-benchmark`| FP16 vs INT8 vs INT4 Benchmark | Compare memory consumption, perplexity, and tokens/sec across quantization formats. | 🔲 Planned |
| **130** | `130-phase7-capstone-custom-domain-llm`| **Phase 7 Capstone: Fine-Tuned Specialized Domain Expert** | Fine-tune and deploy an open-source model specialized in a niche domain. | 🔲 Capstone |

---

### 🔹 Phase 08: Production Capstones & Real-World Systems (Projects 131–150+)
*End-to-end full-stack architectures solving complex enterprise and user problems.*

| # | Capstone Project | Description |
|---|---|---|
| **131** | **Multi-Tenant Enterprise Knowledge Assistant** | Full-stack RAG system with role-based access control, document upload, and citation audit trail. |
| **135** | **Autonomous Research & Newsletter Generator** | Multi-agent workflow that scrapes industry news, synthesizes key takeaways, and drafts weekly digests. |
| **140** | **Real-Time Multimodal Voice Copilot** | Low-latency audio-in/audio-out conversational assistant with vision support. |
| **150** | **Self-Hosting AI Gateway & Proxy** | Unified proxy with load balancing, rate limiting, semantic caching, and automatic failover across 5+ providers. |

---

## 🛠️ Getting Started: Setup Your Environment

### 1. Clone & Navigate
```bash
git clone https://github.com/moazzem-hossain-majumder/AI-ENGINEER-ROADMAP.git
cd AI-ENGINEER-ROADMAP
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Configure API Keys
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your API keys in `.env`:
```ini
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=...
HF_TOKEN=hf_...
OPENAI_API_KEY=...
```

> ⚠️ **Security Warning:** Never commit your `.env` file to Git. The `.gitignore` in this repository is pre-configured to keep your keys safe.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📁 Repository Structure
```
AI-ENGINEER-ROADMAP/
├── .env.example               # Secrets template (Safe for Git)
├── .gitignore                 # Excludes .env, .venv, caches
├── requirements.txt           # Master project dependencies
├── README.md                  # This master roadmap dashboard
├── 01-llm-foundations/        # Phase 1: LLM Core & Prompt Engineering
│   ├── 001-hello-llm/         # Project 1: Anatomy of an LLM Call
│   ├── 002-sampling-parameters# Project 2: Temperature & Sampling
│   ├── 003-multi-turn-chat/   # Project 3: Conversation History Loop
│   ├── 004-structured-outputs/# Project 4: JSON & Schema Validation
│   └── 005-streaming-responses# Project 5: Token Streaming
├── 02-embeddings-vector-db/   # Phase 2: Embeddings & Vector Search
├── 03-rag-systems/            # Phase 3: Retrieval-Augmented Generation
├── 04-function-calling-tools/ # Phase 4: Tools & Structured Actions
├── 05-autonomous-agents/      # Phase 5: Multi-Agent Workflows
├── 06-evaluation-guardrails/  # Phase 6: Evals, Caching & Observability
├── 07-open-source-models/     # Phase 7: Hugging Face & Fine-Tuning
└── 08-full-stack-capstones/   # Phase 8: Full-Stack Enterprise Capstones
```

---

## 💡 How to Study Each Project
Inside each project directory you will find:
1. **`README.md`**:
   - **🎯 Learning Outcome**: Concrete concepts you will master.
   - **📖 Concept Explanation**: Under-the-hood breakdown with diagrams.
   - **💻 Step-by-Step Code Walkthrough**: How the implementation works.
   - **🏋️ Exercises & Experiments**: Interactive challenges to solidify knowledge.
2. **`main.py`**: Fully functional, well-commented code that you can run with `python main.py`.

---

*Authored by Moazzem Hossain Majumder — Built for aspiring and practicing AI Engineers.*
