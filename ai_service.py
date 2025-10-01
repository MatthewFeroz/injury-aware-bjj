import os
import requests
import time
from typing import List, Dict, Any

class BJJAIAdvisor:
    def __init__(self):
        """Initialize the AI advisor with NVIDIA Cloud API and vector database"""
        self.api_key = os.getenv('NVIDIA_API_KEY')
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model_name = "nvidia/nvidia-nemotron-nano-9b-v2"
        self.cache = {}  # Simple cache for responses
        
        # Vector database not used in prompt to minimize payload size
    
    def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 600, temperature: float = 0.1) -> str:
        """Run a chat completion with a list of messages [{role, content}]."""
        if not self.api_key:
            return "AI service not configured. Please set NVIDIA_API_KEY environment variable."

        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.8,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.2,
            "extra_body": {
                "min_thinking_tokens": 0,
                "max_thinking_tokens": 2000
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = self._post_with_retry(self.api_url, payload, headers, max_retries=5, backoff=1.5, timeout=25)

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

            print("[NVIDIA API] Unrecognized content structure keys:", {
                "message_keys": list(message.keys()) if isinstance(message, dict) else type(message),
                "first_keys": list(first.keys()) if isinstance(first, dict) else type(first),
            })
            return "AI response received but content was empty."
        except Exception as e:
            print("[NVIDIA API] Parse error:", e)
            return "AI response received but could not be parsed."

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
            "max_tokens": 1200,
            "temperature": 0.1,
            "top_p": 0.8,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.2,
            "extra_body": {
                "min_thinking_tokens": 0,
                "max_thinking_tokens": 2000
            }
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
                line.startswith("Let me") and ("think" in line.lower() or "analyze" in line.lower()) or
                line.startswith("I need to") and ("recall" in line.lower() or "consider" in line.lower()) or
                line.startswith("First,") and "need to" in line.lower() or
                line.startswith("Okay,") and "tackle" in line.lower() or
                line.startswith("Let's") and "produce" in line.lower() or
                line.startswith("I'll") and ("think" in line.lower() or "analyze" in line.lower()) or
                line.startswith("Now,") and ("let me" in line.lower() or "I'll" in line.lower()) or
                "internal" in line.lower() and "reasoning" in line.lower() or
                line.startswith("Based on") and "I can" in line.lower() or
                line.startswith("To answer") and "I'll" in line.lower() or
                line.startswith("I should") and ("think" in line.lower() or "consider" in line.lower()) or
                "let me think" in line.lower() or
                "I need to think" in line.lower() or
                "let me analyze" in line.lower()):
                continue
            
            # Skip lines that are clearly internal planning
            if (line.startswith("**") and "final answer" in line.lower() or
                line.startswith("**") and "response" in line.lower() and "planning" in line.lower() or
                line.startswith("**") and "thinking" in line.lower() or
                line.startswith("**") and "analysis" in line.lower()):
                continue
                
            cleaned_lines.append(line)
        
        # Join and clean up
        cleaned = '\n'.join(cleaned_lines).strip()
        
        # Remove any remaining internal reasoning markers
        cleaned = cleaned.replace("**Final Answer:**", "").replace("**Response:**", "")
        cleaned = cleaned.replace("**Thinking:**", "").replace("**Analysis:**", "")
        
        # Remove repetitive phrases
        cleaned = cleaned.replace("Let me provide", "Here's").replace("I'll provide", "Here's")
        cleaned = cleaned.replace("Let me give you", "Here's").replace("I'll give you", "Here's")
        
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
        """Create a professional PT-style prompt with proper diagnosis and exercise recommendations"""
        similar_info = ""
        if similar_techniques:
            similar_names = [t['metadata']['technique'] for t in similar_techniques[:3]]
            similar_info = f"\nSIMILAR TECHNIQUES FOUND: {', '.join(similar_names)}"
        
        return f"""
You are a licensed physical therapist with 15+ years of experience treating combat sports athletes. 
A BJJ practitioner presents with: {', '.join(injuries)}.

Training considerations:
SAFE MOVES: {', '.join(safe_moves[:8])}  
UNSAFE MOVES: {', '.join(unsafe_moves[:8])}  
{similar_info}

Provide a comprehensive assessment and treatment plan using this exact markdown format:

## INITIAL ASSESSMENT
**Primary concern:** [Specific injury/pain location and mechanism]
**Pain level:** [Scale 1-10 and aggravating factors]
**Functional limitations:** [2-3 specific movement restrictions]

## TOP 3 RECOMMENDED EXERCISES WITH EXPLANATIONS

### Exercise 1: [Specific name] - [Sets]x[Reps]
**Reasoning:** [Detailed biomechanical reasoning for this specific injury]
**Target:** [Specific muscle/joint/function being addressed]

### Exercise 2: [Specific name] - [Sets]x[Reps]
**Reasoning:** [Detailed biomechanical reasoning for this specific injury]
**Target:** [Specific muscle/joint/function being addressed]

### Exercise 3: [Specific name] - [Sets]x[Reps]
**Reasoning:** [Detailed biomechanical reasoning for this specific injury]
**Target:** [Specific muscle/joint/function being addressed]

## SAFETY ANALYSIS
**Why these moves are SAFE:** [Detailed explanation of biomechanics that protect the injured area]
**Why these moves are UNSAFE:** [Detailed explanation of biomechanical stress on injured tissues]

## TRAINING MODIFICATIONS
**Avoid:** [Specific movements with detailed biomechanical reasoning]
**Warm-up:** [2 targeted activation exercises with reasoning]

## PROGRESSION CRITERIA
**Ready to advance when:** [2 specific functional milestones]
**Stop if:** [3 specific warning signs indicating regression]

**Focus on:** [specific techniques/approaches that promote healing and safe progression]

CRITICAL RULES:
- Maximum 500 words total.
- Use exact markdown format above with clear sections.
- NO internal reasoning, thinking, or analysis.
- NO phrases like "Let me", "I'll", "Based on", "To answer".
- Direct, professional clinical advice only.
- Start immediately with ## INITIAL ASSESSMENT
- MUST end with "Focus on:" statement
"""
    
    def _create_recovery_prompt(self, injuries: List[str]) -> str:
        """Create a professional PT-style recovery assessment and treatment plan"""
        return f"""
You are a licensed physical therapist with specialized training in sports rehabilitation and combat sports medicine. 
A BJJ athlete presents with: {', '.join(injuries)}.

Provide a comprehensive rehabilitation assessment and treatment plan using this exact markdown format:

## CLINICAL ASSESSMENT
**Injury mechanism:** [Specific cause and tissue involvement]
**Current pain pattern:** [Location, intensity, and aggravating movements]
**Functional deficits:** [3 specific movement limitations affecting training]

## REHABILITATION PROTOCOL
**Phase 1 (Weeks 1-2):** [Pain management and tissue protection exercises with detailed reasoning]
**Phase 2 (Weeks 3-4):** [Progressive loading and mobility restoration with biomechanical explanation]
**Phase 3 (Weeks 5-6):** [Sport-specific movement patterns and return to training with progression criteria]

## TREATMENT EXERCISES WITH EXPLANATIONS

### Exercise 1: [Specific name] - [Sets]x[Reps] - [Duration]
**Reasoning:** [Detailed explanation of how this addresses the specific injury]
**Target tissue/function:** [Specific anatomical structures being rehabilitated]

### Exercise 2: [Specific name] - [Sets]x[Reps] - [Duration]
**Reasoning:** [Detailed explanation of how this addresses the specific injury]
**Target tissue/function:** [Specific anatomical structures being rehabilitated]

### Exercise 3: [Specific name] - [Sets]x[Reps] - [Duration]
**Reasoning:** [Detailed explanation of how this addresses the specific injury]
**Target tissue/function:** [Specific anatomical structures being rehabilitated]

## PROGRESSION MONITORING
**Daily assessment:** [2 specific pain/mobility markers with normal ranges]
**Weekly milestones:** [1 functional test to track improvement with success criteria]
**Red flags:** [3 warning signs requiring immediate medical attention with specific symptoms]

**Focus on:** [specific rehabilitation approaches that promote healing and safe return to training]

CRITICAL RULES:
- Maximum 450 words total.
- Use exact markdown format above with clear sections.
- NO internal reasoning, thinking, or analysis.
- NO phrases like "Let me", "I'll", "Based on", "To answer".
- Direct, professional clinical guidance only.
- Start immediately with ## CLINICAL ASSESSMENT
- MUST end with "Focus on:" statement
"""
    def _parse_ai_response(self, response: str) -> Dict[str, str]:
        """Parse the AI response into structured recommendations"""
        # Clean up the response and return as-is since we're not using markdown
        cleaned_response = response.strip()
        
        # Split into recommendations and recovery advice based on content
        lines = cleaned_response.split('\n')
        recommendations = []
        recovery_advice = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Identify sections
            if any(keyword in line.lower() for keyword in ['clinical assessment', 'rehabilitation protocol', 'treatment exercises', 'progression monitoring']):
                current_section = 'recovery'
            elif any(keyword in line.lower() for keyword in ['initial assessment', 'recommended exercises', 'safety analysis', 'training modifications']):
                current_section = 'recommendations'
            
            if current_section == 'recovery':
                recovery_advice.append(line)
            elif current_section == 'recommendations':
                recommendations.append(line)
            else:
                # Default to recommendations if unclear
                recommendations.append(line)
        
        return {
            "recommendations": '\n'.join(recommendations) if recommendations else cleaned_response,
            "recovery_advice": '\n'.join(recovery_advice) if recovery_advice else "Please consult with a healthcare professional for personalized recovery advice."
        }
