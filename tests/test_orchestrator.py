"""Tests for orchestrator."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from gru.claude import Response, ToolUse
from gru.config import Config
from gru.crypto import CryptoManager, SecretStore
from gru.db import Database
from gru.orchestrator import Agent, Orchestrator


@pytest.fixture
async def test_config():
    """Create test config."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            data_dir=Path(tmpdir),
            telegram_token="test_token",
            telegram_admin_ids=[123],
            anthropic_api_key="test_key",
            default_model="test-model",
            max_tokens=1000,
            default_timeout=10,
            max_concurrent_agents=5,
        )
        yield config


@pytest.fixture
async def test_db(test_config):
    """Create test database."""
    db = Database(test_config.db_path)
    await db.connect()
    yield db
    await db.close()


@pytest.fixture
async def test_secrets(test_db, test_config):
    """Create test secret store."""
    crypto = CryptoManager(test_config.data_dir, iterations=1000)
    crypto.initialize("test_password")
    return SecretStore(test_db, crypto)


@pytest.fixture
async def orchestrator(test_config, test_db, test_secrets):
    """Create test orchestrator."""
    orch = Orchestrator(test_config, test_db, test_secrets)
    yield orch
    await orch.stop()


@pytest.mark.asyncio
async def test_spawn_agent(orchestrator):
    """Test spawning an agent."""
    agent = await orchestrator.spawn_agent(
        task="Test task",
        supervised=True,
        priority="normal",
    )

    assert agent["id"] is not None
    assert agent["task"] == "Test task"
    assert agent["status"] == "idle"
    assert agent["supervised"] == 1


@pytest.mark.asyncio
async def test_spawn_agent_with_workdir(orchestrator, test_config):
    """Test spawning agent with custom workdir."""
    workdir = str(test_config.data_dir / "custom_workdir")
    agent = await orchestrator.spawn_agent(
        task="Test task",
        workdir=workdir,
    )

    assert agent["workdir"] == workdir
    assert Path(workdir).exists()


@pytest.mark.asyncio
async def test_get_agent(orchestrator):
    """Test getting an agent."""
    spawned = await orchestrator.spawn_agent(task="Test task")
    agent = await orchestrator.get_agent(spawned["id"])

    assert agent is not None
    assert agent["id"] == spawned["id"]


@pytest.mark.asyncio
async def test_get_nonexistent_agent(orchestrator):
    """Test getting nonexistent agent returns None."""
    agent = await orchestrator.get_agent("nonexistent")
    assert agent is None


@pytest.mark.asyncio
async def test_list_agents(orchestrator):
    """Test listing agents."""
    await orchestrator.spawn_agent(task="Task 1")
    await orchestrator.spawn_agent(task="Task 2")

    agents = await orchestrator.list_agents()
    assert len(agents) == 2


@pytest.mark.asyncio
async def test_list_agents_by_status(orchestrator):
    """Test listing agents filtered by status."""
    await orchestrator.spawn_agent(task="Task 1")

    idle_agents = await orchestrator.list_agents("idle")
    assert len(idle_agents) == 1

    running_agents = await orchestrator.list_agents("running")
    assert len(running_agents) == 0


@pytest.mark.asyncio
async def test_pause_agent(orchestrator):
    """Test pausing an agent."""
    agent = await orchestrator.spawn_agent(task="Test task")

    # Agent must be in _agents dict to be paused
    orchestrator._agents[agent["id"]] = Agent(
        agent_id=agent["id"],
        task="Test task",
        model="test-model",
        supervised=True,
        timeout_mode="block",
        workdir="/tmp",
        orchestrator=orchestrator,
    )

    success = await orchestrator.pause_agent(agent["id"])
    assert success

    updated = await orchestrator.get_agent(agent["id"])
    assert updated["status"] == "paused"


@pytest.mark.asyncio
async def test_pause_nonexistent_agent(orchestrator):
    """Test pausing nonexistent agent fails."""
    success = await orchestrator.pause_agent("nonexistent")
    assert not success


@pytest.mark.asyncio
async def test_resume_agent(orchestrator):
    """Test resuming a paused agent."""
    agent = await orchestrator.spawn_agent(task="Test task")

    # First pause it
    orchestrator._agents[agent["id"]] = Agent(
        agent_id=agent["id"],
        task="Test task",
        model="test-model",
        supervised=True,
        timeout_mode="block",
        workdir="/tmp",
        orchestrator=orchestrator,
    )
    await orchestrator.pause_agent(agent["id"])

    # Then resume
    success = await orchestrator.resume_agent(agent["id"])
    assert success

    updated = await orchestrator.get_agent(agent["id"])
    assert updated["status"] == "running"


