"""
Redis Session Manager for RAG Chatbot
Handles conversation state persistence and session management
"""
import redis
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ConversationMessage:
    """Represents a single message in conversation"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    sources: Optional[List[Dict]] = None


class RedisSessionManager:
    """Manage conversation sessions using Redis"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        session_timeout: int = 3600  # 1 hour default
    ):
        """
        Initialize Redis connection
        
        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number
            password: Redis password (if protected)
            session_timeout: Session timeout in seconds (default: 1 hour)
        """
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logger.info("✅ Connected to Redis successfully")
            self.is_connected = True
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to Redis: {e}")
            logger.warning("Falling back to in-memory session storage")
            self.redis_client = None
            self.is_connected = False
        
        self.session_timeout = session_timeout
        self.in_memory_sessions = {}  # Fallback storage

    @staticmethod
    def _safe_json_loads(value: Optional[str]) -> Any:
        """Best-effort JSON loader that tolerates empty/None values."""
        if not value:
            return None
        try:
            return json.loads(value)
        except Exception:
            logger.warning("⚠️ Stored value is not valid JSON; returning raw string")
            return value
    
    def create_session(self, user_id: str) -> str:
        """Create a new session for user"""
        session_key = f"session:{user_id}"
        
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            # Store JSON strings in Redis for consistency
            "messages": json.dumps([]),
            "metadata": json.dumps({})
        }
        
        if self.is_connected:
            self.redis_client.hset(
                session_key,
                mapping=session_data
            )
            self.redis_client.expire(session_key, self.session_timeout)
            logger.info(f"✅ Session created for user {user_id}")
        else:
            self.in_memory_sessions[session_key] = session_data
        
        return session_key
    
    def get_session(self, user_id: str) -> Optional[Dict]:
        """Retrieve session data for user"""
        session_key = f"session:{user_id}"
        
        try:
            if self.is_connected:
                session_data = self.redis_client.hgetall(session_key)
                if session_data:
                    # Parse JSON fields with fallback
                    if session_data.get("messages"):
                        session_data["messages"] = self._safe_json_loads(session_data["messages"]) or []
                    if session_data.get("metadata"):
                        session_data["metadata"] = self._safe_json_loads(session_data["metadata"]) or {}
                    
                    logger.info(f"✅ Session retrieved from Redis for {user_id}")
                    return session_data
            else:
                if session_key in self.in_memory_sessions:
                    logger.info(f"✅ Session retrieved from memory for {user_id}")
                    return self.in_memory_sessions[session_key]
            
            logger.warning(f"⚠️ Session not found for user {user_id}")
            return None
        
        except Exception as e:
            logger.error(f"❌ Error retrieving session: {e}")
            return None
    
    def add_message(
        self,
        user_id: str,
        role: str,
        content: str,
        sources: Optional[List[Dict]] = None
    ) -> bool:
        """Add a message to conversation history"""
        session_key = f"session:{user_id}"
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "sources": sources or []
        }
        
        try:
            if self.is_connected:
                # Get current messages
                messages_data = self.redis_client.hget(session_key, "messages")
                messages = self._safe_json_loads(messages_data) if messages_data else []
                
                # Add new message
                messages.append(message)
                
                # Update session
                self.redis_client.hset(session_key, "messages", json.dumps(messages))
                self.redis_client.hset(session_key, "last_activity", datetime.now().isoformat())
                self.redis_client.expire(session_key, self.session_timeout)
                
                logger.info(f"✅ Message added to session {user_id} (Redis)")
            else:
                if session_key not in self.in_memory_sessions:
                    self.in_memory_sessions[session_key] = {
                        "user_id": user_id,
                        "messages": [],
                        "metadata": {}
                    }
                
                self.in_memory_sessions[session_key]["messages"].append(message)
                self.in_memory_sessions[session_key]["last_activity"] = datetime.now().isoformat()
                logger.info(f"✅ Message added to session {user_id} (Memory)")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error adding message: {e}")
            return False
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get all messages in conversation"""
        session_key = f"session:{user_id}"
        
        try:
            if self.is_connected:
                messages_data = self.redis_client.hget(session_key, "messages")
                messages = self._safe_json_loads(messages_data) if messages_data else []
            else:
                messages = self.in_memory_sessions.get(session_key, {}).get("messages", [])
            
            return messages
        
        except Exception as e:
            logger.error(f"❌ Error retrieving history: {e}")
            return []
    
    def get_last_n_messages(self, user_id: str, n: int = 5) -> List[Dict]:
        """Get last N messages from conversation"""
        history = self.get_conversation_history(user_id)
        return history[-n:] if len(history) > n else history
    
    def format_history_as_context(self, user_id: str, max_messages: int = 5) -> str:
        """Format conversation history for LLM context"""
        messages = self.get_last_n_messages(user_id, max_messages)
        
        if not messages:
            return ""
        
        history_lines = ["Previous conversation:"]
        for msg in messages:
            role = "You" if msg["role"] == "user" else "Assistant"
            history_lines.append(f"{role}: {msg['content'][:100]}...")
        
        return "\n".join(history_lines)
    
    def clear_session(self, user_id: str) -> bool:
        """Clear/delete session"""
        session_key = f"session:{user_id}"
        
        try:
            if self.is_connected:
                self.redis_client.delete(session_key)
                logger.info(f"✅ Session cleared for {user_id} (Redis)")
            else:
                if session_key in self.in_memory_sessions:
                    del self.in_memory_sessions[session_key]
                    logger.info(f"✅ Session cleared for {user_id} (Memory)")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error clearing session: {e}")
            return False
    
    def get_all_active_sessions(self) -> List[str]:
        """Get all active session keys"""
        try:
            if self.is_connected:
                keys = self.redis_client.keys("session:*")
                logger.info(f"✅ Found {len(keys)} active sessions in Redis")
                return keys
            else:
                keys = list(self.in_memory_sessions.keys())
                logger.info(f"✅ Found {len(keys)} active sessions in memory")
                return keys
        
        except Exception as e:
            logger.error(f"❌ Error getting sessions: {e}")
            return []
    
    def get_session_stats(self) -> Dict:
        """Get statistics about all sessions"""
        try:
            if self.is_connected:
                info = self.redis_client.info()
                sessions = self.redis_client.keys("session:*")
                
                stats = {
                    "backend": "Redis",
                    "total_sessions": len(sessions),
                    "redis_memory_used": info.get("used_memory_human", "N/A"),
                    "redis_connected_clients": info.get("connected_clients", 0)
                }
            else:
                stats = {
                    "backend": "In-Memory",
                    "total_sessions": len(self.in_memory_sessions),
                    "memory_note": "Fallback mode (Redis not available)"
                }
            
            return stats
        
        except Exception as e:
            logger.error(f"❌ Error getting stats: {e}")
            return {}
    
    def extend_session(self, user_id: str) -> bool:
        """Extend session timeout on activity"""
        session_key = f"session:{user_id}"
        
        try:
            if self.is_connected:
                self.redis_client.expire(session_key, self.session_timeout)
                logger.info(f"✅ Session extended for {user_id}")
                return True
            else:
                logger.info(f"✅ Session activity recorded for {user_id}")
                return True
        
        except Exception as e:
            logger.error(f"❌ Error extending session: {e}")
            return False

    # ---------- FSM / metadata helpers ----------
    def get_metadata(self, user_id: str) -> Dict:
        """Retrieve metadata blob for a user (used for FSM state)."""
        session_key = f"session:{user_id}"
        try:
            if self.is_connected:
                raw = self.redis_client.hget(session_key, "metadata")
                metadata = self._safe_json_loads(raw) or {}
            else:
                metadata = self.in_memory_sessions.get(session_key, {}).get("metadata", {})
            return metadata if isinstance(metadata, dict) else {}
        except Exception as e:
            logger.error(f"❌ Error getting metadata: {e}")
            return {}

    def set_metadata(self, user_id: str, metadata: Dict) -> bool:
        """Replace metadata blob for a user session (persists FSM state)."""
        session_key = f"session:{user_id}"
        try:
            if self.is_connected:
                self.redis_client.hset(session_key, "metadata", json.dumps(metadata))
                self.redis_client.hset(session_key, "last_activity", datetime.now().isoformat())
                self.redis_client.expire(session_key, self.session_timeout)
            else:
                if session_key not in self.in_memory_sessions:
                    self.in_memory_sessions[session_key] = {
                        "user_id": user_id,
                        "messages": [],
                        "metadata": {}
                    }
                self.in_memory_sessions[session_key]["metadata"] = metadata
                self.in_memory_sessions[session_key]["last_activity"] = datetime.now().isoformat()
            return True
        except Exception as e:
            logger.error(f"❌ Error setting metadata: {e}")
            return False

    def set_fsm_state(self, user_id: str, state: str, context: Optional[Dict] = None) -> bool:
        """Persist a simple FSM state for this user."""
        meta = self.get_metadata(user_id)
        meta["fsm"] = {
            "state": state,
            "context": context or {},
            "updated_at": datetime.now().isoformat()
        }
        return self.set_metadata(user_id, meta)

    def get_fsm_state(self, user_id: str) -> Optional[Dict]:
        """Fetch the FSM state blob for this user (state + context)."""
        meta = self.get_metadata(user_id)
        return meta.get("fsm")


class ChatbotWithRedisSession:
    """Wrapper to add Redis session management to chatbot"""
    
    def __init__(self, chatbot, session_manager: RedisSessionManager):
        self.chatbot = chatbot
        self.session_manager = session_manager
    
    def chat(self, user_id: str, query: str, use_history: bool = True) -> Dict:
        """
        Chat with session persistence
        
        Args:
            user_id: Unique user identifier
            query: User's question
            use_history: Whether to use conversation history
        
        Returns:
            Response with sources and metadata
        """
        # Get or create session
        session = self.session_manager.get_session(user_id)
        if not session:
            self.session_manager.create_session(user_id)
        
        # Enhance query with history if enabled
        if use_history:
            history_context = self.session_manager.format_history_as_context(user_id)
            if history_context:
                enhanced_query = f"{history_context}\n\nCurrent question: {query}"
            else:
                enhanced_query = query
        else:
            enhanced_query = query
        
        # Get response from chatbot
        response = self.chatbot.chat(enhanced_query)
        
        # Store in Redis
        self.session_manager.add_message(
            user_id=user_id,
            role="user",
            content=query,
            sources=None
        )
        
        self.session_manager.add_message(
            user_id=user_id,
            role="assistant",
            content=response["response"],
            sources=response.get("source_documents", [])
        )
        
        # Extend session timeout
        self.session_manager.extend_session(user_id)
        
        # Add conversation info to response
        response["user_id"] = user_id
        response["conversation_length"] = len(
            self.session_manager.get_conversation_history(user_id)
        )
        response["session_persisted"] = True
        response["backend"] = "Redis" if self.session_manager.is_connected else "Memory"
        
        return response
    
    def get_user_history(self, user_id: str) -> List[Dict]:
        """Get all messages for a user"""
        return self.session_manager.get_conversation_history(user_id)
    
    def clear_user_session(self, user_id: str) -> bool:
        """Clear user's session"""
        return self.session_manager.clear_session(user_id)
