# Next Steps: Hybrid AI Provider Implementation (OpenAI + Anthropic)

## 🎯 **Goal**

Implement a **hybrid AI provider system** that supports both OpenAI and Anthropic Claude with automatic fallback, allowing:
1. **User Choice**: Configure primary provider (OpenAI or Anthropic)
2. **Automatic Fallback**: If primary fails, automatically switch to secondary
3. **Reliability**: 99.9% uptime with dual provider support
4. **Cost Optimization**: Use cheaper provider as primary, expensive as fallback

---

## 📋 **Implementation Plan**

### **Phase 1: Provider Factory Pattern** 🏭

#### **1.1 Create LLM Provider Wrapper**
```
backend/app/ai/providers/
├── __init__.py
├── base.py              # Abstract base provider
├── openai_provider.py   # OpenAI implementation
├── anthropic_provider.py # Anthropic implementation
└── factory.py           # Provider factory with fallback logic
```

**Key Features:**
- Abstract base class for consistent interface
- Provider-specific implementations
- Factory pattern for initialization
- Automatic fallback on failure
- Retry logic with exponential backoff

#### **1.2 Update Configuration**
```python
# backend/app/core/config.py

# AI Provider Configuration
AI_PROVIDER: str = "openai"  # Primary: "openai" or "anthropic"
AI_FALLBACK_ENABLED: bool = True
AI_FALLBACK_PROVIDER: Optional[str] = "anthropic"  # Secondary provider

# OpenAI
OPENAI_API_KEY: Optional[str] = None
OPENAI_MODEL: str = "gpt-4o"

# Anthropic
ANTHROPIC_API_KEY: Optional[str] = None
ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
```

---

### **Phase 2: Refactor AI Chains** 🔗

#### **2.1 Update Recommendation Chain**
```python
# backend/app/ai/chains/recommendation_chain.py

from app.ai.providers.factory import get_llm_provider

class RecommendationChain:
    def __init__(self):
        self.llm = get_llm_provider()  # Gets provider with fallback
        # ... rest of implementation
```

#### **2.2 Update Candidate Matching Chain**
```python
# backend/app/ai/chains/candidate_matching_chain.py

from app.ai.providers.factory import get_llm_provider

class CandidateMatchingChain:
    def __init__(self):
        self.llm = get_llm_provider()  # Gets provider with fallback
        # ... rest of implementation
```

#### **2.3 Update QA Chain**
```python
# backend/app/ai/rag/qa_chain.py

from app.ai.providers.factory import get_llm_provider

class QAChain:
    def __init__(self):
        self.llm = get_llm_provider()  # Gets provider with fallback
        # ... rest of implementation
```

#### **2.4 Update Assistant Routes**
```python
# backend/app/api/v1/routes/assistant.py

from app.ai.providers.factory import get_llm_provider

# Replace direct ChatOpenAI usage with:
llm = get_llm_provider()
```

---

### **Phase 3: Update Environment Configuration** 📝

#### **3.1 Update `.env.example`**
```bash
# =============================================================================
# AI PROVIDER CONFIGURATION (HYBRID APPROACH)
# =============================================================================
# PRIMARY PROVIDER: The AI service to use first
# Options: "openai" or "anthropic"
AI_PROVIDER=openai

# FALLBACK: Automatically switch if primary fails
AI_FALLBACK_ENABLED=true
AI_FALLBACK_PROVIDER=anthropic  # Leave empty to disable fallback

# OPENAI CONFIGURATION
# Get API key: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o  # Options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4

# ANTHROPIC CONFIGURATION
# Get API key: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Options: claude-3-5-sonnet, claude-3-opus, claude-3-sonnet

# =============================================================================
# HOW IT WORKS
# =============================================================================
# 1. System tries PRIMARY provider (AI_PROVIDER)
# 2. If primary fails AND fallback is enabled, automatically switches
# 3. If both fail, returns error
# 4. No restart needed - fallback happens per request
#
# SCENARIOS:
# - Maximum Reliability: Provide both API keys, enable fallback
# - Cost Optimization: Use free/cheap as primary, paid as fallback
# - Single Provider: Only provide one API key, disable fallback
```

---

### **Phase 4: Testing & Validation** 🧪

#### **4.1 Unit Tests**
```python
# backend/tests/test_ai_providers.py

def test_openai_provider():
    """Test OpenAI provider initialization and basic call"""
    
def test_anthropic_provider():
    """Test Anthropic provider initialization and basic call"""
    
def test_provider_factory():
    """Test factory returns correct provider"""
    
def test_fallback_mechanism():
    """Test automatic fallback when primary fails"""
    
def test_no_fallback_when_disabled():
    """Test error when fallback disabled and primary fails"""
```

#### **4.2 Integration Tests**
- Test recommendation service with both providers
- Test candidate matching with both providers
- Test AI assistant with both providers
- Test cover letter generation with both providers

