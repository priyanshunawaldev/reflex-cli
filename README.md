# 🧠 Reflex - AI-Powered Terminal Productivity Tracker

**Tagline**: "Reflect. Focus. Improve."

Reflex is a powerful CLI tool that tracks your tasks, focus sessions, and work logs with AI-powered insights to help you improve your productivity over time. Choose from multiple AI providers or run completely offline — all from your terminal.

## ✨ Features

- 📋 **Task Management** - Add, track, and complete daily tasks
- ⏱️ **Focus Timer** - Pomodoro-style focus sessions with progress bars
- 📖 **Work Logging** - Keep detailed logs of your daily work
- 📊 **Daily Statistics** - View comprehensive productivity metrics
- 🤖 **AI-Powered Reviews** - Smart insights from multiple AI providers
- 🔧 **Flexible AI Integration** - OpenAI, Anthropic Claude, Google Gemini, or local LLMs
- 🔗 **GitHub Integration** - Track your daily commits right in your terminal
- 💰 **Cost-Effective** - Optional local LLM support (completely free)
- 🔒 **Privacy-First** - All data stored locally, API keys never transmitted
- 🛡️ **Offline Mode** - Works perfectly without any AI provider

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/priyanshunawaldev/reflex-cli.git
cd reflex
pip install -r requirements.txt
```

### 2. Choose Your AI Provider (Optional)

**For OpenAI (GPT):**

```bash
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
echo "OPENAI_MODEL=gpt-3.5-turbo" >> .env
```

**For Anthropic (Claude):**

```bash
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env
echo "ANTHROPIC_MODEL=claude-3-haiku-20240307" >> .env
```

**For Google (Gemini):**

```bash
echo "GEMINI_API_KEY=your-key-here" >> .env
echo "GEMINI_MODEL=models/gemini-1.5-pro-latest" >> .env
```

**For Local LLM (Ollama - Free!):**

```bash
# Install Ollama: https://ollama.ai/
ollama serve
ollama pull llama2
echo "OLLAMA_MODEL=llama2" >> .env
```

**Set Default Provider:**

```bash
echo "DEFAULT_PROVIDER=gemini" >> .env  # or anthropic, openai, ollama
```

Now, based on details above, create the .env file.
(Find in Configuration below)

_[GitHub personal access token generate here](https://github.com/settings/tokens)_

I have added `.env.example` file for convenience. Just copy it from below, and then add your details.

**Simple `.env` Setup**

```bash
cp .env.example .env
```

### 3. Install as CLI Tool

```bash
pip install -e .
```

Now you can use `reflex` from anywhere in your terminal!

### Alternative: Direct Usage

If you don't want to install globally, run directly:

```bash
python main.py [command]
```

## 📖 Usage Guide

### Core Commands

| Command         | Description                         |
| --------------- | ----------------------------------- |
| `add "task"`    | 📋 Add a task to your current day   |
| `focus`         | ⏱️ Start a focus session with timer |
| `log "entry"`   | 📝 Add to your daily work log       |
| `complete <id>` | ✅ Mark a task as completed         |
| `list`          | 📋 List all tasks for today         |
| `stats`         | 📊 Show productivity statistics     |
| `review`        | 🤖 AI-powered daily review          |
| `providers`     | 🔧 List supported AI providers      |
| `track-commits` | 🔗 Track today's GitHub commits     |
| `help`          | 📚 Show help message                |
| `full-help`     | 📖 Show this detailed help          |

### AI Configuration

| Section             | Description                                             |
| ------------------- | ------------------------------------------------------- |
| **OPTIONS:**        |                                                         |
| `--provider`        | Specify AI provider (openai, anthropic, gemini, ollama) |
| `--model`           | Specify AI model name                                   |
| **SETUP:**          |                                                         |
| `.env keys`         | Set API keys in `.env` file                             |
| `OPENAI_API_KEY`    | Set OpenAI API key                                      |
| `ANTHROPIC_API_KEY` | Set Anthropic API key                                   |
| `GEMINI_API_KEY`    | Set Gemini API key                                      |

### Detailed Help Section.

```bash
reflex full-help

```

### Task Management

```bash
# Add a new task
reflex add "Write blog post about AI"

# List today's tasks
reflex list-tasks

# Complete a task (use ID from list)
reflex complete 1
```

### Focus Sessions

```bash
# Start a 25-minute focus session (Pomodoro)
reflex start-focus

# The timer shows a progress bar and can be stopped with Ctrl+C
```

### Work Logging & Tracking

```bash
# Log what you're working on
reflex log "Implemented user authentication system"

# Track today's GitHub commits
reflex track-commits

# View today's productivity statistics
reflex stats
```

### AI-Powered Reviews

```bash
# Use default AI provider
reflex review

# Use specific provider
reflex review --provider anthropic
reflex review --provider openai
reflex review --provider gemini
reflex review --provider ollama

# Use specific model
reflex review --provider openai --model gpt-4
reflex review --provider anthropic --model claude-3-sonnet-20240229

# List available providers
reflex providers
```

### Sample Daily Workflow

```bash
# Morning: Plan your day
reflex add "Review pull requests"
reflex add "Write documentation"
reflex add "Team meeting at 2pm"

# Start focused work
reflex start-focus
# ... work for 25 minutes ...

# Log your progress
reflex log "Reviewed 3 PRs, found performance issue in auth module"

# Check your commits
reflex track-commits

# Check your progress
reflex stats

