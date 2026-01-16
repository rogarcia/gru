# Gru

[![CI](https://github.com/zscole/gru/actions/workflows/ci.yml/badge.svg)](https://github.com/zscole/gru/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Self-hosted AI agent orchestration service controlled via Telegram or Discord.

Gru lets you spawn, manage, and interact with Claude-powered AI agents from your phone. Agents can execute bash commands, read/write files, and work autonomously on tasks. Think of it as having a coding assistant you can text from anywhere.

## Quick Start

1. Get your API keys (see [Prerequisites](#prerequisites) below)
2. Clone and install Gru
3. Create your `.env` file with your keys
4. Run `PYTHONPATH=src python -m gru.main`
5. Open Telegram or Discord and message your bot

That's it. You can now spawn AI agents from your phone or desktop.

---

## Prerequisites

You'll need these things before starting:

1. **Python 3.10 or higher**
2. **A bot token** (Telegram and/or Discord)
3. **Your user ID** (for the platform(s) you're using)
4. **An Anthropic API Key**

You can use Telegram, Discord, or both simultaneously. Don't worry if you don't have these yet. Follow the steps below.

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

## Telegram Setup

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

## Discord Setup

### Step 4: Create a Discord Bot

You need to create a bot in the Discord Developer Portal. This is free.

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application**
3. Give it a name (e.g., "Gru") and click **Create**
4. Go to the **Bot** tab in the left sidebar
5. Click **Reset Token** to generate a bot token
6. Copy the token. It looks like:
   ```
   your-bot-token-here
   ```
7. **Save this token.** You'll need it for your `.env` file.

**Important Bot Settings:**
- Under **Privileged Gateway Intents**, enable **Message Content Intent**
- This allows the bot to read message content for natural language commands

**Invite the bot to your server:**

1. Go to the **OAuth2** tab, then **URL Generator**
2. Under **Scopes**, select `bot` and `applications.commands`
3. Under **Bot Permissions**, select:
   - Send Messages
   - Send Messages in Threads
   - Embed Links
   - Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and click **Authorize**

---

### Step 5: Get Your Discord User ID

Gru only responds to authorized users. You need your Discord user ID (a number).

1. Open Discord
2. Go to **User Settings** (gear icon)
3. Go to **Advanced** and enable **Developer Mode**
4. Close settings
5. Right-click on your username anywhere in Discord
6. Click **Copy User ID**
7. **Save this number.** You'll need it for your `.env` file.

**Want to add multiple admins?** You can add multiple user IDs separated by commas (e.g., `123456789012345678,987654321098765432`).

---

## API Key

### Step 6: Get an Anthropic API Key

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
# Required - Anthropic API key
ANTHROPIC_API_KEY=paste_your_anthropic_key_here

# Telegram (optional if using Discord)
GRU_TELEGRAM_TOKEN=paste_your_telegram_bot_token_here
GRU_ADMIN_IDS=paste_your_telegram_user_id_here

# Discord (optional if using Telegram)
GRU_DISCORD_TOKEN=paste_your_discord_bot_token_here
GRU_DISCORD_ADMIN_IDS=paste_your_discord_user_id_here
GRU_DISCORD_GUILD_ID=optional_server_id_to_restrict_to

# Optional - defaults work fine for most users
GRU_MASTER_PASSWORD=pick_any_password_for_encrypting_secrets
GRU_DATA_DIR=~/.gru
GRU_WORKDIR=~/gru-workspace
GRU_DEFAULT_MODEL=claude-sonnet-4-20250514
GRU_MAX_TOKENS=8192
GRU_DEFAULT_TIMEOUT=300
GRU_MAX_AGENTS=10
```

**Example with Telegram only:**

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GRU_TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GRU_ADMIN_IDS=123456789
```

**Example with Discord only:**

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GRU_DISCORD_TOKEN=your-discord-bot-token
GRU_DISCORD_ADMIN_IDS=123456789012345678
```

**Example with both:**

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GRU_TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GRU_ADMIN_IDS=123456789
GRU_DISCORD_TOKEN=your-discord-bot-token
GRU_DISCORD_ADMIN_IDS=123456789012345678
```

### Configuration Options Explained

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `GRU_TELEGRAM_TOKEN` | If using Telegram | Your bot token from @BotFather |
| `GRU_ADMIN_IDS` | If using Telegram | Your Telegram user ID(s), comma-separated |
| `GRU_DISCORD_TOKEN` | If using Discord | Your bot token from Discord Developer Portal |
| `GRU_DISCORD_ADMIN_IDS` | If using Discord | Your Discord user ID(s), comma-separated |
| `GRU_DISCORD_GUILD_ID` | No | Restrict bot to a specific Discord server |
| `GRU_MASTER_PASSWORD` | No | Password for encrypting stored secrets |
| `GRU_DATA_DIR` | No | Where Gru stores its database (default: `~/.gru`) |
| `GRU_WORKDIR` | No | Default directory for agents to work in (default: `~/gru-workspace`) |
| `GRU_DEFAULT_MODEL` | No | Claude model to use (default: `claude-sonnet-4-20250514`) |
| `GRU_MAX_TOKENS` | No | Max tokens per response (default: `8192`) |
| `GRU_DEFAULT_TIMEOUT` | No | Agent timeout in seconds (default: `300`) |
| `GRU_MAX_AGENTS` | No | Max concurrent agents (default: `10`) |

**Note:** You must configure at least one bot interface (Telegram or Discord). You can use both simultaneously.

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
Telegram admin IDs: [123456789]
Discord admin IDs: [123456789012345678]
```

If you have MCP servers configured (optional), you'll also see:

```
MCP server 'filesystem' started with 14 tools
Started 1 MCP server(s)
```

**Now open Telegram or Discord and send a message to your bot!**

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

Commands work the same on both Telegram and Discord. On Telegram, use `/gru <command>`. On Discord, use slash commands `/gru <command>`.

#### Telegram Commands

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

#### Discord Commands

Discord uses slash commands. Type `/gru` and Discord will show available subcommands:

**Spawning Agents:**
```
/gru spawn task:<task>
/gru spawn task:<task> mode:unsupervised
/gru spawn task:<task> mode:oneshot
/gru spawn task:<task> workdir:/path priority:high
```

**Managing Agents:**
```
/gru status
/gru status agent_id:<id>
/gru list
/gru list status:running
/gru pause agent_id:<id>
/gru resume agent_id:<id>
/gru terminate agent_id:<id>
/gru nudge agent_id:<id> message:<text>
/gru logs agent_id:<id>
```

**Approvals (supervised mode):**
```
/gru pending
/gru approve approval_id:<id>
/gru reject approval_id:<id>
```

**Secrets:**
```
/gru secret_set key:<KEY> value:<value>
/gru secret_get key:<KEY>
/gru secret_list
/gru secret_delete key:<KEY>
```

**Templates:**
```
/gru template_save name:<name> task:<task>
/gru template_list
/gru template_use name:<name>
/gru template_delete name:<name>
```

**Discord-specific features:**
- Approval requests appear with clickable Approve/Reject buttons
- Multi-option approvals show numbered option buttons
- Natural language works in any channel the bot can see

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

**Telegram:**
1. **Check your user ID**: Make sure `GRU_ADMIN_IDS` in `.env` matches your Telegram user ID exactly
2. **Check the token**: Make sure `GRU_TELEGRAM_TOKEN` is correct (no extra spaces)
3. **Check Gru is running**: Look at the terminal for errors
4. **Restart Gru**: Stop it (Ctrl+C) and start again

**Discord:**
1. **Check your user ID**: Make sure `GRU_DISCORD_ADMIN_IDS` matches your Discord user ID
2. **Check the token**: Make sure `GRU_DISCORD_TOKEN` is correct
3. **Check Message Content Intent**: Enable it in Discord Developer Portal > Bot settings
4. **Check bot permissions**: Bot needs Send Messages and Read Message History
5. **Check slash commands**: Type `/gru` - if no commands appear, the bot may need to be re-invited

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
Telegram Bot --+
               +--> Orchestrator <-> Claude API
Discord Bot  --+         |
                         +-> Scheduler (priority queue)
                         +-> Database (SQLite)
                         +-> MCP Client (plugin tools)
                         +-> Secret Store (encrypted)
```

Both bots share the same orchestrator. You can run one or both simultaneously.

**Components:**

| File | Purpose |
|------|---------|
| `telegram_bot.py` | Telegram interface, command parsing |
| `discord_bot.py` | Discord interface, slash commands |
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
