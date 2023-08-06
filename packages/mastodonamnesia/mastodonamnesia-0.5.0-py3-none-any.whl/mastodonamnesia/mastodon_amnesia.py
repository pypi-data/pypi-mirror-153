"""
    MastodonAmnesia - deletes old Mastodon toots
    Copyright (C) 2021  Mark S Burgunder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import time
from math import ceil
from typing import Any
from typing import cast
from typing import Dict

import arrow
from alive_progress import alive_bar
from mastodon import MastodonRatelimitError
from rich import print as rprint
from rich import traceback

from . import __version__
from .control import Configuration

traceback.install(show_locals=True)


def main() -> None:
    """Main logic to run MastodonAmnesia."""

    parser = argparse.ArgumentParser(description="Delete old toots.")
    parser.add_argument(
        "-c", "--config-file", action="store", default="config.json", dest="config_file"
    )
    args = parser.parse_args()

    config = Configuration(config_file_name=args.config_file)

    logger = config.bot.logger
    mastodon = config.mastodon_config.mastodon

    now = arrow.now()
    oldest_to_keep = now.shift(seconds=-config.bot.delete_after)

    rprint(f"Welcome to MastodonAmnesia {__version__}")
    rprint(
        f"We are removing toots older than {oldest_to_keep} "
        f"from {config.mastodon_config.base_url}@"
        f"{config.mastodon_config.user_info.user_name}"
    )

    mastodon = config.mastodon_config.mastodon
    toots = mastodon.account_statuses(
        id=config.mastodon_config.user_info.account_id, limit=10
    )
    max_toot_id = toots[-1].get("id") if len(toots) > 0 else None

    # Delete toots
    toots_deleted = 0
    with alive_bar(
        title="Processing toots ..................",
        enrich_print=False,
    ) as progress_bar:
        while True:
            if len(toots) == 0:
                break

            for toot in toots:
                logger.debug(
                    "Processing toot: %s from %s",
                    toot.get("url"),
                    toot.get("created_at"),
                )

                try:
                    toot_created_at = arrow.get(cast(int, toot.get("created_at")))
                    logger.debug(
                        "Oldest to keep vs toot created at %s > %s (%s)",
                        oldest_to_keep,
                        toot_created_at,
                        bool(oldest_to_keep > toot_created_at),
                    )

                    if toot_created_at < oldest_to_keep:
                        if should_keep(toot, config):
                            rprint(
                                f"Not deleting toot: "
                                f"Bookmarked: {toot.get('bookmarked')} - "
                                f"My Fav: {toot.get('favourited')} - "
                                f"Pinned: {toot.get('pinned')} - "
                                f"Poll: {(toot.get('poll') is not None)} - "
                                f"Attachements: {len(toot.get('media_attachments'))} - "
                                f"Faved: {toot.get('favourites_count')} - "
                                f"Boosted: {toot.get('reblogs_count')} - "
                                f"DM: {toot.get('visibility') == 'direct'} -+- "
                                f"{toot.get('url')}"
                            )
                            continue

                        mastodon.status_delete(toot.get("id"))
                        rprint(f"Deleted toot {toot.get('url')} from {toot_created_at}")
                        toots_deleted += 1
                    else:
                        logger.debug(
                            "Skipping toot: %s from %s",
                            toot.get("url"),
                            toot.get("created_at"),
                        )

                except MastodonRatelimitError:
                    need_to_wait = ceil(
                        mastodon.ratelimit_reset - mastodon.ratelimit_lastcall
                    )
                    rprint(f"Deleted a total of {toots_deleted} toots")
                    rprint(
                        f"Need to wait {need_to_wait} seconds "
                        f"(until {arrow.get(mastodon.ratelimit_reset)}) "
                        f'to let server "cool down"',
                    )
                    time.sleep(need_to_wait)

                progress_bar()  # pylint: disable=not-callable

            # Get More toots
            toots = mastodon.account_statuses(
                id=config.mastodon_config.user_info.account_id,
                limit=10,
                max_id=max_toot_id,
            )
            max_toot_id = toots[-1].get("id") if len(toots) > 0 else None

    rprint(f"All old toots deleted! Total of {toots_deleted} toots deleted")


def should_keep(toot: Dict[str, Any], config: Configuration) -> bool:
    """Function to determine if toot should be kept even though it might be a
    candidate for deletion."""
    keeping = False
    if config.bot.skip_deleting_bookmarked:
        keeping = bool(toot.get("bookmarked"))

    if not keeping and config.bot.skip_deleting_faved:
        keeping = bool(toot.get("favourited"))

    if not keeping and config.bot.skip_deleting_pinned:
        keeping = bool(toot.get("pinned"))

    if not keeping and config.bot.skip_deleting_poll:
        keeping = bool(toot.get("poll"))

    if not keeping and config.bot.skip_deleting_dm:
        keeping = toot.get("visibility") == "direct"

    if not keeping and config.bot.skip_deleting_media:
        medias = toot.get("media_attachments")
        if isinstance(medias, list):
            keeping = bool(len(medias))

    if not keeping and config.bot.skip_deleting_faved_at_least:
        keeping = bool(
            toot.get("favourites_count", 0) >= config.bot.skip_deleting_faved_at_least
        )

    if not keeping and config.bot.skip_deleting_boost_at_least:
        keeping = bool(
            toot.get("reblogs_count", 0) >= config.bot.skip_deleting_boost_at_least
        )

    return keeping


# run main programs
if __name__ == "__main__":
    main()
