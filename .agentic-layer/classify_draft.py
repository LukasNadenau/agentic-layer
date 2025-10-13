"""Draft classification using Pydantic AI."""

from pydantic_ai import Agent
from .types import DraftClass, DraftClassification

# Create agent with structured output
agent = Agent(
    'anthropic:claude-3-5-haiku-20241022',
    result_type=DraftClassification,
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
    result = await agent.run(draft_text)
    return result.data.draft_class
