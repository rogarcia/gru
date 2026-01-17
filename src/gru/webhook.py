"""Webhook server for external integrations (Vercel, GitHub, etc.)."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from typing import TYPE_CHECKING

from aiohttp import web

if TYPE_CHECKING:
    from gru.config import Config
    from gru.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


class WebhookServer:
    """HTTP server for receiving webhooks."""

    def __init__(self, config: Config, orchestrator: Orchestrator) -> None:
        self.config = config
        self.orchestrator = orchestrator
        self._app = web.Application()
        self._runner: web.AppRunner | None = None
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up webhook routes."""
        self._app.router.add_post("/webhook/vercel", self._handle_vercel)
        self._app.router.add_get("/health", self._handle_health)

    async def _handle_health(self, request: web.Request) -> web.Response:
        """Health check endpoint."""
        return web.json_response({"status": "ok"})

    async def _handle_vercel(self, request: web.Request) -> web.Response:
        """Handle Vercel deployment webhooks."""
        # Verify signature if secret is configured
        if self.config.webhook_secret:
            signature = request.headers.get("x-vercel-signature", "")
            body = await request.read()
            expected = hmac.new(
                self.config.webhook_secret.encode(),
                body,
                hashlib.sha1,
            ).hexdigest()
            if not hmac.compare_digest(signature, expected):
                logger.warning("Invalid Vercel webhook signature")
                return web.json_response({"error": "Invalid signature"}, status=401)
        else:
            body = await request.read()

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)

        # Extract deployment info
        event_type = payload.get("type", "")
        deployment = payload.get("payload", {})

        # Get branch from git metadata
        branch = deployment.get("deployment", {}).get("meta", {}).get("githubCommitRef", "")
        preview_url = deployment.get("deployment", {}).get("url", "")
        state = deployment.get("deployment", {}).get("state", "")

        # Match branch to agent (gru-agent-{id})
        agent_id = None
        if branch.startswith("gru-agent-"):
            agent_id = branch[len("gru-agent-") :]

        logger.info(f"Vercel webhook: {event_type} branch={branch} url={preview_url} state={state}")

        # Notify on deployment success
        if event_type == "deployment.succeeded" and agent_id and preview_url:
            # Ensure https prefix
            if not preview_url.startswith("http"):
                preview_url = f"https://{preview_url}"

            await self.orchestrator.notify(
                agent_id,
                f"Preview ready: {preview_url}",
            )
            logger.info(f"Notified agent {agent_id} of preview: {preview_url}")

        elif event_type == "deployment.error" and agent_id:
            error = deployment.get("deployment", {}).get("errorMessage", "Unknown error")
            await self.orchestrator.notify(
                agent_id,
                f"Preview deployment failed: {error}",
            )

        return web.json_response({"status": "ok"})

    async def start(self) -> None:
        """Start the webhook server."""
        if not self.config.webhook_enabled:
            logger.info("Webhook server disabled")
            return

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, self.config.webhook_host, self.config.webhook_port)
        await site.start()
        logger.info(f"Webhook server started on {self.config.webhook_host}:{self.config.webhook_port}")

    async def stop(self) -> None:
        """Stop the webhook server."""
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
            logger.info("Webhook server stopped")
