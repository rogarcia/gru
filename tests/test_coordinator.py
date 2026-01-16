"""Tests for agent coordinator."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from gru.coordinator import Coordinator
from gru.db import Database


@pytest.fixture
async def db():
    """Create temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        database = Database(db_path)
        await database.connect()
        yield database
        await database.close()


@pytest.fixture
async def coordinator(db):
    """Create coordinator with database."""
    return Coordinator(db)


@pytest.fixture
async def agents(db):
    """Create test agents."""
    agent1 = await db.create_agent(
        agent_id="agent1",
        task="Task 1",
        model="test-model",
        name="Agent One",
    )
    agent2 = await db.create_agent(
        agent_id="agent2",
        task="Task 2",
        model="test-model",
        name="Agent Two",
    )
    return agent1, agent2


@pytest.mark.asyncio
async def test_send_message(coordinator, agents):
    """Test sending a message between agents."""
    message_id = await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Hello agent2!",
        message_type="info",
    )

    assert message_id is not None
    assert len(message_id) == 8  # UUID prefix


@pytest.mark.asyncio
async def test_send_message_with_metadata(coordinator, agents):
    """Test sending a message with metadata."""
    metadata = {"priority": "high", "retry_count": 0}
    await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Important message",
        metadata=metadata,
    )

    messages = await coordinator.get_messages("agent2")
    assert len(messages) == 1
    assert messages[0]["metadata"] == metadata


@pytest.mark.asyncio
async def test_send_message_with_task_id(coordinator, agents, db):
    """Test sending a message with task ID."""
    await db.create_task(task_id="task1", agent_id="agent1")

    await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Task update",
        task_id="task1",
    )

    messages = await coordinator.get_messages("agent2")
    assert messages[0]["task_id"] == "task1"


@pytest.mark.asyncio
async def test_get_messages_unread_only(coordinator, agents):
    """Test getting unread messages only."""
    await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Message 1",
    )
    await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Message 2",
    )

    # Mark first message as read
    messages = await coordinator.get_messages("agent2", unread_only=True)
    await coordinator.mark_read(messages[0]["id"])

    # Should only get unread message
    unread = await coordinator.get_messages("agent2", unread_only=True)
    assert len(unread) == 1
    assert unread[0]["content"] == "Message 2"


@pytest.mark.asyncio
async def test_get_messages_all(coordinator, agents):
    """Test getting all messages."""
    await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Message 1",
    )
    await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Message 2",
    )

    # Mark first as read
    messages = await coordinator.get_messages("agent2", unread_only=True)
    await coordinator.mark_read(messages[0]["id"])

    # Get all messages
    all_messages = await coordinator.get_messages("agent2", unread_only=False)
    assert len(all_messages) == 2


@pytest.mark.asyncio
async def test_mark_read(coordinator, agents):
    """Test marking a message as read."""
    await coordinator.send_message(
        from_agent="agent1",
        to_agent="agent2",
        content="Read me",
    )

    messages = await coordinator.get_messages("agent2", unread_only=True)
    assert len(messages) == 1

    await coordinator.mark_read(messages[0]["id"])

    unread = await coordinator.get_messages("agent2", unread_only=True)
    assert len(unread) == 0


@pytest.mark.asyncio
async def test_broadcast(coordinator, db):
    """Test broadcasting message to all agents on a task."""
    # Create agents
    await db.create_agent(agent_id="sender", task="Main", model="test")
    await db.create_agent(agent_id="receiver1", task="Sub 1", model="test")
    await db.create_agent(agent_id="receiver2", task="Sub 2", model="test")

    # Create parent task and subtasks
    await db.create_task(task_id="main_task", agent_id="sender")
    await db.create_task(task_id="sub_task1", agent_id="receiver1", parent_task_id="main_task")
    await db.create_task(task_id="sub_task2", agent_id="receiver2", parent_task_id="main_task")

    # Broadcast from sender
    msg_ids = await coordinator.broadcast(
        from_agent="sender",
        content="Update for all",
        task_id="main_task",
    )

    assert len(msg_ids) == 2

    # Check receivers got messages
    messages1 = await coordinator.get_messages("receiver1")
    messages2 = await coordinator.get_messages("receiver2")
    assert len(messages1) == 1
    assert len(messages2) == 1
    assert messages1[0]["content"] == "Update for all"


