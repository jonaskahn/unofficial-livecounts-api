from unofficial_livecounts_api import env
from unofficial_livecounts_api.utils import send_request


class YoutubeChannel:
    def __init__(self, channel_id: str, display_name: str, thumbnail: str):
        self.channel_id = channel_id
        self.display_name = display_name
        self.thumbnail = thumbnail

    def __eq__(self, other):
        return (
            self.channel_id == other.channel_id
            if isinstance(other, YoutubeChannel)
            else False
        )

    def __hash__(self):
        return hash(self.channel_id)

    def __dict__(self):
        return {
            "channel_id": self.channel_id,
            "display_name": self.display_name,
            "thumbnail": self.thumbnail,
        }


class YoutubeChannelCount:
    def __init__(self, channel_id: str, follower_count: int, channel_stats: list[int]):
        self.channel_id = channel_id
        self.follower_count = follower_count
        self.view_count = channel_stats[0]
        self.video_count = channel_stats[1]
        self.goal_count = channel_stats[2]

    def __eq__(self, other):
        if not isinstance(other, YoutubeChannelCount):
            return False
        return self.channel_id == other.channel_id

    def __hash__(self):
        return hash(self.channel_id)

    def __dict__(self):
        return {
            "channel_id": self.channel_id,
            "follower_count": self.follower_count,
            "view_count": self.view_count,
            "video_count": self.video_count,
            "goal_count": self.goal_count,
        }


class YoutubeVideo:
    def __init__(self, video_id: str, display_name: str, thumbnail: str):
        self.video_id = video_id
        self.display_name = display_name
        self.thumbnail = thumbnail

    def __eq__(self, other):
        if not isinstance(other, YoutubeVideo):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "display_name": self.display_name,
            "thumbnail": self.thumbnail,
        }


class YoutubeVideoCount:
    def __init__(self, video_id: str, view_count: int, video_stats: list[int]):
        self.video_id = video_id
        self.view_count = view_count
        self.like_count = video_stats[0]
        self.dislike_count = video_stats[1]
        self.comment_count = video_stats[2]

    def __eq__(self, other):
        if not isinstance(other, YoutubeVideoCount):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "dislike_count": self.dislike_count,
            "comment_count": self.comment_count,
        }


class YoutubeAgent:

    @staticmethod
    def find_channel(query: str) -> list[YoutubeChannel]:
        """
        Find YouTube channel(s) based on the provided query.

        Args:
            query (str): The search query (channel_id or username) to find a channel or list of potential channels.

        Returns:
            list[YoutubeChannel]
        """
        users = send_request(f"{env.YOUTUBE_CHANNEL_SEARCH_API}/{query}").get(
            "userData", []
        )
        return [
            YoutubeChannel(
                channel_id=item.get("id", ""),
                display_name=item.get("username", ""),
                thumbnail=item.get("avatar", ""),
            )
            for item in users
        ]

    @staticmethod
    def fetch_channel_metrics(query: str) -> YoutubeChannelCount:
        """
        Fetch the metrics of a YouTube channel.

        Args:
            query: Channel ID

        Returns:
            YoutubeChannelCount: An object containing the metrics of the YouTube channel.

        Raises:
            YoutubeError: If neither 'query' nor 'channel_id' is provided.
        """
        metrics = send_request(f"{env.YOUTUBE_CHANNEL_STATS_API}/{query}")
        return YoutubeChannelCount(
            channel_id=query,
            follower_count=metrics.get("followerCount", 0),
            channel_stats=metrics.get("bottomOdos", [0, 0, 0]),
        )

    @staticmethod
    def find_video(query: str) -> list[YoutubeVideo]:
        """
        Find a YouTube video based on the provided query.

        Args:
            query (str): The search query to find a video or list of potential videos.

        Returns:
            list[YoutubeVideo]
        """
        videos = send_request(f"{env.YOUTUBE_VIDEO_SEARCH_API}/{query}").get(
            "userData", []
        )
        return [
            YoutubeVideo(
                video_id=item.get("id", ""),
                display_name=item.get("username", ""),
                thumbnail=item.get("avatar", ""),
            )
            for item in videos
        ]

    @staticmethod
    def fetch_video_metrics(query: str) -> YoutubeVideoCount:
        """
        Fetch the metrics of a YouTube video.

        Args:
            query (str): Channel ID

        Returns:
            YoutubeVideoCount: An object containing the metrics of the YouTube video.

        Raises:
            YoutubeError: If neither 'query' nor 'video_id' is provided.
        """
        metrics = send_request(f"{env.YOUTUBE_VIDEO_STATS_API}/{query}")
        return YoutubeVideoCount(
            video_id=query,
            view_count=metrics.get("followerCount", 0),
            video_stats=metrics.get("bottomOdos", [0, 0, 0]),
        )
