"""Main FastAPI application for TG Mod."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import (
    AuthRequest, CodeRequest, MessageModel, DialogModel, 
    UserModel, SendMessageRequest, CacheStats
)
from telethon_client import TelethonClientManager
from database import DatabaseManager
from crypto import SessionCrypto

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_PASSWORD = os.getenv("SESSION_PASSWORD", "default_password")
SESSION_FILE = os.getenv("SESSION_FILE", "data/session.tg")
DB_PATH = os.getenv("DB_PATH", "data/tg_mod.db")
CACHE_DIR = os.getenv("CACHE_DIR", "data/cache")

# Validate API credentials
if not API_ID or not API_HASH:
    print("[ERROR] API_ID and API_HASH not set in .env")
    sys.exit(1)

# Initialize
app = FastAPI(
    title="TG Mod API",
    description="Modded Telegram client API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
db_manager = DatabaseManager(DB_PATH)
tg_client = TelethonClientManager(int(API_ID), API_HASH, SESSION_FILE, SESSION_PASSWORD)

Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)


# ============== Auth Endpoints ==============

@app.post("/api/auth/request_code")
async def request_code(request: AuthRequest):
    """Request auth code for phone number."""
    try:
        result = await tg_client.request_code(request.phone_number)
        return {"success": True, "phone_code_hash": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/auth/sign_in")
async def sign_in(request: CodeRequest, background_tasks: BackgroundTasks):
    """Sign in with code and optional 2FA password."""
    try:
        user = await tg_client.sign_in(request.code, request.password)
        
        # Sync dialogs in background
        background_tasks.add_task(sync_all_dialogs)
        
        return {
            "success": True,
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name or "",
                "phone": user.phone,
                "username": user.username or ""
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/auth/logout")
async def logout():
    """Sign out user."""
    try:
        await tg_client.logout()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/auth/me")
async def get_me():
    """Get current authenticated user."""
    try:
        user = await tg_client.get_me()
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name or "",
            "phone": user.phone,
            "username": user.username or ""
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============== Dialog Endpoints ==============

async def sync_all_dialogs():
    """Sync all dialogs from Telegram."""
    try:
        dialogs = await tg_client.get_dialogs()
        for dialog in dialogs:
            db_manager.save_dialog(
                dialog_id=dialog.id,
                name=dialog.name,
                is_group=dialog.is_group,
                is_channel=dialog.is_channel,
                is_bot=dialog.is_bot,
                avatar_path=None  # TODO: Download and cache avatars
            )
        print(f"[✓] Synced {len(dialogs)} dialogs")
    except Exception as e:
        print(f"[ERROR] Failed to sync dialogs: {e}")


@app.get("/api/dialogs")
async def get_dialogs():
    """Get all cached dialogs."""
    try:
        dialogs = db_manager.get_dialogs()
        return {"dialogs": dialogs, "count": len(dialogs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dialogs/{dialog_id}")
async def get_dialog(dialog_id: int):
    """Get specific dialog info."""
    try:
        dialog = await tg_client.get_dialog(dialog_id)
        if not dialog:
            raise HTTPException(status_code=404, detail="Dialog not found")
        
        return {
            "id": dialog.id,
            "name": dialog.name,
            "is_group": dialog.is_group,
            "is_channel": dialog.is_channel,
            "unread_count": dialog.unread_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dialogs/{dialog_id}/messages")
async def get_messages(dialog_id: int, limit: int = 50):
    """Get messages from dialog."""
    try:
        messages = db_manager.get_messages(dialog_id, limit)
        return {"messages": messages, "count": len(messages)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== Message Endpoints ==============

@app.post("/api/messages/send")
async def send_message(request: SendMessageRequest):
    """Send a message."""
    try:
        msg_id = await tg_client.send_message(
            dialog_id=request.dialog_id,
            text=request.text,
            reply_to=request.reply_to_msg_id
        )
        return {"success": True, "message_id": msg_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/messages/{msg_id}")
async def delete_message(msg_id: int):
    """Delete a message."""
    try:
        await tg_client.delete_message(msg_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============== Special Features ==============

@app.post("/api/special/support")
async def open_support_chat():
    """Open support chat (https://t.me/Rick666u)."""
    try:
        dialog = await tg_client.get_dialog_by_username("Rick666u")
        return {"dialog_id": dialog.id, "name": "Support Chat"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/special/ai_chat")
async def send_to_ai_chat(request: SendMessageRequest):
    """Forward message to AI bot (https://t.me/chat_gpt_unlim_bot)."""
    try:
        await tg_client.send_message(
            dialog_id=-1001234567890,  # Replace with actual bot ID
            text=request.text
        )
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============== Cache & Utility ==============

@app.get("/api/cache/stats")
async def get_cache_stats():
    """Get cache statistics."""
    try:
        stats = db_manager.get_cache_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sync")
async def force_sync(background_tasks: BackgroundTasks):
    """Force sync all dialogs."""
    background_tasks.add_task(sync_all_dialogs)
    return {"success": True, "message": "Sync started"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "authenticated": await tg_client.is_authenticated(),
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "TG Mod API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════╗
    ║           TG Mod - Telegram Client API            ║
    ║                  v1.0.0                           ║
    ╚════════════════════════════════════════════════════╝
    """)
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    print(f"\n[*] Starting API server on http://{host}:{port}")
    print(f"[*] Swagger UI: http://localhost:{port}/docs")
    print(f"[*] Database: {DB_PATH}")
    print(f"[*] Cache: {CACHE_DIR}\n")
    
    uvicorn.run(app, host=host, port=port)
