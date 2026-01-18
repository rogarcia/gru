# Webhooks (Vercel)

Gru can receive Vercel webhooks to notify agents when preview deployments are ready.

## How It Works

1. Agent pushes to branch `gru-agent-<agent_id>`
2. Vercel deploys as preview
3. Vercel sends webhook to Gru
4. Gru notifies the agent with preview URL

## Configuration

```bash
GRU_WEBHOOK_ENABLED=true
GRU_WEBHOOK_HOST=0.0.0.0
GRU_WEBHOOK_PORT=8080
GRU_WEBHOOK_SECRET=your-vercel-webhook-secret
```

## Vercel Setup

1. Go to Vercel project settings
2. Navigate to **Settings** > **Webhooks**
3. Add webhook: `http://your-server:8080/webhook/vercel`
4. Copy signing secret to `GRU_WEBHOOK_SECRET`

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook/vercel` | POST | Vercel deployment events |
| `/health` | GET | Health check (`{"status": "ok"}`) |

## Branch Naming

Agents must push to `gru-agent-<agent_id>` branches for webhook matching.

[Back to README](../README.md)
