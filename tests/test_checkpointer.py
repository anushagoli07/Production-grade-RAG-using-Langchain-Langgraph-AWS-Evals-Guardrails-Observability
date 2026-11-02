"""Tests for LangGraph checkpointer configuration."""

from langgraph.checkpoint.memory import MemorySaver

from app.agents.graph import checkpointer, rag_agent


def test_agent_uses_memory_saver():
    assert isinstance(checkpointer, MemorySaver)
    assert rag_agent.checkpointer is checkpointer