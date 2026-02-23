# Credits: Erwin Lejeune — 2026-02-23
"""Tests for EpsteinAgent instantiation."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestEpsteinAgent:
    @patch("agent.agent.ToolCallingAgent")
    @patch("agent.agent.LiteLLMModel")
    def test_agent_initializes(self, mock_model_cls, mock_agent_cls):
        mock_model_cls.return_value = MagicMock()
        mock_agent_cls.return_value = MagicMock()

        from agent import EpsteinAgent

        agent = EpsteinAgent()
        assert agent._agent is not None
        mock_agent_cls.assert_called_once()
        call_kwargs = mock_agent_cls.call_args
        assert len(call_kwargs.kwargs["tools"]) == 5

    @patch("agent.agent.ToolCallingAgent")
    @patch("agent.agent.LiteLLMModel")
    def test_agent_run_delegates(self, mock_model_cls, mock_agent_cls):
        mock_inner = MagicMock()
        mock_inner.run.return_value = "Answer"
        mock_agent_cls.return_value = mock_inner
        mock_model_cls.return_value = MagicMock()

        from agent import EpsteinAgent

        agent = EpsteinAgent()
        result = agent.run("Who is Ghislaine Maxwell?")
        assert result == "Answer"
        mock_inner.run.assert_called_once_with("Who is Ghislaine Maxwell?")
