"""
Testing feed_media_backup
=========================

"""
import os

from unittest import mock

from click.testing import CliRunner

import feed_media_backup

import pytest

from tinydb import TinyDB

from youtube_dl.utils import DownloadError


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
    assert feed_media_backup.get_urls(inputstr) == expected


@mock.patch('feed_media_backup.youtube_dl.YoutubeDL', autospec=True)
def test_download(patch_ydl, tmpdir):
    """Testing download function."""
    feed_media_backup.download('http://foo.bar', tmpdir.strpath)

    patch_ydl.return_value.__enter__.return_value.download.assert_called_with(
        ['http://foo.bar']
    )


@pytest.mark.parametrize('exception,expected', [
    (DownloadError('foo'), False),
    (IndexError('foo'), False),
    (KeyboardInterrupt('foo'), None)
])
@mock.patch('feed_media_backup.sys', autospec=True)
@mock.patch('feed_media_backup.youtube_dl.YoutubeDL', autospec=True)
def test_download_except(patch_ydl, patch_sys, exception, expected, tmpdir):
    """Testing download function throwing exception."""
    patch_ydl.return_value.__enter__.return_value.download.side_effect = \
        exception

    assert feed_media_backup.download(
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

    with feed_media_backup.change_dir(tmpdir.join('foo').strpath):
        assert os.getcwd() == tmpdir.join('foo').strpath

    assert os.getcwd() == tmpdir.strpath


@pytest.mark.parametrize(
    (
        'force,'
        'verbose,'
        'db_prefill,'
        'db_expect,'
        'exit_code,'
        'download_return,'
        'urls,'
        'info,'
        'debug'
    ),
    [
        (
            False,
            False,
            None,
            [
                {
                    'id': (
                        'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                        'die-jawbreaker-dokumentation-dont-break-down/'
                    )
                }
            ],
            0,
            True,
            [
                (
                    'http://pitchfork.com/news/jawbreaker-documentary'
                    '-dont-break-down-gets-new-trailer-premiere-date-watch/'
                )
            ],
            [
                mock.call('extract links...'),
                mock.call('start to download article media...'),
                mock.call(
                    'downloaded %s',
                    (
                        'http://pitchfork.com/news/jawbreaker'
                        '-documentary-dont-break-down-gets-new-trailer'
                        '-premiere-date-watch/'
                    )
                )
            ],
            [
                mock.call(
                    'found %s',
                    (
                        'http://pitchfork.com/news/jawbreaker-'
                        'documentary-dont-break-down-gets-new-trailer-'
                        'premiere-date-watch/'
                    )
                ),
                mock.call(
                    'write %s to db...',
                    (
                        'tag:xsteadfastx.org,2017-07-13:'
                        '/2017/07/13/die-jawbreaker-dokumentation-'
                        'dont-break-down/'
                    )
                )
            ],
        ),
        (
            False,
            False,
            None,
            [
                {
                    'id': (
                        'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                        'die-jawbreaker-dokumentation-dont-break-down/'
                    )
                }
            ],
            0,
            False,
            [
                (
                    'http://pitchfork.com/news/jawbreaker-documentary'
                    '-dont-break-down-gets-new-trailer-premiere-date-watch/'
                )
            ],
            [
                mock.call(
                    'extract links...'
                    ),
                mock.call(
                    'start to download article media...'
                ),
                mock.call(
                    'did not download %s',
                    'http://pitchfork.com/news/jawbreaker-documentary-'
                    'dont-break-down-gets-new-trailer-premiere-date-watch/'
                )
            ],
            [
                mock.call(
                    'found %s',
                    (
                        'http://pitchfork.com/news/jawbreaker-'
                        'documentary-dont-break-down-gets-new-trailer-'
                        'premiere-date-watch/'
                    )
                ),
                mock.call(
                    'write %s to db...',
                    (
                        'tag:xsteadfastx.org,2017-07-13:'
                        '/2017/07/13/die-jawbreaker-dokumentation-'
                        'dont-break-down/'
                    )
                )
            ],
        ),
        (
            False,
            False,
            {
                'id': (
                    'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                    'die-jawbreaker-dokumentation-dont-break-down/'
                )
            },
            [
                {
                    'id': (
                        'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                        'die-jawbreaker-dokumentation-dont-break-down/'
                    )
                }
            ],
            0,
            False,
            [],
            [],
            [
                mock.call(
                    '%s already in db',
                    (
                        'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                        'die-jawbreaker-dokumentation-dont-break-down/'
                    )
                )
            ],
        ),
        (
            False,
            True,
            {
                'id': (
                    'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                    'die-jawbreaker-dokumentation-dont-break-down/'
                )
            },
            [
                {
                    'id': (
                        'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                        'die-jawbreaker-dokumentation-dont-break-down/'
                    )
                }
            ],
            0,
            False,
            [],
            [],
            [
                mock.call(
                    '%s already in db',
                    (
                        'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                        'die-jawbreaker-dokumentation-dont-break-down/'
                    )
                )
            ],
        ),
        (
            True,
            False,
            {
                'id': (
                    'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                    'die-jawbreaker-dokumentation-dont-break-down/'
                )
            },
            [
                {
                    'id': (
                        'tag:xsteadfastx.org,2017-07-13:/2017/07/13/'
                        'die-jawbreaker-dokumentation-dont-break-down/'
                    )
                }
            ],
            0,
            False,
            [
                (
                    'http://pitchfork.com/news/jawbreaker-documentary'
                    '-dont-break-down-gets-new-trailer-premiere-date-watch/'
                )
            ],
            [
                mock.call(
                    'extract links...'
                    ),
                mock.call(
                    'start to download article media...'
                ),
                mock.call(
                    'did not download %s',
                    'http://pitchfork.com/news/jawbreaker-documentary-'
                    'dont-break-down-gets-new-trailer-premiere-date-watch/'
                )
            ],
            [
                mock.call(
                    'found %s',
                    (
                        'http://pitchfork.com/news/jawbreaker-'
                        'documentary-dont-break-down-gets-new-trailer-'
                        'premiere-date-watch/'
                    )
                )
            ],
        ),

    ]
)
@mock.patch('feed_media_backup.logzero')
@mock.patch('feed_media_backup.logger')
@mock.patch('feed_media_backup.download')
@mock.patch('feed_media_backup.TinyDB')
def test_main(
        patch_tinydb,
        patch_download,
        patch_logger,
        patch_logzero,
        force,
        verbose,
        db_prefill,
        db_expect,
        exit_code,
        download_return,
        urls,
        info,
        debug,
        tmpdir
):
    """Testing main UI."""
    # prepare db mock
    database_loc = tmpdir.join('db.json')
    database = TinyDB(database_loc.strpath)

    if db_prefill:
        database.insert(db_prefill)

    patch_tinydb.return_value = database

    # prepare download mock
    patch_download.return_value = download_return

    runner = CliRunner()

    arg_opts = [
        os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)
            ),
            'test_data_feed.txt'
        ),
        tmpdir.mkdir('foo').strpath,
    ]

    if verbose:
        arg_opts.append('-v')

    if force:
        arg_opts.append('-f')

    result = runner.invoke(
        feed_media_backup.main,
        arg_opts
    )

    assert result.exit_code == exit_code

    if urls:
        for url in urls:
            patch_download.assert_called_with(
                url,
                tmpdir.join('foo').strpath
            )
    else:
        patch_download.assert_not_called()

    assert patch_logger.debug.mock_calls == debug
    assert patch_logger.info.mock_calls == info

    assert database.all() == db_expect

    if verbose:
        loglevel = 10
    else:
        loglevel = 20
    patch_logzero.loglevel.assert_called_with(loglevel)