# End of day: Get AI insights
reflex review
```

## 💡 AI Provider Comparison

| Provider             | Cost/Review | Speed  | Quality   | Local | Best For            |
| -------------------- | ----------- | ------ | --------- | ----- | ------------------- |
| **OpenAI GPT-3.5**   | ~$0.001     | Fast   | Good      | ❌    | General use         |
| **OpenAI GPT-4**     | ~$0.02      | Medium | Excellent | ❌    | Detailed insights   |
| **Anthropic Claude** | ~$0.005     | Fast   | Excellent | ❌    | Thoughtful analysis |
| **Google Gemini**    | ~$0.002     | Fast   | Good      | ❌    | Cost-effective      |
| **Ollama (Local)**   | Free        | Medium | Good      | ✅    | Privacy & offline   |

## 📊 Sample Output

### Daily Stats

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                Today's Productivity Stats                ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Tasks Completed    │ 3                     │
│ Tasks Pending      │ 1                     │
│ Focus Sessions     │ 4                     │
│ Total Focus Time   │ 85 minutes            │
│ Log Entries        │ 6                     │
│ Commits Made       │ 2                     │
└────────────────────┴───────────────────────┘
```

### AI Review Example

```
🤖 AI Daily Review (Claude - claude-3-haiku-20240307)
┌─────────────────────────────────────────────────────────────┐
│ Great progress today! You completed 3 out of 4 tasks and   │
│ maintained excellent focus with 4 sessions totaling 85     │
│ minutes. Your commit activity shows consistent development. │
│                                                             │
│ **What went well:**                                         │
│ • Consistent focus sessions show good time management       │
│ • High task completion rate (75%)                          │
│ • Regular logging demonstrates self-awareness               │
│ • Good commit frequency indicates steady progress           │
│                                                             │
│ **Areas for improvement:**                                  │
│ • One task remains pending - consider breaking it down     │
│ • Could benefit from shorter breaks between sessions       │
│                                                             │
│ **Tomorrow's suggestions:**                                 │
│ • Start with the pending task while energy is high        │
│ • Try 30-minute focus sessions for deeper work            │
│ • Set specific goals for each focus session                │
└─────────────────────────────────────────────────────────────┘
Tokens used: 187 | Cost: ~$0.003
```

## 🛠️ Technical Details

### Architecture

- **CLI Framework**: Typer (elegant, type-hinted CLI)
- **UI**: Rich (beautiful terminal formatting)
- **Database**: SQLite (local, no setup required)
- **AI Providers**: OpenAI, Anthropic, Google, Ollama
- **Configuration**: python-dotenv

### Data Storage

All data is stored locally in `~/.reflex/reflex.db`. Your data never leaves your machine unless you explicitly use AI review features.

### Database Schema

- **tasks**: id, task, completed, date_added, date_completed
- **focus_sessions**: id, duration, date, timestamp
- **logs**: id, entry, date, timestamp

## 🔧 Configuration

### Environment Variables (.env file)

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY="your_gemini_key_here"

# Optional: Specify models (will use defaults if not set)
OPENAI_MODEL=gpt-3.5-turbo
ANTHROPIC_MODEL=claude-3-haiku-20240307
GEMINI_MODEL=models/gemini-1.5-pro-latest
OLLAMA_MODEL=llama2

# Optional: Set default provider
DEFAULT_PROVIDER=gemini

GITHUB_USERNAME="your_github_username"
GITHUB_TOKEN="your_github_token"
```

### Custom Focus Duration

The default focus session is 25 minutes (Pomodoro). You can modify this in the configuration or source code.

## 🛡️ Security & Privacy

### Data Privacy

- **Local First**: All productivity data stored locally in SQLite
- **No Data Transmission**: Your tasks, logs, and stats never leave your machine
- **API Keys**: Stored locally in `.env` file, never transmitted to our servers
- **Offline Mode**: Full functionality without any AI provider

### Security Best Practices

1. **Never commit API keys** - Use `.env` files (git-ignored)
2. **Use environment variables** - Keep keys out of code
3. **Set usage limits** - Monitor costs on provider dashboards
4. **Rotate keys regularly** - Generate new keys periodically
5. **Local processing** - Use Ollama for maximum privacy

## 🚀 Advanced Features

### Offline Mode

Reflex works perfectly without any AI provider. The `reflex review` command will provide basic statistical analysis instead of AI insights.

### Data Export

Your SQLite database can be easily queried or exported:

```bash
# View database location
ls ~/.reflex/

# Query with sqlite3
sqlite3 ~/.reflex/reflex.db "SELECT * FROM tasks WHERE date_added = date('now');"
```

### AI Provider Issues

```bash
# Check available providers
reflex providers

# Test specific provider
reflex review --provider openai

# Verify environment variables
cat .env
```

### Common Issues

- **API Key Issues**: Check `.env` file format (no quotes, no spaces)
- **Ollama Issues**: Ensure `ollama serve` is running and model is pulled
- **Database Issues**: Check permissions on `~/.reflex/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Format code: `black . && isort .`
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with love using:

- [Typer](https://typer.tiangolo.com/) - Amazing CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [OpenAI](https://openai.com/) - GPT models for AI insights
- [Anthropic](https://anthropic.com/) - Claude models for thoughtful analysis
- [Google](https://ai.google.dev/) - Gemini models for cost-effective AI
- [Ollama](https://ollama.ai/) - Local LLM runtime for privacy

---

**Start tracking your productivity today:**

```bash
reflex add "Build something amazing"
reflex start-focus
reflex review
```

_Reflect. Focus. Improve._ 🧠

**Made with ❤️ for developers who want smarter productivity tracking**