@pytest.mark.asyncio
async def test_terminate_agent(orchestrator):
    """Test terminating an agent."""
    agent = await orchestrator.spawn_agent(task="Test task")

    orchestrator._agents[agent["id"]] = Agent(
        agent_id=agent["id"],
        task="Test task",
        model="test-model",
        supervised=True,
        timeout_mode="block",
        workdir="/tmp",
        orchestrator=orchestrator,
    )

    success = await orchestrator.terminate_agent(agent["id"])
    assert success

    updated = await orchestrator.get_agent(agent["id"])
    assert updated["status"] == "terminated"
    assert agent["id"] not in orchestrator._agents


@pytest.mark.asyncio
async def test_nudge_agent(orchestrator):
    """Test nudging an agent with a message."""
    agent = await orchestrator.spawn_agent(task="Test task")

    agent_obj = Agent(
        agent_id=agent["id"],
        task="Test task",
        model="test-model",
        supervised=True,
        timeout_mode="block",
        workdir="/tmp",
        orchestrator=orchestrator,
    )
    orchestrator._agents[agent["id"]] = agent_obj

    success = await orchestrator.nudge_agent(agent["id"], "Hey, update?")
    assert success
    assert len(agent_obj.messages) == 1
    assert agent_obj.messages[0]["content"] == "Hey, update?"


@pytest.mark.asyncio
async def test_get_status(orchestrator):
    """Test getting orchestrator status."""
    await orchestrator.spawn_agent(task="Task 1")

    status = await orchestrator.get_status()

    assert "running" in status
    assert "agents" in status
    assert "scheduler" in status
    assert status["agents"]["total"] == 1


@pytest.mark.asyncio
async def test_run_agent_completion(orchestrator, test_config):
    """Test running an agent to completion."""
    agent_data = await orchestrator.spawn_agent(task="Say hello")

    agent = Agent(
        agent_id=agent_data["id"],
        task="Say hello",
        model="test-model",
        supervised=False,
        timeout_mode="block",
        workdir=str(test_config.data_dir),
        orchestrator=orchestrator,
    )
    orchestrator._agents[agent_data["id"]] = agent

    # Mock Claude to return a simple response
    mock_response = Response(
        content="Hello!",
        tool_uses=[],
        stop_reason="end_turn",
        usage={"input_tokens": 10, "output_tokens": 5},
    )

    with patch.object(orchestrator.claude, "send_message", return_value=mock_response):
        await orchestrator.run_agent(agent, "task123")

    updated = await orchestrator.get_agent(agent_data["id"])
    assert updated["status"] == "completed"


