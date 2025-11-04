"""Branch name generation using Claude/Copilot coding agents."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

import logging
import re
import tempfile
from pathlib import Path
from models import DraftClass
from coding_agent import call_coding_agent
from agent_types import AgentType


async def generate_branch_name(
    run_id: str,
    draft_class: DraftClass,
    draft: str,
    issue_id: str | None = None,
    agent_type: AgentType = AgentType.CLAUDE
) -> str:
    """Generate a branch name from draft text.

    Args:
        run_id: The run identifier
        draft_class: Classification as FEATURE or BUG
        draft: The draft text describing the change
        issue_id: Optional issue identifier
        agent_type: The agent type to use (default: CLAUDE)

    Returns:
        str: Generated branch name following the pattern:
            {feat/bug}_run_{run_id}_{issue_id}_{short_description}

    Raises:
        ValueError: If the agent returns an invalid branch description
        RuntimeError: If the agent execution fails
    """
    logger = logging.getLogger(__name__)
    logger.debug("Generating branch name with %s agent", agent_type.value)

    # Create temporary files for input and output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as draft_file:
        draft_file.write(draft)
        draft_file_path = draft_file.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as output_file:
        output_file_path = output_file.name

    try:
        # Call the coding agent to generate short description
        await call_coding_agent(
            agent_type,
            "branch_name",
            [draft_file_path, output_file_path]
        )

        # Read and validate the result
        output_path = Path(output_file_path)
        if not output_path.exists():
            error_msg = f"Agent did not create output file at: {output_file_path}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        short_desc = output_path.read_text(encoding='utf-8').strip()
        logger.debug("AI suggested: %s", short_desc)

        # Validate the format (should be snake_case, no special chars except underscore)
        if not re.match(r'^[a-z0-9_]+$', short_desc):
            # Try to normalize it
            short_desc = short_desc.lower().replace(' ', '_').replace('-', '_')
            # Remove any remaining invalid characters
            short_desc = re.sub(r'[^a-z0-9_]', '', short_desc)
            logger.warning("Normalized branch description to: %s", short_desc)

        if not short_desc:
            error_msg = "Agent returned empty or invalid branch description"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Determine prefix based on draft class
        prefix = 'feat' if draft_class == DraftClass.FEATURE else 'bug'

        # Build branch name
        parts = [prefix, 'run', run_id]
        if issue_id:
            parts.append(issue_id)
        parts.append(short_desc)

        final_name = '_'.join(parts)
        logger.info("Generated branch name: %s", final_name)

        return final_name

    except Exception as e:
        logger.error("Branch name generation failed: %s", e, exc_info=True)
        raise
    finally:
        # Clean up temporary files
        try:
            Path(draft_file_path).unlink(missing_ok=True)
            Path(output_file_path).unlink(missing_ok=True)
        except Exception as cleanup_error:
            logger.warning("Failed to clean up temporary files: %s", cleanup_error)
