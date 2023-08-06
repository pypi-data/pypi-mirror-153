"""
    Tests the gab driver.
"""

import re
import ssl
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

import feedparser  # type: ignore

# Fix the SSL error for rss sites that don't have a valid certificate.
ssl._create_default_https_context = (  # pylint: disable=protected-access
    ssl._create_unverified_context  # pylint: disable=protected-access
)


_IMG_URL_PATTERN = r"https?://[^\s]+\.(?:png|jpg|jpeg|gif)"
_DEFAULT_LIMIT = 100


@dataclass
class RssEntry:
    """Simple object of parsed RSS entries."""

    title: str
    link: str
    author: str
    published: datetime
    img: Optional[str] = None


def _find_all_img_urls(text: str) -> List[str]:
    """
    Returns all image urls in a string.
    """
    # Use a regular expression to find all image urls
    img_urls = re.findall(_IMG_URL_PATTERN, text)
    return img_urls


def _feed_entry_to_content(entry: feedparser.FeedParserDict) -> RssEntry:
    """
    Converts a feedparser entry to a content string.
    """
    title = entry.title
    link = entry.link
    description = entry.description
    author = getattr(entry, "author", "")
    # Turn the entry.published into a datetime object
    published: time.struct_time = entry.published_parsed
    post_date = datetime.fromtimestamp(time.mktime(published))
    imgs = _find_all_img_urls(description)
    img = imgs[0] if imgs else None
    return RssEntry(
        title=title,
        link=link,
        author=author,
        published=post_date,
        img=img,
    )


def parse_rss_feed(
    feed_url: str,
    limit: Optional[int] = None,
    published_after: Optional[datetime] = None,
) -> List[RssEntry]:
    """
    Generates gab posts from a feed.
    """
    limit = limit or _DEFAULT_LIMIT
    feed = feedparser.parse(feed_url)
    out: List[RssEntry] = []
    for entry in feed.entries:
        print(f"  Parsing entry: {entry.title}")
        if len(out) >= limit:
            print(f"  Reached limit of {limit} posts")
            break
        rss_entry = _feed_entry_to_content(entry)
        if published_after is None:
            out.append(rss_entry)
            continue
        if rss_entry.published > published_after:
            out.append(rss_entry)
            continue
        print(f"  Skipping {entry.title} because it was too old.")
    return out


def unit_test() -> None:
    """Unit test to use for development."""
    days_ago = datetime.now() - timedelta(days=5)
    posts = parse_rss_feed(
        "https://progunnews.com/index.rss", published_after=days_ago
    )
    for post in posts:
        print(post)


if __name__ == "__main__":
    unit_test()
