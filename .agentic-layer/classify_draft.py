"""Draft classification using Claude/Copilot coding agents."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

import logging
from models import DraftClass
from coding_agent import call_coding_agent
from agent_types import AgentType
from get_or_create_folders import get_or_create_run_folder


async def classify_draft(
    run_id: str,
    draft_file_path: str,
    agent_type: AgentType = AgentType.CLAUDE
) -> DraftClass:
    """Classify a draft file as either FEATURE or BUG.

    Args:
        run_id: The run identifier
        draft_file_path: Path to the draft file to classify
        agent_type: The agent type to use (default: CLAUDE)

    Returns:
        DraftClass: The classification (FEATURE or BUG)

    Raises:
        ValueError: If the agent returns an invalid classification
        RuntimeError: If the agent execution fails
    """
    logger = logging.getLogger(__name__)
    logger.debug("Classifying draft with %s agent", agent_type.value)
    logger.debug("Using draft file: %s", draft_file_path)

    # Get run folder
    run_folder = get_or_create_run_folder(run_id)

    # Create output file path in the run folder
    output_file_path = run_folder / "classify_output.txt"

    try:
        # Call the coding agent using the existing draft file
        await call_coding_agent(
            agent_type,
            "classify",
            [draft_file_path, str(output_file_path)]
        )

        # Read and validate the result
        if not output_file_path.exists():
            error_msg = f"Agent did not create output file at: {output_file_path}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        result_text = output_file_path.read_text(encoding='utf-8').strip().upper()
        logger.debug("Classification output: %s", result_text)

        # Validate the result
        if result_text == "FEATURE":
            logger.info("Draft classified as: FEATURE")
            logger.info("Classification result saved to: %s", output_file_path)
            return DraftClass.FEATURE
        elif result_text == "BUG":
            logger.info("Draft classified as: BUG")
            logger.info("Classification result saved to: %s", output_file_path)
            return DraftClass.BUG
        else:
            error_msg = f"Invalid classification result: '{result_text}'. Expected 'FEATURE' or 'BUG'."
            logger.error(error_msg)
            raise ValueError(error_msg)

    except Exception as e:
        logger.error("Draft classification failed: %s", e, exc_info=True)
        raise
