"""Telethon client wrapper for TG Mod."""

import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from pathlib import Path
from typing import Optional, List, Any
import json
from crypto import SessionCrypto


class TelethonClientManager:
    """Manage Telethon client instance."""
    
    def __init__(self, api_id: int, api_hash: str, session_file: str, session_password: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_file = session_file
        self.session_password = session_password
        self.client: Optional[TelegramClient] = None
        self.phone_code_hash = None
    
    async def _get_or_create_client(self) -> TelegramClient:
        """Get or create Telethon client instance."""
        if self.client is None:
            self.client = TelegramClient(
                self.session_file,
                self.api_id,
                self.api_hash
            )
            await self.client.start()
        return self.client
    
    async def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        try:
            client = await self._get_or_create_client()
            return await client.is_user_authorized()
        except Exception as e:
            print(f"[ERROR] Auth check failed: {e}")
            return False
    
    async def request_code(self, phone_number: str) -> str:
        """Request authentication code.
        
        Args:
            phone_number: User's phone number in format +1234567890
            
        Returns:
            Phone code hash
        """
        try:
            client = await self._get_or_create_client()
            result = await client.send_code_request(phone_number)
            self.phone_code_hash = result.phone_code_hash
            return self.phone_code_hash
        except Exception as e:
            print(f"[ERROR] Failed to request code: {e}")
            raise
    
    async def sign_in(self, code: str, password: Optional[str] = None) -> Any:
        """Sign in with code.
        
        Args:
            code: 5-digit code from Telegram
            password: 2FA password if required
            
        Returns:
            User object
        """
        try:
            client = await self._get_or_create_client()
            
            try:
                user = await client.sign_in(phone_code=code)
            except Exception as e:
                if "2FA" in str(e) or "password" in str(e).lower():
                    if not password:
                        raise ValueError("2FA password required")
                    user = await client.sign_in(password=password)
                else:
                    raise
            
            # Save encrypted session
            session_data = {
                "phone": client.session.phone,
                "user_id": user.id,
            }
            SessionCrypto.encrypt_session(
                session_data,
                self.session_password,
                self.session_file
            )
            
            return user
        except Exception as e:
            print(f"[ERROR] Sign in failed: {e}")
            raise
    
    async def sign_out(self) -> bool:
        """Sign out user."""
        try:
            client = await self._get_or_create_client()
            await client.log_out()
            self.client = None
            return True
        except Exception as e:
            print(f"[ERROR] Sign out failed: {e}")
            return False
    
    async def logout(self) -> bool:
        """Alias for sign_out."""
        return await self.sign_out()
    
    async def get_me(self) -> Optional[Any]:
        """Get current user info."""
        try:
            client = await self._get_or_create_client()
            return await client.get_me()
        except Exception as e:
            print(f"[ERROR] Failed to get user: {e}")
            return None
    
    async def get_dialogs(self, limit: int = 100) -> List[Any]:
        """Get all dialogs (chats, groups, channels).
        
        Args:
            limit: Maximum number of dialogs to fetch
            
        Returns:
            List of dialog objects
        """
        try:
            client = await self._get_or_create_client()
            dialogs = await client.get_dialogs(limit=limit)
            return dialogs
        except Exception as e:
            print(f"[ERROR] Failed to get dialogs: {e}")
            return []
    
    async def get_dialog(self, dialog_id: int) -> Optional[Any]:
        """Get specific dialog by ID."""
        try:
            client = await self._get_or_create_client()
            dialog = await client.get_dialogs()
            for d in dialog:
                if d.id == dialog_id:
                    return d
            return None
        except Exception as e:
            print(f"[ERROR] Failed to get dialog: {e}")
            return None
    
    async def get_dialog_by_username(self, username: str) -> Optional[Any]:
        """Get dialog by username."""
        try:
            client = await self._get_or_create_client()
            entity = await client.get_entity(username)
            return entity
        except Exception as e:
            print(f"[ERROR] Failed to get dialog by username: {e}")
            return None
    
    async def get_messages(self, dialog_id: int, limit: int = 50) -> List[Any]:
        """Get messages from dialog.
        
        Args:
            dialog_id: Dialog ID
            limit: Number of messages to fetch
            
        Returns:
            List of message objects
        """
        try:
            client = await self._get_or_create_client()
            messages = await client.get_messages(dialog_id, limit=limit)
            return messages
        except Exception as e:
            print(f"[ERROR] Failed to get messages: {e}")
            return []
    
    async def send_message(self, dialog_id: int, text: str, 
                          reply_to: Optional[int] = None) -> Optional[int]:
        """Send message to dialog.
        
        Args:
            dialog_id: Dialog ID
            text: Message text
            reply_to: Reply to message ID (optional)
            
        Returns:
            Message ID or None
        """
        try:
            client = await self._get_or_create_client()
            message = await client.send_message(
                dialog_id,
                text,
                reply_to=reply_to
            )
            return message.id
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
            return None
    
    async def delete_message(self, msg_id: int) -> bool:
        """Delete message."""
        try:
            client = await self._get_or_create_client()
            await client.delete_messages(None, msg_id)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete message: {e}")
            return False
    
    async def edit_message(self, msg_id: int, text: str) -> bool:
        """Edit message."""
        try:
            client = await self._get_or_create_client()
            await client.edit_message(msg_id, text=text)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to edit message: {e}")
            return False
    
    async def forward_message(self, from_dialog: int, to_dialog: int, 
                             msg_id: int) -> Optional[int]:
        """Forward message."""
        try:
            client = await self._get_or_create_client()
            message = await client.forward_messages(
                to_dialog,
                msg_id,
                from_dialog
            )
            return message.id if message else None
        except Exception as e:
            print(f"[ERROR] Failed to forward message: {e}")
            return None
