import os

from dotenv import load_dotenv

load_dotenv()

PROXY_ENABLED = os.getenv("PROXY_ENABLED", "off")
PROXY_SERVER = os.getenv("PROXY_SERVER", None)

TIKTOK_USER_SEARCH_API = os.getenv("TIKTOK_USER_SEARCH_API", "https://tiktok.livecounts.io/user/search").removesuffix("/")
TIKTOK_USER_STATS_API = os.getenv("TIKTOK_USER_STATS_API", "https://tiktok.livecounts.io/user/stats").removesuffix("/")
TIKTOK_VIDEO_SEARCH_API = os.getenv("TIKTOK_VIDEO_SEARCH_API", "https://tiktok.livecounts.io/video/data").removesuffix("/")
TIKTOK_VIDEO_STATS_API = os.getenv("TIKTOK_VIDEO_STATS_API", "https://tiktok.livecounts.io/video/stats").removesuffix("/")

YOUTUBE_CHANNEL_SEARCH_API = os.getenv("YOUTUBE_CHANNEL_SEARCH_API", "https://api.livecounts.io/youtube-live-subscriber-counter/search").removesuffix("/")
YOUTUBE_VIDEO_SEARCH_API = os.getenv("YOUTUBE_VIDEO_SEARCH_API", "https://api.livecounts.io/youtube-live-view-counter/search").removesuffix("/")
