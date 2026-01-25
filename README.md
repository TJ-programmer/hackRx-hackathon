# HackRx — Document Q&A API

HackRx is a FastAPI-based document question-answering service that:
- Parses documents (PDFs, web pages),
- Splits them into chunks,
- Embeds chunks with a TF-IDF vectorizer,
- Stores embeddings in a Qdrant vector store (in-memory by default),
- Retrieves relevant context via similarity search and generates short answers using an LLM (OpenAI SDK compatible).

This README shows how to run the service locally, call the API, and understand the implementation details and known caveats.

---

## Features
- FastAPI server with a single Q&A endpoint: POST /api/v1/hackrx/run
- Document parsing + chunking (langchain RecursiveCharacterTextSplitter)
- Lightweight TF-IDF embeddings (scikit-learn) tuned to 384 dimensions
- In-memory Qdrant vector store for fast local testing
- LLM answer generation (supports >=1.0 OpenAI SDK or legacy SDK)
- Simple HTTP Bearer token authentication
- Dockerfile for containerized deployment
- Deployment guides included (Render, Railway, Fly.io, localtunnel)

---

## Quick Start (Local)

Prerequisites:
- Python 3.12
- pip
- (Optional) Node.js + npm if you want to use localtunnel for exposing local server

1. Clone repository
```bash
git clone https://github.com/TJ-programmer/hackRx-hackathon.git
cd hackRx-hackathon
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install dependencies
```bash
pip install -r requirements.txt
# or use the app-specific pinned list:
pip install -r app/requirements.txt
```

4. Create a `.env` in the project root (or export environment variables):
```
OPENAI_API_KEY=your_openai_api_key
API_AUTH_TOKEN=your_secure_token
LOG_LEVEL=INFO
```

5. Run the app
```bash
# From repo root
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- Health check: http://localhost:8000/health
- API docs (Swagger): http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

Notes: run_local.py and start_local.* scripts are provided for convenience in the repository.

---

## Quick Start (Docker)

Build and run with Docker:

1. Build image
```bash
docker build -t hackrx:latest .
```

2. Run container
```bash
docker run -e OPENAI_API_KEY=your_key -e API_AUTH_TOKEN=your_token -p 8000:8000 hackrx:latest
```

Visit http://localhost:8000.

---

## API

POST /api/v1/hackrx/run
- Description: Parse the provided document, index it, and answer the list of questions.
- Authentication: Bearer token required. Use header `Authorization: Bearer <API_AUTH_TOKEN>`.

Request body (JSON):
```json
{
  "documents": "https://example.com/document.pdf",
  "questions": ["What is the main point?", "List key takeaways."]
}
```
Note: The Pydantic model expects the field alias `documents` (mapped to `document_url` internally).

Response (JSON):
```json
{
  "answers": ["Single-sentence answer 1", "Single-sentence answer 2"]
}
```

Example curl:
```bash
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_secure_token" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": ["What is the document about?"]
  }'
```

---

## Implementation Notes & Architecture

High-level pipeline:
1. Document parsing (app/parser.py) -> raw text
2. Chunking with RecursiveCharacterTextSplitter (app/chunker.py)
3. Embedding chunks with TF-IDF (app/embedder.py) -> 384-dimensional vectors
4. Store vectors in Qdrant (app/vector_store.py) — currently in-memory QdrantClient
5. For each question:
   - Embed the question
   - Search vector store for top-k similar chunks
   - Pass retrieved context to LLM (app/llm.py) to produce a concise, one-sentence answer

Important implementation details found in the code:
- Embeddings:
  - TF-IDF vectorizer is configured with max_features=384 and normalized to unit vectors, then padded/truncated to 384 dims.
  - Current embedder implementation calls vectorizer.fit_transform() on whatever texts are provided; this fits the vectorizer on the query text when creating question embeddings — which can produce inconsistent embeddings relative to the document chunk embeddings. For production, persist a fitted vectorizer (fit on document chunks) and call transform() for queries.
