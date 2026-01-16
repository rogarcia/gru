# Gru

[![CI](https://github.com/zscole/gru/actions/workflows/ci.yml/badge.svg)](https://github.com/zscole/gru/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Self-hosted AI agent orchestration service controlled via Telegram.

Gru lets you spawn, manage, and interact with Claude-powered AI agents from your phone. Agents can execute bash commands, read/write files, and work autonomously on tasks. Think of it as having a coding assistant you can text from anywhere.

## Quick Start

1. Get your API keys (see [Prerequisites](#prerequisites) below)
2. Clone and install Gru
3. Create your `.env` file with your keys
4. Run `PYTHONPATH=src python -m gru.main`
5. Open Telegram and message your bot

That's it. You can now spawn AI agents from your phone.

---

## Prerequisites

You'll need four things before starting:

1. **Python 3.10 or higher**
2. **A Telegram Bot Token**
3. **Your Telegram User ID**
4. **An Anthropic API Key**

Don't worry if you don't have these yet. Follow the steps below.

---

### Step 1: Install Python

**Check if you already have Python:**

Open your terminal (Terminal on Mac, Command Prompt on Windows) and type:

```bash
python3 --version
```

If you see `Python 3.10` or higher, you're good. Skip to Step 2.

**If you need to install Python:**

- **Mac**: Install [Homebrew](https://brew.sh) first, then run:
  ```bash
  brew install python@3.11
  ```

- **Windows**: Download from [python.org/downloads](https://www.python.org/downloads/). During installation, check "Add Python to PATH".

- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv
  ```

---

### Step 2: Create a Telegram Bot

You need to create a bot on Telegram. This is free and takes 2 minutes.

1. Open Telegram on your phone or desktop
2. Search for **@BotFather** (the official Telegram bot for creating bots)
3. Start a chat and send: `/newbot`
4. BotFather will ask for a **name** for your bot. This is the display name (e.g., "My Gru Bot")
5. BotFather will ask for a **username**. This must end in `bot` (e.g., "my_gru_bot")
6. BotFather will give you a **token** that looks like this:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
7. **Save this token.** You'll need it for your `.env` file.

**Optional but recommended:** Send `/setprivacy` to @BotFather, select your bot, and choose "Disable". This lets your bot read all messages in groups (if you want to use it in groups later).

---

### Step 3: Get Your Telegram User ID

Gru only responds to authorized users. You need your Telegram user ID (a number, not your username).

1. Open Telegram
2. Search for **@userinfobot**
3. Start a chat and send any message
4. The bot will reply with your user ID:
   ```
   Id: 123456789
   ```
5. **Save this number.** You'll need it for your `.env` file.

**Want to add multiple admins?** You can add multiple user IDs separated by commas (e.g., `123456789,987654321`).

---

### Step 4: Get an Anthropic API Key

Gru uses Claude (made by Anthropic) as its AI brain. You need an API key.

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Go to **API Keys** in the left sidebar
4. Click **Create Key**
5. Give it a name (e.g., "Gru")
6. Copy the key. It looks like:
   ```
   sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
7. **Save this key.** You'll need it for your `.env` file.

**Note:** Anthropic API usage costs money. Check their [pricing page](https://www.anthropic.com/pricing). Claude Sonnet is recommended for a balance of capability and cost.

---

## Installation

Now that you have all your keys, let's install Gru.

### Option A: Standard Installation (Recommended)

Open your terminal and run these commands one at a time:

```bash
# 1. Clone the repository
git clone https://github.com/zscole/gru.git

# 2. Enter the directory
cd gru

# 3. Create a virtual environment (keeps dependencies isolated)
python3 -m venv .venv

# 4. Activate the virtual environment
source .venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
```

**Windows users:** Instead of `source .venv/bin/activate`, use:
```bash
.venv\Scripts\activate
```

### Option B: Docker Installation

If you have Docker installed, this is even easier:

```bash
# 1. Clone the repository
git clone https://github.com/zscole/gru.git
cd gru

# 2. Create your .env file (see next section)

# 3. Run with Docker Compose
docker-compose up -d
```

That's it. The bot will start automatically.

---

## Configuration

Create a file called `.env` in the `gru` folder. This file stores your secret keys.

**Easy way:** Copy the example file and edit it:

```bash
cp .env.example .env
```

Then open `.env` in any text editor and fill in your values.

**Manual way:** Create a new file called `.env` with this content:

```bash
# Required - you must fill these in
GRU_TELEGRAM_TOKEN=paste_your_bot_token_here
GRU_ADMIN_IDS=paste_your_user_id_here
ANTHROPIC_API_KEY=paste_your_anthropic_key_here

# Optional - defaults work fine for most users
GRU_MASTER_PASSWORD=pick_any_password_for_encrypting_secrets
GRU_DATA_DIR=~/.gru
GRU_WORKDIR=~/gru-workspace
GRU_DEFAULT_MODEL=claude-sonnet-4-20250514
GRU_MAX_TOKENS=8192
GRU_DEFAULT_TIMEOUT=300
GRU_MAX_AGENTS=10
```

**Example with real values (don't use these!):**

```bash
GRU_TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GRU_ADMIN_IDS=123456789
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GRU_MASTER_PASSWORD=my-super-secret-password-123
```

### Configuration Options Explained

| Variable | Required | Description |
|----------|----------|-------------|
| `GRU_TELEGRAM_TOKEN` | Yes | Your bot token from @BotFather |
| `GRU_ADMIN_IDS` | Yes | Your Telegram user ID(s), comma-separated |
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `GRU_MASTER_PASSWORD` | No | Password for encrypting stored secrets |
| `GRU_DATA_DIR` | No | Where Gru stores its database (default: `~/.gru`) |
| `GRU_WORKDIR` | No | Default directory for agents to work in (default: `~/gru-workspace`) |
| `GRU_DEFAULT_MODEL` | No | Claude model to use (default: `claude-sonnet-4-20250514`) |
| `GRU_MAX_TOKENS` | No | Max tokens per response (default: `8192`) |
| `GRU_DEFAULT_TIMEOUT` | No | Agent timeout in seconds (default: `300`) |
| `GRU_MAX_AGENTS` | No | Max concurrent agents (default: `10`) |

---

## Running Gru

### Standard Installation

Every time you want to run Gru:

```bash
# 1. Open terminal and go to the gru folder
cd gru

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Start Gru
PYTHONPATH=src python -m gru.main
```

**Windows users:** Use this instead:
```bash
set PYTHONPATH=src
python -m gru.main
```

### Docker Installation

```bash
docker-compose up -d
```

To stop: `docker-compose down`

To view logs: `docker-compose logs -f`

### What Success Looks Like

When Gru starts correctly, you'll see:

```
Gru server started
Data directory: /home/you/.gru
Admin IDs: [123456789]
```

If you have MCP servers configured (optional), you'll also see:

```
MCP server 'filesystem' started with 14 tools
Started 1 MCP server(s)
```

**Now open Telegram and send a message to your bot!**

---

## Using Gru

### Your First Agent

Open Telegram, find your bot, and try:

```
/gru spawn write a hello world python script
```

The agent will:
1. Start working on your task
2. Ask for approval before writing files (supervised mode)
3. Send you the result when done

### Talk Naturally

You don't have to use commands. Just chat:

```
build me a simple todo app in python
```

```
what files are in my workspace?
```

```
check on my agents
```

Gru understands what you want and either spawns an agent or answers directly.

### Commands Reference

All commands start with `/gru`:

**Spawning Agents:**
```
/gru spawn <task>                  Start an agent (supervised mode)
/gru spawn <task> --unsupervised   No approval needed
/gru spawn <task> --oneshot        Fire and forget
/gru spawn <task> --workdir /path  Work in specific directory
/gru spawn <task> --priority high  Set priority (high/normal/low)
```

**Managing Agents:**
```
/gru status                        Show overall status
/gru status <agent_id>             Show specific agent
/gru list                          List all agents
/gru list running                  Filter by status
/gru pause <agent_id>              Pause an agent
/gru resume <agent_id>             Resume an agent
/gru terminate <agent_id>          Stop an agent
/gru nudge <agent_id> <message>    Send a message to an agent
/gru logs <agent_id>               View conversation history
```

**Approvals (supervised mode):**
```
/gru pending                       List pending approvals
/gru approve <approval_id>         Approve an action
/gru reject <approval_id>          Reject an action
```

**Secrets (encrypted storage):**
```
/gru secret set KEY value          Store a secret
/gru secret get KEY                Retrieve a secret
/gru secret list                   List all secret keys
/gru secret delete KEY             Delete a secret
```

**Templates:**
```
/gru template save <name> <task>   Save a task template
/gru template list                 List all templates
/gru template use <name>           Spawn from template
/gru template delete <name>        Delete a template
```

### Execution Modes Explained

**Supervised (default):**
- Agent asks permission before running commands or writing files
- You get Telegram buttons to Approve or Reject
- Safest mode, recommended for beginners

**Unsupervised:**
- Agent runs without asking permission
- Use when you trust the task
- Add `--unsupervised` flag

**Oneshot:**
- Fire and forget
- Agent runs to completion without any interaction
- Results are sent when done
- Add `--oneshot` flag

---

## MCP Plugins (Optional)

MCP (Model Context Protocol) lets you extend Gru with additional tools. This is optional but powerful.

### Setup

1. Install Node.js if you don't have it: [nodejs.org](https://nodejs.org)

2. Create `mcp_servers.json` in the gru folder:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your/files"],
      "env": {}
    }
  }
}
```

3. Restart Gru

### Popular MCP Servers

| Server | What it does |
|--------|--------------|
| `@modelcontextprotocol/server-filesystem` | Advanced file operations |
| `@modelcontextprotocol/server-github` | GitHub integration |
| `@modelcontextprotocol/server-postgres` | PostgreSQL database |
| `@modelcontextprotocol/server-puppeteer` | Browser automation |

See [MCP Servers](https://github.com/modelcontextprotocol/servers) for more.

---

## Troubleshooting

### Bot not responding

1. **Check your user ID**: Make sure `GRU_ADMIN_IDS` in `.env` matches your Telegram user ID exactly
2. **Check the token**: Make sure `GRU_TELEGRAM_TOKEN` is correct (no extra spaces)
3. **Check Gru is running**: Look at the terminal for errors
4. **Restart Gru**: Stop it (Ctrl+C) and start again

### "Command not found: python3"

- Make sure Python is installed (see [Step 1](#step-1-install-python))
- On Windows, try `python` instead of `python3`

### "No module named 'gru'"

Make sure you're running with `PYTHONPATH=src`:

```bash
PYTHONPATH=src python -m gru.main
```

### Agent seems stuck

Try these in order:

1. Send a nudge: `/gru nudge <agent_id> hurry up`
2. Check status: `/gru status <agent_id>`
3. Terminate: `/gru terminate <agent_id>`

### Approvals not appearing

- Make sure you're in supervised mode (the default)
- Check Telegram notifications are enabled
- Try `/gru pending` to see if approvals are queued

### API errors

- **"Invalid API key"**: Check `ANTHROPIC_API_KEY` is correct
- **"Rate limited"**: You're sending too many requests, wait a bit
- **"Insufficient credits"**: Add credits at [console.anthropic.com](https://console.anthropic.com)

### Docker issues

- **Port conflict**: Another service is using the same port
- **Container won't start**: Check logs with `docker-compose logs`
- **Permission denied**: Try `sudo docker-compose up -d`

---

## Security Notes

- **Only admins can use the bot**: Users not in `GRU_ADMIN_IDS` are ignored
- **Supervised mode is default for a reason**: Always start here
- **Agents run with your permissions**: They can do anything you can do
- **Use `GRU_WORKDIR`**: Isolate agents to a specific directory
- **Review MCP servers**: They can execute arbitrary code

---

## Architecture

```
Telegram Bot <-> Orchestrator <-> Claude API
                     |
                     +-> Scheduler (priority queue)
                     +-> Database (SQLite)
                     +-> MCP Client (plugin tools)
                     +-> Secret Store (encrypted)
```

**Components:**

| File | Purpose |
|------|---------|
| `telegram_bot.py` | Telegram interface, command parsing |
| `orchestrator.py` | Agent lifecycle, tool execution |
| `claude.py` | Claude API client |
| `scheduler.py` | Priority queue scheduling |
| `mcp.py` | MCP server management |
| `crypto.py` | Secret encryption |
| `db.py` | SQLite database |

---

## Development

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
PYTHONPATH=src pytest tests/ -v

# Lint
ruff check src/ tests/

# Format
ruff format src/ tests/

# Type check
mypy src/
```

---

## License

MIT - see [LICENSE](LICENSE)
