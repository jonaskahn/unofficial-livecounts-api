import re
import warnings

from livecounts_api import env

from unofficial_livecounts_api.error import TiktokError
from unofficial_livecounts_api.utils import send_request


class TiktokUser:
    def __init__(self, user_id: str, username: str, display_name: str, thumbnail: str, verified: bool = None):
        self.user_id = user_id
        self.username = username
        self.thumbnail = thumbnail
        self.display_name = display_name
        self.verified = verified

    def __eq__(self, other):
        return self.user_id == other.user_id if isinstance(other, TiktokUser) else False

    def __hash__(self):
        return hash(self.user_id)

    def __dir__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "display_name": self.display_name,
            "thumbnail": self.thumbnail,
            "verified": self.verified
        }


class TiktokUserCount:
    def __init__(self, user_id: str, follower_count: int, like_count: int, following_count: int, video_count: int):
        self.user_id = user_id
        self.follower_count = follower_count
        self.like_count = like_count
        self.following_count = following_count
        self.video_count = video_count

    def __eq__(self, other):
        if not isinstance(other, TiktokUserCount):
            return False
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "follower_count": self.follower_count,
            "like_count": self.like_count,
            "following_count": self.following_count,
            "video_count": self.video_count
        }


class TiktokVideo:
    def __init__(self, video_id: str, title: str, thumbnail: str, user: TiktokUser):
        self.video_id = video_id
        self.title = title
        self.thumbnail = thumbnail
        self.user = user

    def __eq__(self, other):
        if not isinstance(other, TiktokVideo):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "user": self.user
        }


class TikTokVideoCount:
    def __init__(self, video_id: str, view_count: int, like_count: int, comment_count: int, share_count: int):
        self.video_id = video_id
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count
        self.share_count = share_count

    def __eq__(self, other):
        if not isinstance(other, TikTokVideoCount):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "comment_count": self.comment_count,
            "share_count": self.share_count
        }


class TiktokAgent:

    @staticmethod
    def find_user(query: str, exact: bool = False) -> list[TiktokUser] | TiktokUser:
        """
        Find TikTok user(s) based on the provided query.

        Args:
            query (str): The search query to find a user or list of potential users.
            exact (bool): If True, finds an exact match for the query. Defaults to False.

        Returns:
            list[TiktokUser] | TiktokUser

        Raises:
            TiktokError - if the user is not found.
        """
        return TiktokAgent.__find_exact_user(query) if exact else TiktokAgent.__find_users(query)

    @staticmethod
    def __find_users(query: str) -> list[TiktokUser]:
        data = send_request(f"{env.TIKTOK_USER_SEARCH_API}/{query}")
        return [
            TiktokUser(
                user_id=item.get("userId", ""),
                username=item.get("id", ""),
                display_name=item.get("username", ""),
                verified=item.get("verified", False),
                thumbnail=item.get("avatar", ""),
            )
            for item in data.get("userData", [])
        ]

    @staticmethod
    def __find_exact_user(query: str) -> TiktokUser:
        users = TiktokAgent.__find_users(query)
        for user in users:
            if user.username == query or user.display_name == query:
                return user
        raise TiktokError("tiktok user is not found")

    @staticmethod
    def fetch_user_metrics(query: str = None, user_id: str = None) -> TiktokUserCount:
        """
        Fetch user metrics from TikTok API.

        Args:
            query (str): The username of the TikTok user.
            user_id (str): The ID of the TikTok user.

        Returns:
            TiktokUserCount: An object containing user metrics.

        Raises:
            TiktokError: If neither 'query' nor 'tiktok_id' is provided.
        """
        if user_id is not None:
            return TiktokAgent.__fetch_user_metrics_by_tiktok_id(user_id)
        elif query is not None:
            return TiktokAgent.__fetch_user_metrics_by_query(query)
        else:
            raise TiktokError("must provide either 'query' or 'tiktok_id'")

    @staticmethod
    def __fetch_user_metrics_by_tiktok_id(tiktok_id: str) -> TiktokUserCount:
        metrics = send_request(f"{env.TIKTOK_USER_STATS_API}/{tiktok_id}")
        return TiktokUserCount(
            user_id=tiktok_id,
            follower_count=metrics.get("followerCount", 0),
            like_count=metrics.get("likeCount", 0),
            following_count=metrics.get("followingCount", 0),
            video_count=metrics.get("videoCount", 0)
        )

    @staticmethod
    def __fetch_user_metrics_by_query(query) -> TiktokUserCount:
        user = TiktokAgent.__find_exact_user(query)
        return TiktokAgent.__fetch_user_metrics_by_tiktok_id(user.user_id)

    @staticmethod
    def find_video(query: str = None, video_id: str = None) -> TiktokVideo:
        """
        Find a TikTok video by its ID or URL.

        Args:
            query (str): The URL of the TikTok video.
            video_id (str): The ID of the TikTok video.

        Returns:
            TiktokVideo: An object containing video information.

        Raises:
            TiktokError: If neither 'query' nor 'video_id' is provided.
        """
        if query is not None:
            video_id = TiktokAgent.__extract_video_id_from_given_url(query)
        if video_id is None:
            raise TiktokError("must provide either 'query' or 'video_id'")
        return TiktokAgent.__find_video_by_id(video_id)

    @staticmethod
    def __find_video_by_id(video_id: str) -> TiktokVideo:
        video = send_request(url=f"{env.TIKTOK_VIDEO_SEARCH_API}/{video_id}")
        user = video.get("author", {})
        return TiktokVideo(
            video_id=video_id,
            title=video.get("title", ""),
            thumbnail=video.get("cover", ""),
            user=TiktokUser(
                user_id=user.get("userId", ""),
                username=user.get("id", ""),
                display_name=user.get("username", ""),
                thumbnail=user.get("avatar", "")
            ) if user else None
        )

    @staticmethod
    def __extract_video_id_from_given_url(query) -> str | None:
        try:
            return re.search(r"video/(\d+)", query)[1]
        except Exception as e:
            warnings.warn(f"failed to extract video_id from Tiktok Video URL: {e}")
            return None

    @staticmethod
    def fetch_video_metrics(query: str = None, video_id: str = None) -> TikTokVideoCount:
        """
        Fetch the metrics of a TikTok video.

        Args:
            query (str, optional): The URL of the TikTok video. Defaults to None.
            video_id (str, optional): The ID of the TikTok video. Defaults to None.

        Returns:
            TikTokVideoCount: An object containing the metrics of the TikTok video.

        Raises:
            TiktokError: If neither 'query' nor 'video_id' is provided.
        """
        if query is not None:
            video_id = TiktokAgent.__extract_video_id_from_given_url(query)
        elif video_id is None:
            raise TiktokError("must provide either 'query' or 'video_id'")

        metrics = send_request(f"{env.TIKTOK_VIDEO_STATS_API}/{video_id}")
        return TikTokVideoCount(
            video_id=video_id,
            like_count=metrics.get("likeCount", 0),
            comment_count=metrics.get("commentCount", 0),
            share_count=metrics.get("shareCount", 0),
            view_count=metrics.get("viewCount", 0)
        )
