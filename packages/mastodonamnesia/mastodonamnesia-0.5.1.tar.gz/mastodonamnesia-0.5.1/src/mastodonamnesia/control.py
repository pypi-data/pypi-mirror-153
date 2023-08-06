# pylint: disable=E1136
"""This module contains helper classes and methods to assist with the general
function of this bot.

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
import json
import logging
import os
import sys
from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import TypeVar

from mastodon import Mastodon
from mastodon import MastodonError
from rich.logging import RichHandler

BC = TypeVar("BC", bound="BotConfig")
CFG = TypeVar("CFG", bound="Configuration")
MC = TypeVar("MC", bound="MastodonConfig")
MU = TypeVar("MU", bound="MastodonUser")


@dataclass
class BotConfig:
    """Dataclass holding configuration values for general behaviour of
    MastodonAmnesia."""

    # pylint: disable=too-many-instance-attributes
    log_level: str
    logger: logging.Logger
    delete_after: int
    skip_deleting_pinned: Optional[bool]
    skip_deleting_faved: Optional[bool]
    skip_deleting_bookmarked: Optional[bool]
    skip_deleting_poll: Optional[bool]
    skip_deleting_dm: Optional[bool]
    skip_deleting_media: Optional[bool]
    skip_deleting_faved_at_least: Optional[int]
    skip_deleting_boost_at_least: Optional[int]

    def __init__(  # noqa: max-complexity: 12
        self: BC, config: Optional[dict[str, Any]]
    ) -> None:
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        # It's not that bad ;)
        if not config:
            config = {}

        self.log_level = config.get("log_level", "INFO")
        logging.basicConfig(
            level=self.log_level,
            format="%(name)s[%(process)d] %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            handlers=[RichHandler()],
        )
        self.logger = logging.getLogger("MastodonAmnesia")
        self.delete_after = config.get("delete_after", None)
        self.skip_deleting_bookmarked = config.get("skip_deleting_bookmarked")
        self.skip_deleting_faved = config.get("skip_deleting_faved")
        self.skip_deleting_pinned = config.get("skip_deleting_pinned")
        self.skip_deleting_poll = config.get("skip_deleting_poll")
        self.skip_deleting_dm = config.get("skip_deleting_dm")
        self.skip_deleting_media = config.get("skip_deleting_media")
        self.skip_deleting_faved_at_least = config.get("skip_deleting_faved_at_least")
        self.skip_deleting_boost_at_least = config.get("skip_deleting_boost_at_least")

        if not self.delete_after:
            self._get_delete_after()

        if self.skip_deleting_bookmarked is None:
            self._get_skip_bookmarked()

        if self.skip_deleting_faved is None:
            self._get_skip_faved()

        if self.skip_deleting_pinned is None:
            self._get_skip_pinned()

        if self.skip_deleting_poll is None:
            self._get_skip_poll()

        if self.skip_deleting_dm is None:
            self._get_skip_dm()

        if self.skip_deleting_media is None:
            self._get_skip_media()

        if self.skip_deleting_faved_at_least is None:
            self._get_skip_faved_at_least()

        if self.skip_deleting_boost_at_least is None:
            self._get_skip_boost_at_lease()

    def _get_skip_poll(self: BC) -> None:
        print("Should polls be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_poll = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_poll = True
        else:
            print("! ERROR ... please only respond with 'Y' or 'N'")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_dm(self: BC) -> None:
        print("Should Direct Messages be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_dm = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_dm = True
        else:
            print("! ERROR ... please only respond with 'Y' or 'N'")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_media(self: BC) -> None:
        print(
            "Should Toots with attachements / pictures be deleted "
            "when they get old enough?"
        )
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_media = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_media = True
        else:
            print("! ERROR ... please only respond with 'Y' or 'N'")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_faved_at_least(self: BC) -> None:
        print(
            "Should Toots being favourited a certain mimimum number of times be "
            "excluded from deletion even when they get old enough?"
        )
        print("(enter 0 to disregard this setting)")
        self.skip_deleting_faved_at_least = int(input("[..] Please enter number: "))

    def _get_skip_boost_at_lease(self: BC) -> None:
        print(
            "Should Toots being boosted a certain mimimum number of times be "
            "excluded from deletion even when they get old enough?"
        )
        print("(enter 0 to disregard this setting)")
        self.skip_deleting_boost_at_least = int(input("[..] Please enter number: "))

    def _get_skip_pinned(self: BC) -> None:
        """'Private' method to get skip deleting pinned toots value from user
        if this value has not yet been configured."""
        print("Should pinned toots be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_pinned = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_pinned = True
        else:
            print("! ERROR ... please only respond with 'Y' or 'N'")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_faved(self: BC) -> None:
        """'Private' method to get skip deleting faveroited toots value from
        user if this value has not yet been configured."""
        print("Should favoured toots be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_faved = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_faved = True
        else:
            print("! ERROR ... please only respond with 'Y' or 'N'")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_bookmarked(self: BC) -> None:
        """'Private' method to get skip deleting bookmarked toots from user if
        this value has not yet been configured."""
        print("Should bookmarked toots be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_bookmarked = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_bookmarked = True
        else:
            print("! ERROR ... please only respond with 'Y' or 'N'")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_delete_after(self: BC) -> None:
        """'Private' method to get delete after value from user if this value
        has not yet been configured."""
        print(
            "Please enter maximum age of retained toots in the "
            'format of "number unit"'
        )
        print('For example "1 weeks" or "3 days". Supported units are:')
        print(
            " - seconds\n"
            " - minutes\n"
            " - hours\n"
            " - days\n"
            " - weeks\n"
            " - months"
        )
        max_age = input("[..] Minimum age to delete toots (in seconds): ")
        max_age_parts = max_age.split(" ")
        max_age_number = int(max_age_parts[0])
        max_age_unit = max_age_parts[1]
        if max_age_unit == "seconds":
            self.delete_after = max_age_number
        elif max_age_unit == "minutes":
            self.delete_after = max_age_number * 3600
        elif max_age_unit == "hours":
            self.delete_after = max_age_number * 3600
        elif max_age_unit == "days":
            self.delete_after = max_age_number * 3600 * 24
        elif max_age_unit == "weeks":
            self.delete_after = max_age_number * 3600 * 24 * 7
        elif max_age_unit == "months":
            self.delete_after = max_age_number * 3600 * 24 * 30
        else:
            print("! Error ... unknown unit ({max_age_unit}) specified")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)


@dataclass
class MastodonUser:
    """Dataclass holding information about the mastodon user we use to
    login."""

    email: str
    user_name: str
    access_token: str
    account_id: int

    def __init__(self: MU, user_info: Optional[dict[str, Any]]) -> None:
        if not user_info:
            user_info = {}

        self.email = user_info.get("email", None)
        self.user_name = user_info.get("user_name", None)
        self.access_token = user_info.get("access_token", None)

        if not self.email:
            self.email = input("[..] Enter email address for Mastodon account: ")


@dataclass
class MastodonConfig:
    """Dataclass holding configuration values for Mastodon settings."""

    base_url: str
    user_info: MastodonUser
    client_id: str
    client_access_token: str
    mastodon: Mastodon

    def __init__(self: MC, mastodon_ini: Optional[dict[str, Any]]) -> None:

        if not mastodon_ini:
            mastodon_ini = {}

        self.base_url = mastodon_ini.get("base_url", None)
        self.client_id = mastodon_ini.get("client_id", None)
        self.client_access_token = mastodon_ini.get("client_access_token", None)

        if not self.base_url:
            self.base_url = input("[..] Enter base URL for Mastodon account: ")

        self.user_info = MastodonUser(mastodon_ini.get("user_info", None))

        try:
            if not self.user_info.access_token:
                if not (self.client_id and self.client_access_token):
                    client_details = Mastodon.create_app(
                        "MastodonAmnesia",
                        website="https://gitlab.com/mastopytools/mastodonamnesia",
                        api_base_url=self.base_url,
                    )
                    self.client_id = client_details[0]
                    self.client_access_token = client_details[1]
                self.mastodon = Mastodon(
                    client_id=self.client_id,
                    client_secret=self.client_access_token,
                    api_base_url=self.base_url,
                    ratelimit_method="throw",
                )

                password = input("[..] Enter password for Mastodon account: ")

                self.user_info.access_token = self.mastodon.log_in(
                    username=self.user_info.email, password=password
                )
                userinfo = self.mastodon.account_verify_credentials()

            else:
                self.mastodon = Mastodon(
                    access_token=self.user_info.access_token,
                    api_base_url=self.base_url,
                    ratelimit_method="throw",
                )
                userinfo = self.mastodon.account_verify_credentials()

            self.user_info.user_name = userinfo.get("username")
            self.user_info.account_id = userinfo.get("id")
        except MastodonError as mastodon_error:
            print(f"! Error when setting up Mastodon connection: {mastodon_error}")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)


@dataclass
class Configuration:
    """Dataclass to hold all settings for tootbot."""

    bot: BotConfig
    mastodon_config: MastodonConfig

    def __init__(self: CFG, config_file_name: str = "config.json") -> None:
        config: dict[str, Any] = {"Bot": None, "Mastodon": None}

        if os.path.exists(config_file_name):
            with open(file=config_file_name, encoding="UTF-8") as config_file:
                config = json.load(config_file)

        self.mastodon_config = MastodonConfig(config.get("Mastodon"))
        self.bot = BotConfig(config.get("Bot"))
        self.bot.logger.debug("After instantiation of config classes: %s", self)

        config = {
            "Bot": asdict(self.bot),
            "Mastodon": asdict(self.mastodon_config),
        }
        del config["Mastodon"]["mastodon"]
        del config["Bot"]["logger"]
        with open(file=config_file_name, mode="w", encoding="UTF-8") as config_file:
            json.dump(config, config_file, indent=4)
            self.bot.logger.debug("Saved config: %s", config)
