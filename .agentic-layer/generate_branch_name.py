"""Branch name generation using Pydantic AI."""
# /// script
# dependencies = [
#   "pydantic-ai",
# ]
# ///

import logging
from pydantic_ai import Agent
from models import DraftClass, BranchDescription


# Create agent to generate short branch descriptions
agent = Agent(
    'anthropic:claude-3-5-haiku-20241022',
    output_type=BranchDescription,
    system_prompt=(
        'You generate concise branch name descriptions (3-5 words max). '
        'Use snake_case format. Focus on the key action or change. '
        'Examples: "add_user_auth", "fix_login_crash", "update_api_endpoint"'
    ),
)


async def generate_branch_name(
    run_id: str,
    draft_class: DraftClass,
    draft: str,
    issue_id: str | None = None
) -> str:
    """Generate a branch name from draft text.

    Args:
        run_id: The run identifier
        draft_class: Classification as FEATURE or BUG
        draft: The draft text describing the change
        issue_id: Optional issue identifier

    Returns:
        str: Generated branch name following the pattern:
            {feat/bug}_run_{run_id}_{issue_id}_{short_description}
    """
    logger = logging.getLogger(__name__)
    logger.debug("Generating branch name with Pydantic AI")

    # Generate short description using AI agent
    try:
        result = await agent.run(draft)
        short_desc = result.output.short_description
        logger.debug("AI suggested: %s", short_desc)
    except Exception as e:
        logger.error("Branch name generation failed with Pydantic AI: %s", e, exc_info=True)
        raise

    # Normalize the description (lowercase, underscores)
    short_desc = short_desc.lower().replace(' ', '_').replace('-', '_')

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
