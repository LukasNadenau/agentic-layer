"""Shared Claude Agent configuration utilities."""

from claude_agent_sdk import ClaudeAgentOptions


def get_default_claude_options(model: str = "sonnet") -> ClaudeAgentOptions:
    """
    Create default ClaudeAgentOptions for ADW scripts.

    Args:
        model: The model to use (default: "sonnet")

    Returns:
        ClaudeAgentOptions configured with standard ADW settings
    """
    return ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        model=model
    )
