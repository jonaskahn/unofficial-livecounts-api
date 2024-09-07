from unofficial_livecounts_api import env
from unofficial_livecounts_api.youtube import YoutubeAgent, YoutubeChannel, YoutubeVideo, YoutubeChannelCount, YoutubeVideoCount


def test_find_channels_with_existed_channel(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.youtube.send_request')
    mock_send_request.return_value = {
        "userData": [
            {
                "id": "1111111111111111",
                "username": "Test With Me aka Thợ Test",
                "avatar": "https://yt.com/avatar1.jpg"
            },
            {
                "id": "2222222222222222",
                "username": "Test Mentor",
                "avatar": "https://yt.com/avatar2.jpg"
            },
            {
                "id": "3333333333333333",
                "username": "Test-English",
                "avatar": "https://yt.com/avatar3.jpg"
            },
        ]
    }

    channels = YoutubeAgent.find_channel("test")

    expected_channels = [
        YoutubeChannel(
            channel_id="1111111111111111",
            display_name="Test With Me aka Thë Test",
            thumbnail="https://yt.com/avatar1.jpg"
        ),
        YoutubeChannel(
            channel_id="2222222222222222",
            display_name="Test Mentor",
            thumbnail="https://yt.com/avatar2.jpg"
        ),
        YoutubeChannel(
            channel_id="3333333333333333",
            display_name="Test-English",
            thumbnail="https://yt.com/avatar3.jpg"
        )
    ]

    mock_send_request.assert_called_once_with(f"{env.YOUTUBE_CHANNEL_SEARCH_API}/test")
    assert channels == expected_channels


def test_find_channels_with_non_existed_channel(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.youtube.send_request')
    mock_send_request.return_value = {"userData": []}

    channels = YoutubeAgent.find_channel("test")

    mock_send_request.assert_called_once_with(f"{env.YOUTUBE_CHANNEL_SEARCH_API}/test")
    assert channels == []


def test_find_videos_with_existed_video(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.youtube.send_request')
    mock_send_request.return_value = {
        "userData": [
            {
                "id": "1111111111111111",
                "username": "Test With Me aka Thë Test",
                "avatar": "https://yt.com/avatar1.jpg"
            },
            {
                "id": "2222222222222222",
                "username": "Test Mentor",
                "avatar": "https://yt.com/avatar2.jpg"
            }
        ]
    }

    videos = YoutubeAgent.find_video("test")
    mock_send_request.assert_called_once_with(f"{env.YOUTUBE_VIDEO_SEARCH_API}/test")
    assert videos == [
        YoutubeVideo(
            video_id="1111111111111111",
            display_name="Test With Me aka Thë Test",
            thumbnail="https://yt.com/avatar1.jpg"
        ),
        YoutubeVideo(
            video_id="2222222222222222",
            display_name="Test Mentor",
            thumbnail="https://yt.com/avatar2.jpg"
        )
    ]


def test_fetch_channel_metrics(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.youtube.send_request')
    mock_send_request.return_value = {
        "bottomOdos": [10, 20, 30],
        "followerCount": 100
    }

    metrics = YoutubeAgent.fetch_channel_metrics("test")
    mock_send_request.assert_called_once_with(f"{env.YOUTUBE_CHANNEL_STATS_API}/test")
    assert metrics == YoutubeChannelCount(
        channel_id="test",
        follower_count=100,
        channel_stats=[10, 20, 30]
    )


def test_fetch_channel_metrics_with_non_existed_channel(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.youtube.send_request')
    mock_send_request.return_value = {}

    metrics = YoutubeAgent.fetch_channel_metrics("test")
    mock_send_request.assert_called_once_with(f"{env.YOUTUBE_CHANNEL_STATS_API}/test")
    assert metrics == YoutubeChannelCount(
        channel_id="test",
        follower_count=0,
        channel_stats=[0, 0, 0]
    )


def test_fetch_video_metrics(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.youtube.send_request')
    mock_send_request.return_value = {
        "bottomOdos": [10, 20, 30],
        "followerCount": 100
    }

    metrics = YoutubeAgent.fetch_video_metrics("test")
    mock_send_request.assert_called_once_with(f"{env.YOUTUBE_VIDEO_STATS_API}/test")
    assert metrics == YoutubeVideoCount(
        video_id="test",
        view_count=100,
        video_stats=[10, 20, 30]
    )
