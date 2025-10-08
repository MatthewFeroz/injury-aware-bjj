# Vercel Deployment Guide

This guide explains how to deploy your BJJ Injury-Aware Coach application to Vercel.

## Project Structure

```
├── api/                    # Serverless API functions
│   ├── index.py           # Main Flask app handler
│   ├── ai_service.py      # AI service module
│   ├── bjj_moves.json     # BJJ moves database
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/              # React source code
│   ├── dist/             # Built frontend (generated)
│   └── package.json      # Node.js dependencies
├── vercel.json           # Vercel configuration
└── .env                  # Environment variables (not committed)
```

## Environment Variables

Set these environment variables in your Vercel dashboard:

- `NVIDIA_API_KEY`: Your NVIDIA API key for AI services

## Deployment Steps

1. **Connect to Vercel**:
   - Push your code to GitHub/GitLab
   - Connect your repository to Vercel
   - Vercel will automatically detect the configuration

2. **Set Environment Variables**:
   - Go to your Vercel project settings
   - Add the `NVIDIA_API_KEY` environment variable
   - Redeploy after adding environment variables

3. **Deploy**:
   - Vercel will automatically build and deploy
   - The frontend will be built from `frontend/`
   - The API will be deployed as serverless functions from `api/`

## API Endpoints

- `POST /api/recommendations` - Get BJJ recommendations based on injuries
- `POST /api/chat` - Chat with the AI coach

## Troubleshooting

### 404 Errors
- Ensure your `vercel.json` is correctly configured
- Check that the API routes are properly defined
- Verify the build process completes successfully

### API Errors
- Check that environment variables are set correctly
- Verify the NVIDIA API key is valid
- Check Vercel function logs for detailed error messages

### Build Errors
- Ensure all dependencies are listed in `requirements.txt` and `package.json`
- Check that the frontend builds successfully with `npm run build`
- Verify TypeScript compilation passes

## Local Development

To test locally before deploying:

1. **Backend**:
   ```bash
   cd api
   pip install -r requirements.txt
   python index.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Test API**:
   ```bash
   python test_api.py
   ```

## Configuration Files

### vercel.json
- Defines build configuration for both frontend and backend
- Routes API calls to serverless functions
- Serves static frontend files

### api/requirements.txt
- Python dependencies for the serverless functions
- Must include all required packages

### frontend/package.json
- Node.js dependencies and build scripts
- Includes `vercel-build` script for deployment
