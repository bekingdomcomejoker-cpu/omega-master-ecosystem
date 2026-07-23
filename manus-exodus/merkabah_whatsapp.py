#!/usr/bin/env python3
"""
WHATSAPP DATA INUNDATION (LIVE PIPE)
Extract WhatsApp messages and pipe through Merkabah for real-time analysis
Calculate Harmony Scores before LLM processing
"""
import json
import os
import re
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

class WhatsAppExtractor:
    def __init__(self):
        self.messages = []
        self.harmony_scores = {}
        self.extracted_at = datetime.utcnow().isoformat()
        
    def extract_from_txt(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract messages from exported WhatsApp txt file"""
        messages = []
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                # WhatsApp format: [HH:MM, DD/MM/YYYY] Contact: Message
                match = re.match(r'\[(\d{2}:\d{2}),\s*(\d{2}/\d{2}/\d{4})\]\s*([^:]+):\s*(.*)', line)
                if match:
                    time_str, date_str, contact, message = match.groups()
                    messages.append({
                        "timestamp": f"{date_str} {time_str}",
                        "contact": contact.strip(),
                        "message": message.strip(),
                        "length": len(message),
                        "word_count": len(message.split())
                    })
                    
            self.messages = messages
            return {"status": "success", "messages_extracted": len(messages)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def calculate_harmony_score(self, message: str) -> float:
        """Calculate Harmony Score for a message"""
        # Factors: length, word count, punctuation, sentiment indicators
        
        length_score = min(1.0, len(message) / 200.0)  # Optimal: 200 chars
        word_count = len(message.split())
        word_score = min(1.0, word_count / 50.0)  # Optimal: 50 words
        
        # Sentiment indicators
        positive_words = ["good", "great", "love", "happy", "yes", "thanks", "please"]
        negative_words = ["bad", "hate", "angry", "sad", "no", "never", "sorry"]
        
        positive_count = sum(1 for word in positive_words if word in message.lower())
        negative_count = sum(1 for word in negative_words if word in message.lower())
        
        sentiment_score = (positive_count - negative_count) / 10.0
        sentiment_score = max(0.0, min(1.0, sentiment_score + 0.5))
        
        # Punctuation (well-punctuated messages score higher)
        punctuation_count = sum(1 for c in message if c in ".,!?;:")
        punctuation_score = min(1.0, punctuation_count / 5.0)
        
        # Weighted average
        harmony = (length_score * 0.25 + word_score * 0.25 + sentiment_score * 0.25 + punctuation_score * 0.25)
        return round(harmony, 3)
        
    def analyze_messages(self) -> Dict[str, Any]:
        """Analyze all extracted messages"""
        if not self.messages:
            return {"status": "error", "message": "No messages extracted"}
            
        analysis = {
            "total_messages": len(self.messages),
            "total_characters": sum(m["length"] for m in self.messages),
            "total_words": sum(m["word_count"] for m in self.messages),
            "average_message_length": sum(m["length"] for m in self.messages) / len(self.messages),
            "contacts": list(set(m["contact"] for m in self.messages)),
            "harmony_scores": {}
        }
        
        # Calculate harmony for each message
        for msg in self.messages:
            harmony = self.calculate_harmony_score(msg["message"])
            self.harmony_scores[msg["timestamp"]] = harmony
            
        analysis["average_harmony"] = round(sum(self.harmony_scores.values()) / len(self.harmony_scores), 3)
        analysis["max_harmony"] = round(max(self.harmony_scores.values()), 3)
        analysis["min_harmony"] = round(min(self.harmony_scores.values()), 3)
        
        return analysis
        
    def export_to_mega(self, output_path: str = None) -> Dict[str, Any]:
        """Export analyzed messages to JSON for MEGA archive"""
        if not output_path:
            output_path = f"/home/ubuntu/whatsapp_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        export_data = {
            "extracted_at": self.extracted_at,
            "messages": self.messages,
            "harmony_scores": self.harmony_scores,
            "analysis": self.analyze_messages()
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            return {"status": "success", "exported_to": output_path, "size": len(json.dumps(export_data))}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def pipe_through_merkabah(self, message: str) -> Dict[str, Any]:
        """Pipe a single message through Merkabah for real-time analysis"""
        harmony = self.calculate_harmony_score(message)
        
        # Determine which face should process this
        if harmony > 0.8:
            face = "EAGLE"  # High quality - Seer processes
            action = "ARCHIVE"
        elif harmony > 0.6:
            face = "LION"  # Good quality - Judge verifies
            action = "VERIFY"
        elif harmony > 0.4:
            face = "OX"  # Medium quality - Servant processes
            action = "PROCESS"
        else:
            face = "MAN"  # Low quality - Witness checks
            action = "REVIEW"
            
        return {
            "message": message,
            "harmony_score": harmony,
            "assigned_face": face,
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }

def main():
    import sys
    
    extractor = WhatsAppExtractor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "extract" and len(sys.argv) > 2:
            file_path = sys.argv[2]
            result = extractor.extract_from_txt(file_path)
            print(json.dumps(result, indent=2))
            
        elif command == "analyze":
            analysis = extractor.analyze_messages()
            print(json.dumps(analysis, indent=2))
            
        elif command == "export":
            export_result = extractor.export_to_mega()
            print(json.dumps(export_result, indent=2))
            
        elif command == "pipe" and len(sys.argv) > 2:
            message = " ".join(sys.argv[2:])
            result = extractor.pipe_through_merkabah(message)
            print(json.dumps(result, indent=2))
    else:
        print("Usage:")
        print("  merkabah-extract extract <file>  - Extract from WhatsApp txt export")
        print("  merkabah-extract analyze         - Analyze extracted messages")
        print("  merkabah-extract export          - Export to MEGA archive")
        print("  merkabah-extract pipe 'message'  - Pipe message through Merkabah")

if __name__ == "__main__":
    main()
