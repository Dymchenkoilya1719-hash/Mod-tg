"""SQLite database initialization and management."""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class DatabaseManager:
    """Manage SQLite database for TG Mod."""
    
    def __init__(self, db_path: str = "data/tg_mod.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                phone_number TEXT UNIQUE,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                avatar_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Dialogs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dialogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                is_group BOOLEAN,
                is_channel BOOLEAN,
                is_bot BOOLEAN,
                unread_count INTEGER DEFAULT 0,
                last_message TEXT,
                last_message_date TIMESTAMP,
                avatar_path TEXT,
                pinned BOOLEAN DEFAULT 0,
                muted BOOLEAN DEFAULT 0,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                dialog_id INTEGER,
                sender_id INTEGER,
                text TEXT,
                created_at TIMESTAMP,
                edited_at TIMESTAMP,
                is_read BOOLEAN DEFAULT 0,
                has_media BOOLEAN DEFAULT 0,
                media_type TEXT,
                media_path TEXT,
                forward_from INTEGER,
                reply_to_msg_id INTEGER,
                FOREIGN KEY(dialog_id) REFERENCES dialogs(id)
            )
        """)
        
        # Media cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msg_id INTEGER,
                file_path TEXT UNIQUE,
                file_size INTEGER,
                media_type TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(msg_id) REFERENCES messages(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_dialog(self, dialog_id: int, name: str, is_group: bool, 
                   is_channel: bool, is_bot: bool, avatar_path: str = None):
        """Save/update dialog."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO dialogs 
            (id, name, is_group, is_channel, is_bot, avatar_path, synced_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (dialog_id, name, is_group, is_channel, is_bot, avatar_path))
        
        conn.commit()
        conn.close()
    
    def save_message(self, msg_id: int, dialog_id: int, sender_id: int,
                    text: str, created_at: datetime, is_read: bool = False,
                    has_media: bool = False, media_type: str = None):
        """Save message to database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO messages
            (id, dialog_id, sender_id, text, created_at, is_read, has_media, media_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (msg_id, dialog_id, sender_id, text, created_at, is_read, has_media, media_type))
        
        conn.commit()
        conn.close()
    
    def get_dialogs(self) -> List[dict]:
        """Get all dialogs sorted by last message date."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dialogs 
            ORDER BY pinned DESC, last_message_date DESC
        """)
        
        dialogs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return dialogs
    
    def get_messages(self, dialog_id: int, limit: int = 50) -> List[dict]:
        """Get messages from dialog."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM messages 
            WHERE dialog_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (dialog_id, limit))
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return list(reversed(messages))  # Return in chronological order
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count, SUM(file_size) as total_size FROM media_cache")
        result = cursor.fetchone()
        
        conn.close()
        
        return {
            "media_count": result['count'] or 0,
            "total_size_mb": (result['total_size'] or 0) / (1024 * 1024)
        }


if __name__ == "__main__":
    db = DatabaseManager()
    print("[✓] Database initialized")
