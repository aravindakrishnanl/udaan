from typing import List
from app.schemas import TranslationLog

# In-memory list to store translation logs.
# This list will be cleared when the application restarts.
# For persistence, you would use a database like SQLite.
translation_logs: List[TranslationLog] = []

def add_log_entry(log_entry: TranslationLog):
    """
    Adds a new translation log entry to the in-memory list.
    """
    translation_logs.append(log_entry)
    # In a real database, you would perform an INSERT operation here.
    print(f"Log added: {log_entry.dict()}") # For debugging purposes

def get_all_logs() -> List[TranslationLog]:
    """
    Retrieves all translation log entries from the in-memory list.
    """
    return translation_logs