import os
from datetime import date
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from reflex.tracker.db import get_db_connection
from reflex.tracker.logs import get_today_logs
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
import time

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

class AIProviderError(Exception):
    """Custom exception for AI provider errors"""
    def __init__(self, message: str, error_type: str = "generic", provider: str = "unknown"):
        self.message = message
        self.error_type = error_type
        self.provider = provider
        super().__init__(self.message)

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
    
    def _handle_api_error(self, error: Exception) -> AIProviderError:
        """Convert API errors to standardized format"""
        error_str = str(error).lower()
        
        if "rate limit" in error_str or "429" in error_str:
            return AIProviderError(
                f"Rate limit exceeded for {self.provider_name}. Please try again later.",
                "rate_limit",
                self.provider_name
            )
        elif "quota" in error_str or "billing" in error_str:
            return AIProviderError(
                f"API quota exceeded for {self.provider_name}. Check your billing.",
                "quota_exceeded",
                self.provider_name
            )
        elif "authentication" in error_str or "401" in error_str or "api key" in error_str:
            return AIProviderError(
                f"Authentication failed for {self.provider_name}. Check your API key.",
                "auth_error",
                self.provider_name
            )
        elif "model" in error_str and "not found" in error_str:
            return AIProviderError(
                f"Model '{self.model}' not found for {self.provider_name}. Check model name.",
                "model_not_found",
                self.provider_name
            )
        elif "network" in error_str or "connection" in error_str or "timeout" in error_str:
            return AIProviderError(
                f"Network error connecting to {self.provider_name}. Check your connection.",
                "network_error",
                self.provider_name
            )
        else:
            return AIProviderError(
                f"Error with {self.provider_name}: {str(error)}",
                "generic",
                self.provider_name
            )

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
                temperature=0.7,
                timeout=30
            )
            
            return AIResponse(
                content=response.choices[0].message.content or "",
                model=self.model,
                provider="openai",
                tokens_used=getattr(response.usage, "total_tokens", None)
            )
        except Exception as e:
            raise self._handle_api_error(e)

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
                messages=[{"role": "user", "content": prompt}],
                timeout=30
            )
            
            return AIResponse(
                content=response.content[0].text,
                model=self.model,
                provider="anthropic",
                tokens_used=response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else None
            )
        except Exception as e:
            raise self._handle_api_error(e)

class GeminiProvider(AIProvider):
    """Google Gemini provider implementation"""
    
    def get_default_model(self) -> str:
        return "gemini-1.5-pro"
    
    def is_available(self) -> bool:
        try:
            import google.generativeai as genai
            return bool(self.api_key)
        except ImportError:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> AIResponse:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key) # type: ignore
            model = genai.GenerativeModel(self.model) # type: ignore
            
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
            raise self._handle_api_error(e)

class OllamaProvider(AIProvider):
    """Ollama local LLM provider implementation"""
    
    def __init__(self, api_key: str = None, model: Optional[str] = None): # type: ignore
        # Ollama doesn't need API key, but we maintain the interface
        super().__init__(api_key or "", model)
        self.server_url = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")
    
    def get_default_model(self) -> str:
        return "llama2"
    
    def is_available(self) -> bool:
        try:
            import ollama
            # Test connection to Ollama server
            client = ollama.Client(host=self.server_url)
            client.list()
            return True
        except ImportError:
            return False
        except Exception:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> AIResponse:
        try:
            import ollama
            
            client = ollama.Client(host=self.server_url)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat(
                model=self.model,
                messages=messages
            )
            
            return AIResponse(
                content=response['message']['content'],
                model=self.model,
                provider="ollama"
            )
        except Exception as e:
            raise self._handle_api_error(e)

