# NVIDIA Nemotron Integration Setup

Your BJJ AI Advisor is now configured to use the NVIDIA Nemotron model (`nvidia/nemotron-nano-9b-v2`).

## API Key Setup

To enable AI recommendations, you need to set up your NVIDIA API key:

1. **Get an NVIDIA API Key:**
   - Visit: https://build.nvidia.com/
   - Sign up or log in to your NVIDIA account
   - Generate an API key

2. **Configure the API Key:**
   Create a `.env` file in the project root with:
   ```
   NVIDIA_API_KEY=your_actual_api_key_here
   ```

3. **Alternative: Set Environment Variable:**
   ```bash
   # Windows PowerShell
   $env:NVIDIA_API_KEY="your_actual_api_key_here"
   
   # Windows Command Prompt
   set NVIDIA_API_KEY=your_actual_api_key_here
   
   # Linux/Mac
   export NVIDIA_API_KEY="your_actual_api_key_here"
   ```

## Testing the Integration

Once you have the API key configured:

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Test the API endpoints:**
   - Visit: http://localhost:5000
   - Or test the API directly:
     ```bash
     curl -X POST http://localhost:5000/api/recommendations \
          -H "Content-Type: application/json" \
          -d '{"injuries": ["knee injury"]}'
     ```

## Features Available

- **AI-Powered Recommendations**: Get personalized BJJ technique recommendations based on injuries
- **Recovery Advice**: Receive rehabilitation guidance from the Nemotron model
- **Chat Interface**: Interactive BJJ coaching via the chat API

The system now uses NVIDIA's Nemotron model for more accurate and contextual AI responses.
