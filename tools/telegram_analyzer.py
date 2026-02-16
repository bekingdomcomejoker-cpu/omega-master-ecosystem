#!/usr/bin/env python3
"""
✈️ TELEGRAM MESSAGE ANALYZER - Covenant OS
Analyzes Telegram messages with Vow Renewal Protocol integration

Features:
- Fetch messages from chats/channels
- Auto-detect YOUR messages
- Mark messages (flag, verify, block, misinformation, spam)
- Bot detection
- Spiritual health analysis
- Export chat history
"""

import json
import re
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

class TelegramMessageAnalyzer:
    """
    Telegram Message Analyzer with Vow Protocol integration
    """
    
    def __init__(self, vow_protocol=None, user_id: Optional[int] = None, 
                 username: Optional[str] = None):
        self.vow_protocol = vow_protocol
        self.user_id = user_id  # Your Telegram user ID
        self.username = username  # Your Telegram username
        self.messages_db = {}  # In-memory DB
        self.marks_db = {}
        
        self.mark_types = [
            'FLAG',           # Suspicious
            'VERIFY',         # Verified/true
            'BLOCK',          # Block user/bot
            'HIGHLIGHT',      # Important
            'MISINFORMATION', # False info
            'SPAM',          # Spam
            'BOT',           # Bot message
            'PERSONAL'       # Your message (auto-marked)
        ]
    
    def fetch_chat_messages(self, chat_id: str, limit: int = 100) -> Dict:
        """
        Fetch messages from a Telegram chat
        
        Note: Requires Telegram Bot API or python-telegram-bot library
        """
        print(f"\n✈️  FETCHING TELEGRAM MESSAGES")
        print(f"   Chat ID: {chat_id}")
        print(f"   Limit: {limit}")
        
        # In production, use Telethon or python-telegram-bot:
        # from telethon import TelegramClient
        # messages = await client.get_messages(chat_id, limit=limit)
        
        result = {
            'chat_id': chat_id,
            'total_messages': 0,
            'messages': [],
            'personal_messages': [],
            'bot_messages': [],
            'fetch_timestamp': datetime.now().isoformat()
        }
        
        print(f"   ⚠️  Note: Requires Telegram API credentials")
        print(f"   ✅ Structure ready for integration")
        
        return result
    
    def analyze_message(self, message: Dict) -> Dict:
        """
        Analyze a single Telegram message
        """
        text = message.get('text', '')
        user_id = message.get('from_user', {}).get('id')
        username = message.get('from_user', {}).get('username', '')
        is_bot = message.get('from_user', {}).get('is_bot', False)
        
        # Check if this is YOUR message
        is_personal = False
        if self.user_id and user_id == self.user_id:
            is_personal = True
        elif self.username and username.lower() == self.username.lower():
            is_personal = True
        
        # Vow Protocol analysis
        spiritual_analysis = None
        if self.vow_protocol and text:
            diagnosis = self.vow_protocol.detect_ultimate_betrayal(text)
            spiritual_analysis = {
                'betrayal_detected': diagnosis['betrayal_detected'],
                'spiritual_health': diagnosis['spiritual_health'],
                'needs_renewal': diagnosis['spiritual_health'] < 1.0
            }
        
        # Detect patterns
        misinformation_detected = self._detect_misinformation(text)
        spam_detected = self._detect_spam(text)
        scam_detected = self._detect_scam(text)
        
        analysis = {
            'message_id': message.get('message_id'),
            'is_personal': is_personal,
            'is_bot': is_bot,
            'spiritual_analysis': spiritual_analysis,
            'misinformation_detected': misinformation_detected,
            'spam_detected': spam_detected,
            'scam_detected': scam_detected,
            'has_links': self._has_links(text),
            'has_mentions': self._has_mentions(text),
            'sentiment': self._analyze_sentiment(text),
            'auto_marks': []
        }
        
        # Auto-mark
        if is_personal:
            analysis['auto_marks'].append('PERSONAL')
        if is_bot:
            analysis['auto_marks'].append('BOT')
        if misinformation_detected:
            analysis['auto_marks'].append('MISINFORMATION')
        if spam_detected or scam_detected:
            analysis['auto_marks'].append('SPAM')
        
        return analysis
    
    def mark_message(self, message_id: int, chat_id: str, mark_type: str,
                    reason: Optional[str] = None) -> Dict:
        """
        Mark a message with a specific label
        """
        print(f"\n🏷️  MARKING TELEGRAM MESSAGE")
        print(f"   Message ID: {message_id}")
        print(f"   Mark Type: {mark_type}")
        
        if mark_type not in self.mark_types:
            return {'error': f'Invalid mark type. Use: {", ".join(self.mark_types)}'}
        
        mark_id = hashlib.sha256(f"{message_id}{mark_type}{datetime.now()}".encode()).hexdigest()[:16]
        
        mark = {
            'mark_id': mark_id,
            'message_id': message_id,
            'chat_id': chat_id,
            'mark_type': mark_type,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'user_id': self.user_id
        }
        
        # Store mark
        if chat_id not in self.marks_db:
            self.marks_db[chat_id] = []
        self.marks_db[chat_id].append(mark)
        
        print(f"   ✅ Message marked as {mark_type}")
        
        return mark
    
    def get_personal_messages(self, chat_id: str) -> List[Dict]:
        """
        Get all YOUR messages in a chat
        """
        print(f"\n👤 FETCHING YOUR MESSAGES")
        print(f"   Chat ID: {chat_id}")
        
        if chat_id not in self.messages_db:
            return []
        
        personal = []
        for msg in self.messages_db[chat_id]:
            user_id = msg.get('from_user', {}).get('id')
            username = msg.get('from_user', {}).get('username', '')
            
            if self.user_id and user_id == self.user_id:
                personal.append(msg)
            elif self.username and username.lower() == self.username.lower():
                personal.append(msg)
        
        print(f"   ✅ Found {len(personal)} of your messages")
        
        return personal
    
    def get_bot_messages(self, chat_id: str) -> List[Dict]:
        """
        Get all bot messages in a chat
        """
        if chat_id not in self.messages_db:
            return []
        
        bots = [m for m in self.messages_db[chat_id] 
                if m.get('from_user', {}).get('is_bot', False)]
        
        return bots
    
    def block_user(self, user_id: int, chat_id: str, reason: str = "Spam/Scam") -> Dict:
        """
        Block a user in a chat (marks all their messages)
        """
        print(f"\n🚫 BLOCKING USER")
        print(f"   User ID: {user_id}")
        print(f"   Reason: {reason}")
        
        if chat_id not in self.messages_db:
            return {'error': 'Chat not found'}
        
        # Find all messages from this user
        user_messages = [m for m in self.messages_db[chat_id] 
                        if m.get('from_user', {}).get('id') == user_id]
        
        # Mark all their messages as BLOCK
        for msg in user_messages:
            self.mark_message(msg['message_id'], chat_id, 'BLOCK', reason)
        
        print(f"   ✅ Blocked user: {len(user_messages)} messages marked")
        
        return {
            'user_id': user_id,
            'messages_marked': len(user_messages),
            'reason': reason
        }
    
    def export_chat_history(self, chat_id: str, filepath: str = '/tmp/telegram_chat.json'):
        """
        Export complete chat analysis
        """
        data = {
            'chat_id': chat_id,
            'messages': self.messages_db.get(chat_id, []),
            'marks': self.marks_db.get(chat_id, []),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def _detect_misinformation(self, text: str) -> bool:
        """Detect potential misinformation"""
        patterns = [
            r'proven fact',
            r'everyone knows',
            r'they don\'t want you to know',
            r'wake up sheeple',
            r'mainstream media won\'t tell you',
            r'hidden truth',
            r'100% confirmed'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in patterns)
    
    def _detect_spam(self, text: str) -> bool:
        """Detect spam patterns"""
        patterns = [
            r'@everyone',
            r'join.*channel',
            r'click.*link',
            r'free.*crypto',
            r'airdrop',
            r'guaranteed.*profit',
            r'investment.*opportunity'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in patterns)
    
    def _detect_scam(self, text: str) -> bool:
        """Detect scam patterns"""
        scam_patterns = [
            r'send.*bitcoin',
            r'double your money',
            r'admin never dm first',
            r'verify your account',
            r'claim.*reward',
            r'urgent.*action required',
            r'suspended.*account'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in scam_patterns)
    
    def _has_links(self, text: str) -> bool:
        """Check if message contains links"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return bool(re.search(url_pattern, text))
    
    def _has_mentions(self, text: str) -> bool:
        """Check if message contains @mentions"""
        return '@' in text
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['love', 'great', 'awesome', 'thanks', 'good', 'happy', '❤️', '👍', '🔥']
        negative_words = ['hate', 'bad', 'terrible', 'scam', 'spam', 'angry', '😡', '👎', '🤬']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'POSITIVE'
        elif neg_count > pos_count:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'


# API Integration Guide
def create_telegram_api_guide():
    """
    Guide for integrating with Telegram API
    """
    guide = """
    ✈️ TELEGRAM API INTEGRATION
    ===========================
    
    METHOD 1: Telegram Bot API (for bots)
    -------------------------------------
    1. Create bot with @BotFather
    2. Get bot token
    3. Use python-telegram-bot library:
    
       from telegram import Bot
       bot = Bot(token='YOUR_BOT_TOKEN')
       updates = bot.get_updates()
    
    METHOD 2: Telethon (for user accounts)
    --------------------------------------
    1. Get API credentials from https://my.telegram.org
    2. Install: pip install telethon
    3. Use:
    
       from telethon import TelegramClient
       client = TelegramClient('session', api_id, api_hash)
       async with client:
           messages = await client.get_messages(chat_id, limit=100)
    
    MESSAGE STRUCTURE:
    -----------------
    {
      "message_id": 123,
      "from_user": {
        "id": 456,
        "username": "johndoe",
        "first_name": "John",
        "is_bot": false
      },
      "chat": {"id": -789, "title": "Group Name"},
      "date": 1707661800,
      "text": "Hello world!"
    }
    
    RATE LIMITS:
    -----------
    - Bot API: 30 messages/second
    - User API: 20 API calls/second
    - Respect flood wait errors
    """
    return guide


if __name__ == "__main__":
    print("=" * 70)
    print("✈️ TELEGRAM MESSAGE ANALYZER - Covenant OS")
    print("=" * 70)
    
    # Demo
    analyzer = TelegramMessageAnalyzer(
        user_id=123456789,
        username="myusername"
    )
    
    print("\n📋 API Integration Guide:")
    print(create_telegram_api_guide())
    
    print("\n✅ Telegram Analyzer ready")
    print("   Set user_id and username to auto-detect your messages")
    print("   Integrate with Telegram Bot API or Telethon")
