#!/usr/bin/env python3
"""
Example usage of the playlist fetcher
"""

import subprocess
import sys

def run_example():
    """Run example playlist fetch"""
    
    # Example channel
    channel_url = "https://www.youtube.com/@TechwithShapingpixel"
    
    print("🎯 YouTube Playlist Fetcher - Example Usage")
    print("=" * 50)
    print(f"Channel: {channel_url}")
    print()
    
    # Basic usage
    print("📋 Running basic fetch...")
    try:
        result = subprocess.run([
            "python", "playlist_fetcher.py", channel_url
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Basic fetch completed successfully!")
            print("Output:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
        else:
            print("❌ Basic fetch failed")
            print("Error:", result.stderr)
    except Exception as e:
        print(f"❌ Error running example: {e}")
    
    print("\n💡 Try these commands yourself:")
    print(f"python playlist_fetcher.py \"{channel_url}\"")
    print(f"python playlist_fetcher.py \"{channel_url}\" --detailed")
    print(f"python playlist_fetcher.py \"{channel_url}\" --output my_playlists.txt")

if __name__ == "__main__":
    run_example()
