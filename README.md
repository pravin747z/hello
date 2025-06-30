# YouTube Playlist Fetcher

A Python script that fetches all playlist links from any YouTube channel using yt-dlp.

## 🚀 Features

- ✅ Extracts all public playlists from any YouTube channel
- ✅ Supports different channel URL formats (@username, /c/channel, /channel/UC...)
- ✅ Optional cookies support for private/age-restricted content
- ✅ Detailed playlist information (title, video count, uploader)
- ✅ Saves results to formatted text file
- ✅ Multiple extraction methods for better reliability
- ✅ Error handling and timeout protection

## 📋 Requirements

- Python 3.7+
- yt-dlp

## 🛠️ Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd link_fetcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Basic Usage
```bash
python playlist_fetcher.py "https://www.youtube.com/@channelname"
```

### With Cookies (for private content)
```bash
python playlist_fetcher.py "https://www.youtube.com/@channelname" --cookies cookies.txt
```

### With Custom Output File
```bash
python playlist_fetcher.py "https://www.youtube.com/@channelname" --output my_playlists.txt
```

### With Detailed Information
```bash
python playlist_fetcher.py "https://www.youtube.com/@channelname" --detailed
```

### All Options Combined
```bash
python playlist_fetcher.py "https://www.youtube.com/@channelname" --cookies cookies.txt --output detailed_playlists.txt --detailed
```

## 📄 Output Format

The script creates a text file with:

1. **Detailed Information Section**:
```
YouTube Channel Playlists - Fetched on 2025-06-30 15:30:00
============================================================

1. My Gaming Videos
   URL: https://www.youtube.com/playlist?list=PLxxxxxxxx
   ID: PLxxxxxxxx
   Videos: 25
   Uploader: Channel Name
----------------------------------------
```

2. **Direct Links Section**:
```
Direct Links Only:
====================
https://www.youtube.com/playlist?list=PLxxxxxxxx
https://www.youtube.com/playlist?list=PLyyyyyyyy
```

## 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `channel_url` | YouTube channel URL (required) | - |
| `--cookies` | Path to cookies.txt file | None |
| `--output` | Output file name | `channel_playlists.txt` |
| `--detailed` | Fetch detailed playlist info (slower) | False |

## 🌐 Supported Channel URL Formats

- `https://www.youtube.com/@username`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/channel/UCxxxxxxxxx`
- `https://youtube.com/@username` (without www)

## 🍪 Using Cookies

Cookies help access:
- Private/unlisted playlists you have access to
- Age-restricted content
- Content with regional restrictions
- Better rate limiting

To get cookies:
1. Use browser extension "Get cookies.txt"
2. Export from YouTube while logged in
3. Save as `cookies.txt` in same directory

## ⚠️ Troubleshooting

### No playlists found
- Channel might not have public playlists
- Try with cookies if you have access
- Verify channel URL is correct

### yt-dlp not found
```bash
pip install yt-dlp
```

### Permission errors
- Run as administrator (Windows)
- Check file permissions

## 📝 Example Output

For channel `@TechwithShapingpixel`:
```
✅ Found 5 playlists!
📄 Playlist links saved to: channel_playlists.txt

📊 Summary:
  1. MB-280 (0 videos)
  2. Microsoft Dynamics 365 (0 videos)
  3. GitHub (0 videos)
  4. LPI (0 videos)
  5. MB-230 (0 videos)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is open source. Feel free to use and modify as needed.

## 🔗 Related Tools

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The underlying tool for YouTube data extraction
- [youtube-dl](https://github.com/ytdl-org/youtube-dl) - Alternative YouTube downloader

---

**Happy playlist hunting! 🎵**
