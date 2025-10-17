"""Coding agent abstraction layer for ADW."""

import asyncio
import logging
from pathlib import Path

from agent_types import AgentType
from claude_agent_sdk import query
from claude_options import get_default_claude_options


logger = logging.getLogger(__name__)


async def call_coding_agent(
    agent_type: AgentType,
    slash_command: str,
    arguments: list[str],
    model: str = "sonnet"
) -> bool:
    """
    Execute a coding agent command with unified interface.

    Args:
        agent_type: Type of agent (CLAUDE or COPILOT)
        slash_command: Command name without slash (e.g., "implement", "feature", "bug")
        arguments: List of argument values to pass to the command
        model: Model to use (for Claude Code, default: "sonnet")

    Returns:
        bool: True if command executed successfully

    Raises:
        ValueError: If agent_type is invalid
        FileNotFoundError: If slash command file not found (for Copilot)
        RuntimeError: If agent execution fails
    """
    logger.info(
        "Calling coding agent - Type: %s, Command: %s, Arguments: %s",
        agent_type.value, slash_command, arguments
    )

    try:
        if agent_type == AgentType.CLAUDE:
            command = _build_claude_command(slash_command, arguments)
            logger.debug("Claude command: %s", command)
            await _execute_claude_agent(command, model)
        elif agent_type == AgentType.COPILOT:
            prompt = _build_copilot_command(slash_command, arguments)
            logger.debug("Copilot prompt: %s", prompt[:200])  # Log first 200 chars
            await _execute_copilot_agent(prompt)
        else:
            raise ValueError(f"Invalid agent type: {agent_type}")

        logger.info("Coding agent execution completed successfully")
        return True

    except Exception as e:
        logger.error(
            "Coding agent execution failed - Type: %s, Command: %s, Error: %s",
            agent_type.value, slash_command, e, exc_info=True
        )
        raise


def _build_claude_command(slash_command: str, arguments: list[str]) -> str:
    """Build Claude Code slash command string."""
    args_str = " ".join(str(arg) for arg in arguments)
    command = f"/{slash_command} {args_str}"
    logger.debug("Built Claude command: %s", command)
    return command


def _build_copilot_command(slash_command: str, arguments: list[str]) -> str:
    """Build GitHub Copilot CLI prompt string."""
    file_path = Path(".claude") / "commands" / f"{slash_command}.md"
    args_str = " ".join(str(arg) for arg in arguments)
    prompt = f"execute the prompt specified in {file_path} using the following arguments: {args_str}"
    logger.debug("Built Copilot prompt: %s", prompt)
    return prompt


async def _execute_claude_agent(command: str, model: str) -> None:
    """Execute command using Claude Code SDK."""
    logger.debug("Executing Claude Code SDK with command: %s", command)

    options = get_default_claude_options(model=model)

    try:
        async for message in query(prompt=command, options=options):
            logger.debug("Claude code message: %s", message)
    except Exception as e:
        logger.error("Claude Code SDK query failed: %s", e, exc_info=True)
        raise RuntimeError(f"Claude Code SDK execution failed: {e}") from e


async def _execute_copilot_agent(prompt: str) -> None:
    """Execute prompt using GitHub Copilot CLI."""
    logger.info("Executing GitHub Copilot CLI")

    command_list = ["copilot", "-p", prompt, "--allow-all-tools"]
    logger.debug("Copilot CLI command: %s", command_list)

    try:
        process = await asyncio.create_subprocess_exec(
            *command_list,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        stdout_str = stdout.decode('utf-8', errors='replace')
        stderr_str = stderr.decode('utf-8', errors='replace')

        if stdout_str:
            logger.debug("Copilot stdout: %s", stdout_str)
        if stderr_str:
            logger.debug("Copilot stderr: %s", stderr_str)

        if process.returncode != 0:
            error_msg = (
                f"GitHub Copilot CLI failed with exit code "
                f"{process.returncode}: {stderr_str}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        logger.info("GitHub Copilot CLI execution completed")

    except FileNotFoundError as exc:
        error_msg = (
            "GitHub Copilot CLI not found. "
            "Ensure 'copilot' is installed and in your PATH. "
            "See: https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli"
        )
        logger.error(error_msg)
        raise RuntimeError(error_msg) from exc
    except Exception as e:
        logger.error("GitHub Copilot CLI execution failed: %s", e, exc_info=True)
        raise RuntimeError(f"GitHub Copilot CLI execution failed: {e}") from e
