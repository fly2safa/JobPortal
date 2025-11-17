"""
Company routes for company management.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from beanie import PydanticObjectId
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.models.company import Company
from app.models.user import User, UserRole
from app.api.dependencies import get_current_user, get_current_employer
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/my-company", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
async def create_my_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_employer)
):
    """
    Create a company for the current employer (if they don't have one).
    
    Args:
        company_data: Company creation data
        current_user: Current authenticated employer
        
    Returns:
        Created company object
        
    Raises:
        HTTPException: If user already has a company
    """
    logger.info(f"Company creation attempt by employer: {current_user.email}")
    
    # Check if user already has a company
    if current_user.company_id:
        logger.warning(f"Company creation failed: User already has a company - {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a company associated with your account"
        )
    
    # Create company
    company = Company(
        name=company_data.name,
        description=company_data.description,
        industry=company_data.industry,
        size=company_data.size,
        website=company_data.website,
        email=company_data.email or current_user.email,
        phone=company_data.phone,
        headquarters=company_data.headquarters,
    )
    
    await company.insert()
    logger.info(f"Company created successfully: {company.name} (ID: {company.id})")
    
    # Update user with company_id
    current_user.company_id = str(company.id)
    await current_user.save()
    logger.info(f"User updated with company_id: {current_user.email}")
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        description=company.description,
        industry=company.industry,
        size=company.size,
        website=company.website,
        email=company.email,
        phone=company.phone,
        headquarters=company.headquarters,
        locations=company.locations,
        linkedin_url=company.linkedin_url,
        twitter_url=company.twitter_url,
        logo_url=company.logo_url,
        is_verified=company.is_verified,
        created_at=company.created_at,
        updated_at=company.updated_at,
    )


@router.get("/my-company", response_model=CompanyResponse)
async def get_my_company(current_user: User = Depends(get_current_employer)):
    """
    Get the company associated with the current employer.
    
    Args:
        current_user: Current authenticated employer
        
    Returns:
        Company object
        
    Raises:
        HTTPException: If user doesn't have a company
    """
    if not current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No company associated with your account. Please create one."
        )
    
    try:
        company_oid = PydanticObjectId(current_user.company_id) if isinstance(current_user.company_id, str) else current_user.company_id
        company = await Company.get(company_oid)
    except Exception as e:
        logger.error(f"Error fetching company: {e}")
        company = None
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        description=company.description,
        industry=company.industry,
        size=company.size,
        website=company.website,
        email=company.email,
        phone=company.phone,
        headquarters=company.headquarters,
        locations=company.locations,
        linkedin_url=company.linkedin_url,
        twitter_url=company.twitter_url,
        logo_url=company.logo_url,
        is_verified=company.is_verified,
        created_at=company.created_at,
        updated_at=company.updated_at,
    )


@router.put("/my-company", response_model=CompanyResponse)
async def update_my_company(
    company_data: CompanyUpdate,
    current_user: User = Depends(get_current_employer)
):
    """
    Update the company associated with the current employer.
    
    Args:
        company_data: Company update data
        current_user: Current authenticated employer
        
    Returns:
        Updated company object
        
    Raises:
        HTTPException: If user doesn't have a company
    """
    if not current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No company associated with your account. Please create one."
        )
    
    try:
        company_oid = PydanticObjectId(current_user.company_id) if isinstance(current_user.company_id, str) else current_user.company_id
        company = await Company.get(company_oid)
    except Exception as e:
        logger.error(f"Error fetching company: {e}")
        company = None
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Update fields (only non-None values)
    update_data = company_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    # Update timestamp
    company.updated_at = datetime.utcnow()
    
    await company.save()
    logger.info(f"Company updated successfully: {company.name} (ID: {company.id})")
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        description=company.description,
        industry=company.industry,
        size=company.size,
        website=company.website,
        email=company.email,
        phone=company.phone,
        headquarters=company.headquarters,
        locations=company.locations,
        linkedin_url=company.linkedin_url,
        twitter_url=company.twitter_url,
        logo_url=company.logo_url,
        is_verified=company.is_verified,
        created_at=company.created_at,
        updated_at=company.updated_at,
    )


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: str):
    """
    Get company details by ID (public endpoint).
    
    Args:
        company_id: Company ID
        
    Returns:
        Company object
        
    Raises:
        HTTPException: If company not found
    """
    try:
        company_oid = PydanticObjectId(company_id) if isinstance(company_id, str) else company_id
        company = await Company.get(company_oid)
    except Exception as e:
        logger.error(f"Error fetching company: {e}")
        company = None
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        description=company.description,
        industry=company.industry,
        size=company.size,
        website=company.website,
        email=company.email,
        phone=company.phone,
        headquarters=company.headquarters,
        locations=company.locations,
        linkedin_url=company.linkedin_url,
        twitter_url=company.twitter_url,
        logo_url=company.logo_url,
        is_verified=company.is_verified,
        created_at=company.created_at,
        updated_at=company.updated_at,
    )

