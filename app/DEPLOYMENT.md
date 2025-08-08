# Free Deployment Guide for HackRx API

## Option 1: Railway (Recommended - Easiest)

### Steps:
1. **Sign up for Railway**: Go to [railway.app](https://railway.app) and sign up with GitHub
2. **Connect your repository**: 
   - Push your code to GitHub
   - In Railway dashboard, click "New Project" → "Deploy from GitHub repo"
   - Select your repository
3. **Configure environment variables**:
   - In Railway dashboard, go to your project → Variables tab
   - Add your environment variables (API keys, etc.)
4. **Deploy**: Railway will automatically deploy your app
5. **Get your domain**: Railway provides a free domain like `your-app-name.railway.app`

### Your endpoint will be available at:
```
https://your-app-name.railway.app/api/v1/hackrx/run
```

## Option 2: Render (Alternative)

### Steps:
1. **Sign up for Render**: Go to [render.com](https://render.com) and sign up
2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Choose "Python" as runtime
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Configure environment variables** in the dashboard
4. **Deploy**: Render will build and deploy your app

### Your endpoint will be available at:
```
https://your-app-name.onrender.com/api/v1/hackrx/run
```

## Option 3: Fly.io (Most Generous Free Tier)

### Steps:
1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`
2. **Sign up**: `fly auth signup`
3. **Deploy**: `fly launch` (follow the prompts)
4. **Set secrets**: `fly secrets set YOUR_ENV_VAR=value`

### Your endpoint will be available at:
```
https://your-app-name.fly.dev/api/v1/hackrx/run
```

## Environment Variables Needed

Make sure to set these environment variables in your deployment platform:

```bash
# OpenAI API Key (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key

# Qdrant Configuration
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/app.log

# Authentication (if using)
JWT_SECRET=your_jwt_secret
```

## Testing Your Deployment

Once deployed, test your endpoint with:

```bash
curl -X POST "https://your-domain.com/api/v1/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": ["What is the main topic?", "What are the key points?"]
  }'
```

## Free Tier Limits

- **Railway**: $5 credit monthly (usually enough for small apps)
- **Render**: 750 hours/month free tier
- **Fly.io**: 3 shared-cpu-1x 256mb VMs, 3GB persistent volume storage

## Troubleshooting

1. **Check logs**: Use the deployment platform's log viewer
2. **Environment variables**: Ensure all required env vars are set
3. **Dependencies**: Make sure all packages in requirements.txt are correct
4. **Port configuration**: The app uses `$PORT` environment variable for deployment
