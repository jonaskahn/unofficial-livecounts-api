from unofficial_livecounts_api import env
from unofficial_livecounts_api.error import TwitterError
from unofficial_livecounts_api.utils import send_request


class TwitterUser:
    def __init__(
        self, user_id: str, display_name: str, thumbnail: str, verified: bool = None
    ):
        self.user_id = user_id
        self.thumbnail = thumbnail
        self.display_name = display_name
        self.verified = verified

    def __eq__(self, other):
        return (
            self.user_id == other.user_id if isinstance(other, TwitterUser) else False
        )

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "thumbnail": self.thumbnail,
            "verified": self.verified,
        }


class TwitterUserCount:
    def __init__(self, user_id: str, follower_count: int, user_stats: list[int]):
        self.user_id = user_id
        self.follower_count = follower_count
        self.tweet_count = user_stats[0]
        self.following_count = user_stats[1]
        self.goal_count = user_stats[2]

    def __eq__(self, other):
        if not isinstance(other, TwitterUserCount):
            return False
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "follower_count": self.follower_count,
            "tweet_count": self.tweet_count,
            "following_count": self.following_count,
            "goal_count": self.goal_count,
        }


class TwitterAgent:

    @staticmethod
    def find_user(query: str) -> TwitterUser:
        """
        Find a Twitter user by their username.

        Args:
            query (str): The username of the Twitter user to find.

        Returns:
            TwitterUser

        Raise:
            TwitterError - if the user is not found.
        """
        users = send_request(f"{env.TWITTER_USER_SEARCH_API}/{query}").get(
            "userData", []
        )
        if not users:
            raise TwitterError("user not found")
        return TwitterUser(
            user_id=users[0]["id"],
            display_name=users[0]["username"],
            thumbnail=users[0]["avatar"],
            verified=users[0]["verified"],
        )

    @staticmethod
    def fetch_user_metrics(query: str) -> TwitterUserCount:
        """
        Fetches the metrics of a Twitter user based on their username.

        Args:
            query (str): The username of the Twitter user to fetch metrics for.

        Returns:
            TwitterUserCount: An instance of the TwitterUserCount class containing the metrics of the user.

        Raises:
            None
        """
        metrics = send_request(f"{env.TWITTER_USER_STATS_API}/{query}")
        return TwitterUserCount(
            user_id=query,
            follower_count=metrics.get("followerCount", 0),
            user_stats=metrics.get("bottomOdos", [0, 0, 0]),
        )


class XAgent(TwitterAgent):
    pass
