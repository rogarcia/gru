# Troubleshooting

## Bot Not Responding

**All platforms:**
- Check Gru is running (look for errors in terminal)
- Verify your user ID is in the admin list
- Restart Gru

**Telegram:**
- `GRU_ADMIN_IDS` must match your user ID exactly
- `GRU_TELEGRAM_TOKEN` must have no extra spaces

**Discord:**
- Enable **Message Content Intent** in Developer Portal > Bot
- Bot needs Send Messages and Read Message History permissions
- If slash commands don't appear, re-invite the bot

**Slack:**
- Both tokens required: `GRU_SLACK_BOT_TOKEN` AND `GRU_SLACK_APP_TOKEN`
- Socket Mode must be enabled
- Reinstall app if you changed permissions

## Common Errors

**"Command not found: python3"**
- Install Python from [python.org](https://www.python.org/downloads/)
- Windows: try `python` instead of `python3`

**"No module named 'gru'"**
- Run with: `PYTHONPATH=src python -m gru.main`

**"Invalid API key"**
- Check `ANTHROPIC_API_KEY` is correct

**"Rate limited"**
- Wait a moment, you're sending too many requests

**"Insufficient credits"**
- Add credits at [console.anthropic.com](https://console.anthropic.com)

## Agent Issues

**Agent seems stuck:**
1. Nudge it: `/gru nudge <id> hurry up`
2. Check status: `/gru status <id>`
3. Terminate: `/gru terminate <id>`

**Approvals not appearing:**
- Verify you're in supervised mode (default)
- Check notifications are enabled
- Try `/gru pending`

## Docker Issues

**Port conflict:**
- Another service using the port

**Container won't start:**
- Check logs: `docker-compose logs`

**Permission denied:**
- Try: `sudo docker-compose up -d`

## Health Check

Run `/gru doctor` for automated diagnostics:
- API key status
- Bot connection
- Git availability
- Database status

[Back to README](../README.md)
