"""Module for reading draft text from run folders."""

from get_or_create_folders import get_or_create_run_folder


def read_draft_text(run_id):
    """Reads the draft markdown file for the given run ID and returns its content as a string."""
    run_folder = get_or_create_run_folder(run_id)
    draft_file = run_folder / f"draft_{run_id}.md"

    if not draft_file.exists():
        raise FileNotFoundError(f"Draft file not found: {draft_file}")

    return draft_file.read_text(encoding='utf-8')
