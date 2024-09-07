from livecounts_api import env

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
    def __init__(self, channel_id: str, follower_count: int, channel_count: list[int]):
        self.channel_id = channel_id
        self.follower_count = follower_count
        self.channel_count = channel_count

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
            "channel_count": self.channel_count
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
    def __init__(self, video_id: str, likes: int, dis_likes: int, raw_likes: int, raw_dislikes: int, view_count: int, is_delete: bool = None):
        self.video_id = video_id
        self.likes = likes
        self.dis_likes = dis_likes
        self.raw_likes = raw_likes
        self.raw_dislikes = raw_dislikes
        self.view_count = view_count
        self.is_delete = is_delete

    def __eq__(self, other):
        if not isinstance(other, YoutubeVideoCount):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "likes": self.likes,
            "dis_likes": self.dis_likes,
            "raw_likes": self.raw_likes,
            "raw_dislikes": self.raw_dislikes,
            "view_count": self.view_count,
            "is_delete": self.is_delete
        }


class YoutubeAgent:

    @staticmethod
    def find_user(query: str, exact: bool = False) -> list[YoutubeChannel] | YoutubeChannel:
        """
        Finds a YouTube user based on the provided query.

        Args:
            query (str): The search query (channel_id or username) to find a channel or list of potential channels.
            exact (bool, optional): If True, finds an exact match for the query, strongly recommend use channel_id for query. Defaults to False.

        Returns:
            list[YoutubeUser] | YoutubeUser
        """
        return YoutubeAgent.__find_exact_user(query) if exact else YoutubeAgent.__find_users(query)

    @staticmethod
    def __find_users(query: str) -> list[YoutubeChannel]:
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
    def __find_exact_user(query: str) -> YoutubeChannel:
        users = YoutubeAgent.__find_users(query)
        for user in users:
            if user.channel_id == query:
                return user
        raise YoutubeError("youtube channel is not found")

    @staticmethod
    def find_video(query: str, exact: bool = False) -> list[YoutubeVideo] | YoutubeVideo:
        """
        Finds a YouTube video based on the provided query.

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
            if video.video_id == query:
                return video
        raise YoutubeError("youtube video is not found")
