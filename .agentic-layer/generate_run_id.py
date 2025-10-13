"""Module for generating random run IDs."""

import random
import string

def generate_run_id():
    """Generate and return a random 10 character ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=10))
