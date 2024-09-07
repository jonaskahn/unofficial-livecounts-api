from unofficial_livecounts_api import env
from unofficial_livecounts_api.twitter import TwitterAgent, TwitterUser, TwitterUserCount


def test_find_user_with_existed_user_by_username(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.twitter.send_request')
    mock_send_request.return_value = {
        "userData": [
            {
                "id": "jack",
                "username": "jacky chan",
                "avatar": "https://pbs.twimg.com/cover1.jpg",
                "verified": False
            }
        ]
    }

    user = TwitterAgent.find_user("jack")
    mock_send_request.assert_called_once_with(f"{env.TWITTER_USER_SEARCH_API}/jack")
    assert user == TwitterUser(
        user_id="jack",
        display_name="jacky chan",
        thumbnail="https://pbs.twimg.com/cover1.jpg",
        verified=False
    )


def test_fetch_user_metrics(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.twitter.send_request')
    mock_send_request.return_value = {
        "followerCount": 6536924,
        "bottomOdos": [
            29488,
            0,
            463076
        ]
    }
    metrics = TwitterAgent.fetch_user_metrics("jack")
    mock_send_request.assert_called_once_with(f"{env.TWITTER_USER_STATS_API}/jack")
    assert metrics == TwitterUserCount(
        user_id="jack",
        follower_count=6536924,
        user_stats=[29488, 0, 463076]
    )
