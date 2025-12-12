"""
AI service with tier-based model selection
"""
from typing import Dict, Any, Optional
from app.models import User
import httpx
import json


class AIService:
    """Service for AI model interactions with tier-based selection"""
    
    def __init__(self):
        self.models = {
            "free": {
                "name": "llama-3.1-8b",
                "endpoint": "https://api.together.xyz/v1/chat/completions",
                "max_tokens": 2048,
                "context_window": 8192
            },
            "pro": {
                "name": "gemini-2.0-flash-exp",
                "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent",
                "max_tokens": 4096,
                "context_window": 32768
            },
            "premium": {
                "name": "gemini-2.0-flash-exp",
                "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent",
                "max_tokens": 8192,
                "context_window": 1000000
            }
        }
    
    async def generate_response(
        self, 
        user: User, 
        prompt: str, 
        context: Optional[Dict] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate AI response based on user tier"""
        model_config = self.models.get(user.tier, self.models["free"])
        
        if user.tier == "free":
            return await self._call_llama(prompt, context, system_prompt, model_config)
        else:
            return await self._call_gemini(prompt, context, system_prompt, model_config)
    
    async def _call_llama(
        self, 
        prompt: str, 
        context: Optional[Dict], 
        system_prompt: Optional[str],
        model_config: Dict
    ) -> str:
        """Call Llama model via Together AI"""
        # For now, return a mock response
        # In production, integrate with Together AI or Ollama
        
        base_response = f"[Llama 3.1 Response] I understand your request: '{prompt}'"
        
        if "add feature" in prompt.lower():
            return f"{base_response}\n\nI can help you add a new feature to your mobile app. Based on your request, I'll generate the necessary React Native components and update your specifications. What specific functionality would you like to implement?"
        
        elif "fix bug" in prompt.lower() or "error" in prompt.lower():
            return f"{base_response}\n\nI'll help you debug this issue. Could you provide more details about:\n• The error message you're seeing\n• Which component or screen is affected\n• Steps to reproduce the problem\n\nI'll analyze your code and suggest a solution."
        
        elif "refactor" in prompt.lower():
            return f"{base_response}\n\nI can help refactor your code for better performance and maintainability. Which part of your app would you like to improve? I can optimize:\n• Component structure\n• State management\n• Performance bottlenecks\n• Code organization"
        
        else:
            return f"{base_response}\n\nI'm your AI assistant powered by Llama 3.1. I can help you:\n• Add new features to your app\n• Fix bugs and issues\n• Refactor and optimize code\n• Explain app architecture\n• Generate React Native components\n\nWhat would you like to work on?"
    
    async def _call_gemini(
        self, 
        prompt: str, 
        context: Optional[Dict], 
        system_prompt: Optional[str],
        model_config: Dict
    ) -> str:
        """Call Gemini model"""
        # For now, return a mock response
        # In production, integrate with Google AI Studio
        
        tier_label = "Pro" if model_config["max_tokens"] == 4096 else "Premium"
        base_response = f"[Gemini 2.0 Flash - {tier_label}] Advanced AI Analysis Complete"
        
        if "add feature" in prompt.lower():
            return f"{base_response}\n\n🚀 **Feature Implementation Plan**\n\nI've analyzed your request and can generate a complete implementation including:\n\n• **React Native Components**: Fully functional UI components with proper styling\n• **State Management**: Redux/Context setup with proper data flow\n• **API Integration**: Backend endpoints and data fetching logic\n• **Testing Suite**: Unit and integration tests\n• **Documentation**: Code comments and usage examples\n\nI'll also update your specifications and ensure the new feature integrates seamlessly with your existing architecture. Ready to proceed?"
        
        elif "fix bug" in prompt.lower() or "error" in prompt.lower():
            return f"{base_response}\n\n🔍 **Advanced Debugging Analysis**\n\nI'll perform a comprehensive code analysis to identify and fix the issue:\n\n• **Error Pattern Recognition**: Analyzing common React Native pitfalls\n• **Performance Impact Assessment**: Checking for memory leaks and optimization opportunities\n• **Cross-Platform Compatibility**: Ensuring fixes work on both iOS and Android\n• **Automated Testing**: Generating tests to prevent regression\n\nPlease share the error details, and I'll provide a detailed solution with code examples."
        
        elif "refactor" in prompt.lower():
            return f"{base_response}\n\n⚡ **Intelligent Code Refactoring**\n\nI'll analyze your entire codebase and suggest improvements:\n\n• **Architecture Optimization**: Modern React Native patterns and best practices\n• **Performance Enhancement**: Bundle size reduction and render optimization\n• **Code Quality**: ESLint rules, TypeScript integration, and clean code principles\n• **Scalability Planning**: Preparing your app for future growth\n\nI can refactor specific components or perform a full codebase modernization. What's your priority?"
        
        else:
            return f"{base_response}\n\n✨ **Premium AI Assistant Ready**\n\nI'm your advanced AI assistant powered by Gemini 2.0 Flash with enhanced capabilities:\n\n🎯 **Intelligent Code Generation**: Context-aware React Native components\n🔧 **Advanced Debugging**: Deep code analysis and optimization\n📱 **Cross-Platform Expertise**: iOS and Android best practices\n🚀 **Performance Optimization**: Bundle analysis and render improvements\n📊 **Architecture Planning**: Scalable app design patterns\n\nI have access to your full project context and can provide detailed, production-ready solutions. How can I help you build something amazing?"
    
    async def generate_code(
        self, 
        user: User, 
        task_description: str, 
        agent_type: str,
        project_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generate code based on task and agent type"""
        model_config = self.models.get(user.tier, self.models["free"])
        
        # Enhanced code generation based on tier
        if user.tier in ["pro", "premium"]:
            return await self._generate_advanced_code(task_description, agent_type, project_context, model_config)
        else:
            return await self._generate_basic_code(task_description, agent_type, project_context, model_config)
    
    async def _generate_basic_code(
        self, 
        task_description: str, 
        agent_type: str, 
        project_context: Optional[Dict],
        model_config: Dict
    ) -> Dict[str, Any]:
        """Generate basic code for free tier"""
        if agent_type == "design":
            return {
                "files": {
                    "components/GeneratedComponent.js": f"""import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';

export default function GeneratedComponent() {{
  return (
    <View style={{styles.container}}>
      <Text style={{styles.title}}>Generated by Llama 3.1</Text>
      <Text style={{styles.description}}>{task_description}</Text>
    </View>
  );
}}

const styles = StyleSheet.create({{
  container: {{
    padding: 16,
    backgroundColor: '#f5f5f5',
  }},
  title: {{
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  }},
  description: {{
    fontSize: 14,
    color: '#666',
  }},
}});"""
                },
                "reasoning": f"Created basic React Native component for: {task_description}"
            }
        
        elif agent_type == "backend":
            return {
                "files": {
                    "services/generatedService.js": f"""// Generated API service for: {task_description}
export const generatedService = {{
  async fetchData() {{
    try {{
      const response = await fetch('/api/data');
      return await response.json();
    }} catch (error) {{
      console.error('API Error:', error);
      throw error;
    }}
  }},
  
  async saveData(data) {{
    try {{
      const response = await fetch('/api/data', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(data),
      }});
      return await response.json();
    }} catch (error) {{
      console.error('Save Error:', error);
      throw error;
    }}
  }}
}};"""
                },
                "reasoning": f"Created basic API service for: {task_description}"
            }
        
        else:  # testing
            return {
                "files": {
                    "__tests__/GeneratedComponent.test.js": f"""import React from 'react';
import {{ render }} from '@testing-library/react-native';
import GeneratedComponent from '../components/GeneratedComponent';

describe('GeneratedComponent', () => {{
  it('renders correctly', () => {{
    const {{ getByText }} = render(<GeneratedComponent />);
    expect(getByText('Generated by Llama 3.1')).toBeTruthy();
  }});
  
  it('displays task description', () => {{
    const {{ getByText }} = render(<GeneratedComponent />);
    expect(getByText('{task_description}')).toBeTruthy();
  }});
}});"""
                },
                "reasoning": f"Created basic tests for: {task_description}"
            }
    
    async def _generate_advanced_code(
        self, 
        task_description: str, 
        agent_type: str, 
        project_context: Optional[Dict],
        model_config: Dict
    ) -> Dict[str, Any]:
        """Generate advanced code for pro/premium tiers"""
        tier_label = "Pro" if model_config["max_tokens"] == 4096 else "Premium"
        
        if agent_type == "design":
            return {
                "files": {
                    "components/AdvancedComponent.tsx": f"""import React, {{ useState, useEffect, useMemo }} from 'react';
import {{
  View,
  Text,
  StyleSheet,
  Animated,
  Pressable,
  Dimensions,
}} from 'react-native';
import {{ useTheme }} from '@react-navigation/native';

interface AdvancedComponentProps {{
  title?: string;
  onPress?: () => void;
  variant?: 'primary' | 'secondary';
}}

export default function AdvancedComponent({{
  title = 'Gemini 2.0 Generated',
  onPress,
  variant = 'primary'
}}: AdvancedComponentProps) {{
  const {{ colors }} = useTheme();
  const [pressed, setPressed] = useState(false);
  const animatedValue = useMemo(() => new Animated.Value(1), []);
  
  const handlePressIn = () => {{
    setPressed(true);
    Animated.spring(animatedValue, {{
      toValue: 0.95,
      useNativeDriver: true,
    }}).start();
  }};
  
  const handlePressOut = () => {{
    setPressed(false);
    Animated.spring(animatedValue, {{
      toValue: 1,
      useNativeDriver: true,
    }}).start();
  }};
  
  const dynamicStyles = useMemo(() => StyleSheet.create({{
    container: {{
      backgroundColor: variant === 'primary' ? colors.primary : colors.card,
      borderRadius: 12,
      padding: 16,
      margin: 8,
      shadowColor: colors.shadow,
      shadowOffset: {{ width: 0, height: 2 }},
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    }},
    text: {{
      color: variant === 'primary' ? colors.background : colors.text,
      fontSize: 16,
      fontWeight: '600',
      textAlign: 'center',
    }},
    description: {{
      color: variant === 'primary' ? colors.background : colors.text,
      fontSize: 14,
      opacity: 0.8,
      marginTop: 4,
      textAlign: 'center',
    }},
  }}), [colors, variant]);
  
  return (
    <Animated.View style={{{{ transform: [{{ scale: animatedValue }}] }}}}>
      <Pressable
        style={{dynamicStyles.container}}
        onPress={{onPress}}
        onPressIn={{handlePressIn}}
        onPressOut={{handlePressOut}}
        android_ripple={{{{ color: colors.primary, borderless: false }}}}
      >
        <Text style={{dynamicStyles.text}}>{{title}}</Text>
        <Text style={{dynamicStyles.description}}>
          {task_description} - Generated by Gemini 2.0 Flash ({tier_label})
        </Text>
      </Pressable>
    </Animated.View>
  );
}}""",
                    "hooks/useAdvancedComponent.ts": f"""import {{ useState, useCallback, useEffect }} from 'react';
import {{ Dimensions }} from 'react-native';

export interface UseAdvancedComponentReturn {{
  screenData: {{ width: number; height: number }};
  isLandscape: boolean;
  handleAction: () => void;
  isLoading: boolean;
}}

export function useAdvancedComponent(): UseAdvancedComponentReturn {{
  const [screenData, setScreenData] = useState(Dimensions.get('window'));
  const [isLoading, setIsLoading] = useState(false);
  
  const isLandscape = screenData.width > screenData.height;
  
  useEffect(() => {{
    const subscription = Dimensions.addEventListener('change', ({{ window }}) => {{
      setScreenData(window);
    }});
    
    return () => subscription?.remove();
  }}, []);
  
  const handleAction = useCallback(async () => {{
    setIsLoading(true);
    try {{
      // Simulate async operation for: {task_description}
      await new Promise(resolve => setTimeout(resolve, 1000));
    }} finally {{
      setIsLoading(false);
    }}
  }}, []);
  
  return {{
    screenData,
    isLandscape,
    handleAction,
    isLoading,
  }};
}}"""
                },
                "reasoning": f"Generated advanced TypeScript React Native component with animations, theming, and custom hooks for: {task_description}"
            }
        
        elif agent_type == "backend":
            return {
                "files": {
                    "services/AdvancedAPIService.ts": f"""import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-netinfo/netinfo';

export interface APIResponse<T> {{
  data: T;
  success: boolean;
  message?: string;
}}

export interface CacheConfig {{
  ttl: number; // Time to live in milliseconds
  key: string;
}}

class AdvancedAPIService {{
  private baseURL: string;
  private cache = new Map<string, {{ data: any; timestamp: number; ttl: number }}>();
  
  constructor(baseURL: string = 'https://api.example.com') {{
    this.baseURL = baseURL;
  }}
  
  private async isOnline(): Promise<boolean> {{
    const netInfo = await NetInfo.fetch();
    return netInfo.isConnected ?? false;
  }}
  
  private async getCachedData<T>(key: string): Promise<T | null> {{
    try {{
      const cached = this.cache.get(key);
      if (cached && Date.now() - cached.timestamp < cached.ttl) {{
        return cached.data;
      }}
      
      // Try AsyncStorage for persistent cache
      const stored = await AsyncStorage.getItem(`cache_${{key}}`);
      if (stored) {{
        const parsed = JSON.parse(stored);
        if (Date.now() - parsed.timestamp < parsed.ttl) {{
          return parsed.data;
        }}
      }}
    }} catch (error) {{
      console.warn('Cache retrieval error:', error);
    }}
    return null;
  }}
  
  private async setCachedData(key: string, data: any, ttl: number): Promise<void> {{
    const cacheEntry = {{ data, timestamp: Date.now(), ttl }};
    this.cache.set(key, cacheEntry);
    
    try {{
      await AsyncStorage.setItem(`cache_${{key}}`, JSON.stringify(cacheEntry));
    }} catch (error) {{
      console.warn('Cache storage error:', error);
    }}
  }}
  
  async request<T>(
    endpoint: string,
    options: RequestInit = {{}},
    cacheConfig?: CacheConfig
  ): Promise<APIResponse<T>> {{
    const url = `${{this.baseURL}}${{endpoint}}`;
    const cacheKey = `${{endpoint}}_${{JSON.stringify(options)}}`;
    
    // Try cache first for GET requests
    if ((!options.method || options.method === 'GET') && cacheConfig) {{
      const cached = await this.getCachedData<T>(cacheKey);
      if (cached) {{
        return {{ data: cached, success: true, message: 'From cache' }};
      }}
    }}
    
    // Check network connectivity
    const online = await this.isOnline();
    if (!online) {{
      const cached = await this.getCachedData<T>(cacheKey);
      if (cached) {{
        return {{ data: cached, success: true, message: 'Offline - from cache' }};
      }}
      throw new Error('No network connection and no cached data available');
    }}
    
    try {{
      const response = await fetch(url, {{
        ...options,
        headers: {{
          'Content-Type': 'application/json',
          ...options.headers,
        }},
      }});
      
      if (!response.ok) {{
        throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
      }}
      
      const data = await response.json();
      
      // Cache successful GET requests
      if ((!options.method || options.method === 'GET') && cacheConfig) {{
        await this.setCachedData(cacheKey, data, cacheConfig.ttl);
      }}
      
      return {{ data, success: true }};
    }} catch (error) {{
      console.error('API request failed:', error);
      
      // Try to return cached data on error
      if (cacheConfig) {{
        const cached = await this.getCachedData<T>(cacheKey);
        if (cached) {{
          return {{ data: cached, success: false, message: 'Error - returning cached data' }};
        }}
      }}
      
      throw error;
    }}
  }}
  
  // Specific method for: {task_description}
  async fetchTaskData(): Promise<APIResponse<any>> {{
    return this.request('/task-data', {{}}, {{ key: 'task-data', ttl: 300000 }}); // 5 min cache
  }}
  
  async submitTaskData(data: any): Promise<APIResponse<any>> {{
    return this.request('/task-data', {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}
}}

export const advancedAPIService = new AdvancedAPIService();"""
                },
                "reasoning": f"Generated advanced TypeScript API service with caching, offline support, and network detection for: {task_description}"
            }
        
        else:  # testing
            return {
                "files": {
                    "__tests__/AdvancedComponent.test.tsx": f"""import React from 'react';
import {{ render, fireEvent, waitFor, act }} from '@testing-library/react-native';
import {{ NavigationContainer }} from '@react-navigation/native';
import AdvancedComponent from '../components/AdvancedComponent';

// Mock dependencies
jest.mock('@react-native-async-storage/async-storage', () => ({{
  getItem: jest.fn(),
  setItem: jest.fn(),
}}}));

jest.mock('@react-native-netinfo/netinfo', () => ({{
  fetch: jest.fn(() => Promise.resolve({{ isConnected: true }})),
}}}));

const MockedNavigationProvider = ({{ children }}: {{ children: React.ReactNode }}) => (
  <NavigationContainer>{{children}}</NavigationContainer>
);

describe('AdvancedComponent', () => {{
  beforeEach(() => {{
    jest.clearAllMocks();
  }});
  
  it('renders with default props', () => {{
    const {{ getByText }} = render(
      <MockedNavigationProvider>
        <AdvancedComponent />
      </MockedNavigationProvider>
    );
    
    expect(getByText('Gemini 2.0 Generated')).toBeTruthy();
    expect(getByText(/{task_description}/)).toBeTruthy();
  }});
  
  it('handles press events with animation', async () => {{
    const mockOnPress = jest.fn();
    const {{ getByText }} = render(
      <MockedNavigationProvider>
        <AdvancedComponent title="Test Component" onPress={{mockOnPress}} />
      </MockedNavigationProvider>
    );
    
    const component = getByText('Test Component');
    
    await act(async () => {{
      fireEvent(component, 'pressIn');
    }});
    
    await act(async () => {{
      fireEvent(component, 'pressOut');
    }});
    
    await act(async () => {{
      fireEvent.press(component);
    }});
    
    expect(mockOnPress).toHaveBeenCalledTimes(1);
  }});
  
  it('applies correct styles for different variants', () => {{
    const {{ rerender, getByTestId }} = render(
      <MockedNavigationProvider>
        <AdvancedComponent variant="primary" testID="component" />
      </MockedNavigationProvider>
    );
    
    let component = getByTestId('component');
    expect(component.props.style).toBeDefined();
    
    rerender(
      <MockedNavigationProvider>
        <AdvancedComponent variant="secondary" testID="component" />
      </MockedNavigationProvider>
    );
    
    component = getByTestId('component');
    expect(component.props.style).toBeDefined();
  }});
  
  it('responds to screen orientation changes', async () => {{
    const {{ getByTestId }} = render(
      <MockedNavigationProvider>
        <AdvancedComponent testID="component" />
      </MockedNavigationProvider>
    );
    
    // Simulate orientation change
    await act(async () => {{
      // This would trigger the Dimensions change event in a real environment
    }});
    
    expect(getByTestId('component')).toBeTruthy();
  }});
}});

// Integration test for the hook
describe('useAdvancedComponent', () => {{
  it('provides correct screen data and handlers', async () => {{
    const TestComponent = () => {{
      const {{ screenData, isLandscape, handleAction, isLoading }} = useAdvancedComponent();
      
      return (
        <div>
          <span testID="width">{{screenData.width}}</span>
          <span testID="landscape">{{isLandscape.toString()}}</span>
          <span testID="loading">{{isLoading.toString()}}</span>
          <button testID="action" onPress={{handleAction}}>Action</button>
        </div>
      );
    }};
    
    const {{ getByTestId }} = render(<TestComponent />);
    
    expect(getByTestId('width')).toBeTruthy();
    expect(getByTestId('landscape')).toBeTruthy();
    expect(getByTestId('loading')).toBeTruthy();
    
    const actionButton = getByTestId('action');
    await act(async () => {{
      fireEvent.press(actionButton);
    }});
    
    await waitFor(() => {{
      expect(getByTestId('loading').props.children).toBe('false');
    }});
  }});
}});"""
                },
                "reasoning": f"Generated comprehensive TypeScript test suite with mocking, integration tests, and async testing for: {task_description}"
            }


# Singleton instance
ai_service = AIService()