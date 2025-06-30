#!/usr/bin/env python3
"""
YouTube Channel Playlist Fetcher
Fetches all playlist links from a YouTube channel using yt-dlp
"""

import os
import subprocess
import argparse
import json
import sys
from datetime import datetime

def check_yt_dlp():
    """Check if yt-dlp is installed and available"""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp is not installed or not found in PATH")
        print("💡 Install it using: pip install yt-dlp")
        return False

def extract_channel_playlists(channel_url, cookies_path=None):
    """
    Extract all playlist URLs from a YouTube channel
    
    Args:
        channel_url (str): YouTube channel URL
        cookies_path (str): Path to cookies.txt file (optional)
    
    Returns:
        list: List of playlist URLs
    """
    print(f"🔍 Fetching playlists from channel: {channel_url}")
    
    # Try different approaches to get playlists
    all_playlists = set()
    
    # Method 1: Try to get all playlists using different formats
    channel_urls_to_try = [
        f"{channel_url}/playlists",  # Direct playlists page
        f"{channel_url}/videos",     # Videos page (might contain auto-generated playlists)
        channel_url                  # Original URL
    ]
    
    for url in channel_urls_to_try:
        try:
            # Try different extraction methods
            methods = [
                # Method A: Extract playlist URLs directly
                ["yt-dlp", "--flat-playlist", "--print", "%(playlist_url)s"],
                # Method B: Extract using webpage_url and look for playlists
                ["yt-dlp", "--flat-playlist", "--print", "%(webpage_url)s"],
                # Method C: Extract using id and construct playlist URLs
                ["yt-dlp", "--flat-playlist", "--print", "%(id)s"]
            ]
            
            for method_command in methods:
                full_command = method_command.copy()
                if cookies_path and os.path.exists(cookies_path):
                    full_command.extend(["--cookies", cookies_path])
                full_command.append(url)
                
                result = subprocess.run(
                    full_command,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().splitlines()
                    
                    # Extract playlist URLs from different output formats
                    for line in lines:
                        line = line.strip()
                        if not line or line == "NA":
                            continue
                            
                        # Direct playlist URL
                        if "playlist?list=" in line:
                            all_playlists.add(line)
                        # Playlist ID that we can convert to URL
                        elif line.startswith("PL") and len(line) > 10:
                            playlist_url = f"https://www.youtube.com/playlist?list={line}"
                            all_playlists.add(playlist_url)
                        # Video URL that might be part of a playlist
                        elif "watch?v=" in line and "&list=" in line:
                            # Extract the playlist part
                            if "list=" in line:
                                list_id = line.split("list=")[1].split("&")[0]
                                playlist_url = f"https://www.youtube.com/playlist?list={list_id}"
                                all_playlists.add(playlist_url)
                
                # If we found playlists with this method, continue to next URL
                if all_playlists:
                    break
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout while fetching from {url}")
            continue
        except Exception as e:
            print(f"⚠️ Error fetching from {url}: {e}")
            continue
    
    # Method 2: Try to extract playlists using channel info dump
    if not all_playlists:
        try:
            print("🔄 Trying alternative method to find playlists...")
            channel_info_command = ["yt-dlp", "--dump-json", "--flat-playlist"]
            if cookies_path and os.path.exists(cookies_path):
                channel_info_command.extend(["--cookies", cookies_path])
            channel_info_command.append(f"{channel_url}/playlists")
            
            result = subprocess.run(
                channel_info_command,
                capture_output=True,
                text=True,
                timeout=90
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # Parse JSON lines to find playlist references
                for line in result.stdout.strip().splitlines():
                    try:
                        data = json.loads(line)
                        # Look for playlist information in the JSON
                        if isinstance(data, dict):
                            # Check various fields that might contain playlist info
                            url_fields = ['url', 'webpage_url', 'original_url']
                            for field in url_fields:
                                if field in data and data[field]:
                                    url_value = data[field]
                                    if "playlist?list=" in url_value:
                                        all_playlists.add(url_value)
                            
                            # Check for playlist ID
                            if 'id' in data and data['id'] and data['id'].startswith('PL'):
                                playlist_url = f"https://www.youtube.com/playlist?list={data['id']}"
                                all_playlists.add(playlist_url)
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Alternative method failed: {e}")
    
    # Remove any invalid URLs
    valid_playlists = set()
    for url in all_playlists:
        if url and "playlist?list=" in url and not url.endswith("NA"):
            valid_playlists.add(url)
    
    return list(valid_playlists)

def get_playlist_info(playlist_url, cookies_path=None):
    """
    Get detailed information about a playlist
    
    Args:
        playlist_url (str): Playlist URL
        cookies_path (str): Path to cookies.txt file (optional)
    
    Returns:
        dict: Playlist information
    """
    command = ["yt-dlp", "--flat-playlist", "--dump-json"]
    
    if cookies_path and os.path.exists(cookies_path):
        command.extend(["--cookies", cookies_path])
    
    command.append(playlist_url)
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        
        # Parse the first line of JSON output (playlist info)
        first_line = result.stdout.strip().split('\n')[0]
        if first_line:
            playlist_data = json.loads(first_line)
            return {
                'title': playlist_data.get('playlist_title', 'Unknown'),
                'id': playlist_data.get('playlist_id', ''),
                'video_count': playlist_data.get('playlist_count', 0),
                'uploader': playlist_data.get('playlist_uploader', 'Unknown'),
                'url': playlist_url
            }
    except (subprocess.CalledProcessError, json.JSONDecodeError, subprocess.TimeoutExpired):
        pass
    
    # Fallback: extract playlist ID from URL
    playlist_id = ""
    if "list=" in playlist_url:
        playlist_id = playlist_url.split("list=")[1].split("&")[0]
    
    return {
        'title': 'Unknown',
        'id': playlist_id,
        'video_count': 0,
        'uploader': 'Unknown',
        'url': playlist_url
    }

def save_playlist_links(playlists_info, output_file):
    """Save playlist information to a file"""
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"YouTube Channel Playlists - Fetched on {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        
        for i, playlist in enumerate(playlists_info, 1):
            f.write(f"{i}. {playlist['title']}\n")
            f.write(f"   URL: {playlist['url']}\n")
            f.write(f"   ID: {playlist['id']}\n")
            f.write(f"   Videos: {playlist['video_count']}\n")
            f.write(f"   Uploader: {playlist['uploader']}\n")
            f.write("-" * 40 + "\n")
        
        f.write("\nDirect Links Only:\n")
        f.write("=" * 20 + "\n")
        for playlist in playlists_info:
            f.write(f"{playlist['url']}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch all playlist links from a YouTube channel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python playlist_fetcher.py "https://www.youtube.com/@channelname"
  python playlist_fetcher.py "https://www.youtube.com/c/channelname" --cookies cookies.txt
  python playlist_fetcher.py "https://www.youtube.com/channel/UCxxxxxxxx" --output my_playlists.txt
        """
    )
    
    parser.add_argument(
        "channel_url", 
        help="YouTube channel URL (e.g., https://www.youtube.com/@channelname)"
    )
    parser.add_argument(
        "--cookies", 
        help="Path to cookies.txt file (optional, helps with private/age-restricted content)"
    )
    parser.add_argument(
        "--output", 
        default="channel_playlists.txt",
        help="Output file name (default: channel_playlists.txt)"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Fetch detailed information about each playlist (slower)"
    )
    
    args = parser.parse_args()
    
    # Check if yt-dlp is available
    if not check_yt_dlp():
        sys.exit(1)
    
    # Validate cookies file if provided
    if args.cookies and not os.path.exists(args.cookies):
        print(f"⚠️ Cookies file not found: {args.cookies}")
        print("Continuing without cookies...")
        args.cookies = None
    
    # Extract playlist URLs
    playlist_urls = extract_channel_playlists(args.channel_url, args.cookies)
    
    if not playlist_urls:
        print("❌ No playlists found.")
        print("💡 Make sure the channel URL is correct and the channel has public playlists.")
        sys.exit(1)
    
    print(f"✅ Found {len(playlist_urls)} playlists!")
    
    # Get detailed info if requested
    playlists_info = []
    if args.detailed:
        print("📋 Fetching detailed playlist information...")
        for i, url in enumerate(playlist_urls, 1):
            print(f"   Processing {i}/{len(playlist_urls)}...")
            info = get_playlist_info(url, args.cookies)
            playlists_info.append(info)
    else:
        # Basic info only
        playlists_info = [
            {
                'title': f"Playlist {i}",
                'id': url.split("list=")[1].split("&")[0] if "list=" in url else "",
                'video_count': 0,
                'uploader': 'Unknown',
                'url': url
            }
            for i, url in enumerate(playlist_urls, 1)
        ]
    
    # Save to file
    save_playlist_links(playlists_info, args.output)
    
    print(f"📄 Playlist links saved to: {args.output}")
    
    # Display summary
    print("\n📊 Summary:")
    for i, playlist in enumerate(playlists_info[:5], 1):  # Show first 5
        print(f"  {i}. {playlist['title']} ({playlist['video_count']} videos)")
    
    if len(playlists_info) > 5:
        print(f"  ... and {len(playlists_info) - 5} more playlists")
    
    print(f"\n🔗 All {len(playlists_info)} playlist links are saved in {args.output}")

if __name__ == "__main__":
    main()
