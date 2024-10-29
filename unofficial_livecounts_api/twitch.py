from unofficial_livecounts_api import env
from unofficial_livecounts_api.utils import send_request


class TwitchUser:
    def __init__(self, user_id: str, username: str, display_name: str, thumbnail: str):
        self.user_id = user_id
        self.username = username
        self.display_name = display_name
        self.thumbnail = thumbnail

    def __eq__(self, other):
        return self.user_id == other.user_id if isinstance(other, TwitchUser) else False

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "display_name": self.display_name,
            "thumbnail": self.thumbnail,
        }


class TwitchUserCount:
    def __init__(self, user_id: str, follower_count: int):
        self.user_id = user_id
        self.follower_count = follower_count

    def __eq__(self, other):
        return self.user_id == other.user_id if isinstance(other, TwitchUserCount) else False

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {"user_id": self.user_id, "follower_count": self.follower_count}


class TwitchAgent:

    @staticmethod
    def find_user(query: str) -> list[TwitchUser]:
        """
        Search for Twitch users by username and return a list of matching profiles.

        Args:
            query (str): The username to search for on Twitch

        Returns:
            list[TwitchUser]: A list of TwitchUser objects containing:
                - user_id (str): Unique identifier of the user
                - username (str): Login name of the user
                - display_name (str): Display name shown on profile
                - thumbnail (str): URL to the user's profile picture
        Note:
            Returns an empty list if no users are found matching the query
        """
        raw_user = send_request(f"{env.TWITCH_USER_SEARCH_API}/{query}")
        return [
            TwitchUser(
                user_id=item.get("userId", item.get("userid", "")),
                username=item.get("id", ""),
                display_name=item.get("username", ""),
                thumbnail=item.get("avatar", ""),
            )
            for item in raw_user.get("userData", [])
        ]

    @staticmethod
    def fetch_user_metrics(query: str) -> TwitchUserCount:
        """
        Fetch follower metrics for a specific Twitch user.

        Args:
            query (str): The username of the Twitch user to fetch metrics for

        Returns:
            TwitchUserCount: An object containing user metrics including:
                - user_id (str): Username of the account
                - follower_count (int): Number of followers for the channel
        """
        metrics = send_request(f"{env.TWITCH_USER_STATS_API}/{query}")
        return TwitchUserCount(
            user_id=query,
            follower_count=metrics.get("followerCount", 0),
        )
