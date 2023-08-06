# Playlist2Podcast

Playlist2Podcast is a command line tool that takes a Youtube playlist and creates a podcast feed from this.

Playlist2Podcast is not mature yet and might fail with uncaught errors. If you encounter an error, please create an
[issue](https://codeberg.org/PyYtTools/Playlist2Podcasts/issues)

Currently, Playlist2Podcast:
1) downloads and converts the videos in one or more playlists to opus audio only files,
2) downloads thumbnails and converts them to JPEG format, and
3) creates a podcast feed with the downloaded videos and thumbnails.

Before running, install [Python Poetry](https://python-poetry.org/) and run `poetry install`.

Playlist2Podcast will ask for all necessary parameters when run for the first time and store them in `config.json`
file in the current directory.

Run Playlist2Podcast with the command `poetry run playlist2podcast`

Playlist2Podcast is licences under licensed under
the [GNU Affero General Public License v3.0](http://www.gnu.org/licenses/agpl-3.0.html)
