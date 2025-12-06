from fastapi import APIRouter, HTTPException, Depends
from app.models import Subscription, SubscriptionUpgrade, User
from app.auth import get_current_user
from app.database import get_supabase

router = APIRouter()


@router.get("", response_model=Subscription)
async def get_subscription(current_user: User = Depends(get_current_user)):
    """Get current subscription info"""
    supabase = get_supabase()
    
    # Get projects count
    projects_response = supabase.table("projects")\
        .select("id")\
        .eq("user_id", current_user.id)\
        .execute()
    
    projects_count = len(projects_response.data)
    
    # Determine project limit based on tier
    limits = {
        "free": 1,
        "pro": None,
        "premium": None,
    }
    
    return Subscription(
        tier=current_user.tier,
        credits_remaining=current_user.credits_remaining,
        projects_count=projects_count,
        projects_limit=limits.get(current_user.tier)
    )


@router.post("/upgrade")
async def upgrade_subscription(
    upgrade_data: SubscriptionUpgrade,
    current_user: User = Depends(get_current_user)
):
    """Upgrade subscription tier"""
    # TODO: Implement Polar payment integration
    raise HTTPException(status_code=501, detail="Payment integration not implemented yet")
