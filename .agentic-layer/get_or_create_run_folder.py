"""Module for managing run folder creation."""
# /// script
# dependencies = [
#   "python-dotenv",
# ]
# ///

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_or_create_run_folder(run_id):
    """Creates a folder for the given run ID in the configured run directory."""
    run_directory = os.getenv('RUN_DIRECTORY')

    if not run_directory:
        raise ValueError("RUN_DIRECTORY environment variable is not set")

    run_path = Path(run_directory) / str(run_id)
    run_path.mkdir(parents=True, exist_ok=True)

    return run_path
