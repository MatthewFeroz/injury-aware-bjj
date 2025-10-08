Injury-Aware AI Jiu Jitsu Coach

An intelligent BJJ coaching system that provides injury-aware training recommendations using AI. The system filters Brazilian Jiu Jitsu techniques based on user injuries and provides safe alternatives with AI-powered coaching advice.

## Medical Disclaimer

This tool does not provide medical advice. Always consult a healthcare professional before making training decisions, especially when dealing with injuries.

## Features

### Core Functionality

- Injury-Aware Filtering: JSON knowledge base of 200+ BJJ techniques tagged with injury risks
- AI-Powered Coaching: NVIDIA Nemotron integration for personalized training recommendations
- Interactive Chat: Real-time chat interface with BJJ coach and physical therapist persona
- Smart Recommendations: AI-powered technique filtering and recommendations
- Modern Web Interface: React + TypeScript frontend with Tailwind CSS

### Technical Features

- Flask API: RESTful backend with CORS support
- Real-Time Chat: Session-based chat history with AI responses
- Responsive Design: Mobile-friendly interface
- Vector Search: Semantic similarity search for technique recommendations
- Caching: Intelligent caching for improved performance

## Project Structure

	injury-aware-bjj/
	├── app.py                 # Flask API server
	├── ai_service.py          # NVIDIA AI integration
	├── bjj_moves.json         # BJJ techniques knowledge base
	├── requirements.txt       # Python dependencies
	├── frontend/              # React TypeScript frontend
	│   ├── src/
	│   │   ├── components/
	│   │   │   ├── AppLayout.tsx
	│   │   │   ├── ChatInput.tsx
	│   │   │   ├── ChatMessage.tsx
	│   │   │   ├── InjurySelector.tsx
	│   │   │   └── ui/
	│   │   └── App.tsx
	│   ├── package.json
	│   └── vite.config.ts
	├── templates/
	├── static/
	└── README.md

## Setup & Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- NVIDIA API Key (for AI features)

### Backend Setup

1. Clone the repository:
   
	git clone <repository-url>
	cd injury-aware-bjj

3. Install Python dependencies:
	
   pip install -r requirements.txt

5.  Create a .env file in the root directory:
   
	NVIDIA_API_KEY=your_nvidia_api_key_here
	PORT=5000
	HOST=0.0.0.0

7. Run the Flask server:

	python app.py

### Frontend Setup

1. Navigate to the frontend directory:

	cd frontend

2. Install dependencies:
   
	npm install

4. Start development server:

	npm run dev

6. Build for production:
   
	npm run build

## Configuration

### Environment Variables

| Variable         | Description                           | Required |
| ---------------- | ------------------------------------- | -------- |
| NVIDIA_API_KEY   | NVIDIA Cloud API key for AI features  | Yes      |
| PORT             | Server port (default: 5000)           | No       |
| HOST             | Server host (default: 0.0.0.0)        | No       |

### API Endpoints

- GET / — Main application interface
- POST /api/recommendations — Get injury-aware technique recommendations
- POST /api/chat — Chat with AI coach

## 🚀 Deployment

### Vercel Deployment

This project is configured for Vercel deployment.

1. **Connect to Vercel**
   - Go to [Vercel.com](https://vercel.com)
   - Import your repository

2. **Configure build settings**
   - Vercel will automatically detect the frontend and backend.

3. **Set environment variables**
   - Add `NVIDIA_API_KEY` in the Vercel project settings.

4. **Deploy**
   - Vercel will automatically deploy on every push to main.

## 🔑 API Keys Setup

### NVIDIA API Key
1. Go to [NVIDIA NGC](https://ngc.nvidia.com)
2. Create an account and navigate to API Keys
3. Generate a new API key
4. Add it to your environment variables


## Testing

### Backend Testing

	curl -X POST http://localhost:5000/api/recommendations \
	  -H "Content-Type: application/json" \
	  -d '{"injuries": ["knee_injury"]}'

### Frontend Testing

	cd frontend
	npm run dev
	# Open http://localhost:5173

## Performance Considerations

- Caching: AI responses are cached to reduce API calls
- Rate Limiting: Built-in retry logic for API failures
- Smart Filtering: Intelligent technique filtering based on injury data
- Frontend Optimization: Vite build system for optimized bundles

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the LICENSE file for details.

## Support

If you encounter any issues:

1. Check the Issues page
2. Create a new issue with detailed information
3. Include error logs and environment details

---

**Remember**: This is a prototype for educational purposes. Always consult healthcare professionals for medical advice.