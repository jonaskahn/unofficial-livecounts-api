# 🎶 Unofficial Livecounts.io API

**Unofficial API for Livecounts.io to retrieve live counts for users and videos on TikTok, YouTube, Twitter, Twitch, KickLive, Vlive, and Odysee**

## 📝 Supported API

- **YouTube**: User/Video Count
- **TikTok**: User/Video Count
- **Twitter**: User Count
- **Twitch**: To be supported
- **Vlive**: To be supported
- **Kicklive**: To be supported
- **Odysee-live**: To be supported

## 🕵️ Usage

```shell
pip install unofficial_livecounts_api
```

### Tiktok Live Count API

- **User API**

```python
from unofficial_livecounts_api.tiktok import TiktokAgent

# Find users by username or full name
users = TiktokAgent.find_user(query="best")

# Find exact user by username
user = TiktokAgent.find_user(query="best", exact=True)

# Live count user by username
user_metrics = TiktokAgent.fetch_user_metrics(query="best")

# Live count user by user id
user_metrics = TiktokAgent.fetch_user_metrics(user_id="123456789")
```

- **Video API**

```python
from unofficial_livecounts_api.tiktok import TiktokAgent

# Find a video by given url
video = TiktokAgent.find_video(query="https://tiktok.com/@test/video/122222223233232?test1=value1")

# Find a video by video_id
video = TiktokAgent.find_video(video_id="122222223233232")

# Live count video by a given url
video_metrics = TiktokAgent.fetch_video_metrics(query="https://tiktok.com/@test/video/122222223233232?test1=value1")

# Live count video by a given video_id
video_metrics = TiktokAgent.fetch_video_metrics(video_id="122222223233232")
```

### YouTube API

[Placeholder]

### Twitter API

[Placeholder]

## 📛 Disclaimer

This project aimed to security research, testing purpose. Any misuse of this API for malicious purposes is not condoned.
The developers of this API are not responsible for any illegal or unethical activities carried out using this API.