@pytest.mark.asyncio
async def test_broadcast_with_exclude(coordinator, db):
    """Test broadcasting with exclusions."""
    await db.create_agent(agent_id="sender", task="Main", model="test")
    await db.create_agent(agent_id="receiver1", task="Sub 1", model="test")
    await db.create_agent(agent_id="receiver2", task="Sub 2", model="test")

    await db.create_task(task_id="main_task", agent_id="sender")
    await db.create_task(task_id="sub_task1", agent_id="receiver1", parent_task_id="main_task")
    await db.create_task(task_id="sub_task2", agent_id="receiver2", parent_task_id="main_task")

    # Broadcast excluding receiver1
    msg_ids = await coordinator.broadcast(
        from_agent="sender",
        content="Not for receiver1",
        task_id="main_task",
        exclude=["receiver1"],
    )

    assert len(msg_ids) == 1

    messages1 = await coordinator.get_messages("receiver1")
    messages2 = await coordinator.get_messages("receiver2")
    assert len(messages1) == 0
    assert len(messages2) == 1


@pytest.mark.asyncio
async def test_request_handoff(coordinator, agents, db):
    """Test requesting a task handoff."""
    await db.create_task(task_id="task1", agent_id="agent1")

    context = {"progress": "50%", "remaining_work": ["item1", "item2"]}
    await coordinator.request_handoff(
        from_agent="agent1",
        to_agent="agent2",
        task_id="task1",
        context=context,
    )

    messages = await coordinator.get_messages("agent2")
    assert len(messages) == 1
    assert messages[0]["message_type"] == "handoff"
    assert "Handoff request" in messages[0]["content"]
    assert messages[0]["metadata"] == context


@pytest.mark.asyncio
async def test_set_and_get_context(coordinator, db):
    """Test setting and getting shared context."""
    await db.create_agent(agent_id="agent1", task="Task", model="test")
    await db.create_task(task_id="task1", agent_id="agent1")

    await coordinator.set_context(
        task_id="task1",
        key="result",
        value={"status": "complete", "output": 42},
        agent_id="agent1",
    )

    context = await coordinator.get_context("task1")
    assert context["result"] == {"status": "complete", "output": 42}


@pytest.mark.asyncio
async def test_get_context_specific_key(coordinator, db):
    """Test getting a specific context key."""
    await db.create_agent(agent_id="agent1", task="Task", model="test")
    await db.create_task(task_id="task1", agent_id="agent1")

    await coordinator.set_context("task1", "key1", "value1", "agent1")
    await coordinator.set_context("task1", "key2", "value2", "agent1")

    value = await coordinator.get_context("task1", key="key1")
    assert value == "value1"


@pytest.mark.asyncio
async def test_get_context_missing_key(coordinator, db):
    """Test getting a missing context key."""
    await db.create_agent(agent_id="agent1", task="Task", model="test")
    await db.create_task(task_id="task1", agent_id="agent1")

    value = await coordinator.get_context("task1", key="nonexistent")
    assert value is None


@pytest.mark.asyncio
async def test_resolve_agent_by_id(coordinator, agents):
    """Test resolving agent by ID."""
    resolved = await coordinator.resolve_agent("agent1")
    assert resolved == "agent1"


@pytest.mark.asyncio
async def test_resolve_agent_by_name(coordinator, agents):
    """Test resolving agent by name."""
    resolved = await coordinator.resolve_agent("Agent One")
    assert resolved == "agent1"


@pytest.mark.asyncio
async def test_resolve_agent_nonexistent(coordinator, agents):
    """Test resolving nonexistent agent."""
    resolved = await coordinator.resolve_agent("nonexistent")
    assert resolved is None


@pytest.mark.asyncio
async def test_resolve_agent_inactive(coordinator, db):
    """Test that completed/failed agents are not resolved by name."""
    await db.create_agent(
        agent_id="completed_agent",
        task="Done",
        model="test",
        name="Completed Agent",
    )
    await db.update_agent("completed_agent", status="completed")

    # Should not resolve by name
    resolved = await coordinator.resolve_agent("Completed Agent")
    assert resolved is None

    # But should still resolve by ID
    resolved = await coordinator.resolve_agent("completed_agent")
    assert resolved == "completed_agent"


@pytest.mark.asyncio
async def test_message_types(coordinator, agents):
    """Test different message types."""
    for msg_type in ["request", "response", "info", "handoff"]:
        await coordinator.send_message(
            from_agent="agent1",
            to_agent="agent2",
            content=f"Message type: {msg_type}",
            message_type=msg_type,
        )

    messages = await coordinator.get_messages("agent2", unread_only=False)
    types = [m["message_type"] for m in messages]
    assert "request" in types
    assert "response" in types
    assert "info" in types
    assert "handoff" in types
