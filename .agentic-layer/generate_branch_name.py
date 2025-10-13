"""Branch name generation using Pydantic AI."""

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
    # Generate short description using AI agent
    result = await agent.run(draft)
    short_desc = result.output.short_description

    # Normalize the description (lowercase, underscores)
    short_desc = short_desc.lower().replace(' ', '_').replace('-', '_')

    # Determine prefix based on draft class
    prefix = 'feat' if draft_class == DraftClass.FEATURE else 'bug'

    # Build branch name
    parts = [prefix, 'run', run_id]
    if issue_id:
        parts.append(issue_id)
    parts.append(short_desc)

    return '_'.join(parts)
