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
        return (
            self.user_id == other.user_id
            if isinstance(other, TwitchUserCount)
            else False
        )

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {"user_id": self.user_id, "follower_count": self.follower_count}


class TwitchAgent:

    @staticmethod
    def find_user(query: str) -> list[TwitchUser]:
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
        metrics = send_request(f"{env.TWITCH_USER_STATS_API}/{query}")
        return TwitchUserCount(
            user_id=query,
            follower_count=metrics.get("followerCount", 0),
        )
