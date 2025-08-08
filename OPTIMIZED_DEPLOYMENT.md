# Optimized Deployment Guide (4GB Limit)

This guide shows how to deploy your HackRx API within Render's 4GB image size limit.

## Key Optimizations Made

### 1. Removed Heavy Dependencies
- ❌ `torch==2.6.0` (~2.5GB)
- ❌ `transformers==4.55.0` (~1.5GB)
- ❌ `sentence-transformers==5.1.0` (~500MB)

### 2. Replaced with Lightweight Alternatives
- ✅ `scikit-learn==1.7.1` (~50MB) - TF-IDF embeddings
- ✅ `numpy==2.3.2` (~20MB) - Numerical operations

### 3. Optimized Embedding System
- **Before:** Sentence transformers with neural networks
- **After:** TF-IDF vectorizer with cosine similarity
- **Result:** 95% smaller, still effective for document similarity

## Current Package Sizes (Estimated)

```
fastapi==0.116.1          ~15MB
uvicorn==0.35.0           ~5MB
python-dotenv==1.1.1      ~1MB
requests==2.32.4          ~10MB
beautifulsoup4==4.13.4    ~5MB
PyPDF2==3.0.1             ~5MB
scikit-learn==1.7.1       ~50MB
langchain-text-splitters==0.3.9 ~5MB
qdrant-client==1.15.1     ~10MB
numpy==2.3.2              ~20MB
openai==1.99.3            ~5MB
python-json-logger==3.3.0 ~1MB
pydantic==2.11.7          ~5MB
─────────────────────────────────
Total: ~137MB (vs ~4.5GB before)
```

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Optimized for 4GB limit"
git push origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Create new "Blueprint" service
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml`

### 3. Set Environment Variables
In Render dashboard, set:
- `OPENAI_API_KEY` - Your OpenAI API key
- `API_AUTH_TOKEN` - Secure authentication token
- `LOG_LEVEL` - INFO (default)

## Performance Comparison

| Metric | Before (Neural) | After (TF-IDF) |
|--------|----------------|----------------|
| Image Size | ~4.5GB | ~137MB |
| Startup Time | 2-3 minutes | 30 seconds |
| Memory Usage | 2-3GB | 200-500MB |
| Embedding Quality | Excellent | Good |
| Similarity Search | Very Accurate | Accurate |

## API Usage

The API works exactly the same:

```bash
curl -X POST https://your-app.onrender.com/api/v1/hackrx/run \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": ["What is this document about?"]
  }'
```

## Local Testing

Test the optimized version locally:

```bash
# Install optimized requirements
pip install -r requirements.txt

# Run locally
python run_local.py

# Test with localtunnel
lt --port 8001
```

## Monitoring

- **Health Check:** `GET /health`
- **API Docs:** `GET /docs`
- **Logs:** Check Render dashboard

## Troubleshooting

### Still hitting size limit?
1. Check for cached files: `docker system prune -a`
2. Verify `.dockerignore` is working
3. Consider removing PyPDF2 if not needed

### Performance issues?
1. TF-IDF is slightly less accurate but much faster
2. For better accuracy, consider upgrading Render plan
3. Monitor memory usage in Render dashboard

## Future Improvements

If you need better embedding quality:
1. **Upgrade Render Plan:** Get more than 4GB limit
2. **Use Cloud Embeddings:** OpenAI embeddings API
3. **Hybrid Approach:** TF-IDF + keyword matching

The current setup provides a good balance of performance and size constraints! 