# IT HelpDesk AI

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F00?style=flat)
![Claude](https://img.shields.io/badge/Claude_API-Anthropic-6B4FBB?style=flat)

An AI-powered IT Helpdesk Chatbot that uses **RAG (Retrieval-Augmented Generation)** and **AI Agents** to answer IT support questions accurately from a curated knowledge base.

---

## Architecture

```
User Query
    |
    v
+----------+     +---------------+     +--------------+
| React UI |---->|   FastAPI     |---->| Router Agent |
| (Vite +  |     |   Backend     |     | (Classify    |
| Tailwind)|<----|   Port 8000   |     |  Category)   |
+----------+     +---------------+     +------+-------+
                                              |
                                              v
                                    +------------------+
                                    |  RAG Pipeline     |
                                    |                   |
                                    |  1. Retriever     |
                                    |     (ChromaDB)    |
                                    |  2. Reranker      |
                                    |  3. Generator     |
                                    |     (Claude LLM)  |
                                    +--------+---------+
                                             |
                                             v
                                    +------------------+
                                    | Escalation Agent  |
                                    | (Human handoff    |
                                    |  detection)       |
                                    +------------------+
```

## Features

- **RAG-Powered Responses** — Answers grounded in a curated IT knowledge base, not hallucinated
- **Smart Query Routing** — AI agent classifies queries into categories for targeted retrieval
- **Escalation Detection** — Automatically detects when human IT support is needed
- **Source Citations** — Every response cites the source document for transparency
- **Confidence Scoring** — Visual confidence indicators on each response
- **User Feedback** — Thumbs up/down rating system with analytics
- **Multi-Turn Conversations** — Maintains context across conversation turns
- **Analytics Dashboard** — Track query patterns, satisfaction rates, and escalations
- **Modern Dark UI** — Professional chat interface built with React + Tailwind CSS

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, Tailwind CSS, Recharts |
| **Backend** | Python 3.11+, FastAPI, Uvicorn |
| **Vector DB** | ChromaDB (persistent local storage) |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **LLM** | Anthropic Claude API (claude-sonnet-4-20250514) |
| **AI Agents** | Router Agent, Escalation Agent, Feedback Agent |

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp ../.env.example ../.env
# Edit .env and add your ANTHROPIC_API_KEY

# 5. Index knowledge base documents (first time)
cd ..
python -m backend.knowledge_base.embedder

# 6. Start the API server
cd backend
python main.py
# Server runs on http://localhost:8000
```

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
# App runs on http://localhost:5173
```

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send a message and get AI response |
| `POST` | `/feedback` | Submit feedback on a response |
| `GET` | `/analytics` | Get usage analytics and metrics |
| `POST` | `/admin/reindex` | Re-index knowledge base documents |
| `GET` | `/health` | Health check endpoint |

### POST /chat

**Request:**
```json
{
  "message": "How do I reset my password?",
  "conversation_id": "optional-uuid"
}
```

**Response:**
```json
{
  "response": "To reset your password, follow these steps...",
  "sources": [
    { "document": "password-reset.md", "relevance": 0.92 }
  ],
  "category": "password",
  "confidence": 0.89,
  "escalated": false,
  "conversation_id": "uuid-string"
}
```

### POST /feedback

**Request:**
```json
{
  "conversation_id": "uuid",
  "message_id": "uuid",
  "rating": "helpful",
  "feedback_text": "Very clear instructions!"
}
```

## Knowledge Base

The chatbot is trained on 10 IT support documents covering:

| Document | Category |
|----------|----------|
| Password Reset | password |
| VPN Setup | vpn |
| WiFi Troubleshooting | wifi |
| Email Setup | email |
| Software Installation | software |
| Printer Setup | printer |
| Security Policies | security |
| Hardware Issues | hardware |
| Onboarding Checklist | onboarding |
| Cloud Services | cloud |

## How RAG Works

1. **Document Processing** — IT support documents are split into small chunks (500 chars) with metadata
2. **Embedding** — Each chunk is converted to a vector using sentence-transformers (all-MiniLM-L6-v2)
3. **Storage** — Vectors are stored in ChromaDB for fast similarity search
4. **Retrieval** — When a user asks a question, the most relevant chunks are retrieved
5. **Reranking** — Retrieved chunks are scored and reranked for relevance
6. **Generation** — Claude LLM generates a response using ONLY the retrieved context

This ensures responses are accurate, grounded in real documentation, and never hallucinated.

## Screenshots

> Screenshots will be added after deployment

## Future Improvements

- Slack / Microsoft Teams integration
- JIRA ticket creation for escalated issues
- Voice support (speech-to-text input)
- Multi-language support
- Fine-tuned embedding model for IT domain
- User authentication and role-based access
- Knowledge base admin UI for document management
- Automated knowledge base updates from IT wiki

---

Built with Claude API by Anthropic | Portfolio Project
