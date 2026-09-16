import sqlite3

# ==========================================================
# Functions related to subjects
# ==========================================================

SUBJECTS = "subjects.db"

def init_subject_db(db_name=SUBJECTS):
    """Create the subjects table if it doesn't already exist"""

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY,
            subject TEXT NOT NULL,
            filename TEXT NOT NULL
        )
    """)
    conn.commit()

# ============================================================
# Functions related to flashcards
# ============================================================

DB_NAME = "flashcards.db"

def init_db(db_name=DB_NAME):
    """Create the cards table if it doesn't already exist."""

    # opens a connection to 'flashcards.db' (creates the file if it doesn't exist)
    # and closes it automatically when done
    with sqlite3.connect(db_name) as conn:
        # create a cursor object, which is used to send SQL commands to the database
        cursor = conn.cursor()
        # execute sql command (this one creates the 'cards' table, only if it doesn't exist)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                front TEXT NOT NULL,
                back TEXT NOT NULL
            )
        """)
        # Explicitly commit the changes 
        conn.commit()


def add_card(front, back, db_name=DB_NAME):
    """Add a card to the database using parameterized queries."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cards (front, back) VALUES (?, ?)",
            # pass the values as a tuple matching the order of the '?' placeholders above.
            (front, back)
        )
        conn.commit()

def get_all_cards(db_name=DB_NAME):
    """Get all cards from the database."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, front, back FROM cards")
        return cursor.fetchall()

