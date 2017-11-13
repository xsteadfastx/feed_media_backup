feed_media_backup
=================

[![Build Status](https://travis-ci.org/xsteadfastx/feed_media_backup.svg?branch=master)](https://travis-ci.org/xsteadfastx/feed_media_backup)
[![codecov](https://codecov.io/gh/xsteadfastx/feed_media_backup/branch/master/graph/badge.svg)](https://codecov.io/gh/xsteadfastx/feed_media_backup)
[![PyPI](https://img.shields.io/pypi/v/feed_media_backup.svg)](https://pypi.org/project/feed-media-backup/)

`feed_media_backup` is a simple downloader of feed media. Some weeks ago i browsed my blog and found out that alot of media i linked and shared are no longer available. This is pretty bad for people browsing the blog or even found it through a web search. Its also frustrating if you use the blog as log for things you dont want to forget or appriciate.

With this little script you have the chance to backup it at least for yourself. Thanks to [youtube-dl](https://github.com/rg3/youtube-dl). 

**This is a educational experiment and should never be used to steal anything or violate any copyrights!!1!!!11!**

```
Usage: feed_media_backup [OPTIONS] FEED DEST

  Backups media from blog RSS feeds.

Options:
  -f, --force    No matter if already worked through feed item.
  -v, --verbose  More verbose.
  --version      Show the version and exit.
  --help         Show this message and exit.

```

Install
-------

**Again... dont violate any copyrights!1!!!1!!**

There are a few options to install `feed_media_backup`:

1. `wget https://github.com/xsteadfastx/feed_media_backup/archive/feed_media_backup-`uname -s`-`uname -m`.pex -O feed_media_backup`
2. `pip install feed_media_backup`
3. `pip install git+https://github.com/xsteadfastx/feed_media_backup#egg=feed_media_backup`
4. `git clone https://github.com/xsteadfastx/feed_media_backup.git && cd feed_media_backup && pipenv --three && pipenv install && pipenv run pip install -e .`