class AIProviderManager:
    """Manages AI providers and handles provider selection"""
    
    def __init__(self):
        self.providers = {}
        self.valid_provider_names = ["openai", "anthropic", "gemini", "ollama"]
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
                    console.print(f"[dim]✓ {provider_name} provider initialized[/dim]")
            except Exception as e:
                console.print(f"[yellow]⚠️ Failed to initialize {provider_name}: {e}[/yellow]")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def validate_provider_name(self, provider_name: str) -> bool:
        """Validate if provider name is supported"""
        return provider_name.lower() in self.valid_provider_names
    
    def get_provider(self, provider_name: Optional[str] = None) -> Optional[AIProvider]:
        """Get provider with proper fallback logic"""
        # Check passed-in provider name first
        if provider_name:
            provider_name = provider_name.lower()
            if not self.validate_provider_name(provider_name):
                raise AIProviderError(
                    f"Unsupported provider '{provider_name}'. Valid options: {', '.join(self.valid_provider_names)}",
                    "invalid_provider"
                )
            
            if provider_name in self.providers:
                return self.providers[provider_name]
            else:
                raise AIProviderError(
                    f"Provider '{provider_name}' is not available. Check configuration.",
                    "provider_unavailable"
                )
        
        # Then check the environment variable
        env_default = os.getenv("DEFAULT_PROVIDER", "").lower()
        if env_default:
            if not self.validate_provider_name(env_default):
                console.print(f"[yellow]⚠️ Invalid DEFAULT_PROVIDER '{env_default}' in .env file. Valid options: {', '.join(self.valid_provider_names)}[/yellow]")
            elif env_default in self.providers:
                return self.providers[env_default]
            else:
                console.print(f"[yellow]⚠️ DEFAULT_PROVIDER '{env_default}' is not available. Falling back to first available.[/yellow]")

        # Fallback to first available
        if self.providers:
            return next(iter(self.providers.values()))
        
        return None

def generate_ai_review(provider_name: Optional[str] = None, model_name: Optional[str] = None):
    """Generate AI review of the day with comprehensive error handling"""
    try:
        manager = AIProviderManager()
        available_providers = manager.get_available_providers()
        
        if not available_providers:
            console.print("[red]❌ No AI providers available. Please configure at least one:[/red]")
            console.print("• Set OPENAI_API_KEY environment variable")
            console.print("• Set ANTHROPIC_API_KEY environment variable")
            console.print("• Set GEMINI_API_KEY environment variable")
            console.print("• Install and run Ollama locally")
            console.print("\n[blue]Falling back to basic review:[/blue]")
            generate_basic_review()
            return
        
        # Show available providers if multiple and no specific choice
        if len(available_providers) > 1 and not provider_name:
            env_default = os.getenv("DEFAULT_PROVIDER", "").lower()
            if env_default and env_default in available_providers:
                default_name = env_default
            else:
                default_name = available_providers[0]
            
            console.print(f"[blue]ℹ️ Available AI providers: {', '.join(available_providers)}[/blue]")
            console.print(f"[blue]Using: {default_name} (default)[/blue]")
            console.print("[blue]Specify provider with: python main.py review --provider <name>[/blue]")
        
        # Get provider with error handling
        try:
            provider = manager.get_provider(provider_name)
        except AIProviderError as e:
            console.print(f"[red]❌ {e.message}[/red]")
            console.print("[blue]Falling back to basic review:[/blue]")
            generate_basic_review()
            return
        
        if not provider:
            console.print("[red]❌ No provider available[/red]")
            console.print("[blue]Falling back to basic review:[/blue]")
            generate_basic_review()
            return
        
        # Override model if specified and validate
        if model_name:
            if not model_name.strip():
                console.print("[yellow]⚠️ Empty model name provided, using default[/yellow]")
            else:
                provider.model = model_name.strip()
        
        console.print(f"[green]✅ Using provider: {provider.provider_name} ({provider.model})[/green]")
        
        # Gather today's data with error handling
        try:
            daily_summary = get_daily_summary()
        except Exception as e:
            console.print(f"[red]❌ Error gathering daily summary: {e}[/red]")
            console.print("[blue]Falling back to basic review:[/blue]")
            generate_basic_review()
            return
        
        # Validate daily summary structure
        if not validate_daily_summary(daily_summary):
            console.print("[yellow]⚠️ Invalid daily summary structure[/yellow]")
            console.print("[blue]Falling back to basic review:[/blue]")
            generate_basic_review()
            return
        
        # Create AI prompt
        prompt = create_review_prompt(daily_summary)
        system_prompt = "You are a productivity coach. Provide concise, actionable advice based on the user's daily work summary. Be encouraging but honest."
        
        # Get AI response with retry logic
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
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
                
                return  # Success, exit function
                
            except AIProviderError as e:
                if attempt < max_retries and e.error_type == "network_error":
                    console.print(f"[yellow]⚠️ {e.message} Retrying in 2 seconds... (attempt {attempt + 1}/{max_retries + 1})[/yellow]")
                    time.sleep(2)
                    continue
                else:
                    console.print(f"[red]❌ {e.message}[/red]")
                    if e.error_type == "rate_limit":
                        console.print("[blue]💡 Try again in a few minutes or use a different provider[/blue]")
                    elif e.error_type == "model_not_found":
                        console.print(f"[blue]💡 Available models depend on your {e.provider} account tier[/blue]")
                    break
            except Exception as e:
                console.print(f"[red]❌ Unexpected error with {provider.provider_name}: {e}[/red]")
                break
        
        console.print("[blue]Falling back to basic review:[/blue]")
        generate_basic_review()
        
    except Exception as e:
        console.print(f"[red]❌ Critical error in AI review generation: {e}[/red]")
        console.print("[blue]Falling back to basic review:[/blue]")
        generate_basic_review()

