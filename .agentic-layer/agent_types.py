"""Agent types for coding agent abstraction."""

from enum import Enum


class AgentType(Enum):
    """Enumeration for coding agent types."""
    CLAUDE = "claude"
    COPILOT = "copilot"

    @classmethod
    def from_string(cls, value: str) -> "AgentType":
        """Convert string to AgentType enum, case-insensitive.

        Args:
            value: String representation of agent type ("claude" or "copilot")

        Returns:
            AgentType: The corresponding enum value

        Raises:
            ValueError: If value is not a valid agent type
        """
        value_lower = value.lower()
        if value_lower == "claude":
            return cls.CLAUDE
        if value_lower == "copilot":
            return cls.COPILOT
        raise ValueError(f"Invalid agent type: {value}. Must be 'claude' or 'copilot'")
