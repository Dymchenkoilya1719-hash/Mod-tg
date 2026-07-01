"""Pydantic models for API requests/responses."""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AuthRequest(BaseModel):
    """Authentication request model."""
    phone_number: str
    

class CodeRequest(BaseModel):
    """Code verification request."""
    code: str
    password: Optional[str] = None  # 2FA password if required


class MessageModel(BaseModel):
    """Single message model."""
    id: int
    dialog_id: int
    sender_id: int
    text: str
    created_at: datetime
    edited_at: Optional[datetime] = None
    is_read: bool
    has_media: bool
    media_type: Optional[str] = None
    forward_from: Optional[int] = None
    reply_to_msg_id: Optional[int] = None


class DialogModel(BaseModel):
    """Chat/Dialog model."""
    id: int
    name: str
    is_group: bool
    is_channel: bool
    is_bot: bool
    unread_count: int
    last_message: Optional[str]
    last_message_date: Optional[datetime]
    avatar_path: Optional[str]
    pinned: bool = False
    muted: bool = False


class UserModel(BaseModel):
    """Current authenticated user."""
    id: int
    phone_number: str
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    avatar_path: Optional[str]
    status: str  # "online", "offline", "away"


class SendMessageRequest(BaseModel):
    """Send message request."""
    dialog_id: int
    text: str
    reply_to_msg_id: Optional[int] = None
    media_path: Optional[str] = None


class EditMessageRequest(BaseModel):
    """Edit message request."""
    msg_id: int
    text: str


class CacheStats(BaseModel):
    """Cache statistics."""
    total_size_mb: float
    media_count: int
    messages_cached: int
    last_cleanup: Optional[datetime]
