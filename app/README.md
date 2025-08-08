# HackRx API

A FastAPI-based document Q&A system that processes documents and answers questions using vector search and LLM.

## Features

- Document parsing (PDF, web pages)
- Text chunking and embedding
- Vector similarity search
- Question answering with LLM
- JSON logging
- Authentication support

## API Endpoint

```
POST /api/v1/hackrx/run
```

### Request Body
```json
{
  "documents": "https://example.com/document.pdf",
  "questions": ["What is the main topic?", "What are the key points?"]
}
```

### Response
```json
{
  "answers": ["Answer 1", "Answer 2"]
}
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_key
export QDRANT_URL=your_qdrant_url
export QDRANT_API_KEY=your_qdrant_key
```

3. Run the application:
```bash
uvicorn main:app --reload
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for free deployment options.

## Health Check

```
GET /health
```

Returns the API status for monitoring.
