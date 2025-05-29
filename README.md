# 🧠 Reflex - Terminal-Based AI Productivity Tracker

**Tagline**: "Reflect. Focus. Improve."

Reflex is a powerful CLI tool that tracks your tasks, focus sessions, and work logs. It uses AI to help you improve how you work over time — all from the terminal.

## ✨ Features

- 📋 **Task Management**: Add and track daily tasks
- ⏱️ **Focus Timer**: Pomodoro-style focus sessions with progress bars
- 📖 **Work Logging**: Keep detailed logs of your daily work
- 📊 **Daily Statistics**: View your productivity metrics
- 🤖 **AI Reviews**: Get personalized productivity insights from GPT
- 💾 **Local Storage**: All data stored locally in SQLite database

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd reflex
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up OpenAI API** (optional, for AI reviews):
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

4. **Install as CLI tool**:
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

### Basic Commands

#### 📋 Task Management
```bash
# Add a new task
reflex add "Write blog post about AI"

# List today's tasks
reflex list

# Complete a task (use ID from list)
reflex complete 1
```

#### ⏱️ Focus Sessions
```bash
# Start a 25-minute focus session (Pomodoro)
reflex start focus

# The timer shows a progress bar and can be stopped with Ctrl+C
```

#### 📖 Work Logging
```bash
# Log what you're working on
reflex log "Implemented user authentication system"

# Add detailed progress notes
reflex log "Fixed bug in payment processing - issue was with API timeout"
```

#### 📊 Daily Stats
```bash
# View today's productivity statistics
reflex stats
```

#### 🤖 AI Review
```bash
# Get AI-powered daily review and suggestions
reflex review
```

### Sample Workflow

Here's how a typical day might look:

```bash
# Morning: Plan your day
reflex add "Review pull requests"
reflex add "Write documentation"
reflex add "Team meeting at 2pm"

# Start working with focus
reflex start focus
# ... work for 25 minutes ...

# Log your progress
reflex log "Reviewed 3 PRs, found performance issue in auth module"

# Check your progress
reflex stats

# End of day: Get AI insights
reflex review
```

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
└────────────────────┴───────────────────────┘
```

### AI Review Example
```
🤖 AI Daily Review
┌─────────────────────────────────────────────────────────────────┐
│ Great productivity today! You maintained excellent focus with 4  │
│ sessions totaling 85 minutes. Your task completion rate is      │
│ strong at 75%.                                                  │
│                                                                 │
│ What went well:                                                 │
│ • Consistent focus sessions throughout the day                  │
│ • Good documentation of progress in logs                        │
│                                                                 │
│ Tomorrow's suggestions:                                         │
│ • Try to complete that pending task first thing                 │
│ • Consider slightly longer focus sessions (30-35 min)          │
│ • Keep up the detailed logging - it shows great self-awareness │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technical Details

### Architecture
- **CLI Framework**: Typer (elegant, type-hinted CLI)
- **UI**: Rich (beautiful terminal formatting)
- **Database**: SQLite (local, no setup required)
- **AI**: OpenAI GPT-3.5-turbo
- **Configuration**: python-dotenv

### Data Storage
All data is stored locally in `~/.reflex/reflex.db`. Your data never leaves your machine unless you explicitly use the AI review feature.

### Database Schema
- **tasks**: id, task, completed, date_added, date_completed
- **focus_sessions**: id, duration, date, timestamp
- **logs**: id, entry, date, timestamp

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Required for AI reviews
OPENAI_API_KEY=your_openai_api_key_here
```

### Custom Focus Duration
The default focus session is 25 minutes (Pomodoro). You can modify this in `tracker/focus.py`.

## 🚀 Advanced Features

### Without AI (Works Offline)
Reflex works perfectly without an OpenAI API key. The `reflex review` command will provide basic statistical analysis instead of AI insights.

### Data Export
Your SQLite database can be easily queried or exported:
```bash
# View database location
ls ~/.reflex/

# Query with sqlite3
sqlite3 ~/.reflex/reflex.db "SELECT * FROM tasks WHERE date_added = date('now');"
```

## 🤝 Contributing

This is an MVP implementation. Some ideas for extensions:

### Planned Features
- 🗓️ **Weekly/Monthly Reports**: Longer-term productivity analysis
- 📈 **Productivity Trends**: Charts and graphs of your progress
- 🔗 **GitHub Integration**: Automatically track commits
- 📤 **Export Options**: Markdown, CSV, or JSON exports
- ⚙️ **Custom Timers**: Different focus session lengths
- 🏷️ **Task Categories**: Tag and categorize your tasks
- 📱 **Cross-platform**: Package as standalone executable

### Development Setup
```bash
# Clone and setup
git clone <repo>
cd reflex
pip install -r requirements.txt

# Run tests (when added)
pytest

# Build standalone executable (optional)
pip install pyinstaller
pyinstaller --onefile main.py
```

## 📝 License

MIT License - feel free to modify and distribute!

## 🙏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - Amazing CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [OpenAI](https://openai.com/) - AI-powered insights

---

**Start tracking your productivity today:**
```bash
reflex add "Build something amazing"
reflex start focus
```

*Reflect. Focus. Improve.* 🧠