- Vector store:
  - By default QdrantClient is instantiated with location=":memory:", so the collection is in-memory and ephemeral.
  - For persistence / production use, replace QdrantClient(...) to point to a remote Qdrant instance (see app/DEPLOYMENT.md and OPTIMIZED_DEPLOYMENT.md).
- LLM:
  - The code attempts to use the modern OpenAI SDK (OpenAI client) with base_url configured to https://openrouter.ai/api/v1 and falls back to the legacy openai library if needed.
  - Default model in generate_answer() is "deepseek/deepseek-chat-v3-0324:free". Modify the model and max_tokens via the function signature or environment as appropriate.
- Authentication:
  - app/auth.py enforces a Bearer token; API_AUTH_TOKEN (env) must be set. If not set, the server returns a 500 on verification calls.

---

## Environment Variables

Minimum required:
- OPENAI_API_KEY — required for LLM calls (app/llm.py will raise if missing)
- API_AUTH_TOKEN — required by app/auth.py for endpoint access

Optional / recommended:
- LOG_LEVEL — e.g., INFO, DEBUG
- LOG_FILE_PATH — if the app is extended to log to file
- For production Qdrant usage:
  - QDRANT_URL, QDRANT_API_KEY — if you change vector_store.py to connect to a remote Qdrant instance

Note: The current code uses an in-memory Qdrant instance by default. If you want persistence, update app/vector_store.py to use QdrantClient(url=..., api_key=...) and set the appropriate environment vars.

---

## Troubleshooting

- "OPENAI_API_KEY not set" / server startup error
  - Ensure OPENAI_API_KEY is in your environment or in a .env loaded by python-dotenv.
- 401 Unauthorized / Invalid or missing token
  - Provide `Authorization: Bearer <API_AUTH_TOKEN>` header where API_AUTH_TOKEN matches the env var.
- Empty answers / "Failed to extract content"
  - Confirm the document URL is accessible and parseable. The parser supports common web pages and PDFs; network access may be required.
- Embedding dimension mismatches / no results
  - Ensure embedder and vector_store dimensions match (currently 384). If you modify embedder dimensions, update vector_store.dimension accordingly.
- Ephemeral vectors (data lost between restarts)
  - Qdrant is in-memory by default. Use a persistent Qdrant instance for production.

---

## Testing & Development

- Unit testing: repository contains a test file test_llm.py. You can run tests with:
```bash
# If using pytest
pip install pytest
pytest
```
- Logging: the project uses python-json-logger via app/logging_config.py. Set LOG_LEVEL to DEBUG for verbose logs during development.

---

## Deployment

- The repository contains detailed deployment guides:
  - LOCAL_DEPLOYMENT.md — exposes local server via localtunnel
  - OPTIMIZED_DEPLOYMENT.md — notes on slimming dependencies for constrained image sizes
  - app/DEPLOYMENT.md — step-by-step for Railway, Render, Fly.io

- For production you will likely:
  - Use a persistent Qdrant instance
  - Persist the fitted TF-IDF vectorizer (or use remote embeddings like OpenAI Embeddings)
  - Replace the in-memory Qdrant client with a remote client using URL/API key
  - Add rate limiting, CORS, and more robust auth (JWT or OAuth) as needed

---

## Security Notes
- Do not commit .env files or API keys to source control.
- API_AUTH_TOKEN is a simple bearer token — rotate it regularly and consider a stronger auth mechanism for public deployments.
- Limit access to the OpenAI API key and monitor usage to avoid unexpected charges.

---

## Contributing
- Fork the repo, create a feature branch, and open a pull request. Please document breaking changes.
- If you improve production readiness (persistence, embedding consistency, tests), include migration notes.

---

## License
No license file is included in the repository. Check with the repository owner for licensing terms before using the code in production.

---

If you'd like, I can:
- Add a short "How it works" diagram or ASCII flowchart,
- Draft a small patch that persists the TF-IDF vectorizer to disk and switches question embeddings to transform() for consistency,
- Add a sample integration test that runs the full pipeline on a small text file.
