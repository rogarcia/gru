# Slack Setup

## Create an App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** > **From scratch**
3. Name it and select your workspace

## Enable Socket Mode

1. Go to **Socket Mode** in sidebar
2. Toggle **Enable Socket Mode** ON
3. Create an App-Level Token with `connections:write` scope
4. Copy the `xapp-...` token (this is your `GRU_SLACK_APP_TOKEN`)

## Add Bot Permissions

Go to **OAuth & Permissions** > **Bot Token Scopes** and add:
- `chat:write`
- `commands`
- `im:history`
- `im:write`

## Create Slash Command

1. Go to **Slash Commands**
2. Click **Create New Command**
3. Command: `/gru`
4. Description: "Gru agent orchestrator"
5. Save

## Install to Workspace

1. Go to **Install App**
2. Click **Install to Workspace**
3. Copy the **Bot User OAuth Token** (`xoxb-...`)

## Get Your User ID

1. Click your profile picture in Slack
2. Click **Profile** > three dots menu > **Copy member ID**

## Environment Variables

```bash
GRU_SLACK_BOT_TOKEN=xoxb-xxxx-xxxx-xxxx
GRU_SLACK_APP_TOKEN=xapp-1-xxxx-xxxx
GRU_SLACK_ADMIN_IDS=U01ABC123DE
```

## Troubleshooting

**Bot not responding:**
- Verify both tokens are set (bot AND app token)
- Check Socket Mode is enabled
- Verify all scopes are added
- Reinstall app if permissions changed

[Back to README](../README.md)
