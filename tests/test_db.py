"""Tests for database layer."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from gru.db import Database


@pytest.fixture
async def db():
    """Create a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        database = Database(db_path)
        await database.connect()
        yield database
        await database.close()


@pytest.mark.asyncio
async def test_create_agent(db: Database):
    """Test agent creation."""
    agent = await db.create_agent(
        agent_id="test123",
        task="Test task",
        model="claude-sonnet-4-20250514",
        name="Test Agent",
        supervised=True,
        priority="normal",
    )

    assert agent["id"] == "test123"
    assert agent["task"] == "Test task"
    assert agent["status"] == "idle"
    assert agent["supervised"] == 1


@pytest.mark.asyncio
async def test_get_agent(db: Database):
    """Test agent retrieval."""
    await db.create_agent(
        agent_id="test123",
        task="Test task",
        model="claude-sonnet-4-20250514",
    )

    agent = await db.get_agent("test123")
    assert agent is not None
    assert agent["id"] == "test123"

    missing = await db.get_agent("nonexistent")
    assert missing is None


@pytest.mark.asyncio
async def test_update_agent(db: Database):
    """Test agent update."""
    await db.create_agent(
        agent_id="test123",
        task="Test task",
        model="claude-sonnet-4-20250514",
    )

    await db.update_agent("test123", status="running")

    agent = await db.get_agent("test123")
    assert agent["status"] == "running"


@pytest.mark.asyncio
async def test_create_task(db: Database):
    """Test task creation."""
    await db.create_agent(
        agent_id="agent1",
        task="Agent task",
        model="claude-sonnet-4-20250514",
    )

    task = await db.create_task(
        task_id="task123",
        agent_id="agent1",
        priority="high",
    )

    assert task["id"] == "task123"
    assert task["priority"] == "high"
    assert task["priority_score"] == 100


@pytest.mark.asyncio
async def test_conversation(db: Database):
    """Test conversation history."""
    await db.create_agent(
        agent_id="agent1",
        task="Agent task",
        model="claude-sonnet-4-20250514",
    )

    await db.add_message("agent1", "user", "Hello")
    await db.add_message("agent1", "assistant", "Hi there")

    conversation = await db.get_conversation("agent1")
    assert len(conversation) == 2
    assert conversation[0]["role"] == "user"
    assert conversation[1]["role"] == "assistant"


@pytest.mark.asyncio
async def test_secrets(db: Database):
    """Test secret storage."""
    await db.store_secret("api_key", b"encrypted", b"nonce123")

    result = await db.get_secret("api_key")
    assert result is not None
    assert result[0] == b"encrypted"
    assert result[1] == b"nonce123"

    keys = await db.list_secrets()
    assert "api_key" in keys

    deleted = await db.delete_secret("api_key")
    assert deleted

    result = await db.get_secret("api_key")
    assert result is None


@pytest.mark.asyncio
async def test_templates(db: Database):
    """Test template management."""
    await db.save_template(
        name="code_review",
        task="Review the code in {file}",
        priority="high",
    )

    template = await db.get_template("code_review")
    assert template is not None
    assert template["name"] == "code_review"
    assert template["priority"] == "high"

    templates = await db.list_templates()
    assert len(templates) == 1

    deleted = await db.delete_template("code_review")
    assert deleted


@pytest.mark.asyncio
async def test_agent_messages(db: Database):
    """Test agent message coordination."""
    await db.create_agent(
        agent_id="agent1",
        task="Task 1",
        model="claude-sonnet-4-20250514",
    )
    await db.create_agent(
        agent_id="agent2",
        task="Task 2",
        model="claude-sonnet-4-20250514",
    )

    await db.send_agent_message(
        message_id="msg1",
        from_agent="agent1",
        to_agent="agent2",
        task_id=None,
        message_type="info",
        content="Hello agent2",
    )

    messages = await db.get_agent_messages("agent2", unread_only=True)
    assert len(messages) == 1
    assert messages[0]["content"] == "Hello agent2"

    await db.mark_message_read("msg1")

    messages = await db.get_agent_messages("agent2", unread_only=True)
    assert len(messages) == 0


@pytest.mark.asyncio
async def test_shared_context(db: Database):
    """Test shared context."""
    await db.create_agent(
        agent_id="agent1",
        task="Task",
        model="claude-sonnet-4-20250514",
    )
    await db.create_task(
        task_id="task1",
        agent_id="agent1",
    )

    await db.set_shared_context("task1", "key1", {"value": 1}, "agent1")
    await db.set_shared_context("task1", "key2", "string_value", "agent1")

    context = await db.get_shared_context("task1")
    assert context["key1"] == {"value": 1}
    assert context["key2"] == "string_value"