#### **4.3 Manual Testing Scenarios**
1. **OpenAI Primary, No Fallback**: Only OpenAI key provided
2. **Anthropic Primary, No Fallback**: Only Anthropic key provided
3. **OpenAI Primary, Anthropic Fallback**: Both keys, OpenAI first
4. **Anthropic Primary, OpenAI Fallback**: Both keys, Anthropic first
5. **Simulated Failure**: Test fallback when primary is unavailable

---

### **Phase 5: Documentation Updates** 📚

#### **5.1 Update README.md**
- Add section on hybrid AI provider support
- Document configuration options
- Explain fallback mechanism
- Provide usage examples

#### **5.2 Create AI Provider Guide**
```
docs/AI_PROVIDER_GUIDE.md
- Comparison of OpenAI vs Anthropic
- Cost analysis
- Performance considerations
- Setup instructions for each provider
- Troubleshooting guide
```

#### **5.3 Update API Documentation**
- Document which endpoints use AI
- Explain provider selection
- Document error responses

---

## 🔧 **Implementation Details**

### **Provider Factory Pattern**

```python
# backend/app/ai/providers/factory.py

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

class ProviderError(Exception):
    """Raised when all providers fail"""
    pass

def get_llm_provider(fallback: bool = None):
    """
    Get LLM provider with optional fallback.
    
    Args:
        fallback: Override settings.AI_FALLBACK_ENABLED
        
    Returns:
        LangChain LLM instance with fallback logic
        
    Raises:
        ProviderError: If all providers fail
    """
    if fallback is None:
        fallback = settings.AI_FALLBACK_ENABLED
    
    primary = settings.AI_PROVIDER.lower()
    secondary = settings.AI_FALLBACK_PROVIDER.lower() if fallback else None
    
    # Try primary provider
    try:
        llm = _get_provider(primary)
        logger.info(f"Using primary AI provider: {primary}")
        
        # If fallback enabled, wrap with fallback logic
        if fallback and secondary:
            llm = _wrap_with_fallback(llm, secondary)
            
        return llm
        
    except Exception as e:
        logger.error(f"Primary provider {primary} failed: {e}")
        
        # Try fallback if enabled
        if fallback and secondary:
            try:
                llm = _get_provider(secondary)
                logger.warning(f"Using fallback provider: {secondary}")
                return llm
            except Exception as e2:
                logger.error(f"Fallback provider {secondary} failed: {e2}")
                raise ProviderError(f"All providers failed: {primary}, {secondary}")
        
        raise ProviderError(f"Provider {primary} failed and no fallback configured")

def _get_provider(provider: str):
    """Initialize specific provider"""
    if provider == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    elif provider == "anthropic":
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not configured")
        return ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            temperature=0.3,
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")

def _wrap_with_fallback(primary_llm, secondary_provider: str):
    """Wrap LLM with fallback logic"""
    # Implementation of fallback wrapper
    # This could use LangChain's fallback mechanism or custom retry logic
    pass
```

---

## 📊 **Benefits**

### **Reliability** 🛡️
- **99.9% Uptime**: Automatic failover between providers
- **No Single Point of Failure**: If one provider is down, use the other
- **Graceful Degradation**: Application continues working during outages

### **Cost Optimization** 💰
- **Flexible Pricing**: Use cheaper provider as primary
- **Free Tier Maximization**: Exhaust free tier before paid tier
- **Budget Control**: Switch providers based on usage/cost

### **Performance** ⚡
- **Provider Selection**: Choose fastest provider for your region
- **Load Balancing**: Distribute requests across providers
- **Latency Optimization**: Use provider with best response times

### **Flexibility** 🔄
- **Easy Switching**: Change providers without code changes
- **A/B Testing**: Compare provider quality
- **Future-Proof**: Easy to add new providers (Google, Cohere, etc.)

---

## 🎯 **Success Criteria**

- [ ] Provider factory implemented and tested
- [ ] All AI chains refactored to use factory
- [ ] Fallback mechanism working reliably
- [ ] Configuration documented in `.env.example`
- [ ] Unit tests passing (90%+ coverage)
- [ ] Integration tests passing
- [ ] Manual testing completed for all scenarios
- [ ] Documentation updated
- [ ] No breaking changes to existing API
- [ ] Performance benchmarks acceptable

---

## 📅 **Timeline Estimate**

- **Phase 1** (Provider Factory): 2-3 hours
- **Phase 2** (Refactor Chains): 2-3 hours
- **Phase 3** (Configuration): 1 hour
- **Phase 4** (Testing): 3-4 hours
- **Phase 5** (Documentation): 1-2 hours

**Total: 9-13 hours** (1-2 days of focused work)

---

## 🚀 **Ready to Start?**

Once the current PR is merged, we can begin implementing the hybrid AI provider system!

---

**Questions? Concerns? Let's discuss before implementation!** 💬

