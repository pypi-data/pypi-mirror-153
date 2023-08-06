# MastodonAmnesia

***!!! BEWARE, THIS TOOL WILL DELETE SOME OF YOUR MASTODON TOOTS !!!***

MastodonAmnesia is a command line (CLI) tool to help delete old toots from Mastodon. It respects rate limits imposed by
Mastodon servers.

Install MastodonAmnesia from Pypi using:
`pip install mastodon_amnesia`
and then run `mastodonamnesia`

Or alternatively you can run MastodonAmnesia from [source][4] by cloning the repository using the following command line:
`git clone https://codeberg.org/MarvinsMastodonTools/mastodonamnesia.git`

As MastodonAmnesia is now using [Poetry][1] for dependency control, please install Poetry before proceeding further.

Before running, make sure you have all required python modules installed. With [Poetry][1] this is as easy as:
`poetry install --no-dev`

MastodonAmnesia will ask for all necessary parameters when run for the first time and store them in `config.json`
file in the current directory.

Run MastodonAmnesia with the command `poetry run mastodonamnesia`


MastodonAmnesia is licences under licensed under
the [GNU Affero General Public License v3.0][2]

## Supporting MastodonAmnesia

There are a number of ways you can support MastodonAmnesia:

- Create an issue with problems or ideas you have with/for MastodonAmnesia
- You can [buy me a coffee][3].
- You can send me small change in Monero to the address below:

Monero donation address:
`86ZnRsiFqiDaP2aE3MPHCEhFGTeipdQGJZ1FNnjCb7s9Gax6ZNgKTyUPmb21WmT1tk8FgM7cQSD5K7kRtSAt1y7G3Vp98nT`

[1]: https://python-poetry.org/
[2]: http://www.gnu.org/licenses/agpl-3.0.html
[3]: https://www.buymeacoffee.com/marvin8
[4]: https://codeberg.org/MarvinsMastodonTools/mastodonamnesia
