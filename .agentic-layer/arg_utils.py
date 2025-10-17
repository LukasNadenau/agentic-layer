"""Shared argument parsing utilities for ADW scripts."""
import argparse
from agent_types import AgentType


def add_agent_argument(parser: argparse.ArgumentParser) -> None:
    """
    Add the --agent argument to an argument parser.

    Args:
        parser: The argument parser to add the agent argument to
    """
    parser.add_argument(
        "--agent",
        choices=["claude", "copilot"],
        default="claude",
        help="Coding agent to use (default: claude)"
    )


def parse_agent_type(args: argparse.Namespace) -> AgentType:
    """
    Parse the agent type from parsed arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        AgentType: The agent type enum value

    Raises:
        ValueError: If the agent string is invalid
    """
    return AgentType.from_string(args.agent)
