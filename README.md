# JobPortal

Content Generation for the MongoDB database. Using a script(s) to create Candidates, Employer, Jobs, Applications, etc. 


The JobPortal project aims to develop a secure, scalable, and user-friendly platform connecting job seekers and employers. 
The core functionalities for job seekers include creating profiles, uploading resumes, searching and applying for jobs, and receiving notifications.
Employers can post jobs, review applications, schedule interviews, and communicate with candidates.

The system will also leverage AI for personalized job recommendations, resume parsing, and candidate matching.

---

## ðŸ¤– AI Provider Configuration (NEW!)

### Automatic Fallback System

TalentNest now supports **dual AI provider configuration** with **automatic fallback** for maximum reliability and uptime.

#### Supported Providers

- **OpenAI** (GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-4)
- **Anthropic** (Claude 3.5 Sonnet, Claude 3 Opus)

#### How It Works

1. **Primary Provider**: System uses your configured primary AI provider (default: OpenAI)
2. **Automatic Fallback**: If primary fails (outage, rate limit, error), automatically switches to fallback provider
3. **Per-Request**: Fallback happens per request, no restart needed
4. **Transparent**: Users don't notice the switch

#### Benefits

- âœ… **99.9% Uptime** - Dual provider redundancy
- âœ… **No Manual Intervention** - Automatic failover during outages
- âœ… **Cost Optimization** - Use cheaper provider as primary, expensive as fallback
- âœ… **Seamless UX** - Transparent to end users

#### Configuration

In your \ackend/.env\ file:

\\\ash
# Primary Provider
AI_PROVIDER=openai  # or "anthropic"

# Enable Automatic Fallback (Recommended)
AI_FALLBACK_ENABLED=true

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o

# Anthropic Configuration (Optional - for fallback)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
\\\

#### Production Recommendation

For maximum reliability in production:

1. Configure **both** OpenAI and Anthropic API keys
2. Set \AI_FALLBACK_ENABLED=true\
3. Choose the **cheaper** provider as primary
4. More expensive provider becomes automatic fallback
5. Only pay for fallback when primary fails

#### Cost Strategy Examples

**Option A: OpenAI Primary**
\\\ash
AI_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini  # Cheaper
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Fallback
\\\

**Option B: Anthropic Primary**
\\\ash
AI_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Primary
OPENAI_MODEL=gpt-4o  # Fallback
\\\

#### Logging

The system logs all provider switches:

- âœ… \Using primary AI provider: openai (model: gpt-4o)\
- ðŸ”„ \Fallback available: anthropic\
- âš ï¸ \Primary provider 'openai' failed: [error]\
- ðŸ”„ \Switched to fallback provider: anthropic (model: claude-3-5-sonnet)\
- âŒ \All AI providers failed. Primary (openai): [error]. Fallback (anthropic): [error]\

#### Technical Details

- **Architecture**: Provider Factory pattern with automatic fallback
- **Location**: \ackend/app/ai/providers/\
- **Entry Point**: \get_llm()\ function
- **Error Handling**: Graceful degradation with \ProviderError\
- **Refactored Services**: All AI services (QA chain, assistant, resume parser) now use the factory

---

For more details, see \ackend/.env.example\ and \ackend/app/ai/providers/README.md\ (if available).
