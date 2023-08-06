# coding=utf-8
""" Watch Torrent RSS feeds and download new torrent files.
"""
# Copyright (C) 2015-2022 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import click
import feedparser
import hashlib
import json
import logging
import os
import re
import requests
import socket
import sys
import time
from collections import namedtuple
from functools import partial
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

# Globals and Logging
cfg_file = os.path.expanduser('~/.blacksap.cfg')
config = {'feeds': list(), 'app': dict()}
http_header = {'user-agent': "Mozilla/5.0"}
RSSFeed = namedtuple('RSSFeed', ['data', 'hash'])
_getaddrinfo = socket.getaddrinfo  # For disabling IPv6

log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(levelname)s:%(funcName)s:%(message)s'))
log.addHandler(log_handler)
log.setLevel(logging.WARNING)
log.propagate = False  # Keeps our messages out of the root logger.


def disable_ipv6(host, port, family=0, socktype=0, proto=0, flags=0):
    """ Hack from http://stackoverflow.com/questions/2014534/force-python-mechanize-urllib2-to-only-use-a-requests
    to disable IPv6 within requests module

    :return: Patched function to assign socket.getaddrinfo to
    """
    return _getaddrinfo(host, port, socket.AF_INET, socktype, proto, flags)


def enabled_feeds(feeds):
    """ Return only enabled feeds from config.  If feed doesn't have enabled flag, add it.

    :param feeds: List of feed configs read from config file
    :return: List of feed configs
    """
    enabled = list()
    for f in feeds:
        if 'enabled' in f.keys():
            if f['enabled']:
                enabled.append(f)
        else:
            f['enabled'] = True
            enabled.append(f)
    return enabled


class BSError(Exception):
    """ blacksap error class
    """


class BSTimer(object):
    """ Class to time certain operations
    """

    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.delta = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        """ Star the timer
        """
        self.start_time = time.time()

    def stop(self):
        """ Stop the timer
        """
        self.stop_time = time.time()
        self.delta = format(float(self.stop_time - self.start_time), '.4f')


def _blacksap(destination, reverse, count, feed):
    """ Private function which allows run sub-command to be threaded

    :param destination: Path to destination directory for torrent files
    :param reverse: Reverse RSS feed data before downloading torrents
    :param count: Limit the number of torrent files to download
    :param feed: Feed Config
    :return: Feed config
    """
    try:
        rss = download_rss_feed(feed['url'])
    except BSError as err:
        log.debug(err)
        click.echo(feed['name'] + ': Unable to update RSS', err=True)
        return feed

    if feed['new'] and count == -1:
        count = 1
        feed['new'] = False

    if count == -1 and feed['hash'] == rss.hash:
        click.echo(feed['name'] + ': No new torrent files')
    else:
        feed['hash'] = rss.hash  # Update the hash now that we've checked it
        entries = rss.data['entries']
        downloaded_torrents = list()
        if reverse:
            entries = list(reversed(entries))
        if count == 0:
            entries = list()
        elif count > 0:
            entries = entries[0:count]
        if 'rules' in feed.keys():
            log.info('RegEx Rules Enabled')
        for torrent in entries:
            log.debug(torrent)
            try:
                torrent_name = torrent['torrent_filename']
            except KeyError:
                torrent_name = torrent['title']
            if count == -1 and torrent_name == feed['last']:
                break
            else:
                try:
                    torrent_url = [x['href'] for x in torrent['links'] if x['type'] == 'application/x-bittorrent'].pop()
                except IndexError:
                    torrent_url = [x['href'] for x in torrent['links']].pop()
                if 'rules' in feed.keys():
                    for expr in feed['rules']:
                        if re.search(expr, torrent_name):
                            log.info('RegEx Match: (' + expr + ') for: ' + torrent_name)
                            if torrent_name not in downloaded_torrents:
                                try:
                                    download_torrent_file(torrent_url, destination, torrent_name)
                                    downloaded_torrents.append(torrent_name)
                                    break
                                except BSError as err:
                                    log.debug(err)
                else:
                    if torrent_name not in downloaded_torrents:
                        try:
                            download_torrent_file(torrent_url, destination, torrent_name)
                            downloaded_torrents.append(torrent_name)
                        except BSError as err:
                            log.debug(err)
        if len(downloaded_torrents) == 0:
            click.echo(feed['name'] + ': No new torrent files')
        else:
            click.echo(feed['name'] + ': downloaded ' + str(len(downloaded_torrents)) + ' torrents')
            if reverse:
                feed['last'] = downloaded_torrents.pop()
            else:
                feed['last'] = downloaded_torrents[0]
    return feed


