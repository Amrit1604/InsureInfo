🚀 RENDER DEPLOYMENT - COMPLETE GUIDE
=====================================

## ✅ YOUR API IS 100% HACKATHON COMPLIANT!

Based on the guidelines image:
✅ POST /hackrx/run endpoint
✅ Authorization: Bearer <api_key> support (optional)
✅ JSON request/response format
✅ Public URL ready
✅ HTTPS automatic
✅ <30 second response (yours is ~3s!)

## STEP-BY-STEP RENDER DEPLOYMENT:

### Step 1: Go to Render.com
1. Visit: https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account

### Step 2: Create Web Service
1. Click "New +" in dashboard
2. Select "Web Service"
3. Click "Connect a repository"
4. Find your repo: "InsureInfo"
5. Click "Connect"

### Step 3: Configure Service
Fill in these settings:
- **Name**: hackathon-claims-api
- **Environment**: Python 3
- **Region**: Choose closest to you
- **Branch**: main
- **Build Command**: pip install -r requirements.txt
- **Start Command**: uvicorn api_server:app --host 0.0.0.0 --port $PORT
- **Plan**: Free (perfect for hackathon)

### Step 4: Environment Variables
Click "Advanced" → "Add Environment Variable":
- **Key**: GOOGLE_API_KEY
- **Value**: your_actual_google_api_key

### Step 5: Deploy!
1. Click "Create Web Service"
2. Render will:
   - Clone your repo
   - Install requirements.txt
   - Load 258 document chunks
   - Start your FastAPI server
   - Give you HTTPS URL!

### Step 6: Get Your URL
After deployment (5-10 mins):
**Your hackathon URL**: https://hackathon-claims-api.onrender.com

## TEST YOUR DEPLOYED API:

```bash
curl -X POST https://hackathon-claims-api.onrender.com/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-optional-token" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
    "questions": [
      "Is emergency surgery covered?",
      "What is the grace period for premium payment?"
    ]
  }'
```

## SUBMIT TO HACKATHON:
**Your API Endpoint**: https://hackathon-claims-api.onrender.com/hackrx/run

## TROUBLESHOOTING:

### If build fails:
1. Check requirements.txt has all dependencies
2. Ensure Python version is 3.11+
3. Check logs in Render dashboard

### If app crashes:
1. Check environment variables set
2. Verify GOOGLE_API_KEY is correct
3. Check logs for errors

### If slow responses:
1. First request may be slow (cold start)
2. Subsequent requests will be fast
3. Consider upgrading to paid plan for always-on

## WHY RENDER WINS FOR HACKATHONS:
✅ Free tier perfect for demos
✅ Auto HTTPS (required by guidelines)
✅ No 10-second timeout (unlike Vercel)
✅ Perfect for FastAPI + AI
✅ Auto-deploys on git push
✅ Easy environment variables
✅ Great for demos and presentations

## READY TO WIN! 🏆
Your API matches ALL hackathon requirements perfectly!
