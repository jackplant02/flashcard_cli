import sqlite3

DB_NAME = "flashcards_app.db"

def get_connection(db_name=DB_NAME):
    """Return a connection to the database."""

    # Create a connection to the database.
    conn = sqlite3.connect(db_name)
    # Turn on foreign key enforcement (SQLite disables this feature by default per connection)
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


def init_db(db_name=DB_NAME):
    """Create both tables in a single database file."""

    # open the connection using the function defined above
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # Subjects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        # initialize the 'cards' table with a foreign key link to 'subjects'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
            )
        """)
        conn.commit()


def add_subject(name, db_name=DB_NAME):
    """Add a subject and return its assigned id"""

    with get_connection(db_name) as conn:

        cursor = conn.cursor()
        cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        conn.commit()
        return cursor.lastrowid

def get_all_subjects(db_name=DB_NAME):
    """Return all subjects currently in the database"""

    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM subjects")
        return [row[0] for row in cursor.fetchall()]









