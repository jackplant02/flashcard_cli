import sqlite3

DB_NAME = "flashcards_app.db"

def get_connection(db_name=DB_NAME):
    """Return a connection to the database."""

    # Create a connection to the database.
    conn = sqlite3.connect(db_name)
    # Turn on foreign key enforcement (SQLite disables this feature by default per connection)
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


def init_db():
    """Create both tables in a single database file."""

    #open the connection using the function defined above
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Subjects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        # Cards table referencing subjects via foreign key
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

