"""
AI-powered specification generator service
"""
from typing import Dict, Optional
import re


class SpecGeneratorService:
    """Service for generating project specifications from user prompts"""
    
    def __init__(self):
        pass
    
    async def generate_specs_from_prompt(self, user_prompt: str, project_name: str) -> Dict[str, str]:
        """Generate all three spec files from a user prompt"""
        
        # Analyze the prompt to extract key information
        analysis = self._analyze_prompt(user_prompt)
        
        # Generate each spec file
        design_spec = self._generate_design_spec(analysis, project_name)
        requirements_spec = self._generate_requirements_spec(analysis, project_name)
        tasks_spec = self._generate_tasks_spec(analysis, project_name)
        
        return {
            "design": design_spec,
            "requirements": requirements_spec,
            "tasks": tasks_spec
        }
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, any]:
        """Analyze user prompt to extract key features and requirements"""
        prompt_lower = prompt.lower()
        
        # Detect app type
        app_types = {
            "social": ["social", "chat", "messaging", "friends", "posts", "feed"],
            "ecommerce": ["shop", "store", "buy", "sell", "cart", "payment", "product"],
            "productivity": ["todo", "task", "note", "calendar", "reminder", "organize"],
            "fitness": ["fitness", "workout", "exercise", "health", "steps", "calories"],
            "finance": ["money", "budget", "expense", "bank", "finance", "investment"],
            "education": ["learn", "course", "study", "quiz", "education", "lesson"],
            "entertainment": ["game", "music", "video", "movie", "entertainment"],
            "utility": ["tool", "utility", "calculator", "converter", "helper"]
        }
        
        detected_type = "general"
        for app_type, keywords in app_types.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected_type = app_type
                break
        
        # Detect features
        features = []
        feature_keywords = {
            "authentication": ["login", "signup", "auth", "user", "account"],
            "database": ["save", "store", "data", "database", "persist"],
            "api": ["api", "server", "backend", "fetch", "request"],
            "navigation": ["screen", "page", "navigate", "route", "tab"],
            "notifications": ["notify", "alert", "push", "notification"],
            "camera": ["camera", "photo", "image", "picture"],
            "location": ["location", "map", "gps", "address"],
            "payment": ["pay", "payment", "stripe", "purchase", "buy"],
            "social": ["share", "social", "facebook", "twitter", "instagram"],
            "offline": ["offline", "sync", "cache", "local"]
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                features.append(feature)
        
        # Extract entities (nouns that might be data models)
        entities = self._extract_entities(prompt)
        
        return {
            "app_type": detected_type,
            "features": features,
            "entities": entities,
            "original_prompt": prompt
        }
    
    def _extract_entities(self, prompt: str) -> list:
        """Extract potential data entities from the prompt"""
        # Simple entity extraction - in production, use NLP
        common_entities = [
            "user", "profile", "post", "comment", "like", "follow",
            "product", "order", "cart", "payment", "review",
            "task", "project", "note", "reminder", "category",
            "workout", "exercise", "meal", "goal", "progress",
            "transaction", "budget", "expense", "income", "account"
        ]
        
        found_entities = []
        prompt_lower = prompt.lower()
        
        for entity in common_entities:
            if entity in prompt_lower:
                found_entities.append(entity.capitalize())
        
        return found_entities[:5]  # Limit to 5 entities
    
    def _generate_design_spec(self, analysis: Dict, project_name: str) -> str:
        """Generate design specification"""
        app_type = analysis["app_type"]
        features = analysis["features"]
        
        # App type specific design patterns
        design_patterns = {
            "social": {
                "navigation": "Tab Navigation with Feed, Profile, Messages, Notifications",
                "key_screens": ["Feed", "Profile", "Chat", "Notifications", "Settings"],
                "ui_elements": ["Avatar", "Post Card", "Comment Section", "Like Button", "Follow Button"]
            },
            "ecommerce": {
                "navigation": "Stack Navigation with Product Catalog, Cart, Profile",
                "key_screens": ["Product List", "Product Detail", "Cart", "Checkout", "Profile"],
                "ui_elements": ["Product Card", "Add to Cart Button", "Price Display", "Rating Stars"]
            },
            "productivity": {
                "navigation": "Tab Navigation with Tasks, Calendar, Settings",
                "key_screens": ["Task List", "Task Detail", "Calendar", "Categories", "Settings"],
                "ui_elements": ["Task Item", "Checkbox", "Date Picker", "Priority Indicator"]
            }
        }
        
        pattern = design_patterns.get(app_type, design_patterns["productivity"])
        
        return f"""# Design Specification - {project_name}

## Project Overview
{analysis['original_prompt']}

## App Type
{app_type.capitalize()} Application

## Architecture Overview

### Navigation Structure
- **Primary Navigation**: {pattern['navigation']}
- **Screen Flow**: Linear with modal overlays for forms and details

### Key Screens
{chr(10).join([f"- **{screen}**: Main {screen.lower()} interface" for screen in pattern['key_screens']])}

## UI/UX Design

### Design System
- **Color Scheme**: Modern neutral palette with brand accent
  - Primary: #007AFF (iOS Blue)
  - Secondary: #34C759 (Success Green)
  - Background: #F2F2F7 (Light Gray)
  - Text: #000000 (Black) / #8E8E93 (Gray)

### Typography
- **Headers**: SF Pro Display, Bold, 24-32px
- **Body**: SF Pro Text, Regular, 16px
- **Captions**: SF Pro Text, Regular, 12px

### Component Library
{chr(10).join([f"- **{element}**: Reusable {element.lower()} component" for element in pattern['ui_elements']])}

## Technical Stack

### Frontend Framework
- **React Native**: Cross-platform mobile development
- **Expo**: Development and deployment platform
- **React Navigation**: Screen navigation and routing

### State Management
- **React Context**: Global state management
- **AsyncStorage**: Local data persistence

### UI Components
- **React Native Elements**: Pre-built UI components
- **Vector Icons**: Iconography system

## Responsive Design

### Screen Sizes
- **Phone**: 375x667 (iPhone SE) to 428x926 (iPhone 14 Pro Max)
- **Tablet**: 768x1024 (iPad) and larger

### Accessibility
- **VoiceOver**: Screen reader support
- **Dynamic Type**: Font size scaling
- **High Contrast**: Color accessibility
- **Touch Targets**: Minimum 44x44pt tap areas

## Features Integration
{chr(10).join([f"- **{feature.capitalize()}**: Integrated throughout the app experience" for feature in features])}

## Performance Considerations
- **Image Optimization**: WebP format with lazy loading
- **Bundle Splitting**: Code splitting for faster load times
- **Caching Strategy**: Intelligent data caching
- **Offline Support**: Core functionality available offline
"""

    def _generate_requirements_spec(self, analysis: Dict, project_name: str) -> str:
        """Generate requirements specification"""
        features = analysis["features"]
        entities = analysis["entities"]
        
        return f"""# Requirements Specification - {project_name}

## Project Overview
{analysis['original_prompt']}

## Functional Requirements

### Core User Stories

#### Epic 1: User Management
- **US-001**: As a user, I want to create an account so that I can access the app
- **US-002**: As a user, I want to log in to my account so that I can access my data
- **US-003**: As a user, I want to update my profile so that I can keep my information current
- **US-004**: As a user, I want to reset my password so that I can regain access if forgotten

#### Epic 2: Core Functionality
{chr(10).join([f"- **US-{100+i:03d}**: As a user, I want to manage {entity.lower()}s so that I can organize my {entity.lower()} data" for i, entity in enumerate(entities)])}

#### Epic 3: Data Management
- **US-201**: As a user, I want my data to be saved automatically so that I don't lose my work
- **US-202**: As a user, I want to sync my data across devices so that I can access it anywhere
- **US-203**: As a user, I want to export my data so that I can back it up or migrate

### Feature Requirements
{chr(10).join([f"- **{feature.upper()}-001**: Implement {feature} functionality with secure and reliable operation" for feature in features])}

## Acceptance Criteria

### User Registration (US-001)
- GIVEN a new user visits the app
- WHEN they provide valid email, password, and name
- THEN an account is created and they are logged in
- AND they receive a welcome message
- AND their profile is initialized with default settings

### User Authentication (US-002)
- GIVEN an existing user
- WHEN they provide correct email and password
- THEN they are logged into their account
- AND they can access all app features
- AND their session persists until logout

### Data Persistence (US-201)
- GIVEN a user makes changes to their data
- WHEN they navigate away or close the app
- THEN their changes are automatically saved
- AND they can retrieve the data when they return

## Non-Functional Requirements

### Performance
- **Response Time**: All user interactions respond within 200ms
- **Load Time**: App launches within 3 seconds on average devices
- **Offline**: Core features work without internet connection
- **Battery**: Minimal battery drain during normal usage

### Security
- **Authentication**: Secure JWT-based authentication
- **Data Encryption**: All sensitive data encrypted at rest and in transit
- **Privacy**: User data is private and not shared without consent
- **Compliance**: GDPR compliant data handling

### Scalability
- **Users**: Support up to 100,000 concurrent users
- **Data**: Handle large datasets efficiently
- **Growth**: Architecture supports feature expansion

### Usability
- **Accessibility**: WCAG 2.1 AA compliance
- **Internationalization**: Support for multiple languages
- **Platform**: Consistent experience across iOS and Android
- **Learning Curve**: New users can complete core tasks within 5 minutes

## Technical Requirements

### Platform Support
- **iOS**: iOS 13.0 and later
- **Android**: Android 8.0 (API level 26) and later
- **Expo**: Compatible with Expo SDK 49+

### Integration Requirements
- **Backend API**: RESTful API integration
- **Push Notifications**: Real-time notifications
- **Analytics**: User behavior tracking
- **Crash Reporting**: Automatic error reporting

## Constraints and Assumptions

### Constraints
- Must work on devices with 2GB RAM minimum
- App size should not exceed 50MB
- Must comply with app store guidelines
- Development timeline: 12 weeks

### Assumptions
- Users have basic smartphone literacy
- Stable internet connection for initial setup
- Users will grant necessary permissions
- Backend API is reliable and performant
"""

    def _generate_tasks_spec(self, analysis: Dict, project_name: str) -> str:
        """Generate implementation tasks"""
        features = analysis["features"]
        entities = analysis["entities"]
        
        return f"""# Implementation Tasks - {project_name}

## Phase 1: Project Setup and Foundation (Week 1-2)

### Setup Tasks
- [ ] **SETUP-001**: Initialize React Native project with Expo
- [ ] **SETUP-002**: Configure development environment and tools
- [ ] **SETUP-003**: Set up version control and CI/CD pipeline
- [ ] **SETUP-004**: Configure ESLint, Prettier, and TypeScript
- [ ] **SETUP-005**: Set up testing framework (Jest + React Native Testing Library)

### Navigation and Routing
- [ ] **NAV-001**: Install and configure React Navigation
- [ ] **NAV-002**: Create main navigation structure
- [ ] **NAV-003**: Implement screen transitions and animations
- [ ] **NAV-004**: Add deep linking support
- [ ] **NAV-005**: Create navigation guards for protected routes

## Phase 2: Authentication and User Management (Week 3-4)

### Authentication
- [ ] **AUTH-001**: Create login screen with form validation
- [ ] **AUTH-002**: Create signup screen with email verification
- [ ] **AUTH-003**: Implement password reset functionality
- [ ] **AUTH-004**: Add biometric authentication (Face ID/Touch ID)
- [ ] **AUTH-005**: Create user profile management screen

### User Interface Foundation
- [ ] **UI-001**: Create design system and theme configuration
- [ ] **UI-002**: Build reusable component library
- [ ] **UI-003**: Implement responsive layout system
- [ ] **UI-004**: Add dark mode support
- [ ] **UI-005**: Create loading states and error boundaries

## Phase 3: Core Features Implementation (Week 5-8)

### Data Models and Storage
{chr(10).join([f"- [ ] **DATA-{i+1:03d}**: Implement {entity} data model and CRUD operations" for i, entity in enumerate(entities)])}

### Feature Implementation
{chr(10).join([f"- [ ] **FEAT-{i+1:03d}**: Implement {feature} functionality" for i, feature in enumerate(features)])}

### API Integration
- [ ] **API-001**: Set up API client with authentication
- [ ] **API-002**: Implement data synchronization
- [ ] **API-003**: Add offline data caching
- [ ] **API-004**: Handle API error states
- [ ] **API-005**: Implement retry logic and network detection

## Phase 4: Advanced Features (Week 9-10)

### Performance Optimization
- [ ] **PERF-001**: Implement image lazy loading and caching
- [ ] **PERF-002**: Optimize bundle size and code splitting
- [ ] **PERF-003**: Add performance monitoring
- [ ] **PERF-004**: Implement background sync
- [ ] **PERF-005**: Optimize database queries and indexing

### User Experience Enhancements
- [ ] **UX-001**: Add haptic feedback and animations
- [ ] **UX-002**: Implement pull-to-refresh functionality
- [ ] **UX-003**: Add search and filtering capabilities
- [ ] **UX-004**: Create onboarding flow and tutorials
- [ ] **UX-005**: Implement accessibility features

## Phase 5: Testing and Quality Assurance (Week 11)

### Testing Implementation
- [ ] **TEST-001**: Write unit tests for core business logic
- [ ] **TEST-002**: Create integration tests for API calls
- [ ] **TEST-003**: Add end-to-end tests for critical user flows
- [ ] **TEST-004**: Implement visual regression testing
- [ ] **TEST-005**: Performance testing and optimization

### Quality Assurance
- [ ] **QA-001**: Manual testing on multiple devices
- [ ] **QA-002**: Accessibility testing and compliance
- [ ] **QA-003**: Security testing and vulnerability assessment
- [ ] **QA-004**: Load testing and stress testing
- [ ] **QA-005**: User acceptance testing

## Phase 6: Deployment and Launch (Week 12)

### App Store Preparation
- [ ] **DEPLOY-001**: Create app store assets (icons, screenshots, descriptions)
- [ ] **DEPLOY-002**: Configure app signing and certificates
- [ ] **DEPLOY-003**: Set up analytics and crash reporting
- [ ] **DEPLOY-004**: Create privacy policy and terms of service
- [ ] **DEPLOY-005**: Submit to App Store and Google Play

### Launch Activities
- [ ] **LAUNCH-001**: Set up production monitoring and alerts
- [ ] **LAUNCH-002**: Create user documentation and help center
- [ ] **LAUNCH-003**: Prepare customer support processes
- [ ] **LAUNCH-004**: Plan marketing and user acquisition
- [ ] **LAUNCH-005**: Monitor launch metrics and user feedback

## Ongoing Maintenance

### Post-Launch Tasks
- [ ] **MAINT-001**: Monitor app performance and user feedback
- [ ] **MAINT-002**: Regular security updates and dependency management
- [ ] **MAINT-003**: Feature updates based on user requests
- [ ] **MAINT-004**: Bug fixes and performance improvements
- [ ] **MAINT-005**: Platform updates (iOS/Android version compatibility)

## Risk Mitigation

### Technical Risks
- **Risk**: Third-party API changes or downtime
- **Mitigation**: Implement fallback mechanisms and caching

### Timeline Risks
- **Risk**: Feature scope creep
- **Mitigation**: Strict change control and MVP focus

### Quality Risks
- **Risk**: Performance issues on older devices
- **Mitigation**: Regular testing on minimum spec devices
"""


# Singleton instance
spec_generator = SpecGeneratorService()