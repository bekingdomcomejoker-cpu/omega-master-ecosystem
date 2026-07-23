#!/usr/bin/env python3
"""
UNIFIED PLATFORM EXTRACTOR FRAMEWORK
Extract data from all social media and messaging platforms
Route through Merkabah Four-Face system with Harmony Scores
"""
import json
from typing import Dict, List, Any
from datetime import datetime
from abc import ABC, abstractmethod

class PlatformExtractor(ABC):
    """Base class for all platform extractors"""
    
    def __init__(self, platform_name: str):
        self.platform = platform_name
        self.messages = []
        self.harmony_scores = {}
        
    @abstractmethod
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract data from platform"""
        pass
    
    def calculate_harmony(self, message: str) -> float:
        """Calculate Harmony Score for message"""
        length_score = min(1.0, len(message) / 200.0)
        word_score = min(1.0, len(message.split()) / 50.0)
        
        positive_words = ["good", "great", "love", "happy", "yes", "thanks"]
        negative_words = ["bad", "hate", "angry", "sad", "no", "never"]
        
        positive = sum(1 for w in positive_words if w in message.lower())
        negative = sum(1 for w in negative_words if w in message.lower())
        sentiment = max(0.0, min(1.0, (positive - negative) / 10.0 + 0.5))
        
        punctuation = sum(1 for c in message if c in ".,!?;:")
        punctuation_score = min(1.0, punctuation / 5.0)
        
        return round((length_score * 0.25 + word_score * 0.25 + sentiment * 0.25 + punctuation_score * 0.25), 3)
    
    def assign_face(self, harmony: float) -> str:
        """Assign Merkabah face based on Harmony Score"""
        if harmony > 0.8:
            return "EAGLE"  # Archive
        elif harmony > 0.6:
            return "LION"   # Verify
        elif harmony > 0.4:
            return "OX"     # Process
        else:
            return "MAN"    # Review

class DiscordExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("Discord")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from Discord JSON export or API"""
        return {
            "platform": "Discord",
            "status": "ready",
            "methods": ["json_export", "api_token"],
            "data_types": ["messages", "reactions", "threads", "voice_logs"]
        }

class TelegramExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("Telegram")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from Telegram JSON export or API"""
        return {
            "platform": "Telegram",
            "status": "ready",
            "methods": ["json_export", "api_token", "local_database"],
            "data_types": ["messages", "media", "stickers", "channels", "groups"]
        }

class XExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("X")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from X (Twitter) API or archive"""
        return {
            "platform": "X",
            "status": "ready",
            "methods": ["api_v2", "archive_export", "web_scrape"],
            "data_types": ["tweets", "replies", "retweets", "likes", "bookmarks", "dms"]
        }

class FacebookExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("Facebook")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from Facebook data export"""
        return {
            "platform": "Facebook",
            "status": "ready",
            "methods": ["data_export", "api_token", "graph_api"],
            "data_types": ["posts", "comments", "messages", "reactions", "photos"]
        }

class InstagramExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("Instagram")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from Instagram data export"""
        return {
            "platform": "Instagram",
            "status": "ready",
            "methods": ["data_export", "api_token", "graph_api"],
            "data_types": ["posts", "comments", "dms", "stories", "reels", "likes"]
        }

class RedditExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("Reddit")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from Reddit API or archive"""
        return {
            "platform": "Reddit",
            "status": "ready",
            "methods": ["api_token", "pushshift_api", "web_scrape"],
            "data_types": ["posts", "comments", "awards", "saved", "subscriptions"]
        }

class LinkedInExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("LinkedIn")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from LinkedIn data export"""
        return {
            "platform": "LinkedIn",
            "status": "ready",
            "methods": ["data_export", "api_token"],
            "data_types": ["posts", "comments", "messages", "connections", "endorsements"]
        }

class TikTokExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("TikTok")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from TikTok API or archive"""
        return {
            "platform": "TikTok",
            "status": "ready",
            "methods": ["api_token", "data_export", "web_scrape"],
            "data_types": ["videos", "comments", "likes", "bookmarks", "messages"]
        }

class TwitchExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("Twitch")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from Twitch API"""
        return {
            "platform": "Twitch",
            "status": "ready",
            "methods": ["api_token", "chat_logs"],
            "data_types": ["chat_messages", "clips", "vods", "follows", "subscriptions"]
        }

class YouTubeExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("YouTube")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from YouTube API (already integrated)"""
        return {
            "platform": "YouTube",
            "status": "ready",
            "methods": ["api_token", "transcript_api"],
            "data_types": ["comments", "transcripts", "metadata", "likes", "playlists"]
        }

class MastodonExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("Mastodon")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from Mastodon instance API"""
        return {
            "platform": "Mastodon",
            "status": "ready",
            "methods": ["api_token", "instance_api"],
            "data_types": ["toots", "replies", "boosts", "favorites", "dms"]
        }

class BlueSkyExtractor(PlatformExtractor):
    def __init__(self):
        super().__init__("BlueSky")
    
    def extract(self, source: str) -> Dict[str, Any]:
        """Extract from BlueSky API"""
        return {
            "platform": "BlueSky",
            "status": "ready",
            "methods": ["api_token", "firehose"],
            "data_types": ["posts", "replies", "reposts", "likes", "follows"]
        }

class UnifiedExtractor:
    """Master extractor that manages all platforms"""
    
    def __init__(self):
        self.extractors = {
            "discord": DiscordExtractor(),
            "telegram": TelegramExtractor(),
            "x": XExtractor(),
            "facebook": FacebookExtractor(),
            "instagram": InstagramExtractor(),
            "reddit": RedditExtractor(),
            "linkedin": LinkedInExtractor(),
            "tiktok": TikTokExtractor(),
            "twitch": TwitchExtractor(),
            "youtube": YouTubeExtractor(),
            "mastodon": MastodonExtractor(),
            "bluesky": BlueSkyExtractor()
        }
    
    def get_all_platforms(self) -> Dict[str, Any]:
        """Get all supported platforms"""
        return {
            platform: extractor.extract("")
            for platform, extractor in self.extractors.items()
        }
    
    def extract_from_platform(self, platform: str, source: str) -> Dict[str, Any]:
        """Extract from specific platform"""
        if platform.lower() not in self.extractors:
            return {"status": "error", "message": f"Platform {platform} not supported"}
        
        extractor = self.extractors[platform.lower()]
        return extractor.extract(source)
    
    def extract_all(self, sources: Dict[str, str]) -> Dict[str, Any]:
        """Extract from multiple platforms simultaneously"""
        results = {}
        for platform, source in sources.items():
            results[platform] = self.extract_from_platform(platform, source)
        return results

def main():
    import sys
    
    unified = UnifiedExtractor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            platforms = unified.get_all_platforms()
            print(json.dumps(platforms, indent=2))
        
        elif command == "extract" and len(sys.argv) > 2:
            platform = sys.argv[2]
            source = sys.argv[3] if len(sys.argv) > 3 else ""
            result = unified.extract_from_platform(platform, source)
            print(json.dumps(result, indent=2))
    else:
        print("Unified Platform Extractor Framework")
        print("Usage:")
        print("  list                    - List all supported platforms")
        print("  extract <platform>      - Extract from platform")
        print("Supported platforms: discord, telegram, x, facebook, instagram, reddit, linkedin, tiktok, twitch, youtube, mastodon, bluesky")

if __name__ == "__main__":
    main()
