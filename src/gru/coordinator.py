"""Agent coordination for message passing and shared context."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gru.db import Database


class Coordinator:
    """Coordinates communication between agents."""

    def __init__(self, db: Database) -> None:
        self.db = db

    async def send_message(
        self,
        from_agent: str | None,
        to_agent: str | None,
        content: str,
        message_type: str = "info",
        task_id: str | None = None,
        metadata: dict | None = None,
    ) -> str:
        """Send a message from one agent to another."""
        message_id = str(uuid.uuid4())[:8]
        await self.db.send_agent_message(
            message_id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            task_id=task_id,
            message_type=message_type,
            content=content,
            metadata=metadata,
        )
        return message_id

    async def get_messages(
        self,
        agent_id: str,
        unread_only: bool = True,
    ) -> list[dict[str, Any]]:
        """Get messages for an agent."""
        return await self.db.get_agent_messages(agent_id, unread_only)

    async def mark_read(self, message_id: str) -> None:
        """Mark a message as read."""
        await self.db.mark_message_read(message_id)

    async def broadcast(
        self,
        from_agent: str,
        content: str,
        task_id: str,
        exclude: list[str] | None = None,
    ) -> list[str]:
        """Broadcast a message to all agents on a task."""
        exclude = exclude or []
        # Get all agents for the task
        tasks = await self.db.fetchall(
            "SELECT DISTINCT agent_id FROM tasks WHERE id = ? OR parent_task_id = ?",
            (task_id, task_id),
        )
        message_ids = []
        for task in tasks:
            agent_id = task["agent_id"]
            if agent_id != from_agent and agent_id not in exclude:
                msg_id = await self.send_message(
                    from_agent=from_agent,
                    to_agent=agent_id,
                    content=content,
                    message_type="info",
                    task_id=task_id,
                )
                message_ids.append(msg_id)
        return message_ids

    async def request_handoff(
        self,
        from_agent: str,
        to_agent: str,
        task_id: str,
        context: dict[str, Any],
    ) -> str:
        """Request a task handoff to another agent."""
        return await self.send_message(
            from_agent=from_agent,
            to_agent=to_agent,
            content=f"Handoff request for task {task_id}",
            message_type="handoff",
            task_id=task_id,
            metadata=context,
        )

    async def set_context(
        self,
        task_id: str,
        key: str,
        value: Any,
        agent_id: str,
    ) -> None:
        """Set a shared context value."""
        await self.db.set_shared_context(task_id, key, value, agent_id)

    async def get_context(self, task_id: str, key: str | None = None) -> Any:
        """Get shared context value(s)."""
        context = await self.db.get_shared_context(task_id)
        if key:
            return context.get(key)
        return context

    async def resolve_agent(self, identifier: str) -> str | None:
        """Resolve an agent name or ID to an agent ID."""
        # Try direct ID lookup
        agent = await self.db.get_agent(identifier)
        if agent:
            return agent["id"]
        # Try name lookup
        row = await self.db.fetchone(
            "SELECT id FROM agents WHERE name = ? AND status IN ('idle', 'running', 'paused')",
            (identifier,),
        )
        return row["id"] if row else None
