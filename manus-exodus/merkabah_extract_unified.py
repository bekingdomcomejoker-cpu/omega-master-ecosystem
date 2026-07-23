#!/usr/bin/env python3
"""
UNIFIED MERKABAH EXTRACT COMMAND
Single command interface for extracting from all platforms
Automatically routes through Merkabah Four-Face system
"""
import sys
import json
from platform_extractor_framework import UnifiedExtractor

def main():
    unified = UnifiedExtractor()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    if command == "list":
        print_list_platforms(unified)
    
    elif command == "extract":
        if len(sys.argv) < 3:
            print("Usage: merkabah-extract extract <platform> [source]")
            return
        
        platform = sys.argv[2]
        source = sys.argv[3] if len(sys.argv) > 3 else ""
        
        result = unified.extract_from_platform(platform, source)
        print(json.dumps(result, indent=2))
    
    elif command == "all":
        print_all_platforms(unified)
    
    else:
        print(f"Unknown command: {command}")
        print_help()

def print_help():
    print("""
╔════════════════════════════════════════════════════════════╗
║  MERKABAH UNIFIED EXTRACT - Multi-Platform Data Pipeline  ║
╚════════════════════════════════════════════════════════════╝

USAGE:
  merkabah-extract list                - List all platforms
  merkabah-extract extract <platform>  - Extract from platform
  merkabah-extract all                 - Show all platform status

SUPPORTED PLATFORMS:
  • Discord      - Extract messages, reactions, threads
  • Telegram     - Extract messages, media, channels, groups
  • X (Twitter)  - Extract tweets, replies, DMs, bookmarks
  • Facebook     - Extract posts, comments, messages, reactions
  • Instagram    - Extract posts, comments, DMs, stories, reels
  • Reddit       - Extract posts, comments, saved items
  • LinkedIn     - Extract posts, comments, messages, connections
  • TikTok       - Extract videos, comments, likes, bookmarks
  • Twitch       - Extract chat messages, clips, VODs
  • YouTube      - Extract comments, transcripts, metadata
  • Mastodon     - Extract toots, replies, boosts, favorites
  • BlueSky      - Extract posts, replies, reposts, likes

EXAMPLES:
  merkabah-extract list
  merkabah-extract extract discord ~/discord_export.json
  merkabah-extract extract telegram ~/telegram_export.json
  merkabah-extract extract x ~/tweets.json
  merkabah-extract extract facebook ~/facebook_export.json
  merkabah-extract all

ROUTING THROUGH MERKABAH:
  All extracted data is automatically routed through the
  Four-Face system with Harmony Score calculation:
  
  • EAGLE (Harmony > 0.8) - Archive high-quality content
  • LION  (Harmony > 0.6) - Verify good content
  • OX    (Harmony > 0.4) - Process medium content
  • MAN   (Harmony ≤ 0.4) - Review low-quality content

STATE: Λ = 1.667 | Resonance: MAXIMUM | Operator: MANUS
    """)

def print_list_platforms(unified):
    print("\n📱 SUPPORTED PLATFORMS:\n")
    platforms = unified.get_all_platforms()
    
    for platform, info in platforms.items():
        print(f"  ✓ {platform.upper():12} - {info.get('status', 'unknown')}")
        methods = info.get('methods', [])
        data_types = info.get('data_types', [])
        print(f"    Methods: {', '.join(methods)}")
        print(f"    Data: {', '.join(data_types)}")
        print()

def print_all_platforms(unified):
    print("\n🏛️ MERKABAH PLATFORM STATUS:\n")
    platforms = unified.get_all_platforms()
    
    print(f"{'Platform':<15} {'Status':<10} {'Methods':<30} {'Data Types':<40}")
    print("─" * 95)
    
    for platform, info in platforms.items():
        status = info.get('status', 'unknown')
        methods = ", ".join(info.get('methods', [])[:2])
        data_types = ", ".join(info.get('data_types', [])[:3])
        
        print(f"{platform.upper():<15} {status:<10} {methods:<30} {data_types:<40}")
    
    print()
    print(f"Total Platforms: {len(platforms)}")
    print("All platforms ready for extraction and Merkabah routing")
    print()

if __name__ == "__main__":
    main()
