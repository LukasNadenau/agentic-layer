"""Draft classification using Pydantic AI."""
# /// script
# dependencies = [
#   "pydantic-ai",
# ]
# ///

import logging
from pydantic_ai import Agent
from models import DraftClass, DraftClassification

# Create agent with structured output
agent = Agent(
    'anthropic:claude-3-5-haiku-20241022',
    output_type=DraftClassification,
    system_prompt=(
        'You are a classifier that determines whether a draft describes a FEATURE or a BUG. '
        'A FEATURE is a new capability, enhancement, or functionality. '
        'A BUG is a defect, error, or problem that needs to be fixed.'
    ),
)

async def classify_draft(draft_text: str) -> DraftClass:
    """Classify a draft text as either FEATURE or BUG.

    Args:
        draft_text: The draft text to classify

    Returns:
        DraftClass: The classification (FEATURE or BUG)
    """
    logger = logging.getLogger(__name__)
    logger.debug("Classifying draft with Pydantic AI")

    try:
        result = await agent.run(draft_text)
        logger.info("Draft classified as: %s", result.output.draft_class)
        return result.output.draft_class
    except Exception as e:
        logger.error("Draft classification failed with Pydantic AI: %s", e, exc_info=True)
        raise
