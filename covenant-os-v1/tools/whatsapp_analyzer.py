#!/usr/bin/env python3
"""
💬 WHATSAPP MESSAGE ANALYZER - Covenant OS
Analyzes WhatsApp messages with Vow Renewal Protocol integration

Features:
- Parse WhatsApp chat exports
- Auto-detect YOUR messages
- Mark messages (flag, verify, block, misinformation, spam)
- Media detection
- Spiritual health analysis
- Group chat analysis
"""

import json
import re
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

class WhatsAppMessageAnalyzer:
    """
    WhatsApp Message Analyzer with Vow Protocol integration
    """
    
    def __init__(self, vow_protocol=None, phone_number: Optional[str] = None,
                 name: Optional[str] = None):
        self.vow_protocol = vow_protocol
        self.phone_number = phone_number  # Your WhatsApp number
        self.name = name  # Your name in chats
        self.messages_db = {}  # In-memory DB
        self.marks_db = {}
        
        self.mark_types = [
            'FLAG',           # Suspicious
            'VERIFY',         # Verified/true
            'BLOCK',          # Block contact
            'HIGHLIGHT',      # Important
            'MISINFORMATION', # False info
            'SPAM',          # Spam
            'SCAM',          # Scam attempt
            'PERSONAL'       # Your message (auto-marked)
        ]
    
    def parse_chat_export(self, filepath: str) -> Dict:
        """
        Parse WhatsApp chat export (.txt file)
        
        Format: [DD/MM/YYYY, HH:MM:SS] Contact Name: Message
        """
        print(f"\n💬 PARSING WHATSAPP CHAT EXPORT")
        print(f"   File: {filepath}")
        
        messages = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # WhatsApp export pattern
            # [01/02/2026, 10:30:15] John Doe: Hello world!
            pattern = r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.+)'
            
            matches = re.finditer(pattern, content, re.MULTILINE)
            
            for match in matches:
                date, time, sender, text = match.groups()
                
                message = {
                    'date': date,
                    'time': time,
                    'sender': sender.strip(),
                    'text': text.strip(),
                    'is_media': self._is_media_message(text),
                    'timestamp': f"{date} {time}"
                }
                
                messages.append(message)
            
            print(f"   ✅ Parsed {len(messages)} messages")
            
        except FileNotFoundError:
            print(f"   ❌ File not found: {filepath}")
            return {'error': 'File not found'}
        
        result = {
            'filepath': filepath,
            'total_messages': len(messages),
            'messages': messages,
            'personal_messages': self._filter_personal_messages(messages),
            'parse_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def analyze_message(self, message: Dict) -> Dict:
        """
        Analyze a single WhatsApp message
        """
        text = message.get('text', '')
        sender = message.get('sender', '')
        
        # Check if this is YOUR message
        is_personal = False
        if self.name and sender.lower() == self.name.lower():
            is_personal = True
        elif self.phone_number and self.phone_number in sender:
            is_personal = True
        
        # Vow Protocol analysis
        spiritual_analysis = None
        if self.vow_protocol and text and not message.get('is_media'):
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
        forward_detected = self._is_forwarded(text)
        
        analysis = {
            'sender': sender,
            'is_personal': is_personal,
            'is_media': message.get('is_media', False),
            'is_forwarded': forward_detected,
            'spiritual_analysis': spiritual_analysis,
            'misinformation_detected': misinformation_detected,
            'spam_detected': spam_detected,
            'scam_detected': scam_detected,
            'has_links': self._has_links(text),
            'sentiment': self._analyze_sentiment(text),
            'auto_marks': []
        }
        
        # Auto-mark
        if is_personal:
            analysis['auto_marks'].append('PERSONAL')
        if misinformation_detected:
            analysis['auto_marks'].append('MISINFORMATION')
        if spam_detected:
            analysis['auto_marks'].append('SPAM')
        if scam_detected:
            analysis['auto_marks'].append('SCAM')
        
        return analysis
    
    def mark_message(self, message_index: int, chat_id: str, mark_type: str,
                    reason: Optional[str] = None) -> Dict:
        """
        Mark a message with a specific label
        """
        print(f"\n🏷️  MARKING WHATSAPP MESSAGE")
        print(f"   Message Index: {message_index}")
        print(f"   Mark Type: {mark_type}")
        
        if mark_type not in self.mark_types:
            return {'error': f'Invalid mark type. Use: {", ".join(self.mark_types)}'}
        
        mark_id = hashlib.sha256(f"{message_index}{mark_type}{datetime.now()}".encode()).hexdigest()[:16]
        
        mark = {
            'mark_id': mark_id,
            'message_index': message_index,
            'chat_id': chat_id,
            'mark_type': mark_type,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store mark
        if chat_id not in self.marks_db:
            self.marks_db[chat_id] = []
        self.marks_db[chat_id].append(mark)
        
        print(f"   ✅ Message marked as {mark_type}")
        
        return mark
    
    def get_personal_messages(self, messages: List[Dict]) -> List[Dict]:
        """
        Get all YOUR messages from a chat
        """
        return self._filter_personal_messages(messages)
    
    def _filter_personal_messages(self, messages: List[Dict]) -> List[Dict]:
        """Filter messages to find your own"""
        personal = []
        
        for msg in messages:
            sender = msg.get('sender', '')
            
            if self.name and sender.lower() == self.name.lower():
                personal.append(msg)
            elif self.phone_number and self.phone_number in sender:
                personal.append(msg)
        
        return personal
    
    def get_group_participants(self, messages: List[Dict]) -> List[str]:
        """
        Get list of all participants in a group chat
        """
        participants = set()
        
        for msg in messages:
            sender = msg.get('sender', '')
            if sender:
                participants.add(sender)
        
        return sorted(list(participants))
    
    def analyze_group_activity(self, messages: List[Dict]) -> Dict:
        """
        Analyze group chat activity
        """
        participants = {}
        
        for msg in messages:
            sender = msg.get('sender', '')
            if sender:
                if sender not in participants:
                    participants[sender] = {
                        'message_count': 0,
                        'media_count': 0,
                        'first_message': msg.get('timestamp'),
                        'last_message': msg.get('timestamp')
                    }
                
                participants[sender]['message_count'] += 1
                participants[sender]['last_message'] = msg.get('timestamp')
                
                if msg.get('is_media'):
                    participants[sender]['media_count'] += 1
        
        # Sort by message count
        sorted_participants = sorted(
            participants.items(),
            key=lambda x: x[1]['message_count'],
            reverse=True
        )
        
        return {
            'total_participants': len(participants),
            'total_messages': len(messages),
            'participants': dict(sorted_participants),
            'most_active': sorted_participants[0][0] if sorted_participants else None
        }
    
    def export_analysis(self, chat_id: str, filepath: str = '/tmp/whatsapp_analysis.json'):
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
    
    def _is_media_message(self, text: str) -> bool:
        """Check if message is media attachment"""
        media_patterns = [
            '<Media omitted>',
            'image omitted',
            'video omitted',
            'audio omitted',
            'sticker omitted',
            'document omitted',
            'Contact card omitted'
        ]
        
        text_lower = text.lower()
        return any(pattern.lower() in text_lower for pattern in media_patterns)
    
    def _is_forwarded(self, text: str) -> bool:
        """Check if message is forwarded"""
        return text.startswith('Forwarded:') or '↩️' in text
    
    def _detect_misinformation(self, text: str) -> bool:
        """Detect potential misinformation"""
        patterns = [
            r'forward.*10.*people',
            r'share.*family.*friends',
            r'proven.*fact',
            r'doctors.*hate',
            r'government.*hiding',
            r'wake up',
            r'they don\'t want you to know'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in patterns)
    
    def _detect_spam(self, text: str) -> bool:
        """Detect spam patterns"""
        patterns = [
            r'click.*link',
            r'limited.*offer',
            r'free.*gift',
            r'congratulations.*won',
            r'claim.*prize',
            r'urgent.*action'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in patterns)
    
    def _detect_scam(self, text: str) -> bool:
        """Detect scam patterns"""
        scam_patterns = [
            r'send.*money',
            r'bank.*details',
            r'account.*suspended',
            r'verify.*identity',
            r'tax.*refund',
            r'lottery.*winner',
            r'inheritance.*claim'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in scam_patterns)
    
    def _has_links(self, text: str) -> bool:
        """Check if message contains links"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return bool(re.search(url_pattern, text))
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['love', 'great', 'awesome', 'thanks', 'happy', '❤️', '😊', '👍', '🎉']
        negative_words = ['hate', 'bad', 'terrible', 'sad', 'angry', '😡', '😢', '👎', '💔']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'POSITIVE'
        elif neg_count > pos_count:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'


# Integration Guide
def create_whatsapp_guide():
    """
    Guide for exporting and analyzing WhatsApp chats
    """
    guide = """
    💬 WHATSAPP CHAT EXPORT GUIDE
    ============================
    
    HOW TO EXPORT A CHAT:
    --------------------
    1. Open WhatsApp
    2. Open the chat you want to export
    3. Tap the three dots (⋮) menu
    4. Select "More" → "Export chat"
    5. Choose "Without Media" or "Include Media"
    6. Save the .txt file
    
    EXPORT FORMAT:
    -------------
    [01/02/2026, 10:30:15] John Doe: Hello!
    [01/02/2026, 10:31:22] Jane Smith: Hi there!
    [01/02/2026, 10:32:45] John Doe: <Media omitted>
    
    NOTES:
    -----
    - WhatsApp doesn't provide API access for messages
    - Must use chat export feature
    - Media files can be included or omitted
    - Export includes system messages (joins, leaves, etc.)
    - Maximum export: 40,000 messages without media
    
    USAGE:
    -----
    analyzer = WhatsAppMessageAnalyzer(name="Your Name")
    result = analyzer.parse_chat_export("chat.txt")
    
    # Analyze all messages
    for msg in result['messages']:
        analysis = analyzer.analyze_message(msg)
        print(analysis)
    """
    return guide


if __name__ == "__main__":
    print("=" * 70)
    print("💬 WHATSAPP MESSAGE ANALYZER - Covenant OS")
    print("=" * 70)
    
    # Demo
    analyzer = WhatsAppMessageAnalyzer(
        name="Your Name",
        phone_number="+1234567890"
    )
    
    print("\n📋 WhatsApp Export Guide:")
    print(create_whatsapp_guide())
    
    print("\n✅ WhatsApp Analyzer ready")
    print("   Export a chat from WhatsApp")
    print("   Use parse_chat_export('file.txt') to analyze")
