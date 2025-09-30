import os
import requests
import time
from typing import List, Dict, Any
from dotenv import load_dotenv
# Vector DB disabled in prompt path during troubleshooting

# Load environment variables
load_dotenv()

class BJJAIAdvisor:
    def __init__(self):
        """Initialize the AI advisor with NVIDIA Cloud API and vector database"""
        self.api_key = os.getenv('NVIDIA_API_KEY')
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        # Use a broadly available model on NVIDIA Integrate API
        self.model_name = "meta/llama-3.1-8b-instruct"
        self.cache = {}  # Simple cache for responses
        
        # Vector database not used in prompt to minimize payload size
    
    def get_ai_recommendations(self, injuries: List[str], safe_moves: List[str], unsafe_moves: List[str]) -> Dict[str, str]:
        """
        Get AI-powered recommendations for BJJ training with injuries
        
        Args:
            injuries: List of user's injuries
            safe_moves: List of safe techniques
            unsafe_moves: List of unsafe techniques
            
        Returns:
            Dictionary with AI recommendations and recovery advice
        """
        if not self.api_key:
            return {
                "recommendations": "AI service not configured. Please set NVIDIA_API_KEY environment variable.",
                "recovery_advice": "Consult with a healthcare professional for personalized recovery advice."
            }
        
        # Check cache first
        cache_key = f"rec_{hash(tuple(sorted(injuries)))}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Build prompt without vector-based context
        prompt = self._create_recommendation_prompt(injuries, safe_moves, unsafe_moves, None)
        
        try:
            # Get AI response from NVIDIA Cloud API
            ai_response = self._call_nvidia_api(prompt)
            
            # Parse the response into structured recommendations
            result = self._parse_ai_response(ai_response)
            
            # Cache the result
            self.cache[cache_key] = result
            return result
            
        except Exception as e:
            print(f"Error calling NVIDIA Cloud API: {e}")
            return {
                "recommendations": "Unable to get AI recommendations at this time. Please check your API key and internet connection.",
                "recovery_advice": "Please consult with a healthcare professional for personalized advice."
            }
    
    def get_recovery_advice(self, injuries: List[str]) -> str:
        """
        Get AI-powered recovery advice for specific injuries
        
        Args:
            injuries: List of user's injuries
            
        Returns:
            Recovery advice string
        """
        if not self.api_key:
            return "AI service not configured. Please consult with a healthcare professional."
        
        # Check cache first
        cache_key = f"recov_{hash(tuple(sorted(injuries)))}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        prompt = self._create_recovery_prompt(injuries)
        
        try:
            result = self._call_nvidia_api(prompt)
            # Cache the result
            self.cache[cache_key] = result
            return result
        except Exception as e:
            print(f"Error getting recovery advice: {e}")
            return "Unable to get recovery advice at this time. Please check your API key and internet connection."
    
    def _call_nvidia_api(self, prompt: str) -> str:
        """Call the NVIDIA Cloud API with a prompt"""
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 128,
            "temperature": 0.3
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = self._post_with_retry(self.api_url, payload, headers, max_retries=5, backoff=1.5, timeout=25)
        except Exception as first_exc:
            # Give up fast if retries already failed
            raise first_exc
        # Log raw response for debugging
        try:
            print("[NVIDIA API] status:", response.status_code)
            preview = response.text[:500]
            print("[NVIDIA API] body preview:", preview)
        except Exception:
            pass

        response.raise_for_status()
        
        try:
            result = response.json()
        except Exception as e:
            print("[NVIDIA API] JSON parse error:", e)
            raise

        try:
            choices = result.get("choices", [])
            first = choices[0] if choices else {}
            message = first.get("message", {}) or {}

            # Candidate fields in order of preference
            candidates = [
                message.get("content"),
                message.get("reasoning_content"),
                first.get("text"),
                (first.get("delta") or {}).get("content"),
                (result.get("output") or {}).get("text"),
            ]

            for c in candidates:
                if isinstance(c, str) and c.strip():
                    return self._clean_response(c.strip())

            # Last-resort: dump minimal info for debugging
            print("[NVIDIA API] Unrecognized content structure keys:", {
                "message_keys": list(message.keys()) if isinstance(message, dict) else type(message),
                "first_keys": list(first.keys()) if isinstance(first, dict) else type(first),
            })
            return "AI response received but content was empty."
        except Exception as e:
            print("[NVIDIA API] Parse error:", e)
            return "AI response received but could not be parsed."
    
    def _clean_response(self, response: str) -> str:
        """Clean up reasoning model responses to remove internal thinking"""
        # Remove common reasoning patterns
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip internal reasoning patterns
            if (line.startswith("The user asks") or 
                line.startswith("We can do:") or 
                line.startswith("Let me") and "think" in line.lower() or
                line.startswith("I need to") and "recall" in line.lower() or
                line.startswith("First,") and "need to" in line.lower() or
                line.startswith("Okay,") and "tackle" in line.lower() or
                line.startswith("Let's") and "produce" in line.lower() or
                "internal" in line.lower() and "reasoning" in line.lower()):
                continue
            
            # Skip lines that are clearly internal planning
            if (line.startswith("**") and "final answer" in line.lower() or
                line.startswith("**") and "response" in line.lower() and "planning" in line.lower()):
                continue
                
            cleaned_lines.append(line)
        
        # Join and clean up
        cleaned = '\n'.join(cleaned_lines).strip()
        
        # Remove any remaining internal reasoning markers
        cleaned = cleaned.replace("**Final Answer:**", "").replace("**Response:**", "")
        
        return cleaned

    def _post_with_retry(
        self,
        url: str,
        json_payload: Dict[str, Any],
        headers: Dict[str, str],
        max_retries: int = 3,
        backoff: float = 1.5,
        timeout: int = 20,
    ) -> requests.Response:
        """POST with retry for transient errors (e.g., 429/5xx) using exponential backoff."""
        last_exc: Exception | None = None
        last_resp: requests.Response | None = None
        for attempt in range(max_retries):
            try:
                resp = requests.post(url, json=json_payload, headers=headers, timeout=timeout)
                # Retry on common transient statuses
                if resp.status_code in (429, 500, 502, 503, 504):
                    # Allow one retry cycle for transient upstream issues
                    wait_seconds = backoff ** attempt
                    time.sleep(wait_seconds)
                    last_resp = resp
                    last_exc = requests.HTTPError(f"HTTP {resp.status_code}")
                    continue
                return resp
            except (requests.ConnectionError, requests.Timeout) as e:
                last_exc = e
                wait_seconds = backoff ** attempt
                time.sleep(wait_seconds)
                continue
        # If all retries exhausted, raise last captured exception or a generic HTTPError
        if last_resp is not None:
            return last_resp
        if last_exc:
            raise last_exc
        raise requests.HTTPError("Request failed after retries")
    
    def _create_recommendation_prompt(
        self, injuries: List[str], safe_moves: List[str], unsafe_moves: List[str], similar_techniques: List[Dict] = None
    ) -> str:
        """Create a concise, clinically structured prompt for move recommendations"""
        similar_info = ""
        if similar_techniques:
            similar_names = [t['metadata']['technique'] for t in similar_techniques[:3]]
            similar_info = f"\nSIMILAR TECHNIQUES FOUND: {', '.join(similar_names)}"
        
        return f"""
You are a licensed physical therapist and BJJ coach. 
A student presents with: {', '.join(injuries)}.

Training considerations:
SAFE MOVES: {', '.join(safe_moves[:8])}  
UNSAFE MOVES: {', '.join(unsafe_moves[:8])}  
{similar_info}

Provide a concise consult note in bullet points only:
1. **Risk Analysis**: 2–3 bullets explaining why the listed moves are safe/unsafe (focus on mechanics, e.g., joint stress).
2. **Training Modifications**: Up to 3 safer move substitutions or strategy adaptations.
3. **Warm‑Up/Preparation**: 2–3 specific drills/activations tailored to the injury.

Rules:
- Keep response under 100 words.
- Use professional, clinical tone.
- No speculative "thinking" or filler text.
- No internal reasoning or planning.
- Direct, actionable advice only.
- Bullet points only.
"""
    
    def _create_recovery_prompt(self, injuries: List[str]) -> str:
        """Create a concise, professional rehab guidance prompt"""
        return f"""
You are a licensed physical therapist specializing in combat sports. 
A BJJ athlete presents with: {', '.join(injuries)}.

Provide a concise consult note, in bullet points only:

1. **Self‑Check**: Up to 2 bullets of safe ways to gauge severity (mobility, swelling, pain levels).
2. **Rehab Exercises**: Exactly 3 evidence‑based exercises (with sets/reps).
3. **Training Timeline**: 3 clear stages (rest → light drill → return to rolling).
4. **Red Flags**: Up to 3 warning signs where training should stop.

Rules:
- Max 100 words total.
- Bullets only, no paragraphs.
- Avoid speculation or inner reasoning — authoritative clinical guidance only.
- No internal reasoning or planning.
- Direct, actionable advice only.
- End with: "Always consult your healthcare provider before returning to full training."
"""
    def _parse_ai_response(self, response: str) -> Dict[str, str]:
        """Parse the AI response into structured recommendations"""
        # Simple parsing - in a production app, you might want more sophisticated parsing
        lines = response.split('\n')
        
        recommendations = []
        recovery_advice = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'recovery' in line.lower() or 'rehabilitation' in line.lower():
                current_section = 'recovery'
            elif 'recommendation' in line.lower() or 'training' in line.lower():
                current_section = 'recommendations'
            
            if current_section == 'recommendations':
                recommendations.append(line)
            elif current_section == 'recovery':
                recovery_advice.append(line)
            else:
                # Default to recommendations if unclear
                recommendations.append(line)
        
        return {
            "recommendations": '\n'.join(recommendations) if recommendations else response,
            "recovery_advice": '\n'.join(recovery_advice) if recovery_advice else "Please consult with a healthcare professional for personalized recovery advice."
        }