@pytest.mark.asyncio
async def test_run_agent_with_tool_use(orchestrator, test_config):
    """Test running agent that uses tools."""
    agent_data = await orchestrator.spawn_agent(task="Read a file")

    agent = Agent(
        agent_id=agent_data["id"],
        task="Read a file",
        model="test-model",
        supervised=False,
        timeout_mode="block",
        workdir=str(test_config.data_dir),
        orchestrator=orchestrator,
    )
    orchestrator._agents[agent_data["id"]] = agent

    # Create a test file
    test_file = test_config.data_dir / "test.txt"
    test_file.write_text("test content")

    # First response: tool use
    tool_response = Response(
        content="I'll read the file.",
        tool_uses=[ToolUse(id="tu1", name="read_file", input={"path": str(test_file)})],
        stop_reason="tool_use",
        usage={"input_tokens": 10, "output_tokens": 5},
    )

    # Second response: completion
    final_response = Response(
        content="The file contains: test content",
        tool_uses=[],
        stop_reason="end_turn",
        usage={"input_tokens": 20, "output_tokens": 10},
    )

    call_count = 0

    async def mock_send(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return tool_response
        return final_response

    with patch.object(orchestrator.claude, "send_message", side_effect=mock_send):
        await orchestrator.run_agent(agent, "task123")

    updated = await orchestrator.get_agent(agent_data["id"])
    assert updated["status"] == "completed"


@pytest.mark.asyncio
async def test_run_agent_failure(orchestrator, test_config):
    """Test agent failure handling."""
    agent_data = await orchestrator.spawn_agent(task="Fail")

    agent = Agent(
        agent_id=agent_data["id"],
        task="Fail",
        model="test-model",
        supervised=False,
        timeout_mode="block",
        workdir=str(test_config.data_dir),
        orchestrator=orchestrator,
    )
    orchestrator._agents[agent_data["id"]] = agent

    with patch.object(orchestrator.claude, "send_message", side_effect=Exception("API Error")):
        await orchestrator.run_agent(agent, "task123")

    updated = await orchestrator.get_agent(agent_data["id"])
    assert updated["status"] == "failed"
    assert "API Error" in updated["error"]


@pytest.mark.asyncio
async def test_execute_bash(orchestrator, test_config):
    """Test bash execution."""
    result = await orchestrator._execute_bash("echo hello", str(test_config.data_dir))
    assert "hello" in result


@pytest.mark.asyncio
async def test_execute_bash_timeout(orchestrator, test_config):
    """Test bash execution timeout."""
    result = await orchestrator._execute_bash("sleep 100", str(test_config.data_dir))
    assert "timed out" in result.lower()


@pytest.mark.asyncio
async def test_read_file(orchestrator, test_config):
    """Test file reading."""
    test_file = test_config.data_dir / "test.txt"
    test_file.write_text("file content")

    result = await orchestrator._read_file(str(test_file), str(test_config.data_dir))
    assert result == "file content"


@pytest.mark.asyncio
async def test_read_file_not_found(orchestrator, test_config):
    """Test reading nonexistent file."""
    result = await orchestrator._read_file("nonexistent.txt", str(test_config.data_dir))
    assert "not found" in result.lower()


@pytest.mark.asyncio
async def test_write_file(orchestrator, test_config):
    """Test file writing."""
    test_path = test_config.data_dir / "output.txt"

    workdir = str(test_config.data_dir)
    result = await orchestrator._write_file(str(test_path), "new content", workdir)

    assert "successfully" in result.lower()
    assert test_path.read_text() == "new content"


@pytest.mark.asyncio
async def test_search_files(orchestrator, test_config):
    """Test file search."""
    (test_config.data_dir / "file1.txt").write_text("a")
    (test_config.data_dir / "file2.txt").write_text("b")

    result = await orchestrator._search_files("*.txt", ".", str(test_config.data_dir))

    assert "file1.txt" in result
    assert "file2.txt" in result


@pytest.mark.asyncio
async def test_approval_auto_approve_without_callback(orchestrator, test_config):
    """Test that actions auto-approve when no callback is set."""
    agent_data = await orchestrator.spawn_agent(task="Test")

    agent = Agent(
        agent_id=agent_data["id"],
        task="Test",
        model="test-model",
        supervised=True,
        timeout_mode="block",
        workdir=str(test_config.data_dir),
        orchestrator=orchestrator,
    )

    # No approval callback set, should auto-approve
    result = await orchestrator._request_approval(agent, "bash", {"command": "ls"}, "task1")
    assert result is True


@pytest.mark.asyncio
async def test_pending_approvals(orchestrator):
    """Test getting pending approvals."""
    # Create an agent first (FK constraint)
    agent = await orchestrator.spawn_agent(task="Test")

    await orchestrator.db.create_approval(
        approval_id="appr1",
        agent_id=agent["id"],
        action_type="bash",
        action_details={"command": "rm -rf /"},
    )

    pending = await orchestrator.get_pending_approvals()
    assert len(pending) == 1
    assert pending[0]["id"] == "appr1"


@pytest.mark.asyncio
async def test_approve_action(orchestrator):
    """Test approving an action."""
    agent = await orchestrator.spawn_agent(task="Test")

    await orchestrator.db.create_approval(
        approval_id="appr1",
        agent_id=agent["id"],
        action_type="bash",
        action_details={"command": "ls"},
    )

    success = await orchestrator.approve("appr1", approved=True)
    assert success

    approval = await orchestrator.db.get_approval("appr1")
    assert approval["status"] == "approved"


@pytest.mark.asyncio
async def test_reject_action(orchestrator):
    """Test rejecting an action."""
    agent = await orchestrator.spawn_agent(task="Test")

    await orchestrator.db.create_approval(
        approval_id="appr1",
        agent_id=agent["id"],
        action_type="bash",
        action_details={"command": "rm -rf /"},
    )

    success = await orchestrator.approve("appr1", approved=False)
    assert success

    approval = await orchestrator.db.get_approval("appr1")
    assert approval["status"] == "rejected"