def download_torrent_file(url, destination, filename, proxies=None):
    """Attempt to download a torrent file to a destination

    :param url: URL of torrent file
    :param destination: POSX path to output location
    :param filename: Name of the output file
    :param proxies: Dictionary of HTTP/HTTPS SOCKS Proxies
    :return: True on file write
    :raises: BSError
    """
    global http_header
    if filename.endswith('.torrent') is False:
        filename += '.torrent'
    if url.startswith('http') is False:
        raise BSError('Not a url', url)
    if '?' in url:
        url = str(url.split('?')[0])
    rdata = requests.get(url, headers=http_header, proxies=proxies)
    if rdata.status_code != 200:
        raise BSError(rdata.status_code, rdata.reason)
    else:
        filename = filename.replace('/', '_')
        with open(destination + filename, 'wb') as tf:
            tf.write(rdata.content)
        return True


def download_rss_feed(url, proxies=None):
    """ Download an RSS feed and parse the contents.  Follows Redirects.

    :param url: URL to RSS feed
    :param proxies: Dictionary of HTTP/HTTPS SOCKS Proxies
    :return: NamedTuple(data, hash)
    :raises: BSError
    """
    global http_header, log
    if url.startswith('http') is False:
        raise BSError('Not a url', url)
    try:
        log.debug('GET: ' + url)
        log.debug('Headers: ' + str(http_header))
        rdata = requests.get(url, headers=http_header, timeout=5, proxies=proxies)
    except requests.exceptions.Timeout:
        raise BSError('Download timed out')
    except Exception as err:
        if 'Address type not supported' in str(err):
            raise BSError('IPv6 not supported by proxy')
        else:
            raise BSError(err)
    if rdata.status_code != 200:
        raise BSError(rdata.status_code, rdata.reason)
    if rdata.url != url:
        return download_rss_feed(rdata.url)
    else:
        parsed_feed = feedparser.parse(rdata.text)
        if 'bozo_exception' in parsed_feed.keys():
            raise BSError(rdata.status_code, parsed_feed['bozo_exception'])
        else:
            return RSSFeed(data=parsed_feed, hash=hashlib.sha1(rdata.text.encode('utf-8')).hexdigest())


@click.group()
@click.version_option()
@click.option('--debug', '-d', is_flag=True, help='Enable debug output')
@click.option('--verbose', '-v', count=True, help='Increase debug verbosity')
def cli(**kwargs):
    """ Track torrent RSS feeds and download torrent files
    """
    global cfg_file, config, log
    if kwargs['debug']:
        log.setLevel(logging.INFO)
        if kwargs['verbose']:
            log.setLevel(logging.DEBUG)
    log.debug(kwargs)
    if os.path.exists(cfg_file):
        log.info('Reading configuration file: ' + cfg_file)
        with open(cfg_file) as fp:
            try:
                config = json.load(fp)
            except json.decoder.JSONDecodeError as err:
                log.debug(err)
                click.echo('Error reading: ' + cfg_file, err=True)
                sys.exit(1)
    else:
        log.info('No configuration file found. Starting fresh.')

    try:
        _proxies = dict(config['app']['proxies'])
        if sorted(_proxies.keys()) != ['http', 'https']:
            raise click.UsageError('Proxies config requires setting for http and https')
        log.info('Proxies: ' + str(_proxies))
    except (KeyError, ValueError):
        config['app']['proxies'] = dict(http=None, https=None)

    try:
        if not bool(config['app']['ipv6']):
            socket.getaddrinfo = disable_ipv6
            log.info('IPv6: Disabled')
    except (KeyError, ValueError):
        config['app']['ipv6'] = True
    log.debug(config)


@cli.command('track')
@click.option('--name', '-N', help='Name for RSS Feed')
@click.argument('url', required=True)
def cli_track(**kwargs):
    """ Track a new RSS feed
    """
    global cfg_file, config, log
    log.debug(kwargs)
    for feed in config['feeds']:
        if kwargs['url'] == feed['url']:
            click.echo('Already tracking: ' + feed['name'])
            break
    else:
        try:
            rss_feed, rss_hash = download_rss_feed(kwargs['url'])
        except (requests.HTTPError, BSError) as err:
            log.debug(err)
            click.echo('Unable to download: ' + kwargs['url'], err=True)
            sys.exit(err[0])
        feed = {'url': kwargs['url'],
                'name': rss_feed['feed']['title'],
                'hash': rss_hash,
                'enabled': True,
                'new': True,
                'last': None}
        if kwargs['name']:
            feed['name'] = kwargs['name']
        config['feeds'].append(feed)
        with open(cfg_file, 'w') as fp:
            json.dump(config, fp, indent=2)
        log.debug('Wrote config file')
        click.echo('Added RSS feed: ' + feed['name'])
    sys.exit(0)


