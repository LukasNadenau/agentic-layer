"""Draft classification using Claude/Copilot coding agents."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

import logging
import tempfile
from pathlib import Path
from models import DraftClass
from coding_agent import call_coding_agent
from agent_types import AgentType


async def classify_draft(
    draft_text: str,
    agent_type: AgentType = AgentType.CLAUDE
) -> DraftClass:
    """Classify a draft text as either FEATURE or BUG.

    Args:
        draft_text: The draft text to classify
        agent_type: The agent type to use (default: CLAUDE)

    Returns:
        DraftClass: The classification (FEATURE or BUG)

    Raises:
        ValueError: If the agent returns an invalid classification
        RuntimeError: If the agent execution fails
    """
    logger = logging.getLogger(__name__)
    logger.debug("Classifying draft with %s agent", agent_type.value)

    # Create temporary files for input and output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as draft_file:
        draft_file.write(draft_text)
        draft_file_path = draft_file.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as output_file:
        output_file_path = output_file.name

    try:
        # Call the coding agent
        await call_coding_agent(
            agent_type,
            "classify",
            [draft_file_path, output_file_path]
        )

        # Read and validate the result
        output_path = Path(output_file_path)
        if not output_path.exists():
            error_msg = f"Agent did not create output file at: {output_file_path}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        result_text = output_path.read_text(encoding='utf-8').strip().upper()

        # Validate the result
        if result_text == "FEATURE":
            logger.info("Draft classified as: FEATURE")
            return DraftClass.FEATURE
        elif result_text == "BUG":
            logger.info("Draft classified as: BUG")
            return DraftClass.BUG
        else:
            error_msg = f"Invalid classification result: '{result_text}'. Expected 'FEATURE' or 'BUG'."
            logger.error(error_msg)
            raise ValueError(error_msg)

    except Exception as e:
        logger.error("Draft classification failed: %s", e, exc_info=True)
        raise
    finally:
        # Clean up temporary files
        try:
            Path(draft_file_path).unlink(missing_ok=True)
            Path(output_file_path).unlink(missing_ok=True)
        except Exception as cleanup_error:
            logger.warning("Failed to clean up temporary files: %s", cleanup_error)
