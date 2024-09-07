# 🎶 Unofficial Livecounts.io API

**Unofficial API for Livecounts.io to retrieve live counts for users and videos on TikTok, YouTube, Twitter, Twitch, KickLive, Vlive, and Odysee**

## 📝 Supported APIs

- [x] **YouTube**: User/Video Count
- [x] **TikTok**: User/Video Count
- [x] **Twitter**: User Count
- [ ] **Twitch**: To be supported
- [ ] **Vlive**: To be supported
- [ ] **Kicklive**: To be supported
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

# Find exact (one) user
exact_user = TiktokAgent.find_user(query="best", exact=True)

# Live count user
user_metric_by_query = TiktokAgent.fetch_user_metrics(query="best")
user_metric_by_user_id = TiktokAgent.fetch_user_metrics(user_id="123456789")
```

- **Video API**

```python
from unofficial_livecounts_api.tiktok import TiktokAgent

# Find a video
video_by_query = TiktokAgent.find_video(query="https://tiktok.com/@test/video/122222223233232?test1=value1")
video_by_video_id = TiktokAgent.find_video(video_id="122222223233232")

# Live count video
video_metric_by_query = TiktokAgent.fetch_video_metrics(query="https://tiktok.com/@test/video/122222223233232?test1=value1")
video_metric_by_video_id = TiktokAgent.fetch_video_metrics(video_id="122222223233232")
```

### YouTube API

- **User API**

```python
from unofficial_livecounts_api.youtube import YoutubeAgent

# Find channels by given query
channels = YoutubeAgent.find_channel(query="test")

# Find exact channel by given query
channel = YoutubeAgent.find_channel(query="test", exact=True)

# Live count channel
channel_metrics_by_query = YoutubeAgent.fetch_channel_metrics(query="test")
channel_metrics_by_channel_id = YoutubeAgent.fetch_channel_metrics(channel_id="123456789")

```

- **Video API**

```python
from unofficial_livecounts_api.youtube import YoutubeAgent

# Find videos by given query
videos = YoutubeAgent.find_video(query="test")

# Find exact video by given query
video = YoutubeAgent.find_video(query="test", exact=True)

# Live count video
video_metrics_by_query = YoutubeAgent.fetch_video_metrics(query="test")
video_metrics_by_video_id = YoutubeAgent.fetch_video_metrics(video_id="123456789")
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
