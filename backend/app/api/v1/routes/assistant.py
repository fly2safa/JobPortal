"""
AI Assistant routes for chat and cover letter generation.
"""
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from app.models.user import User
from app.models.conversation import Conversation, MessageRole
from app.api.dependencies import get_current_user
from app.ai.rag.qa_chain import qa_chain
from app.core.config import settings
from app.core.logging import get_logger
from openai import AsyncOpenAI

logger = get_logger(__name__)
router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


# Schemas
class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    message: str
    conversation_id: str


class CoverLetterRequest(BaseModel):
    """Request schema for cover letter generation."""
    job_id: str
    job_title: str
    job_description: str
    company_name: str
    user_name: str
    user_skills: List[str] = Field(default_factory=list)
    user_experience: Optional[str] = None


class CoverLetterResponse(BaseModel):
    """Response schema for cover letter generation."""
    cover_letter: str


class ConversationListResponse(BaseModel):
    """Response schema for conversation list."""
    conversations: List[dict]
    total: int


# Endpoints
@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Chat with the AI assistant.
    
    Args:
        request: Chat request with message and optional conversation_id
        current_user: Current authenticated user
        
    Returns:
        Assistant's response and conversation_id
    """
    logger.info(f"Chat request from user {current_user.email}: {request.message[:50]}...")
    
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation = await Conversation.get(request.conversation_id)
            if not conversation or conversation.user_id != str(current_user.id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            conversation = Conversation(
                user_id=str(current_user.id),
                context_type="general"
            )
            await conversation.insert()
        
        # Add user message to conversation
        conversation.add_message(MessageRole.USER, request.message)
        
        # Get conversation history for context
        history = conversation.get_messages_for_llm(limit=10)
        
        # Build user context
        user_context = {
            "role": current_user.role,
            "name": f"{current_user.first_name} {current_user.last_name}",
        }
        
        # Get answer from QA chain
        answer = await qa_chain.answer_question(
            question=request.message,
            conversation_history=history[:-1],  # Exclude the current message
            user_context=user_context
        )
        
        # Add assistant response to conversation
        conversation.add_message(MessageRole.ASSISTANT, answer)
        await conversation.save()
        
        logger.info(f"Generated response for user {current_user.email}")
        
        return ChatResponse(
            message=answer,
            conversation_id=str(conversation.id)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request"
        )


@router.get("/conversations", response_model=ConversationListResponse)
async def get_conversations(
    current_user: User = Depends(get_current_user),
    limit: int = 20
):
    """
    Get user's conversation history.
    
    Args:
        current_user: Current authenticated user
        limit: Maximum number of conversations to return
        
    Returns:
        List of conversations
    """
    try:
        conversations = await Conversation.find(
            Conversation.user_id == str(current_user.id)
        ).sort(-Conversation.updated_at).limit(limit).to_list()
        
        conversation_list = []
        for conv in conversations:
            conversation_list.append({
                "id": str(conv.id),
                "title": conv.title or "New Conversation",
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "message_count": len(conv.messages)
            })
        
        return ConversationListResponse(
            conversations=conversation_list,
            total=len(conversation_list)
        )
        
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch conversations"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific conversation with all messages.
    
    Args:
        conversation_id: Conversation ID
        current_user: Current authenticated user
        
    Returns:
        Conversation with messages
    """
    try:
        conversation = await Conversation.get(conversation_id)
        
        if not conversation or conversation.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return {
            "id": str(conversation.id),
            "title": conversation.title,
            "messages": conversation.messages,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch conversation"
        )


@router.post("/generate-cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter(
    request: CoverLetterRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a cover letter for a job application using AI.
    
    Args:
        request: Cover letter generation request
        current_user: Current authenticated user
        
    Returns:
        Generated cover letter
    """
    logger.info(f"Cover letter generation request from {current_user.email} for job {request.job_id}")
    
    try:
        if not settings.OPENAI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service is not configured. Please write your cover letter manually."
            )
        
        # Get current date for the cover letter
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Build prompt for cover letter generation
        prompt = f"""Generate a professional cover letter for the following job application:

Job Title: {request.job_title}
Company: {request.company_name}
Applicant Name: {request.user_name}
Applicant Skills: {', '.join(request.user_skills) if request.user_skills else 'Not specified'}
Applicant Experience: {request.user_experience or 'Not specified'}

Job Description:
{request.job_description}

Instructions:
- Write a professional, compelling cover letter
- Start with the date: {current_date}
- DO NOT include placeholder addresses like [Your Address], [City, State, Zip Code], [Email Address], [Phone Number], [Company Address]
- After the date, skip a line and write "Hiring Manager" followed by the company name "{request.company_name}"
- Then skip a line and start with "Dear Hiring Manager,"
- Highlight relevant skills and experience
- Express genuine interest in the position
- Keep it concise (3-4 paragraphs)
- Use a professional but friendly tone
- Make it personalized to this specific job
- End with "Sincerely," followed by the applicant name: {request.user_name}

Format example:
{current_date}

Hiring Manager
{request.company_name}

Dear Hiring Manager,

[Body paragraphs here...]

Sincerely,
{request.user_name}

Generate the cover letter now:"""

        # Call OpenAI API using new v1.0+ syntax
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert career coach and professional writer specializing in cover letters."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=800
        )
        
        cover_letter = response.choices[0].message.content
        
        logger.info(f"Generated cover letter for user {current_user.email}")
        
        return CoverLetterResponse(cover_letter=cover_letter)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating cover letter: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate cover letter. Please try again or write it manually."
        )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a conversation.
    
    Args:
        conversation_id: Conversation ID
        current_user: Current authenticated user
    """
    try:
        conversation = await Conversation.get(conversation_id)
        
        if not conversation or conversation.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        await conversation.delete()
        logger.info(f"Deleted conversation {conversation_id} for user {current_user.email}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation"
        )

