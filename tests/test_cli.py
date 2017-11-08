"""Testing cli."""

import os
from unittest import mock

import pytest
from click.testing import CliRunner
from tinydb import TinyDB

from feed_media_backup import cli


@pytest.mark.parametrize(
    (
        'force,'
        'verbose,'
        'db_prefill,'
        'db_expect,'
        'exit_code,'
        'download_return,'
        'urls,'
        'utils_info,'
        'utils_debug,'
        'cli_info,'
        'cli_debug'
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
            # utils info
            [],
            # utils debug
            [
                mock.call(
                    'found %s',
                    (
                        'http://pitchfork.com/news/jawbreaker-'
                        'documentary-dont-break-down-gets-new-trailer-'
                        'premiere-date-watch/'
                    )
                ),
            ],
            # cli info
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
            # cli debug
            [
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
            # utils info
            [],
            # utils debug
            [
                mock.call(
                    'found %s',
                    (
                        'http://pitchfork.com/news/jawbreaker-'
                        'documentary-dont-break-down-gets-new-trailer-'
                        'premiere-date-watch/'
                    )
                ),
            ],
            # cli info
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
            # cli debug
            [
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
            # utils info
            [],
            # utils debug
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
            # cli info
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
            # cli debug
            [],
        ),

    ]
)
@mock.patch('feed_media_backup.cli.loglevel')
@mock.patch('feed_media_backup.cli.logger')
@mock.patch('feed_media_backup.utils.logger')
@mock.patch('feed_media_backup.cli.download')
@mock.patch('feed_media_backup.cli.TinyDB')
def test_main(
        patch_tinydb,
        patch_download,
        patch_utils_logger,
        patch_cli_logger,
        patch_loglevel,
        force,
        verbose,
        db_prefill,
        db_expect,
        exit_code,
        download_return,
        urls,
        utils_info,
        utils_debug,
        cli_info,
        cli_debug,
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
        cli.main,
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

    assert patch_utils_logger.debug.mock_calls == utils_debug
    assert patch_cli_logger.debug.mock_calls == cli_debug

    assert patch_utils_logger.info.mock_calls == utils_info
    assert patch_cli_logger.info.mock_calls == cli_info

    assert database.all() == db_expect

    if verbose:
        loglevel = 10
    else:
        loglevel = 20
    patch_loglevel.assert_called_with(loglevel)
