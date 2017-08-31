"""
feed_media_backup
=================

"""
import logging

import os

import sys

from contextlib import contextmanager

from typing import Generator, List

from bs4 import BeautifulSoup

import click

import feedparser

import logzero
from logzero import logger

from tinydb import Query, TinyDB

import youtube_dl


__version__ = '0.0.1'


@contextmanager
def change_dir(directory: str) -> Generator[str, None, None]:
    """Contextmanager to temporary change working directory."""
    cwd = os.path.abspath(os.getcwd())
    os.chdir(os.path.abspath(directory))
    yield os.getcwd()
    os.chdir(cwd)


def get_urls(html: str) -> List[str]:
    """Extract urls from html."""
    soup = BeautifulSoup(html, 'lxml')

    urls = [a['href'] for a in soup.find_all('a')]
    logger.debug('found %s', ' '.join(urls))

    return urls


def download(url: str, dest: str) -> bool:
    """Download media from url."""
    # youtube-dl options
    ydl_opts = {
        'logger': logger,
    }
    with change_dir(dest):

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return True

        except youtube_dl.utils.DownloadError:
            logger.error('Could not find media')

            return False

        except KeyboardInterrupt:
            sys.exit()

        except BaseException as error:
            logger.exception(str(error))
            return False


@click.command()
@click.argument(
    'feed'
)
@click.argument(
    'dest',
    type=click.Path(exists=True)
)
@click.option(
    '--force', '-f',
    is_flag=True,
    help='No matter if already worked through feed item.'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='More verbose.'
)
@click.version_option()
def main(feed: str, dest: str, force: bool, verbose: bool) -> None:
    """Backups media from blog RSS feeds."""
    # set log level
    if verbose:
        logzero.loglevel(logging.DEBUG)
    else:
        logzero.loglevel(logging.INFO)

    # database init
    database = TinyDB(os.path.join(dest, 'db.json'))
    feed_item = Query()

    parsed_feed = feedparser.parse(feed)  # type: feedparser.FeedParserDict
    for entry in parsed_feed['entries']:

        already_in_db = database.search(feed_item.id == entry['id'])

        if not already_in_db or force:

            # getting links
            logger.info('extract links...')

            urls = []  # type: List[str]
            for content in entry.content:
                urls.extend(get_urls(content['value']))

            # try to download links
            logger.info('start to download article media...')
            for url in urls:

                downloaded = download(url, dest)

                if downloaded:
                    logger.info('downloaded %s', url)
                else:
                    logger.info('did not download %s', url)

            # write to db
            if not already_in_db:
                logger.debug('write %s to db...', entry['id'])
                database.insert(
                    {
                        'id': entry['id']
                    }
                )

        else:
            logger.debug('%s already in db', entry['id'])