def validate_daily_summary(summary: Dict[str, Any]) -> bool:
    """Validate the structure of daily summary"""
    try:
        required_keys = ['stats', 'tasks', 'logs']
        if not all(key in summary for key in required_keys):
            return False
        
        # Validate stats structure
        stats = summary['stats']
        required_stats = ['completed_tasks', 'pending_tasks', 'focus_sessions', 'total_focus_time', 'log_entries']
        if not all(key in stats for key in required_stats):
            return False
        
        # Ensure numeric values
        for key in required_stats:
            if not isinstance(stats[key], (int, float)):
                return False
        
        return True
    except Exception:
        return False

def get_daily_summary():
    """Get summary of today's activities with error handling"""
    try:
        from reflex.tracker.db import get_daily_stats
        
        stats = get_daily_stats()
        logs = get_today_logs()
        
        # Get today's tasks with error handling
        tasks = []
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            today = date.today().isoformat()
            
            cursor.execute("SELECT task, completed FROM tasks WHERE date_added = ?", (today,))
            tasks = cursor.fetchall()
            conn.close()
        except Exception as e:
            console.print(f"[yellow]⚠️ Could not fetch tasks: {e}[/yellow]")
            tasks = []
        
        return {
            'stats': stats,
            'tasks': tasks,
            'logs': logs
        }
    except Exception as e:
        # Return default structure if there's an error
        console.print(f"[yellow]⚠️ Error getting daily summary: {e}[/yellow]")
        return {
            'stats': {
                'completed_tasks': 0,
                'pending_tasks': 0,
                'focus_sessions': 0,
                'total_focus_time': 0,
                'log_entries': 0
            },
            'tasks': [],
            'logs': []
        }

