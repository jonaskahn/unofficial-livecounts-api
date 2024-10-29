from unofficial_livecounts_api import env
from unofficial_livecounts_api.tiktok import (
    TiktokAgent,
    TiktokUser,
    TiktokUserCount,
    TiktokVideo,
    TikTokVideoCount,
)


def test_find_users_with_existed_user(mocker):
    mock_send_request = mocker.patch("unofficial_livecounts_api.tiktok.send_request")
    mock_send_request.return_value = {
        "userData": [
            {
                "userId": "12345",
                "id": "user1",
                "username": "best1",
                "verified": True,
                "avatar": "http://example.com/avatar1.jpg",
            },
            {
                "userId": "67890",
                "id": "user2",
                "username": "best2",
                "verified": False,
                "avatar": "http://example.com/avatar2.jpg",
            },
            {
                "userId": "67890",
                "id": "user3",
                "username": "user3-no-s-bet",
                "verified": False,
                "avatar": "http://example.com/avatar2.jpg",
            },
        ]
    }

    users = TiktokAgent.find_user("best")

    expected_users = [
        TiktokUser(
            user_id="12345",
            username="user1",
            display_name="best1",
            verified=True,
            thumbnail="http://example.com/avatar1.jpg",
        ),
        TiktokUser(
            user_id="67890",
            username="user2",
            display_name="best2",
            verified=False,
            thumbnail="http://example.com/avatar2.jpg",
        ),
        TiktokUser(
            user_id="67890",
            username="user3",
            display_name="user3-no-s-bet",
            verified=False,
            thumbnail="http://example.com/avatar2.jpg",
        ),
    ]
    mock_send_request.assert_called_once_with(f"{env.TIKTOK_USER_SEARCH_API}/best")
    assert users == expected_users


def test_find_users_with_not_existed_user(mocker):
    mock_send_request = mocker.patch("unofficial_livecounts_api.tiktok.send_request")
    mock_response = {"userData": []}
    mock_send_request.return_value = mock_response
    users = TiktokAgent.find_user("best")
    mock_send_request.assert_called_once_with(f"{env.TIKTOK_USER_SEARCH_API}/best")
    assert users == []


def test_fetch_user_metrics_with_existed_user_by_id(mocker):
    mock_send_request = mocker.patch("unofficial_livecounts_api.tiktok.send_request")
    mock_send_request.return_value = {
        "followerCount": 1,
        "likeCount": 2,
        "followingCount": 3,
        "videoCount": 4,
    }
    tiktok_metrics = TiktokAgent.fetch_user_metrics(query="7324489913931613189")
    expect_metrics: TiktokUserCount = TiktokUserCount(
        user_id="7324489913931613189",
        follower_count=1,
        like_count=2,
        following_count=3,
        video_count=4,
    )
    mock_send_request.assert_called_once_with(
        f"{env.TIKTOK_USER_STATS_API}/7324489913931613189"
    )
    assert tiktok_metrics == expect_metrics
    assert tiktok_metrics.user_id == expect_metrics.user_id
    assert tiktok_metrics.follower_count == expect_metrics.follower_count
    assert tiktok_metrics.like_count == expect_metrics.like_count
    assert tiktok_metrics.following_count == expect_metrics.following_count
    assert tiktok_metrics.video_count == expect_metrics.video_count


def test_find_video_with_existed_video_by_id(mocker):
    mock_send_request = mocker.patch("unofficial_livecounts_api.tiktok.send_request")
    mock_send_request.return_value = {
        "title": "bo-so-et",
        "id": "1",
        "cover": "http://example.com/cover1.jpg",
        "author": {
            "id": "best",
            "username": "bo-so-et",
            "userId": "1111",
            "avatar": "http://example.com/avatar1.jpg",
        },
    }
    video = TiktokAgent.find_video(query="1")
    mock_send_request.assert_called_once_with(
        url="https://tiktok.livecounts.io/video/data/1"
    )
    assert video == TiktokVideo(
        video_id="1",
        title="bo-so-et",
        thumbnail="http://example.com/avatar2.jpg",
        user=TiktokUser(
            user_id="1111",
            username="bo-so-et",
            display_name="bo-so-et",
            thumbnail="http://example.com/avatar1.jpg",
        ),
    )


def test_fetch_video_stats_with_existed_video_with_id(mocker):
    mocker_send_request = mocker.patch("unofficial_livecounts_api.tiktok.send_request")
    mocker_send_request.return_value = {
        "viewCount": 1,
        "commentCount": 2,
        "likeCount": 3,
        "shareCount": 4,
    }
    video = TiktokAgent.fetch_video_metrics(query="1")
    mocker_send_request.assert_called_once_with(f"{env.TIKTOK_VIDEO_STATS_API}/1")
    assert video == TikTokVideoCount(
        video_id="1", view_count=1, comment_count=2, like_count=3, share_count=4
    )
