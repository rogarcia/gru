# Discord Setup

## Create a Bot

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application**, name it, click **Create**
3. Go to **Bot** tab
4. Click **Reset Token** and copy it
5. Enable **Message Content Intent** under Privileged Gateway Intents

## Invite to Server

1. Go to **OAuth2** > **URL Generator**
2. Select scopes: `bot`, `applications.commands`
3. Select permissions: Send Messages, Send Messages in Threads, Embed Links, Read Message History
4. Open the generated URL and authorize

## Get Your User ID

1. Open Discord Settings > Advanced > Enable **Developer Mode**
2. Right-click your username anywhere
3. Click **Copy User ID**

Multiple admins: separate IDs with commas

## Environment Variables

```bash
GRU_DISCORD_TOKEN=your-bot-token
GRU_DISCORD_ADMIN_IDS=123456789012345678
GRU_DISCORD_GUILD_ID=optional-server-id  # Optional: restrict to one server
```

## Troubleshooting

**Bot not responding:**
- Verify Message Content Intent is enabled
- Check bot has Send Messages permission
- If `/gru` shows no commands, re-invite the bot

**Slash commands not appearing:**
- Remove and re-add the bot to refresh commands

[Back to README](../README.md)
