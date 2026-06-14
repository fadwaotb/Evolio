"""
In-memory "database" placeholder.

IMPORTANT (next step): Replace everything in this file with a real SQLite /
SQLAlchemy setup. For now we just keep simple Python dictionaries in memory so
the rest of the backend has somewhere to read and write data. All data is lost
when the server restarts -- that is expected for this phase.

Each dict below stands in for a future database table. The router code only ever
touches these dicts through small helper functions, so swapping in SQLite later
should not require changing the routers much.
"""

# --- "Tables" (just dictionaries keyed by id) -------------------------------

# users:        user_id -> {id, name, email, hashed_password, role}
users = {}

# profiles:     user_id -> profile dict (one profile per student)
profiles = {}

# resumes:      user_id -> resume metadata dict (one resume per student)
resumes = {}

# projects:     project_id -> project dict (each has an "owner_id")
projects = {}

# project_images: image_id -> image metadata dict (each has a "project_id")
project_images = {}

# share_links:  token -> share link dict (each has an "owner_id")
share_links = {}

# reviews:      user_id -> review dict {status, feedback: [...]}
reviews = {}


# --- Simple id generator ----------------------------------------------------

# We use a single counter so ids are easy to read while testing.
_counter = {"value": 0}


def next_id():
    """Return the next integer id (1, 2, 3, ...)."""
    _counter["value"] += 1
    return _counter["value"]


# --- Tiny lookup helpers ----------------------------------------------------

def get_user_by_email(email):
    """Find a user by email, or return None if not found."""
    for user in users.values():
        if user["email"].lower() == email.lower():
            return user
    return None