def create_review_prompt(summary):
    """Create the prompt for AI review with safe data access"""
    try:
        stats = summary.get('stats', {})
        tasks = summary.get('tasks', [])
        logs = summary.get('logs', [])
        
        # Safe access to stats with defaults
        completed_tasks = stats.get('completed_tasks', 0)
        pending_tasks = stats.get('pending_tasks', 0)
        focus_sessions = stats.get('focus_sessions', 0)
        total_focus_time = stats.get('total_focus_time', 0)
        log_entries = stats.get('log_entries', 0)
        
        prompt = f"""Today's work summary:
- Tasks completed: {completed_tasks}
- Tasks pending: {pending_tasks}
- Focus sessions: {focus_sessions} ({total_focus_time} minutes total)
- Log entries: {log_entries}

Tasks:
"""
        
        if tasks:
            for task_data in tasks:
                if len(task_data) >= 2:
                    task, completed = task_data[0], task_data[1]
                    status = "✅" if completed else "⏳"
                    prompt += f"- {status} {task}\n"
        else:
            prompt += "- No tasks recorded today\n"
        
        if logs:
            prompt += "\nWork log entries:\n"
            for log_data in logs:
                if isinstance(log_data, (list, tuple)) and len(log_data) >= 1:
                    entry = log_data[0]
                    prompt += f"- {entry}\n"
                elif isinstance(log_data, str):
                    prompt += f"- {log_data}\n"
        
        prompt += """

Analyze this day. Provide:
1. What went well
2. Areas for improvement
3. Specific suggestions for tomorrow
Keep it concise and actionable."""
        
        return prompt
    except Exception as e:
        console.print(f"[yellow]⚠️ Error creating prompt: {e}[/yellow]")
        return "Please provide a general productivity review for today."

def generate_basic_review():
    """Generate a basic review without AI"""
    try:
        summary = get_daily_summary()
        
        if not validate_daily_summary(summary):
            console.print(Panel(
                "📊 Unable to generate detailed review due to data issues.\n\n"
                "💡 General suggestions:\n"
                "- Set clear daily goals\n"
                "- Use focus sessions for deep work\n"
                "- Log your progress regularly\n"
                "- Review and adjust your approach",
                title="📊 Basic Daily Review",
                border_style="green"
            ))
            return
        
        stats = summary['stats']
        
        review_text = "📊 Basic Daily Review:\n\n"
        
        # Analyze productivity
        if stats['completed_tasks'] > 0:
            review_text += f"✅ Great job completing {stats['completed_tasks']} task(s)!\n"
        else:
            review_text += "⚠️ No tasks completed today. Consider breaking down large tasks into smaller ones.\n"
        
        if stats['focus_sessions'] > 0:
            avg_session = stats['total_focus_time'] / stats['focus_sessions'] if stats['focus_sessions'] > 0 else 0
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
    except Exception as e:
        console.print(f"[red]❌ Error generating basic review: {e}[/red]")
        console.print(Panel(
            "💡 Daily Productivity Tips:\n\n"
            "- Start each day with clear goals\n"
            "- Use time-blocking for focused work\n"
            "- Take regular breaks to maintain energy\n"
            "- Review progress at end of day\n"
            "- Adjust strategies based on what works",
            title="📊 General Productivity Guide",
            border_style="blue"
        ))

def list_providers():
    """List all available AI providers"""
    try:
        manager = AIProviderManager()
        available = manager.get_available_providers()
        
        console.print("[bold]Available AI Providers:[/bold]")
        if available:
            for provider in available:
                console.print(f"✅ {provider}")
        else:
            console.print("[red]❌ No providers configured[/red]")
        
        console.print("\n[bold]Supported Providers:[/bold]")
        for provider in manager.valid_provider_names:
            status = "✅" if provider in available else "❌"
            console.print(f"{status} {provider}")
        
        console.print("\n[bold]Configuration:[/bold]")
        console.print("• OpenAI: Set OPENAI_API_KEY")
        console.print("• Anthropic: Set ANTHROPIC_API_KEY") 
        console.print("• Gemini: Set GEMINI_API_KEY")
        console.print("• Ollama: Install Ollama locally")
        
        # Show current default
        default_provider = os.getenv("DEFAULT_PROVIDER", "").lower()
        if default_provider:
            if manager.validate_provider_name(default_provider):
                status = "✅" if default_provider in available else "❌ (not available)"
                console.print(f"\n[bold]Default Provider:[/bold] {default_provider} {status}")
            else:
                console.print(f"\n[bold red]Invalid Default Provider:[/bold red] {default_provider}")
        else:
            console.print(f"\n[dim]No default provider set in .env file[/dim]")
            
    except Exception as e:
        console.print(f"[red]❌ Error listing providers: {e}[/red]")