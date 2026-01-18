# Telegram Setup

## Create a Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Enter a display name (e.g., "My Gru Bot")
4. Enter a username ending in `bot` (e.g., "my_gru_bot")
5. Copy the token:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

**Optional:** Send `/setprivacy` to @BotFather, select your bot, choose "Disable" to let it read group messages.

## Get Your User ID

1. Search for **@userinfobot** in Telegram
2. Send any message
3. Copy the ID number it returns

Multiple admins: separate IDs with commas (e.g., `123456789,987654321`)

## Environment Variables

```bash
GRU_TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GRU_ADMIN_IDS=123456789
```

## Troubleshooting

**Bot not responding:**
- Verify `GRU_ADMIN_IDS` matches your user ID exactly
- Check `GRU_TELEGRAM_TOKEN` has no extra spaces
- Restart Gru

[Back to README](../README.md)
