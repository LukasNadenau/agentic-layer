"""Module for creating specification files using Claude Code."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

from pathlib import Path
from dotenv import load_dotenv
from get_or_create_run_folder import get_or_create_run_folder
from models import DraftClass
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


async def create_spec(run_id: str, draft_file_path: str, draft_class: DraftClass) -> Path | None:
    """
    Creates a spec file by calling Claude Code with the appropriate command.

    Args:
        run_id: The run identifier
        draft_file_path: Path to the draft file
        draft_class: Classification of the draft (DraftClass.FEATURE or DraftClass.BUG)

    Returns:
        Path | None: Path to the spec file if successfully created, None otherwise
    """
    # Get or create run folder
    run_folder = get_or_create_run_folder(run_id)

    # Generate spec file path
    spec_file_path = run_folder / f"spec_{run_id}.md"

    # Determine which command to use based on draft class
    if draft_class == DraftClass.FEATURE:
        command = f"/feature {run_id} {draft_file_path} {spec_file_path}"
    elif draft_class == DraftClass.BUG:
        command = f"/bug {run_id} {draft_file_path} {spec_file_path}"
    else:
        raise ValueError(f"Unknown draft class: {draft_class}. Expected DraftClass.FEATURE or DraftClass.BUG.")

    # Set up options with write restriction to spec file path only
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"]
    )

    # Use query to send the slash command
    async for _ in query(prompt=command, options=options):
        pass

    # Check if spec file was created
    spec_exists = spec_file_path.exists()

    if spec_exists:
        print(f"✓ Spec file created successfully at: {spec_file_path}")
        return spec_file_path
    else:
        print(f"✗ Spec file was not created at: {spec_file_path}")
        return None
