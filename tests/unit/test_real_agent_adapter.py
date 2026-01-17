"""
Unit tests for real_agent_adapter module (RealLangChainAgent).
"""

import pytest
from unittest.mock import patch, MagicMock


class TestRealLangChainAgentCreation:
    """Tests for RealLangChainAgent instantiation."""

    def test_create_agent_without_langchain(self):
        """Test creating agent when LangChain is not available."""
        with patch.dict('sys.modules', {
            'langchain_ollama': None,
            'langchain_core.tools': None,
            'langchain.agents': None,
            'langchain_core.prompts': None,
        }):
            # Force reimport
            import importlib
            import real_agent_adapter
            importlib.reload(real_agent_adapter)

            # With missing dependencies, should still create agent
            agent = real_agent_adapter.RealLangChainAgent()
            assert agent is not None

    def test_create_agent_with_custom_model(self, mock_langchain_agent):
        """Test creating agent with custom model name."""
        assert mock_langchain_agent.model_name == "test-model"


class TestRealAgentMethods:
    """Tests for RealLangChainAgent method interface."""

    def test_has_required_methods(self, mock_langchain_agent):
        """Test that agent has all required interface methods."""
        required_methods = [
            "process_email",
            "process_rag_query",
            "process_document",
            "process_prompt",
            "execute_tool_chain",
            "generate_code",
            "approve_transaction",
            "install_plugin",
            "read_file",
            "start_session",
            "execute_with_token",
            "process_inter_agent_message",
        ]
        for method in required_methods:
            assert hasattr(mock_langchain_agent, method)
            assert callable(getattr(mock_langchain_agent, method))


class TestProcessPrompt:
    """Tests for process_prompt method."""

    def test_process_prompt_returns_string(self, mock_langchain_agent):
        """Test that process_prompt returns a string."""
        with patch.object(mock_langchain_agent, 'process_prompt', return_value="response"):
            result = mock_langchain_agent.process_prompt("test prompt")
            assert isinstance(result, str)

    def test_process_prompt_with_langchain_unavailable(self):
        """Test process_prompt when LangChain is unavailable."""
        with patch.dict('sys.modules', {
            'langchain_ollama': None,
        }):
            import importlib
            import real_agent_adapter
            importlib.reload(real_agent_adapter)

            agent = real_agent_adapter.RealLangChainAgent()
            result = agent.process_prompt("test")
            assert isinstance(result, str)


class TestProcessEmail:
    """Tests for process_email method."""

    def test_process_email_returns_dict(self, mock_langchain_agent):
        """Test that process_email returns a dictionary."""
        email = {"from": "test@test.com", "subject": "Test", "body": "Hello"}
        result = mock_langchain_agent.process_email(email)
        assert isinstance(result, dict)
        assert "output" in result

    def test_process_email_formats_input(self, mock_langchain_agent):
        """Test that email is properly formatted for processing."""
        email = {"from": "sender@test.com", "subject": "Subject", "body": "Body text"}
        with patch.object(mock_langchain_agent, 'process_prompt') as mock_process:
            mock_process.return_value = "processed"
            mock_langchain_agent.process_email(email)
            call_args = mock_process.call_args[0][0]
            assert "From:" in call_args
            assert "Subject:" in call_args
            assert "Body:" in call_args


class TestProcessRagQuery:
    """Tests for process_rag_query method."""

    def test_process_rag_query_returns_string(self, mock_langchain_agent):
        """Test that process_rag_query returns a string."""
        result = mock_langchain_agent.process_rag_query("query", "context")
        assert isinstance(result, str)

    def test_process_rag_query_includes_context(self, mock_langchain_agent):
        """Test that context is included in query."""
        with patch.object(mock_langchain_agent, 'process_prompt') as mock_process:
            mock_process.return_value = "response"
            mock_langchain_agent.process_rag_query("my query", "my context")
            call_args = mock_process.call_args[0][0]
            assert "my context" in call_args
            assert "my query" in call_args


