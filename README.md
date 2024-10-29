# 🎶 Unofficial Livecounts.io API

**Unofficial API for Livecounts.io to retrieve live counts for users and videos on TikTok, YouTube, Twitter, Twitch,
KickLive, Vlive, and Odysee**

## 📝 Supported APIs

- [x] **YouTube**: User/Video Count
- [x] **TikTok**: User/Video Count
- [x] **Twitter**: User Count
- [x] **Twitch**: User Count
- [ ] **Kicklive**: To be supported
- [ ] **Vlive**: To be supported
- [ ] **Odysee-live**: To be supported

## 🕵️ Usage

```shell
pip install unofficial_livecounts_api
```

### Tiktok API

- **User API**

```python
from unofficial_livecounts_api.tiktok import TiktokAgent

# Find users
users = TiktokAgent.find_user(query="best")

# Live count a user
user_metric_by_user_id = TiktokAgent.fetch_user_metrics(query="123456789")
```

- **Video API**

```python
from unofficial_livecounts_api.tiktok import TiktokAgent

# Find a video
video_by_query = TiktokAgent.find_video(query="https://tiktok.com/@test/video/122222223233232?test1=value1")
video_by_video_id = TiktokAgent.find_video(query="122222223233232")

# Live count video
video_metric_by_query = TiktokAgent.fetch_video_metrics(
    query="https://tiktok.com/@test/video/122222223233232?test1=value1")
video_metric_by_video_id = TiktokAgent.fetch_video_metrics(query="122222223233232")
```

### YouTube API

- **User API**

```python
from unofficial_livecounts_api.youtube import YoutubeAgent

# Find channels by given query
channels = YoutubeAgent.find_channel(query="test")

# Live count channel
channel_metrics_by_query = YoutubeAgent.fetch_channel_metrics(query="test")

```

- **Video API**

```python
from unofficial_livecounts_api.youtube import YoutubeAgent

# Find videos by given query
videos = YoutubeAgent.find_video(query="test")

# Live count a video
video_metrics_by_query = YoutubeAgent.fetch_video_metrics(query="123456789")
```

### Twitter API

```python
from unofficial_livecounts_api.twitter import TwitterAgent

# Find users by given query
user = TwitterAgent.find_user(query="jack")

# Live count user
metrics = TwitterAgent.fetch_user_metrics(query="jack")
```

## 📛 Disclaimer

This project aimed to security research, testing purpose. Any misuse of this API for malicious purposes is not condoned.
The developers of this API are not responsible for any illegal or unethical activities carried out using this API.
