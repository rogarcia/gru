# Commands Reference

Commands work the same across platforms. Telegram uses `/gru <command>`, Discord and Slack use the `/gru` slash command.

## Quick Start

| Command | Description |
|---------|-------------|
| `/gru examples` | Copy-paste example tasks |
| `/gru create <template>` | Create from template |
| `/gru doctor` | Health check |
| `/gru setup` | Guided setup help |

## Spawning Agents

```
/gru spawn <task>                  # Supervised mode (default)
/gru spawn <task> --unsupervised   # No approval needed
/gru spawn <task> --oneshot        # Fire and forget
/gru spawn <task> --workdir /path  # Specific directory
/gru spawn <task> --priority high  # Priority: high/normal/low
```

## Managing Agents

```
/gru status                  # Overall status
/gru status <id>             # Specific agent
/gru list                    # List all agents
/gru list running            # Filter by status
/gru pause <id>              # Pause agent
/gru resume <id>             # Resume agent
/gru terminate <id>          # Stop agent
/gru nudge <id> <message>    # Send message to agent
/gru logs <id>               # View conversation history
```

## Deploy

```
/gru deploy vercel    # Deploy to Vercel
/gru deploy netlify   # Deploy to Netlify
/gru deploy surge     # Deploy to Surge.sh
```

## Approvals (Supervised Mode)

```
/gru pending              # List pending approvals
/gru approve <id>         # Approve action
/gru reject <id>          # Reject action
```

## Secrets

```
/gru secret set KEY value   # Store encrypted secret
/gru secret get KEY         # Retrieve secret
/gru secret list            # List all keys
/gru secret delete KEY      # Delete secret
```

## Templates

```
/gru template save <name> <task>   # Save task template
/gru template list                 # List templates
/gru template use <name>           # Spawn from template
/gru template delete <name>        # Delete template
```

## Project Templates

| Template | Creates |
|----------|---------|
| `react-app` | React + TypeScript + Tailwind |
| `next-app` | Next.js 14 with app router |
| `express-api` | Express + TypeScript + JWT |
| `fastapi` | FastAPI + SQLAlchemy |
| `landing-page` | Responsive landing page |
| `cli-tool` | Python CLI with Click |
| `discord-bot` | Discord.py bot |
| `chrome-extension` | Chrome extension (MV3) |

Usage: `/gru create react-app` or `/gru create react-app --workdir /path`

## Execution Modes

**Supervised (default):** Agent asks permission before commands/file writes. Approve or reject via buttons.

**Unsupervised:** Agent runs without asking. Use `--unsupervised` flag.

**Oneshot:** Fire and forget. Results sent when done. Use `--oneshot` flag.

## Agent References

You can reference agents by:
- Full ID: `gru-agent-abc123`
- Number: `1`, `2`, etc. (assigned in order)
- Nickname: Set with `/gru nickname <id> <name>`

[Back to README](../README.md)
