"""
Demo Script: BEFORE vs AFTER - Comparison
Shows the difference between in-memory and Redis-backed sessions
"""
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.redis_session import RedisSessionManager, ChatbotWithRedisSession


def demo_before_scenario():
    """Demo: In-memory only (context lost)"""
    print("\n" + "="*70)
    print("🔵 SCENARIO 1: BEFORE (In-Memory Only)")
    print("="*70)
    print("\nSimulating user conversation with in-memory storage...\n")
    
    # Simulate conversation history (in memory)
    conversation_history = []
    user_id = "user_123"
    
    print(f"📌 User ID: {user_id}")
    print(f"📍 Storage: Python list in RAM\n")
    
    # Message 1
    msg1 = {
        "role": "user",
        "content": "What is machine learning?",
        "timestamp": time.time()
    }
    conversation_history.append(msg1)
    print(f"✏️ User: {msg1['content']}")
    
    msg1_resp = {
        "role": "assistant",
        "content": "Machine learning is a subset of AI...",
        "timestamp": time.time()
    }
    conversation_history.append(msg1_resp)
    print(f"🤖 Bot: {msg1_resp['content']}\n")
    
    print(f"💾 Stored in memory: {len(conversation_history)} messages")
    
    # Simulate server restart
    print("\n⏳ Simulating server restart in 3 seconds...")
    print("   (In-memory data will be lost)")
    time.sleep(1)
    print("   2...")
    time.sleep(1)
    print("   1...")
    time.sleep(1)
    
    # After restart - conversation_history is gone!
    print("\n❌ SERVER RESTARTED")
    print("💨 All in-memory data lost!")
    
    conversation_history = []  # Reset
    print(f"📝 Messages after restart: {len(conversation_history)}")
    
    # User tries to continue
    print("\n👤 User reconnects and asks:")
    print("✏️ User: Tell me more about machine learning")
    print("🤖 Bot: ❌ I don't have context. What would you like to know?")
    print("😞 User: I just told you about machine learning!")
    print("\n⚠️  PROBLEM: Context lost! User has to repeat everything.")
    
    return True


def demo_after_scenario():
    """Demo: With Redis (context persists)"""
    print("\n\n" + "="*70)
    print("🔴 SCENARIO 2: AFTER (With Redis)")
    print("="*70)
    print("\nSimulating user conversation with Redis persistence...\n")
    
    # Initialize Redis session manager
    session_manager = RedisSessionManager()
    user_id = "user_456"
    
    print(f"📌 User ID: {user_id}")
    print(f"📍 Storage: Redis (persistent)")
    print(f"🔗 Redis Connected: {session_manager.is_connected}")
    
    if not session_manager.is_connected:
        print("\n⚠️  Note: Redis not available, using in-memory fallback")
        print("   (Install Redis: brew install redis)")
    
    print()
    
    # Create session
    session_manager.create_session(user_id)
    print("✅ Session created in Redis\n")
    
    # Message 1
    print("✏️ User: What is machine learning?")
    session_manager.add_message(
        user_id=user_id,
        role="user",
        content="What is machine learning?"
    )
    
    print("🤖 Bot: Machine learning is a subset of AI...")
    session_manager.add_message(
        user_id=user_id,
        role="assistant",
        content="Machine learning is a subset of AI that enables systems to learn from data."
    )
    
    history = session_manager.get_conversation_history(user_id)
    print(f"💾 Stored in Redis: {len(history)} messages\n")
    
    # Show session data
    print("📋 Session data in Redis:")
    session = session_manager.get_session(user_id)
    if session:
        print(f"   Created: {session.get('created_at', 'N/A')}")
        print(f"   Last Activity: {session.get('last_activity', 'N/A')}")
        print(f"   Messages: {len(history)}")
    
    # Simulate server restart
    print("\n⏳ Simulating server restart in 3 seconds...")
    print("   (Redis data will persist!)")
    time.sleep(1)
    print("   2...")
    time.sleep(1)
    print("   1...")
    time.sleep(1)
    
    # After restart - data still in Redis!
    print("\n✅ SERVER RESTARTED")
    print("📥 Loading session from Redis...\n")
    
    # Simulate new app instance loading session
    new_session_manager = RedisSessionManager()
    loaded_session = new_session_manager.get_session(user_id)
    
    if loaded_session:
        print("✅ Session loaded successfully!")
        loaded_history = new_session_manager.get_conversation_history(user_id)
        print(f"📝 Messages after restart: {len(loaded_history)}")
        
        print("\n👤 User reconnects and asks:")
        print("✏️ User: Tell me more about machine learning")
        
        # Show context
        context = new_session_manager.format_history_as_context(user_id, max_messages=2)
        print(f"\n📖 Context loaded:\n{context}\n")
        
        print("🤖 Bot: Based on our earlier discussion about ML,")
        print("        neural networks are a subset of deep learning...")
        print("\n✅ SUCCESS: Context persisted! Conversation continues seamlessly!")
    else:
        print("❌ Could not load session from Redis")
    
    return True


def comparison_table():
    """Show comparison table"""
    print("\n\n" + "="*70)
    print("📊 COMPARISON SUMMARY")
    print("="*70 + "\n")
    
    comparison = [
        ("Feature", "BEFORE (In-Memory)", "AFTER (Redis)"),
        ("-" * 25, "-" * 30, "-" * 30),
        ("Server Restart", "❌ Context Lost", "✅ Context Restored"),
        ("Idle Session", "❌ Lost immediately", "✅ Persists 1+ hour"),
        ("History Available", "❌ No", "✅ Yes"),
        ("Multiple Servers", "❌ No", "✅ Yes"),
        ("Automatic Cleanup", "❌ No", "✅ Yes (TTL)"),
        ("Production Ready", "❌ No", "✅ Yes"),
    ]
    
    for row in comparison:
        print(f"{row[0]:<25} | {row[1]:<30} | {row[2]:<30}")


def main():
    """Run demonstrations"""
    print("\n" + "="*70)
    print("🎓 RAG Chatbot Interview Scenario Demo")
    print("   Redis Integration: BEFORE vs AFTER")
    print("="*70)
    
    try:
        # Demo 1: Before scenario
        demo_before_scenario()
        
        # Demo 2: After scenario  
        demo_after_scenario()
        
        # Comparison
        comparison_table()
        
        print("\n" + "="*70)
        print("🎯 KEY TAKEAWAYS")
        print("="*70)
        print("""
✅ BEFORE Mode Problems:
   • Session data lost on server restart
   • Users lose context when idle
   • Can't scale horizontally
   • No conversation history

✅ AFTER Mode Benefits:
   • Session data persists in Redis
   • Users can idle and reconnect
   • Scales across multiple servers
   • Full conversation history available

💡 Interview Talking Points:
   1. Identified root cause (backend session design, not UI)
   2. Implemented Redis for persistence
   3. Added fallback for graceful degradation
   4. Enabled horizontal scaling
   5. Improved user experience significantly

🔧 To Try Yourself:
   1. Start Redis: redis-server
   2. Run BEFORE: python main.py
   3. Run AFTER: python main_with_redis.py --redis
   4. Notice the difference in behavior!
        """)
        
        print("="*70)
        print("✨ Demo completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: This demo works best with Redis running")
        print("Install Redis: brew install redis")
        print("Start Redis: redis-server")


if __name__ == "__main__":
    main()
