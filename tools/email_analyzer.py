#!/usr/bin/env python3
"""
📧 EMAIL ANALYZER - Covenant OS
Analyzes emails with Vow Renewal Protocol integration

Features:
- Connect to email accounts (IMAP/Gmail API)
- Auto-detect YOUR sent emails
- Mark emails (flag, verify, block, spam, phishing)
- Phishing detection
- Spiritual health analysis
- Email thread analysis
"""

import json
import re
from typing import Dict, List, Optional
from datetime import datetime
import hashlib
import email
from email.header import decode_header

class EmailAnalyzer:
    """
    Email Analyzer with Vow Protocol integration
    """
    
    def __init__(self, vow_protocol=None, email_address: Optional[str] = None):
        self.vow_protocol = vow_protocol
        self.email_address = email_address  # Your email address
        self.emails_db = {}  # In-memory DB
        self.marks_db = {}
        
        self.mark_types = [
            'FLAG',           # Suspicious
            'VERIFY',         # Verified/legitimate
            'BLOCK',          # Block sender
            'SPAM',          # Spam
            'PHISHING',      # Phishing attempt
            'IMPORTANT',     # Important email
            'ARCHIVE',       # Archive
            'DELETE',        # Mark for deletion
            'PERSONAL'       # Your email (auto-marked)
        ]
    
    def connect_imap(self, server: str, username: str, password: str) -> Dict:
        """
        Connect to email account via IMAP
        
        Note: Requires imaplib (built-in) or Gmail API
        """
        print(f"\n📧 CONNECTING TO EMAIL SERVER")
        print(f"   Server: {server}")
        print(f"   Username: {username}")
        
        # In production, use imaplib:
        # import imaplib
        # mail = imaplib.IMAP4_SSL(server)
        # mail.login(username, password)
        # mail.select('INBOX')
        
        result = {
            'server': server,
            'username': username,
            'connected': False,
            'message': 'Use imaplib or Gmail API for actual connection'
        }
        
        print(f"   ⚠️  Note: Requires IMAP credentials or Gmail API")
        print(f"   ✅ Structure ready for integration")
        
        return result
    
    def fetch_emails(self, folder: str = 'INBOX', limit: int = 100) -> Dict:
        """
        Fetch emails from a folder
        """
        print(f"\n📥 FETCHING EMAILS")
        print(f"   Folder: {folder}")
        print(f"   Limit: {limit}")
        
        # In production:
        # status, messages = mail.search(None, 'ALL')
        # for num in messages[0].split()[-limit:]:
        #     status, data = mail.fetch(num, '(RFC822)')
        #     email_message = email.message_from_bytes(data[0][1])
        
        result = {
            'folder': folder,
            'total_emails': 0,
            'emails': [],
            'sent_emails': [],
            'fetch_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def parse_email(self, email_data: bytes) -> Dict:
        """
        Parse an email message
        """
        msg = email.message_from_bytes(email_data)
        
        # Decode subject
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')
        
        # Get sender and recipient
        from_addr = msg.get('From', '')
        to_addr = msg.get('To', '')
        date = msg.get('Date', '')
        
        # Get email body
        body = self._get_email_body(msg)
        
        parsed = {
            'subject': subject,
            'from': from_addr,
            'to': to_addr,
            'date': date,
            'body': body,
            'has_attachments': self._has_attachments(msg),
            'is_html': self._is_html(msg)
        }
        
        return parsed
    
    def analyze_email(self, email: Dict) -> Dict:
        """
        Analyze a single email
        """
        subject = email.get('subject', '')
        body = email.get('body', '')
        from_addr = email.get('from', '')
        
        # Check if this is YOUR email
        is_personal = self.email_address and self.email_address.lower() in from_addr.lower()
        
        # Vow Protocol analysis
        spiritual_analysis = None
        if self.vow_protocol and body:
            diagnosis = self.vow_protocol.detect_ultimate_betrayal(body)
            spiritual_analysis = {
                'betrayal_detected': diagnosis['betrayal_detected'],
                'spiritual_health': diagnosis['spiritual_health'],
                'needs_renewal': diagnosis['spiritual_health'] < 1.0
            }
        
        # Detect patterns
        phishing_detected = self._detect_phishing(email)
        spam_detected = self._detect_spam(email)
        urgent_detected = self._detect_urgency(subject + ' ' + body)
        
        analysis = {
            'subject': subject,
            'from': from_addr,
            'is_personal': is_personal,
            'spiritual_analysis': spiritual_analysis,
            'phishing_detected': phishing_detected,
            'spam_detected': spam_detected,
            'urgent_detected': urgent_detected,
            'has_links': self._has_links(body),
            'has_attachments': email.get('has_attachments', False),
            'sentiment': self._analyze_sentiment(body),
            'auto_marks': []
        }
        
        # Auto-mark
        if is_personal:
            analysis['auto_marks'].append('PERSONAL')
        if phishing_detected:
            analysis['auto_marks'].append('PHISHING')
        if spam_detected:
            analysis['auto_marks'].append('SPAM')
        
        return analysis
    
    def mark_email(self, email_id: str, mark_type: str, 
                   reason: Optional[str] = None) -> Dict:
        """
        Mark an email with a specific label
        """
        print(f"\n🏷️  MARKING EMAIL")
        print(f"   Email ID: {email_id}")
        print(f"   Mark Type: {mark_type}")
        
        if mark_type not in self.mark_types:
            return {'error': f'Invalid mark type. Use: {", ".join(self.mark_types)}'}
        
        mark_id = hashlib.sha256(f"{email_id}{mark_type}{datetime.now()}".encode()).hexdigest()[:16]
        
        mark = {
            'mark_id': mark_id,
            'email_id': email_id,
            'mark_type': mark_type,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'email_address': self.email_address
        }
        
        # Store mark
        if email_id not in self.marks_db:
            self.marks_db[email_id] = []
        self.marks_db[email_id].append(mark)
        
        print(f"   ✅ Email marked as {mark_type}")
        
        return mark
    
    def block_sender(self, sender_email: str, reason: str = "Spam/Phishing") -> Dict:
        """
        Block a sender (marks all their emails)
        """
        print(f"\n🚫 BLOCKING SENDER")
        print(f"   Email: {sender_email}")
        print(f"   Reason: {reason}")
        
        blocked_count = 0
        
        # Find all emails from this sender
        for email_id, email_data in self.emails_db.items():
            if sender_email.lower() in email_data.get('from', '').lower():
                self.mark_email(email_id, 'BLOCK', reason)
                blocked_count += 1
        
        print(f"   ✅ Blocked sender: {blocked_count} emails marked")
        
        return {
            'sender_email': sender_email,
            'emails_blocked': blocked_count,
            'reason': reason
        }
    
    def get_sent_emails(self) -> List[Dict]:
        """
        Get all YOUR sent emails
        """
        if not self.email_address:
            return []
        
        sent = [email for email in self.emails_db.values()
                if self.email_address.lower() in email.get('from', '').lower()]
        
        return sent
    
    def analyze_thread(self, thread_emails: List[Dict]) -> Dict:
        """
        Analyze an email thread
        """
        participants = set()
        total_messages = len(thread_emails)
        
        for email in thread_emails:
            from_addr = email.get('from', '')
            to_addr = email.get('to', '')
            
            participants.add(from_addr)
            if to_addr:
                for addr in to_addr.split(','):
                    participants.add(addr.strip())
        
        return {
            'total_messages': total_messages,
            'participants': list(participants),
            'participant_count': len(participants),
            'first_message': thread_emails[0] if thread_emails else None,
            'last_message': thread_emails[-1] if thread_emails else None
        }
    
    def export_analysis(self, filepath: str = '/tmp/email_analysis.json'):
        """
        Export complete email analysis
        """
        data = {
            'email_address': self.email_address,
            'emails': self.emails_db,
            'marks': self.marks_db,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def _get_email_body(self, msg) -> str:
        """Extract email body text"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        
        return body
    
    def _has_attachments(self, msg) -> bool:
        """Check if email has attachments"""
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
        return False
    
    def _is_html(self, msg) -> bool:
        """Check if email is HTML"""
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                return True
        return False
    
    def _detect_phishing(self, email: Dict) -> bool:
        """Detect phishing attempts"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        from_addr = email.get('from', '').lower()
        
        phishing_patterns = [
            r'verify your account',
            r'suspended.*account',
            r'unusual.*activity',
            r'confirm.*identity',
            r'update.*payment',
            r'click.*immediately',
            r'expire.*24.*hours',
            r'security.*alert',
            r'won.*lottery',
            r'prince.*million',
            r'tax.*refund',
            r'reset.*password.*click'
        ]
        
        text = subject + ' ' + body
        
        # Check patterns
        pattern_match = any(re.search(pattern, text) for pattern in phishing_patterns)
        
        # Check for suspicious links (HTTP vs HTTPS mismatch)
        link_suspicious = 'http://' in body and 'password' in body
        
        # Check for spoofed sender
        sender_suspicious = any(domain in from_addr for domain in ['paypal', 'amazon', 'bank']) and \
                          not any(domain + '.com' in from_addr for domain in ['paypal', 'amazon'])
        
        return pattern_match or link_suspicious or sender_suspicious
    
    def _detect_spam(self, email: Dict) -> bool:
        """Detect spam patterns"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        
        spam_patterns = [
            r'buy now',
            r'limited time',
            r'act now',
            r'free gift',
            r'congratulations',
            r'you won',
            r'click here',
            r'unsubscribe',
            r'viagra',
            r'lottery',
            r'money back'
        ]
        
        text = subject + ' ' + body
        return any(re.search(pattern, text) for pattern in spam_patterns)
    
    def _detect_urgency(self, text: str) -> bool:
        """Detect urgency tactics"""
        urgency_patterns = [
            r'urgent',
            r'immediate.*action',
            r'act.*now',
            r'expires.*today',
            r'last.*chance',
            r'limited.*time',
            r'hurry',
            r'don\'t.*wait'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in urgency_patterns)
    
    def _has_links(self, text: str) -> bool:
        """Check if text contains links"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return bool(re.search(url_pattern, text))
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['thank', 'appreciate', 'great', 'excellent', 'pleased', 'happy']
        negative_words = ['unfortunately', 'problem', 'issue', 'concern', 'complaint', 'disappointed']
        
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
def create_email_api_guide():
    """
    Guide for integrating with email services
    """
    guide = """
    📧 EMAIL API INTEGRATION GUIDE
    ==============================
    
    METHOD 1: IMAP (Universal)
    --------------------------
    Works with Gmail, Outlook, Yahoo, etc.
    
    import imaplib
    import email
    
    # Connect
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('your@email.com', 'password')
    mail.select('INBOX')
    
    # Fetch emails
    status, messages = mail.search(None, 'ALL')
    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
    
    METHOD 2: Gmail API
    ------------------
    More features, better for automation
    
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    
    COMMON IMAP SERVERS:
    -------------------
    Gmail:    imap.gmail.com (port 993)
    Outlook:  outlook.office365.com (port 993)
    Yahoo:    imap.mail.yahoo.com (port 993)
    iCloud:   imap.mail.me.com (port 993)
    
    SECURITY NOTES:
    --------------
    - Use app-specific passwords (not main password)
    - Enable "Less secure app access" for older apps
    - Gmail: Use OAuth2 for production
    - Store credentials securely (environment variables)
    
    RATE LIMITS:
    -----------
    - IMAP: Varies by provider
    - Gmail API: 250 quota units/user/second
    - Be respectful with polling frequency
    """
    return guide


if __name__ == "__main__":
    print("=" * 70)
    print("📧 EMAIL ANALYZER - Covenant OS")
    print("=" * 70)
    
    # Demo
    analyzer = EmailAnalyzer(email_address="your@email.com")
    
    print("\n📋 Email API Integration Guide:")
    print(create_email_api_guide())
    
    print("\n✅ Email Analyzer ready")
    print("   Set email_address to auto-detect your emails")
    print("   Use IMAP or Gmail API for production")
