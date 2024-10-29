import re
import warnings

import validators

from unofficial_livecounts_api import env
from unofficial_livecounts_api.utils import send_request


class TiktokUser:
    def __init__(
        self,
        user_id: str,
        username: str,
        display_name: str,
        thumbnail: str,
        verified: bool = None,
    ):
        self.user_id = user_id
        self.username = username
        self.thumbnail = thumbnail
        self.display_name = display_name
        self.verified = verified

    def __eq__(self, other):
        return self.user_id == other.user_id if isinstance(other, TiktokUser) else False

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "display_name": self.display_name,
            "thumbnail": self.thumbnail,
            "verified": self.verified,
        }


class TiktokUserCount:
    def __init__(
        self,
        user_id: str,
        follower_count: int,
        like_count: int,
        following_count: int,
        video_count: int,
    ):
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
            "video_count": self.video_count,
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
            "user": self.user,
        }


class TikTokVideoCount:
    def __init__(
        self,
        video_id: str,
        view_count: int,
        like_count: int,
        comment_count: int,
        share_count: int,
    ):
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
            "share_count": self.share_count,
        }


class TiktokAgent:

    @staticmethod
    def find_user(query: str) -> list[TiktokUser]:
        """
        Search for TikTok users based on a username query.

        Args:
            query (str): The username to search for on TikTok

        Returns:
            list[TiktokUser]: A list of TiktokUser objects containing:
                - user_id (str): Unique identifier of the user
                - username (str): Login name of the user
                - display_name (str): Display name shown on profile
                - verified (bool): Account verification status
                - thumbnail (str): URL to the user's profile picture
        """
        raw_users = send_request(f"{env.TIKTOK_USER_SEARCH_API}/{query}")
        return [
            TiktokUser(
                user_id=item.get("userId", ""),
                username=item.get("id", ""),
                display_name=item.get("username", ""),
                verified=item.get("verified", False),
                thumbnail=item.get("avatar", ""),
            )
            for item in raw_users.get("userData", [])
        ]

    @staticmethod
    def fetch_user_metrics(query: str) -> TiktokUserCount:
        """
        Fetch engagement metrics and statistics for a TikTok user.

        Args:
            query (str): The user_id of the TikTok user to fetch metrics for

        Returns:
            TiktokUserCount: An object containing user metrics including:
                - user_id (str): Unique identifier of the user
                - follower_count (int): Number of accounts following this user
                - like_count (int): Total number of likes received across all videos
                - following_count (int): Number of accounts this user follows
                - video_count (int): Total number of videos posted
        """
        metrics = send_request(f"{env.TIKTOK_USER_STATS_API}/{query}")
        return TiktokUserCount(
            user_id=query,
            follower_count=metrics.get("followerCount", 0),
            like_count=metrics.get("likeCount", 0),
            following_count=metrics.get("followingCount", 0),
            video_count=metrics.get("videoCount", 0),
        )

    @staticmethod
    def find_video(query: str) -> TiktokVideo:
        """
        Find a TikTok video by its URL or video ID.

        Args:
            query (str): Either a full TikTok video URL or a video ID

        Returns:
            TiktokVideo: An object containing video information including:
                - video_id (str): Unique identifier of the video
                - title (str): Title/caption of the video
                - thumbnail (str): URL to the video's cover image
                - user (TiktokUser | None): Author's profile information,
                  or None if user data is unavailable
        """
        if validators.url(query):
            query = TiktokAgent.__extract_video_id_from_given_url(query)
        return TiktokAgent.__find_video_by_id(query)

    @staticmethod
    def __find_video_by_id(video_id: str) -> TiktokVideo:
        """
        Internal method to fetch video information using a video ID.

        Args:
            video_id (str): The unique identifier of the TikTok video

        Returns:
            TiktokVideo: Video information and associated user data
        """
        video = send_request(url=f"{env.TIKTOK_VIDEO_SEARCH_API}/{video_id}")
        user = video.get("author", {})
        return TiktokVideo(
            video_id=video_id,
            title=video.get("title", ""),
            thumbnail=video.get("cover", ""),
            user=(
                TiktokUser(
                    user_id=user.get("userId", ""),
                    username=user.get("id", ""),
                    display_name=user.get("username", ""),
                    thumbnail=user.get("avatar", ""),
                )
                if user
                else None
            ),
        )

    @staticmethod
    def __extract_video_id_from_given_url(query) -> str | None:
        """
        Internal method to extract video ID from a TikTok URL.

        Args:
            query (str): Full TikTok video URL

        Returns:
            str | None: The extracted video ID or None if extraction fails

        Note:
            Issues a warning if video ID extraction fails
        """
        try:
            return re.search(r"video/(\d+)", query)[1]
        except Exception as e:
            warnings.warn(f"failed to extract video_id from Tiktok Video URL: {e}")
            return None

    @staticmethod
    def fetch_video_metrics(query: str) -> TikTokVideoCount:
        """
        Fetch engagement metrics for a TikTok video.

        Args:
            query (str): Either a full TikTok video URL or a video ID

        Returns:
            TikTokVideoCount: An object containing video metrics including:
                - video_id (str): Unique identifier of the video
                - like_count (int): Number of likes on the video
                - comment_count (int): Number of comments on the video
                - share_count (int): Number of times the video was shared
                - view_count (int): Number of video views
        """
        if validators.url(query):
            query = TiktokAgent.__extract_video_id_from_given_url(query)
        metrics = send_request(f"{env.TIKTOK_VIDEO_STATS_API}/{query}")
        return TikTokVideoCount(
            video_id=query,
            like_count=metrics.get("likeCount", 0),
            comment_count=metrics.get("commentCount", 0),
            share_count=metrics.get("shareCount", 0),
            view_count=metrics.get("viewCount", 0),
        )
