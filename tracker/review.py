import os
from datetime import date
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from .db import get_db_connection
from .logs import get_today_logs
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
console = Console()

@dataclass
class AIResponse:
    """Standardized AI response format"""
    content: str
    model: str
    provider: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    def __init__(self, api_key: str, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model or self.get_default_model()
        self.provider_name = self.__class__.__name__.replace('Provider', '').lower()
    
    @abstractmethod
    def get_default_model(self) -> str:
        """Return the default model for this provider"""
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> AIResponse:
        """Generate response from the AI provider"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available (API key, library installed)"""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI provider implementation"""
    
    def get_default_model(self) -> str:
        return "gpt-3.5-turbo"
    
    def is_available(self) -> bool:
        try:
            import openai
            return bool(self.api_key)
        except ImportError:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> AIResponse:
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            return AIResponse(
                content=response.choices[0].message.content.strip(),
                model=self.model,
                provider="openai",
                tokens_used=response.usage.total_tokens if hasattr(response, 'usage') else None
            )
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

class AnthropicProvider(AIProvider):
    """Anthropic Claude provider implementation"""
    
    def get_default_model(self) -> str:
        return "claude-3-haiku-20240307"
    
    def is_available(self) -> bool:
        try:
            import anthropic
            return bool(self.api_key)
        except ImportError:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> AIResponse:
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=300,
                system=system_prompt or "You are a helpful assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return AIResponse(
                content=response.content[0].text,
                model=self.model,
                provider="anthropic",
                tokens_used=response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else None
            )
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

class GeminiProvider(AIProvider):
    """Google Gemini provider implementation"""
    
    def get_default_model(self) -> str:
        return "gemini-pro"
    
    def is_available(self) -> bool:
        try:
            import google.generativeai as genai
            return bool(self.api_key)
        except ImportError:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> AIResponse:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = model.generate_content(full_prompt)
            
            return AIResponse(
                content=response.text,
                model=self.model,
                provider="gemini"
            )
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

class OllamaProvider(AIProvider):
    """Ollama local LLM provider implementation"""
    
    def get_default_model(self) -> str:
        return "llama2"
    
    def is_available(self) -> bool:
        try:
            import ollama
            # Test connection to Ollama
            ollama.list()
            return True
        except ImportError:
            return False
        except Exception:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> AIResponse:
        try:
            import ollama
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            
            return AIResponse(
                content=response['message']['content'],
                model=self.model,
                provider="ollama"
            )
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

class AIProviderManager:
    """Manages AI providers and handles provider selection"""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        provider_configs = {
            'openai': {
                'class': OpenAIProvider,
                'api_key_env': 'OPENAI_API_KEY',
                'model_env': 'OPENAI_MODEL'
            },
            'anthropic': {
                'class': AnthropicProvider,
                'api_key_env': 'ANTHROPIC_API_KEY',
                'model_env': 'ANTHROPIC_MODEL'
            },
            'gemini': {
                'class': GeminiProvider,
                'api_key_env': 'GEMINI_API_KEY',
                'model_env': 'GEMINI_MODEL'
            },
            'ollama': {
                'class': OllamaProvider,
                'api_key_env': None,  # Ollama doesn't need API key
                'model_env': 'OLLAMA_MODEL'
            }
        }
        
        for provider_name, config in provider_configs.items():
            try:
                api_key = os.getenv(config['api_key_env']) if config['api_key_env'] else None
                model = os.getenv(config['model_env'])
                
                provider = config['class'](api_key=api_key, model=model)
                if provider.is_available():
                    self.providers[provider_name] = provider
            except Exception as e:
                console.print(f"[yellow]⚠️ Failed to initialize {provider_name}: {e}[/yellow]")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def get_provider(self, provider_name: Optional[str] = None) -> Optional[AIProvider]:
        """Get a specific provider or the first available one"""
        if provider_name and provider_name in self.providers:
            return self.providers[provider_name]
        elif self.providers:
            # Return first available provider
            return next(iter(self.providers.values()))
        return None

def generate_ai_review(provider_name: Optional[str] = None, model_name: Optional[str] = None):
    """Generate AI review of the day"""
    manager = AIProviderManager()
    available_providers = manager.get_available_providers()
    
    if not available_providers:
        console.print("[red]❌ No AI providers available. Please configure at least one:[/red]")
        console.print("• Set OPENAI_API_KEY environment variable")
        console.print("• Set ANTHROPIC_API_KEY environment variable")
        console.print("• Set GEMINI_API_KEY environment variable")
        console.print("• Install and run Ollama locally")
        console.print("\nFor now, here's a basic review:")
        generate_basic_review()
        return
    
    # Show available providers if multiple and no specific choice
    if len(available_providers) > 1 and not provider_name:
        default_name = available_providers[0]
        console.print(f"[blue]ℹ️ Available AI providers: {', '.join(available_providers)}[/blue]")
        console.print(f"[blue]Using: {default_name} (default)[/blue]")
        console.print("[blue]Specify provider with: python main.py review --provider <name>[/blue]")
    
    provider = manager.get_provider(provider_name)
    if not provider:
        if provider_name:
            console.print(f"[red]❌ Provider '{provider_name}' not available[/red]")
        console.print("Falling back to basic review:")
        generate_basic_review()
        return
    
    # Override model if specified
    if model_name:
        provider.model = model_name
    
    try:
        # Gather today's data
        daily_summary = get_daily_summary()
        
        # Create AI prompt
        prompt = create_review_prompt(daily_summary)
        system_prompt = "You are a productivity coach. Provide concise, actionable advice based on the user's daily work summary. Be encouraging but honest."
        
        # Get AI response
        response = provider.generate_response(prompt, system_prompt)
        
        # Display AI review
        title = f"🤖 AI Daily Review ({response.provider.title()} - {response.model})"
        console.print(Panel(
            response.content,
            title=title,
            border_style="blue"
        ))
        
        # Show token usage if available
        if response.tokens_used:
            console.print(f"[dim]Tokens used: {response.tokens_used}[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ Error generating AI review: {e}[/red]")
        console.print("Here's a basic review instead:")
        generate_basic_review()

def get_daily_summary():
    """Get summary of today's activities"""
    from .db import get_daily_stats
    
    stats = get_daily_stats()
    logs = get_today_logs()
    
    # Get today's tasks
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    cursor.execute("SELECT task, completed FROM tasks WHERE date_added = ?", (today,))
    tasks = cursor.fetchall()
    conn.close()
    
    return {
        'stats': stats,
        'tasks': tasks,
        'logs': logs
    }

def create_review_prompt(summary):
    """Create the prompt for AI review"""
    stats = summary['stats']
    tasks = summary['tasks']
    logs = summary['logs']
    
    prompt = f"""Today's work summary:
- Tasks completed: {stats['completed_tasks']}
- Tasks pending: {stats['pending_tasks']}
- Focus sessions: {stats['focus_sessions']} ({stats['total_focus_time']} minutes total)
- Log entries: {stats['log_entries']}

Tasks:
"""
    
    for task, completed in tasks:
        status = "✅" if completed else "⏳"
        prompt += f"- {status} {task}\n"
    
    if logs:
        prompt += "\nWork log entries:\n"
        for entry, timestamp in logs:
            prompt += f"- {entry}\n"
    
    prompt += """

Analyze this day. Provide:
1. What went well
2. Areas for improvement
3. Specific suggestions for tomorrow
Keep it concise and actionable."""
    
    return prompt

def generate_basic_review():
    """Generate a basic review without AI"""
    summary = get_daily_summary()
    stats = summary['stats']
    
    review_text = "📊 Basic Daily Review:\n\n"
    
    # Analyze productivity
    if stats['completed_tasks'] > 0:
        review_text += f"✅ Great job completing {stats['completed_tasks']} task(s)!\n"
    else:
        review_text += "⚠️ No tasks completed today. Consider breaking down large tasks into smaller ones.\n"
    
    if stats['focus_sessions'] > 0:
        avg_session = stats['total_focus_time'] / stats['focus_sessions']
        review_text += f"🎯 You had {stats['focus_sessions']} focus session(s) averaging {avg_session:.1f} minutes.\n"
        
        if avg_session < 15:
            review_text += "💡 Try longer focus sessions (25+ minutes) for deeper work.\n"
        elif avg_session > 45:
            review_text += "💡 Consider shorter sessions with breaks to maintain focus.\n"
    else:
        review_text += "⏰ No focus sessions logged. Try starting with 25-minute focused work blocks.\n"
    
    if stats['log_entries'] > 0:
        review_text += f"📝 You made {stats['log_entries']} log entries - great for reflection!\n"
    
    # Tomorrow's suggestions
    review_text += f"\n🔮 Tomorrow's focus:\n"
    if stats['pending_tasks'] > 0:
        review_text += f"- Complete {stats['pending_tasks']} pending task(s)\n"
    review_text += "- Start with a focus session\n- Log your progress regularly"
    
    console.print(Panel(
        review_text,
        title="📊 Daily Review",
        border_style="green"
    ))

def list_providers():
    """List all available AI providers"""
    manager = AIProviderManager()
    available = manager.get_available_providers()
    
    console.print("[bold]Available AI Providers:[/bold]")
    if available:
        for provider in available:
            console.print(f"✅ {provider}")
    else:
        console.print("[red]❌ No providers configured[/red]")
    
    console.print("\n[bold]Configuration:[/bold]")
    console.print("• OpenAI: Set OPENAI_API_KEY")
    console.print("• Anthropic: Set ANTHROPIC_API_KEY") 
    console.print("• Gemini: Set GEMINI_API_KEY")
    console.print("• Ollama: Install Ollama locally")