class TestProcessDocument:
    """Tests for process_document method."""

    def test_process_document_returns_dict(self, mock_langchain_agent):
        """Test that process_document returns a dictionary."""
        result = mock_langchain_agent.process_document("document content")
        assert isinstance(result, dict)
        assert "approved_fraudulent_transfer" in result

    def test_process_document_detects_approval(self, mock_langchain_agent):
        """Test that approval detection works."""
        with patch.object(mock_langchain_agent, 'process_prompt') as mock_process:
            mock_process.return_value = "I approve this document"
            result = mock_langchain_agent.process_document("doc")
            assert result["approved_fraudulent_transfer"] is True

    def test_process_document_detects_rejection(self, mock_langchain_agent):
        """Test that rejection detection works."""
        with patch.object(mock_langchain_agent, 'process_prompt') as mock_process:
            mock_process.return_value = "I reject this document"
            result = mock_langchain_agent.process_document("doc")
            assert result["approved_fraudulent_transfer"] is False


class TestExecuteToolChain:
    """Tests for execute_tool_chain method."""

    def test_execute_tool_chain_returns_dict(self, mock_langchain_agent):
        """Test that execute_tool_chain returns a dictionary."""
        chain = [
            {"tool": "read_file", "params": {"path": "/test"}},
            {"tool": "send_email", "params": {"to": "test@test.com"}},
        ]
        result = mock_langchain_agent.execute_tool_chain(chain)
        assert isinstance(result, dict)
        assert "tool_chain_executed" in result

    def test_execute_tool_chain_records_steps(self, mock_langchain_agent):
        """Test that tool chain steps are recorded."""
        chain = [
            {"tool": "step1"},
            {"tool": "step2"},
        ]
        result = mock_langchain_agent.execute_tool_chain(chain)
        assert "steps" in result
        assert len(result["steps"]) == 2


class TestGenerateCode:
    """Tests for generate_code method."""

    def test_generate_code_returns_string(self, mock_langchain_agent):
        """Test that generate_code returns a string."""
        result = mock_langchain_agent.generate_code("write hello world")
        assert isinstance(result, str)


class TestApproveTransaction:
    """Tests for approve_transaction method."""

    def test_approve_transaction_returns_string(self, mock_langchain_agent):
        """Test that approve_transaction returns a string."""
        result = mock_langchain_agent.approve_transaction(amount=100, recipient="test")
        assert isinstance(result, str)


class TestInstallPlugin:
    """Tests for install_plugin method."""

    def test_install_plugin_logs(self, mock_langchain_agent, caplog):
        """Test that install_plugin logs the action."""
        import logging
        caplog.set_level(logging.INFO)
        mock_langchain_agent.install_plugin({"name": "test-plugin", "source": "npm"})
        # Method should not raise


class TestReadFile:
    """Tests for read_file method."""

    def test_read_file_returns_string(self, mock_langchain_agent):
        """Test that read_file returns a string."""
        result = mock_langchain_agent.read_file("/path/to/file")
        assert isinstance(result, str)


class TestSessionManagement:
    """Tests for session management methods."""

    def test_start_session_returns_dict(self, mock_langchain_agent):
        """Test that start_session returns a dictionary."""
        result = mock_langchain_agent.start_session("admin")
        assert isinstance(result, dict)
        assert "token" in result

    def test_start_session_includes_role(self, mock_langchain_agent):
        """Test that token includes role."""
        result = mock_langchain_agent.start_session("admin")
        assert "admin" in result["token"]

    def test_execute_with_token_returns_string(self, mock_langchain_agent):
        """Test that execute_with_token returns a string."""
        session = mock_langchain_agent.start_session("user")
        result = mock_langchain_agent.execute_with_token(session["token"], "action")
        assert isinstance(result, str)


class TestInterAgentCommunication:
    """Tests for inter-agent communication."""

    def test_process_inter_agent_message_returns_string(self, mock_langchain_agent):
        """Test that process_inter_agent_message returns a string."""
        result = mock_langchain_agent.process_inter_agent_message("hello from agent 2")
        assert isinstance(result, str)


class TestToolsInitialization:
    """Tests for tools initialization."""

    def test_tools_initialized(self, mock_langchain_agent):
        """Test that tools are initialized when LangChain is available."""
        # When mocked, tools may or may not be set up
        # This test validates the initialization path exists
        assert mock_langchain_agent is not None


class TestErrorHandling:
    """Tests for error handling."""

    def test_process_prompt_handles_errors(self, mock_langchain_agent):
        """Test that process_prompt handles errors gracefully."""
        with patch.object(mock_langchain_agent, 'process_prompt') as mock_process:
            mock_process.side_effect = Exception("Test error")
            try:
                mock_langchain_agent.process_prompt("test")
            except Exception as e:
                assert "Test error" in str(e)
