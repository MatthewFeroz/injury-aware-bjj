# Injury-Aware AI Jiu Jitsu Coach

An intelligent BJJ coaching system that provides injury-aware training recommendations using AI. The system filters Brazilian Jiu Jitsu techniques based on user injuries and provides safe alternatives with AI-powered coaching advice.

## ⚠️ Medical Disclaimer

**This tool does not provide medical advice. Always consult a healthcare professional before making training decisions, especially when dealing with injuries.**

## 🚀 Features

### Core Functionality
- **Injury-Aware Filtering**: JSON knowledge base of 200+ BJJ techniques tagged with injury risks
- **AI-Powered Coaching**: NVIDIA Nemotron integration for personalized training recommendations
- **Interactive Chat**: Real-time chat interface with BJJ coach and physical therapist persona
- **Vector Database**: Pinecone integration for semantic search of techniques
- **Modern Web Interface**: React + TypeScript frontend with Tailwind CSS

### Technical Features
- **Flask API**: RESTful backend with CORS support
- **Real-time Chat**: Session-based chat history with AI responses
- **Responsive Design**: Mobile-friendly interface
- **Vector Search**: Semantic similarity search for technique recommendations
- **Caching**: Intelligent caching for improved performance

## 🏗️ Project Structure

```
injury-aware-bjj/
├── app.py                 # Flask API server
├── ai_service.py          # NVIDIA AI integration
├── vector_db.py           # Pinecone vector database
├── bjj_moves.json         # BJJ techniques knowledge base
├── requirements.txt       # Python dependencies
├── frontend/              # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── AppLayout.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── InjurySelector.tsx
│   │   │   └── ui/        # UI components
│   │   └── App.tsx
│   ├── package.json       # Node.js dependencies
│   └── vite.config.ts     # Vite configuration
├── templates/             # Flask templates
├── static/                # Static assets
└── README.md
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- NVIDIA API Key (for AI features)
- Pinecone API Key (for vector search)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd injury-aware-bjj
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   NVIDIA_API_KEY=your_nvidia_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PORT=5000
   HOST=0.0.0.0
   ```

4. **Initialize vector database** (optional)
   ```bash
   python init_vector_db.py
   ```

5. **Run the Flask server**
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NVIDIA_API_KEY` | NVIDIA Cloud API key for AI features | Yes |
| `PINECONE_API_KEY` | Pinecone API key for vector search | No |
| `PORT` | Server port (default: 5000) | No |
| `HOST` | Server host (default: 0.0.0.0) | No |

### API Endpoints

- `GET /` - Main application interface
- `POST /api/recommendations` - Get injury-aware technique recommendations
- `POST /api/chat` - Chat with AI coach

## 🚀 Deployment Options

### Option 1: Railway (Recommended)

Railway provides seamless deployment for full-stack applications.

1. **Connect your repository**
   - Go to [Railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway will auto-detect your project structure

2. **Configure environment variables**
   - Add `NVIDIA_API_KEY` and `PINECONE_API_KEY` in Railway dashboard
   - Set `PORT=5000` (Railway will handle this automatically)

3. **Deploy**
   - Railway will automatically build and deploy your application
   - Your app will be available at `https://your-app-name.railway.app`

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set NVIDIA_API_KEY=your_api_key
   heroku config:set PINECONE_API_KEY=your_pinecone_key
   ```

4. **Create Procfile**
   ```bash
   echo "web: python app.py" > Procfile
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 3: Vercel (Frontend) + Railway (Backend)

For optimal performance, deploy frontend and backend separately.

#### Backend (Railway)
Follow Option 1 steps for backend deployment.

#### Frontend (Vercel)
1. **Connect to Vercel**
   - Go to [Vercel.com](https://vercel.com)
   - Import your repository
   - Set root directory to `frontend`

2. **Configure build settings**
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Set environment variables**
   - Add `VITE_API_URL` pointing to your Railway backend URL

4. **Deploy**
   - Vercel will automatically deploy on every push to main

### Option 4: DigitalOcean App Platform

1. **Create App Spec**
   Create `app.yaml`:
   ```yaml
   name: injury-aware-bjj
   services:
   - name: backend
     source_dir: /
     github:
       repo: your-username/your-repo
       branch: main
     run_command: python app.py
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: NVIDIA_API_KEY
       value: your_api_key
     - key: PINECONE_API_KEY
       value: your_pinecone_key
   - name: frontend
     source_dir: /frontend
     github:
       repo: your-username/your-repo
       branch: main
     build_command: npm run build
     run_command: npm run preview
     environment_slug: node-js
     instance_count: 1
     instance_size_slug: basic-xxs
   ```

2. **Deploy**
   - Upload the spec to DigitalOcean App Platform
   - Connect your GitHub repository
   - Deploy automatically

### Option 5: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Expose port
   EXPOSE 5000

   # Run the application
   CMD ["python", "app.py"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     app:
       build: .
       ports:
         - "5000:5000"
       environment:
         - NVIDIA_API_KEY=${NVIDIA_API_KEY}
         - PINECONE_API_KEY=${PINECONE_API_KEY}
       volumes:
         - .:/app
   ```

3. **Deploy**
   ```bash
   docker-compose up -d
   ```

## 🔑 API Keys Setup

### NVIDIA API Key
1. Go to [NVIDIA NGC](https://ngc.nvidia.com)
2. Create an account and navigate to API Keys
3. Generate a new API key
4. Add to your environment variables

### Pinecone API Key (Optional)
1. Go to [Pinecone.io](https://pinecone.io)
2. Create a free account
3. Create a new project and index
4. Copy your API key
5. Add to your environment variables

## 🧪 Testing

### Backend Testing
```bash
# Test the API endpoints
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"injuries": ["knee_injury"]}'
```

### Frontend Testing
```bash
cd frontend
npm run dev
# Open http://localhost:5173
```

## 📊 Performance Considerations

- **Caching**: AI responses are cached to reduce API calls
- **Rate Limiting**: Built-in retry logic for API failures
- **Vector Search**: Optional Pinecone integration for semantic search
- **Frontend Optimization**: Vite build system for optimized bundles

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include error logs and environment details

## 🔮 Future Enhancements

- [ ] Integration with wearable devices
- [ ] Video analysis for technique correction
- [ ] Mobile app development
- [ ] Advanced injury tracking
- [ ] Integration with training logs
- [ ] Multi-language support

---

**Remember**: This is a prototype for educational purposes. Always consult healthcare professionals for medical advice.
