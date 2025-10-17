"""Git branch creation utility for ADW."""
import subprocess
import sys


def create_branch(branch_name):
    """Create a new git branch using git CLI commands.

    Args:
        branch_name: Name of the branch to create
    """
    try:
        # Create and checkout the new branch
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Successfully created and checked out branch: {branch_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e.stderr}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_branch.py <branch_name>", file=sys.stderr)
        sys.exit(1)

    create_branch(sys.argv[1])