@cli.command('untrack')
@click.argument('url', required=True)
def cli_untrack(**kwargs):
    """ Stop tracking an RSS feed
    """
    global cfg_file, config, log
    log.debug(kwargs)
    if len(config['feeds']) == 0:
        click.echo('Zero feeds tracked', err=True)
        sys.exit(0)
    newfeeds = list()
    for feed in config['feeds']:
        if feed['url'] != kwargs['url']:
            newfeeds.append(feed)
        else:
            click.echo('Untracked RSS feed: ' + feed['name'])
    if len(newfeeds) == len(config['feeds']):
        click.echo('Not being tracked: ' + kwargs['url'], err=True)
    config['feeds'] = newfeeds
    with open(cfg_file, 'w') as fp:
        json.dump(config, fp, indent=2)
    log.debug('Wrote config file')
    sys.exit(0)


@cli.command('tracking')
def cli_tracking():
    """ List tracked RSS feeds
    """
    global config, log
    if len(config['feeds']) == 0:
        click.echo('Zero feeds tracked', err=True)
        sys.exit(0)
    totalfeeds = len(config['feeds'])
    click.echo('Total RSS feeds tracked: ' + str(totalfeeds))
    for feed in config['feeds']:
        log.debug(feed)
        click.echo('-' * 16)
        click.echo(feed['name'])
        click.echo('-' * 16)
        click.echo('URL: ' + feed['url'])
        if 'enabled' in feed.keys():
            click.echo('ENABLED: ' + str(feed['enabled']))
        if 'rules' in feed.keys():
            click.echo('RULES: %i enabled' % len(feed['rules']))
        else:
            click.echo('RULES: disabled')
        click.echo('LAST FILE: ' + str(feed['last']))
    sys.exit(0)


@cli.command('run', short_help='Run blacksap on all tracked feeds')
@click.option('--reverse', '-R', is_flag=True, help='Read the feeds in reverse order (oldest to newest)')
@click.option('--count', '-c', default=-1, type=int, help='Number of torrent files to download')
@click.option('--output', '-o', type=click.Path(exists=True, file_okay=False, writable=True), required=True,
              help='Output directory for torrent files')
@click.argument('url', nargs=-1)
def cli_run(**kwargs):
    """ Update all RSS feeds and download new torrent files to output directory

    If count == -1 then all new torrent files will be downloaded.  If it is set to a non-zero
    number then exactly that many torrent files will be downloaded from each feed tracked regardless
    whether they are new in the feed or not.

    If url is specified, only the url of the feed specified will be updated. This url must already be
    tracked by blacksap!
    """
    global cfg_file, config, log
    log.debug(kwargs)
    if len(config['feeds']) == 0:
        click.echo('Zero feeds tracked', err=True)
        sys.exit(0)

    if kwargs['output'].endswith('/') is False:
        kwargs['output'] += '/'

    if len(kwargs['url']) == 0:
        feeds = enabled_feeds(config['feeds'])
    else:
        feeds = list()
        for url in kwargs['url']:
            for feed in config['feeds']:
                if url == feed['url']:
                    feeds.append(feed)
                    break
            else:
                click.echo('Feed not tracked: ' + url, err=True)
        if len(feeds) == 0:
            click.echo('Zero feeds to update')
            sys.exit(0)

    timer = BSTimer()
    timer.start()
    try:
        threads = int(config['app']['threads'])
    except (KeyError, ValueError):
        threads = min(cpu_count(), (len(feeds) // cpu_count()))
        config['app']['threads'] = threads
    bsfunc = partial(_blacksap, kwargs['output'], kwargs['reverse'], kwargs['count'])
    if threads > 1:
        log.info('Threads: ' + str(threads))
        bspool = ThreadPool(processes=threads)
        feeds_updated = bspool.map(bsfunc, feeds)
        bspool.close()
        bspool.join()
    else:
        feeds_updated = list(map(bsfunc, feeds))
    timer.stop()
    click.echo('%d feeds checked in %s seconds' % (len(feeds), timer.delta))
    if len(feeds_updated) == len(config['feeds']):
        config['feeds'] = feeds_updated
    else:
        for idx, feed in enumerate(config['feeds']):
            for update in feeds_updated:
                if update['url'] == feed['url']:
                    config['feeds'][idx] = update
                    break
    with open(cfg_file, 'w') as fp:
        json.dump(config, fp, indent=2)
    log.debug('Wrote config file')
    sys.exit(0)


if __name__ == '__main__':
    print('Please install blacksap using "pip install blacksap" or "make install"')
    sys.exit(1)
