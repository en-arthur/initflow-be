from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.models import MarketplaceComponent, ComponentIntegration, User
from app.auth import get_current_user

router = APIRouter()


@router.get("/search", response_model=List[MarketplaceComponent])
async def search_marketplace(
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None)
):
    """Search marketplace components"""
    # Mock marketplace components
    all_components = [
        {
            "id": "auth-template",
            "name": "Authentication Template",
            "description": "Complete authentication system with login, signup, and password reset",
            "category": "Authentication",
            "tags": ["auth", "login", "security"],
            "preview_url": "https://example.com/preview/auth",
            "spec_template": {},
            "code_template": {},
            "dependencies": ["@react-native-async-storage/async-storage"],
            "downloads": 1250,
            "rating": 4.8,
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "payment-module",
            "name": "Payment Integration",
            "description": "Stripe payment integration with card processing",
            "category": "Payments",
            "tags": ["stripe", "payments", "checkout"],
            "preview_url": "https://example.com/preview/payments",
            "spec_template": {},
            "code_template": {},
            "dependencies": ["@stripe/stripe-react-native"],
            "downloads": 890,
            "rating": 4.6,
            "created_at": "2024-01-15T00:00:00Z"
        },
        {
            "id": "navigation-stack",
            "name": "Navigation Stack",
            "description": "Pre-configured React Navigation with common patterns",
            "category": "Navigation",
            "tags": ["navigation", "routing", "screens"],
            "preview_url": "https://example.com/preview/navigation",
            "spec_template": {},
            "code_template": {},
            "dependencies": ["@react-navigation/native", "@react-navigation/stack"],
            "downloads": 2100,
            "rating": 4.9,
            "created_at": "2024-01-10T00:00:00Z"
        }
    ]
    
    # Filter components based on search criteria
    filtered_components = all_components
    
    if query:
        query_lower = query.lower()
        filtered_components = [
            comp for comp in filtered_components
            if query_lower in comp["name"].lower() or query_lower in comp["description"].lower()
        ]
    
    if category:
        filtered_components = [
            comp for comp in filtered_components
            if comp["category"].lower() == category.lower()
        ]
    
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        filtered_components = [
            comp for comp in filtered_components
            if any(tag in [t.lower() for t in comp["tags"]] for tag in tag_list)
        ]
    
    return [MarketplaceComponent(**comp) for comp in filtered_components]


@router.get("/components/{component_id}", response_model=MarketplaceComponent)
async def get_component(component_id: str):
    """Get a specific marketplace component"""
    # Mock marketplace components
    mock_components = {
        "auth-template": {
            "id": "auth-template",
            "name": "Authentication Template",
            "description": "Complete authentication system with login, signup, and password reset",
            "category": "Authentication",
            "tags": ["auth", "login", "security"],
            "preview_url": "https://example.com/preview/auth",
            "spec_template": {
                "requirements": "User authentication with email/password",
                "design": "Modern login and signup screens",
                "tasks": ["Implement login screen", "Add signup flow", "Create password reset"]
            },
            "code_template": {
                "screens/LoginScreen.js": "// Login screen implementation",
                "services/auth.js": "// Authentication service"
            },
            "dependencies": ["@react-native-async-storage/async-storage", "react-native-keychain"],
            "downloads": 1250,
            "rating": 4.8,
            "created_at": "2024-01-01T00:00:00Z"
        },
        "payment-module": {
            "id": "payment-module",
            "name": "Payment Integration",
            "description": "Stripe payment integration with card processing",
            "category": "Payments",
            "tags": ["stripe", "payments", "checkout"],
            "preview_url": "https://example.com/preview/payments",
            "spec_template": {
                "requirements": "Payment processing with Stripe",
                "design": "Payment forms and checkout flow",
                "tasks": ["Setup Stripe", "Create payment forms", "Handle transactions"]
            },
            "code_template": {
                "services/stripe.js": "// Stripe integration",
                "screens/CheckoutScreen.js": "// Checkout screen"
            },
            "dependencies": ["@stripe/stripe-react-native"],
            "downloads": 890,
            "rating": 4.6,
            "created_at": "2024-01-15T00:00:00Z"
        }
    }
    
    if component_id not in mock_components:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found"
        )
    
    return MarketplaceComponent(**mock_components[component_id])


@router.post("/projects/{project_id}/integrate")
async def integrate_component(
    project_id: str,
    integration: ComponentIntegration,
    current_user: User = Depends(get_current_user)
):
    """Integrate a marketplace component into a project"""
    # This would update the project's spec files and generate code
    # For now, just return success
    return {
        "message": f"Component {integration.component_id} integrated successfully",
        "project_id": project_id
    }
