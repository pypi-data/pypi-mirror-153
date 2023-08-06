"""The SubsPlease RSS module."""
import re

import feedparser


class SubsPleaseRSS:
    """SubsPleaseRSS class."""

    def __init__(
        self, quality: str = "1080", url: str = "https://subsplease.org/rss/"
    ) -> None:
        """Init SubsPleaseRSS class.

        Args:
            quality: Quality of videos on RSS feed.
            url: URL to SubsPlease RSS channel.

        """
        self.quality = self.choose_quality(quality)
        self.rss_url = f"{url}?t&r={self.quality}"

    @staticmethod
    def choose_quality(quality: str) -> str:
        """Choose video quality.

        Args:
            quality: Quality of videos on RSS feed.

        Returns:
            A string containing video resolution.

        Raises:
            ValueError: Provided quality string is not valid.

        """
        available_quality = ["sd", "720", "1080"]
        if str(quality) in available_quality:
            return quality
        else:
            raise ValueError(f"Quality {str(quality)} is not available.")

    def get_entries(self) -> list:
        """Get RSS entries.

        Returns:
            A list of all entry titles.

        """
        feed = feedparser.parse(self.rss_url)
        return [entry.title for entry in feed.entries]

    @staticmethod
    def extract_title_and_episode(entry: str) -> list:
        """Extract anime title and episode from RSS entry title.

        Args:
            entry: RSS entry title from `get_entries` method.

        Returns:
            A list containing anime title and episode.

        """
        removed_suffix = entry.rsplit(" ", 2)[0]
        removed_prefix = removed_suffix.split(" ", 1)[1]
        title_dirty = removed_prefix.rsplit(" ", 1)[0]
        title = re.sub(" -$", "", title_dirty)
        episode_dirty = removed_suffix.split(" ")[-1]
        episode = episode_dirty.replace("(", "").replace(")", "")
        return [title, episode]

    def check_for_new_episode(self, title: str, watched_episode: str) -> bool:
        """Choose video quality.

        Args:
            title: Anime title.
            watched_episode: Last seen episode.

        Returns:
            True if there is a new episode.
            False if there is a new episode.

        Raises:
            ValueError: Provided anime title string is not valid.

        """
        entries = self.get_entries()
        for entry in entries:
            if title in entry:
                current_episode = self.extract_title_and_episode(entry)[1]
                if watched_episode != current_episode:
                    return True
                return False
        raise ValueError(f"Anime {title} is not in current schedule.")
