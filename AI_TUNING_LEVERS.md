# NVIDIA NeMo Tron AI Tuning Levers

## Overview
This document outlines all the available tuning parameters and levers to optimize the NVIDIA NeMo Tron model for injury-based BJJ coaching recommendations.

## Current Configuration
- **Model**: `nvidia/nemotron-nano-9b-v2`
- **API Endpoint**: `https://integrate.api.nvidia.com/v1/chat/completions`
- **Max Reasoning Tokens**: 2000 tokens
- **Response Format**: Structured exercise plans with bullet points

## Primary Tuning Levers

### 1. Temperature (0.0 - 1.0)
**Current Setting**: 0.1
- **Lower (0.0-0.3)**: More deterministic, consistent responses
- **Higher (0.7-1.0)**: More creative, varied responses
- **Recommendation**: Keep at 0.1 for clinical, consistent advice

### 2. Top-p (0.0 - 1.0)
**Current Setting**: 0.8
- **Lower (0.1-0.5)**: More focused, conservative responses
- **Higher (0.8-1.0)**: More diverse vocabulary and approaches
- **Recommendation**: Adjust between 0.7-0.9 based on response variety needs

### 3. Frequency Penalty (-2.0 to 2.0)
**Current Setting**: 0.2
- **Positive (0.1-0.5)**: Reduces repetition, encourages variety
- **Negative (-0.1 to -0.5)**: Allows more repetition for emphasis
- **Recommendation**: Increase to 0.3-0.4 if responses become repetitive

### 4. Presence Penalty (-2.0 to 2.0)
**Current Setting**: 0.2
- **Positive (0.1-0.5)**: Encourages new topics and concepts
- **Negative (-0.1 to -0.5)**: Maintains focus on existing topics
- **Recommendation**: Keep at 0.2 for balanced topic coverage

### 5. Max Tokens (50 - 4000)
**Current Settings**:
- Chat: 200 tokens
- API calls: 400 tokens
- **Recommendation**: Increase to 300-500 for more detailed exercise plans

### 6. Thinking Tokens (0 - 2000)
**Current Setting**: 0-2000
- **Min Thinking**: 0 (no internal reasoning)
- **Max Thinking**: 2000 (extensive internal analysis)
- **Recommendation**: Keep at 0-2000 for optimal reasoning capacity

## Secondary Tuning Levers

### 7. System Prompt Engineering
**Current Approach**: Strict format requirements with bullet points
- **Modify**: Add more specific injury context
- **Enhance**: Include severity levels and recovery stages
- **Customize**: Add sport-specific terminology

### 8. Response Cleaning
**Current Filters**: Remove internal reasoning patterns
- **Expand**: Add more verbose phrase patterns
- **Refine**: Target specific medical terminology
- **Optimize**: Improve bullet point formatting

### 9. Cache Strategy
**Current**: Simple hash-based caching
- **Enhance**: Add TTL and invalidation
- **Optimize**: Cache by injury combinations
- **Scale**: Implement distributed caching

### 10. Model Selection
**Current**: `nemotron-nano-9b-v2`
- **Alternatives**: 
  - `nemotron-7b-v2` (larger, more capable)
  - `nemotron-3b-v2` (smaller, faster)
- **Consider**: Model performance vs. cost trade-offs

## Injury-Specific Optimizations

### 11. Injury Severity Levels
- **Mild**: Focus on prevention and modification
- **Moderate**: Emphasize rehabilitation and gradual return
- **Severe**: Prioritize medical consultation and rest

### 12. Recovery Stage Adaptation
- **Acute**: Rest, ice, compression, elevation
- **Subacute**: Gentle mobility and activation
- **Chronic**: Strength training and sport-specific drills

### 13. Sport-Specific Context
- **BJJ Focus**: Ground-based movements, joint locks, submissions
- **Combat Sports**: Impact, contact, and intensity considerations
- **Grappling**: Grip strength, core stability, flexibility

## Performance Monitoring

### 14. Response Quality Metrics
- **Completeness**: All required sections present
- **Accuracy**: Medically sound advice
- **Clarity**: Easy to understand and follow
- **Actionability**: Specific, measurable instructions

### 15. User Feedback Integration
- **Rating System**: 1-5 stars for response quality
- **Feedback Loop**: Incorporate user preferences
- **A/B Testing**: Compare different parameter sets

## Recommended Parameter Sets

### Conservative (Clinical Focus)
```
temperature: 0.05
top_p: 0.7
frequency_penalty: 0.3
presence_penalty: 0.3
max_tokens: 300
```

### Balanced (Current)
```
temperature: 0.1
top_p: 0.8
frequency_penalty: 0.2
presence_penalty: 0.2
max_tokens: 400
```

### Creative (Varied Responses)
```
temperature: 0.2
top_p: 0.9
frequency_penalty: 0.1
presence_penalty: 0.1
max_tokens: 500
```

## Implementation Notes

### Code Locations
- **Main Configuration**: `ai_service.py` lines 25-37, 164-176
- **Chat Configuration**: `app.py` line 113
- **Prompt Templates**: `ai_service.py` lines 327-359, 363-395

### Environment Variables
- `NVIDIA_API_KEY`: Required for API access
- `MODEL_TEMPERATURE`: Override default temperature
- `MAX_TOKENS`: Override default token limits

### Monitoring
- Log response lengths and quality
- Track API usage and costs
- Monitor user satisfaction scores

## Troubleshooting

### Common Issues
1. **Too Verbose**: Increase frequency_penalty, decrease temperature
2. **Too Repetitive**: Increase presence_penalty, adjust top_p
3. **Incomplete Responses**: Increase max_tokens, check prompt format
4. **Inconsistent Quality**: Lower temperature, refine system prompts

### Performance Optimization
1. **Response Time**: Reduce max_tokens, optimize prompts
2. **Cost Control**: Monitor API usage, implement caching
3. **Quality Assurance**: Regular prompt testing, user feedback

## Future Enhancements

### Advanced Features
- **Multi-modal Input**: Image analysis for injury assessment
- **Personalization**: User history and preference learning
- **Integration**: Electronic health records and medical databases
- **Real-time**: Live coaching and form correction

### Model Improvements
- **Fine-tuning**: Custom training on BJJ-specific data
- **Ensemble**: Multiple model voting for consensus
- **Specialization**: Injury-specific model variants
- **Optimization**: Quantization and compression for speed

---

*Last Updated: December 2024*
*Version: 1.0*
