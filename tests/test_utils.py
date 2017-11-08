"""Testing utils."""

import os
from unittest import mock

import pytest
from youtube_dl.utils import DownloadError

from feed_media_backup import utils


@pytest.mark.parametrize('inputstr,expected', [
    (
        'foo <a href="http://foo.bar">bar</a>',
        [
            'http://foo.bar'
        ]
    ),
])
def test_get_urls(inputstr, expected):
    """Testing get_urls function."""
    assert utils.get_urls(inputstr) == expected


@mock.patch('feed_media_backup.utils.youtube_dl.YoutubeDL', autospec=True)
def test_download(patch_ydl, tmpdir):
    """Testing download function."""
    utils.download('http://foo.bar', tmpdir.strpath)

    patch_ydl.return_value.__enter__.return_value.download.assert_called_with(
        ['http://foo.bar']
    )


@pytest.mark.parametrize('exception,expected', [
    (DownloadError('foo'), False),
    (IndexError('foo'), False),
    (KeyboardInterrupt('foo'), None)
])
@mock.patch('feed_media_backup.utils.sys', autospec=True)
@mock.patch('feed_media_backup.utils.youtube_dl.YoutubeDL', autospec=True)
def test_download_except(patch_ydl, patch_sys, exception, expected, tmpdir):
    """Testing download function throwing exception."""
    patch_ydl.return_value.__enter__.return_value.download.side_effect = \
        exception

    assert utils.download(
        'http://foo.bar',
        tmpdir.strpath
    ) is expected

    if exception == KeyboardInterrupt:
        patch_sys.exit.assert_called_once()


def test_change_dir(tmpdir):
    """Testing change_dir function."""
    tmpdir.mkdir('foo')
    os.chdir(tmpdir.strpath)

    assert os.getcwd() == tmpdir.strpath

    with utils.change_dir(tmpdir.join('foo').strpath):
        assert os.getcwd() == tmpdir.join('foo').strpath

    assert os.getcwd() == tmpdir.strpath
