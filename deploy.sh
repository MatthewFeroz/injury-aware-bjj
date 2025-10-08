#!/bin/bash

# BJJ Injury-Aware Coach - Vercel Deployment Script

echo "🚀 Starting Vercel deployment process..."

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Please run this script from the project root."
    exit 1
fi

# Check if API directory exists
if [ ! -d "api" ]; then
    echo "❌ Error: api directory not found."
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found."
    exit 1
fi

echo "✅ Project structure looks good"

# Build frontend
echo "📦 Building frontend..."
cd frontend
if ! npm run build; then
    echo "❌ Frontend build failed"
    exit 1
fi
cd ..

echo "✅ Frontend built successfully"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI not found. Please install it with: npm i -g vercel"
    echo "📝 You can also deploy manually by pushing to your connected Git repository"
    exit 0
fi

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
if vercel --prod; then
    echo "✅ Deployment successful!"
    echo "🌐 Your app should be live at the URL provided above"
else
    echo "❌ Deployment failed"
    exit 1
fi

echo "🎉 Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set your NVIDIA_API_KEY environment variable in Vercel dashboard"
echo "2. Redeploy after setting environment variables"
echo "3. Test your API endpoints"
