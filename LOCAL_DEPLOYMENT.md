# Local Deployment with Localtunnel

This guide will help you run your HackRx API locally and expose it to the internet using localtunnel.

## Prerequisites

1. **Node.js and npm** (for localtunnel)
2. **Python 3.12** (already installed)
3. **Virtual environment** (already set up)

## Step 1: Install Localtunnel

```bash
npm install -g localtunnel
```

## Step 2: Set Up Environment Variables

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
API_AUTH_TOKEN=your_secure_token_here
LOG_LEVEL=INFO
```

## Step 3: Start the FastAPI Server

### Option A: Using the provided script (Recommended)
```bash
# Windows (Command Prompt)
start_local.bat

# Windows (PowerShell)
.\start_local.ps1

# Or manually
henv\Scripts\activate
python run_local.py
```

### Option B: Manual start
```bash
# Activate virtual environment
henv\Scripts\activate

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Your API will be available at: `http://localhost:8001`

## Step 4: Expose with Localtunnel

In a new terminal window, run:

```bash
lt --port 8001
```

This will give you a public URL like: `https://abc123.loca.lt`

## Step 5: Test Your API

1. **Health Check:**
   ```
   GET https://abc123.loca.lt/health
   ```

2. **API Endpoint:**
   ```
   POST https://abc123.loca.lt/api/v1/hackrx/run
   Headers: Authorization: Bearer your_secure_token_here
   Content-Type: application/json
   
   Body:
   {
     "documents": "https://example.com/document.pdf",
     "questions": ["What is this document about?"]
   }
   ```

## API Documentation

Once running, visit:
- **Swagger UI:** `http://localhost:8001/docs`
- **ReDoc:** `http://localhost:8001/redoc`

## Troubleshooting

### Port already in use
```bash
# Find process using port 8001
netstat -ano | findstr :8001

# Kill the process
taskkill /PID <process_id> /F
```

### Localtunnel issues
```bash
# Use a specific subdomain
lt --port 8001 --subdomain hackrx-api

# Use a different port
lt --port 8001 --local-host localhost
```

### Virtual environment issues
```bash
# Recreate virtual environment
rmdir /s henv
python -m venv henv
henv\Scripts\activate
pip install -r requirements.txt
```

## Security Notes

1. **API Token:** Always use a strong API token
2. **Environment Variables:** Never commit `.env` files
3. **Public Exposure:** Localtunnel makes your API publicly accessible
4. **Rate Limiting:** Consider implementing rate limiting for production

## Next Steps

Once your local deployment is working:
1. Test all endpoints
2. Set up proper environment variables
3. Consider deploying to Render or other platforms
4. Implement additional security measures 