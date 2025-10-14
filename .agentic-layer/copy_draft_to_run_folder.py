"""Module for copying draft files to run folders."""

import shutil
from pathlib import Path
from get_or_create_folders import get_or_create_run_folder


def copy_draft_to_run_folder(run_id, draft_file_path):
    """Copies a markdown file to the run folder and names it draft_{run_id}.md."""
    run_folder = get_or_create_run_folder(run_id)

    source_path = Path(draft_file_path)
    destination_path = run_folder / f"draft_{run_id}.md"

    shutil.copy2(source_path, destination_path)

    return destination_path
