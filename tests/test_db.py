import sqlite3
import pytest
from flashcard_program.db import get_connection, init_db, add_subject, get_all_subjects, delete_subject

@pytest.fixture
def test_db(tmp_path):
    """Creates a fresh, temporary SQLite database path and initializes tables."""
    db_path = str(tmp_path / "test_flashcards.db")
    init_db(db_path)
    return db_path


# ==========================================================
# Tests for get_connection
# ==========================================================

def test_get_connection_enables_foreign_keys(tmp_path):
    """Verify get_connection explicitly turns foreign keys ON."""
    db_path = str(tmp_path / "fk_check.db")
    conn = get_connection(db_path)
    
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys;")
    (fk_status,) = cursor.fetchone()
    conn.close()

    assert fk_status == 1


# ==========================================================
# Tests for init_db
# ==========================================================

def test_init_db_creates_both_tables(test_db):
    """Verify init_db creates both 'subjects' and 'cards' tables."""
    with get_connection(test_db) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('subjects', 'cards')
        """)
        tables = {row[0] for row in cursor.fetchall()}

    assert tables == {"subjects", "cards"}


def test_init_db_is_idempotent(test_db):
    """Verify calling init_db multiple times does not drop existing data."""
    add_subject("Computer Science", db_name=test_db)

    # Call init_db a second time
    init_db(test_db)

    with get_connection(test_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM subjects")
        rows = cursor.fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "Computer Science"


# ==========================================================
# Tests for add_subject
# ==========================================================

def test_add_subject_returns_id_and_inserts_row(test_db):
    """Verify add_subject inserts data correctly and returns the primary key ID."""
    sub_id = add_subject("Biology", db_name=test_db)
    assert sub_id == 1

    with get_connection(test_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM subjects WHERE id = ?", (sub_id,))
        row = cursor.fetchone()

    assert row == (1, "Biology")


def test_add_multiple_subjects_increments_id(test_db):
    """Verify inserting multiple subjects increments primary key IDs."""
    id_1 = add_subject("Math", db_name=test_db)
    id_2 = add_subject("History", db_name=test_db)

    assert id_1 == 1
    assert id_2 == 2


def test_add_duplicate_subject_raises_integrity_error(test_db):
    """Verify the UNIQUE constraint prevents duplicate subject names."""
    add_subject("Chemistry", db_name=test_db)

    with pytest.raises(sqlite3.IntegrityError):
        add_subject("Chemistry", db_name=test_db)

# ==========================================================
# Tests for delete_subject
# ==========================================================

def test_delete_subject_removes_row(test_db):
    """Verify delete_subject removes the subject from the database."""
    add_subject("Biology", db_name=test_db)

    delete_subject("Biology", db_name=test_db)

    assert get_all_subjects(db_name=test_db) == []

# ==========================================================
# Tests for get_all_subjects
# ==========================================================

def test_get_all_subjects(test_db):
    """Verify that all existing subjects are retrieved."""
    add_subject("Math", db_name=test_db)
    add_subject("History", db_name=test_db)

    subjects = get_all_subjects(db_name=test_db)

    assert len(subjects) == 2
    assert "Math" in subjects
    assert "History" in subjects

def test_get_all_subjects_empty(test_db):
    """Verify get_all_subjects returns an empty list when no subjects exist."""
    assert get_all_subjects(db_name=test_db) == []