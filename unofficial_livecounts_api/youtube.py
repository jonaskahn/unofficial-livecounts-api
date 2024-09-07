from unofficial_livecounts_api import env
from unofficial_livecounts_api.error import YoutubeError
from unofficial_livecounts_api.utils import send_request


class YoutubeChannel:
    def __init__(self, channel_id: str, display_name: str, thumbnail: str):
        self.channel_id = channel_id
        self.display_name = display_name
        self.thumbnail = thumbnail

    def __eq__(self, other):
        return self.channel_id == other.channel_id if isinstance(other, YoutubeChannel) else False

    def __hash__(self):
        return hash(self.channel_id)

    def __dir__(self):
        return {
            "channel_id": self.channel_id,
            "display_name": self.display_name,
            "thumbnail": self.thumbnail
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
            "goal_count": self.goal_count
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
            "thumbnail": self.thumbnail
        }


class YoutubeVideoCount:
    def __init__(self, video_id: str, view_count: int, video_stats: list[str]):
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
            "comment_count": self.comment_count
        }


class YoutubeAgent:

    @staticmethod
    def find_channel(query: str, exact: bool = False) -> list[YoutubeChannel] | YoutubeChannel:
        """
        Find YouTube channel(s) based on the provided query.

        Args:
            query (str): The search query (channel_id or username) to find a channel or list of potential channels.
            exact (bool, optional): If True, finds an exact match for the query, strongly recommend use channel_id for query. Defaults to False.

        Returns:
            list[YoutubeChannel] | YoutubeChannel
        """
        return YoutubeAgent.__find_exact_channel(query) if exact else YoutubeAgent.__find_channels(query)

    @staticmethod
    def __find_channels(query: str) -> list[YoutubeChannel]:
        users = send_request(f"{env.YOUTUBE_CHANNEL_SEARCH_API}/{query}").get("userData", [])
        return [
            YoutubeChannel(
                channel_id=item.get("id", ""),
                display_name=item.get("username", ""),
                thumbnail=item.get("avatar", ""),
            )
            for item in users
        ]

    @staticmethod
    def __find_exact_channel(query: str) -> YoutubeChannel:
        users = YoutubeAgent.__find_channels(query)
        for user in users:
            if user.channel_id == query or user.display_name == query:
                return user
        raise YoutubeError("youtube channel is not found")

    @staticmethod
    def fetch_channel_metrics(query: str = None, channel_id: str = None) -> YoutubeChannelCount:
        """
        Fetch the metrics of a YouTube channel.

        Args:
            query (str, optional): The search query (channel_id or username) to find a channel. Defaults to None.
            channel_id (str, optional): The ID of the YouTube channel. Defaults to None.

        Returns:
            YoutubeChannelCount: An object containing the metrics of the YouTube channel.

        Raises:
            YoutubeError: If neither 'query' nor 'channel_id' is provided.
        """
        if channel_id is not None:
            return YoutubeAgent.__fetch_channel_metrics_by_id(channel_id)
        elif query is not None:
            return YoutubeAgent.__fetch_channel_metrics_by_query(query)
        else:
            raise YoutubeError("must provide either 'query' or 'channel_id'")

    @staticmethod
    def __fetch_channel_metrics_by_id(channel_id) -> YoutubeChannelCount:
        metrics = send_request(f"{env.YOUTUBE_CHANNEL_STATS_API}/{channel_id}")
        return YoutubeChannelCount(
            channel_id=channel_id,
            follower_count=metrics.get("followerCount", 0),
            channel_stats=metrics.get("bottomOdos", [0, 0, 0]),
        )

    @staticmethod
    def __fetch_channel_metrics_by_query(query) -> YoutubeChannelCount:
        channel = YoutubeAgent.__find_exact_channel(query)
        return YoutubeAgent.__fetch_channel_metrics_by_id(channel.channel_id)

    @staticmethod
    def find_video(query: str, exact: bool = False) -> list[YoutubeVideo] | YoutubeVideo:
        """
        Find a YouTube video based on the provided query.

        Args:
            query (str): The search query (video_id or title) to find a video or list of potential videos.
            exact (bool, optional): If True, finds an exact match for the query, strongly recommend use video_id for query. Defaults to False.

        Returns:
            list[YoutubeVideo] | YoutubeVideo
        """
        return YoutubeAgent.__find_exact_video(query) if exact else YoutubeAgent.__find_videos(query)

    @staticmethod
    def __find_videos(query: str) -> list[YoutubeVideo]:
        videos = send_request(f"{env.YOUTUBE_VIDEO_SEARCH_API}/{query}").get("userData", [])
        return [
            YoutubeVideo(
                video_id=item.get("id", ""),
                display_name=item.get("username", ""),
                thumbnail=item.get("avatar", ""),
            )
            for item in videos
        ]

    @staticmethod
    def __find_exact_video(query: str) -> YoutubeVideo:
        videos = YoutubeAgent.__find_videos(query)
        for video in videos:
            print(video.video_id)
            if video.video_id == query or video.display_name == query:
                return video
        raise YoutubeError("youtube video is not found")

    @staticmethod
    def fetch_video_metrics(query: str = None, video_id: str = None) -> YoutubeVideoCount:
        """
        Fetch the metrics of a YouTube video.

        Args:
            query (str, optional): The search query (video_id or title) to find a video. Defaults to None.
            video_id (str, optional): The ID of the YouTube video. Defaults to None.

        Returns:
            YoutubeVideoCount: An object containing the metrics of the YouTube video.

        Raises:
            YoutubeError: If neither 'query' nor 'video_id' is provided.
        """
        if video_id is not None:
            return YoutubeAgent.__fetch_video_metrics_by_id(video_id)
        elif query is not None:
            return YoutubeAgent.__fetch_video_metrics_by_query(query)
        else:
            raise YoutubeError("must provide either 'query' or 'video_id'")

    @staticmethod
    def __fetch_video_metrics_by_id(video_id) -> YoutubeVideoCount:
        metrics = send_request(f"{env.YOUTUBE_VIDEO_STATS_API}/{video_id}")
        return YoutubeVideoCount(
            video_id=video_id,
            view_count=metrics.get("followerCount", 0),
            video_stats=metrics.get("bottomOdos", [0, 0, 0]),
        )

    @staticmethod
    def __fetch_video_metrics_by_query(query):
        video = YoutubeAgent.__find_exact_video(query)
        return YoutubeAgent.__fetch_video_metrics_by_id(video.video_id)
