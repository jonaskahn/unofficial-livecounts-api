from unofficial_livecounts_api import env
from unofficial_livecounts_api.twitch import TwitchAgent, TwitchUser, TwitchUserCount


def test_find_user_with_existed_user_by_username(mocker):
    mock_send_request = mocker.patch("unofficial_livecounts_api.twitch.send_request")
    mock_send_request.return_value = {
        "userData": [
            {
                "userid": "101020771",
                "id": "repaz",
                "display_name": "Repaz",
                "avatr": "https://static-cdn.jtvnw.net/jtv_user_pictures/98e43b4c-ad0f-4964-88a9-d3de34eb58ac-profile_image-300x300.png",
            }
        ]
    }

    user = TwitchAgent.find_user("repaz")
    mock_send_request.assert_called_once_with(f"{env.TWITCH_USER_SEARCH_API}/repaz")
    assert user[0] == TwitchUser(
        user_id="101020771",
        username="repaz",
        display_name="Repaz",
        thumbnail="https://static-cdn.jtvnw.net/jtv_user_pictures/98e43b4c-ad0f-4964-88a9-d3de34eb58ac-profile_image-300x300.png",
    )


def test_fetch_user_metrics(mocker):
    mock_send_request = mocker.patch("unofficial_livecounts_api.twitch.send_request")
    mock_send_request.return_value = {"followerCount": 6536924}
    metrics = TwitchAgent.fetch_user_metrics("101020771")
    mock_send_request.assert_called_once_with(f"{env.TWITCH_USER_STATS_API}/101020771")
    assert metrics == TwitchUserCount(user_id="101020771", follower_count=6536924)
