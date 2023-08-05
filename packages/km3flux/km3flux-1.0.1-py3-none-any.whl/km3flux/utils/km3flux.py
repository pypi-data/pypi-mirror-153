#!/usr/bin/env python3
"""
Updates the files in the data folder by scraping the publications.
Existing data files are not re-downloaded.

Usage:
    km3flux [-spx] update
    km3flux show
    km3flux (-h | --help)
    km3flux --version

Options:
    -x    Overwrite existing files when updating.
    -s    Include seasonal flux data from Honda.
    -p    Include production height tables from Honda.
    -h    Show this screen.
    -v    Show the version.

Currently only the Honda fluxes are download from
https://www.icrr.u-tokyo.ac.jp/~mhonda/
"""
import os
import re
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
    from docopt import docopt
    from tqdm import tqdm
except ModuleNotFoundError:
    print("Install the optional dependencies to be able to manage the archive:\n\n"
          "    pip install 'km3flux[all]'\n")
    exit(1)

import km3flux
from km3flux.data import basepath

URL = "https://www.icrr.u-tokyo.ac.jp/~mhonda/"

log = km3flux.logger.get_logger("km3flux")


def get_honda(include_seasonal=False, include_production_height=False, overwrite=False):
    """Grab all the Honda fluxes"""

    def archive_data(url, year, overwrite=False):
        """Archives a file from `url` under `year`.

        Currently, only Honda files are downloaded so there is no logic in place
        to manage multiple download target locations. Therefore "honda/" is
        hard-coded.
        """
        target_path = basepath / "honda" / year / os.path.basename(url)
        if not overwrite and os.path.exists(target_path):
            return
        os.makedirs(target_path.parent, exist_ok=True)
        r = requests.get(url)
        if not r.ok:
            log.error(
                "Unable to retrieve '%s', reason: '%s' (status code %d)",
                url,
                r.reason,
                r.status_code,
            )
        else:
            with open(target_path, "wb") as fobj:
                fobj.write(r.content)

    def get_all_data(url, year, overwrite=False, label=""):
        """Downloads all the datafiles from a given `url`"""
        p = requests.get(url)
        s = BeautifulSoup(p.content, "html.parser")
        hrefs = [a["href"] for a in s.find_all("a") if a["href"].endswith(".d.gz")]
        for href in tqdm(hrefs, label):
            data_url = urljoin(p.url, href)
            archive_data(data_url, year, overwrite)

    print("Updating Honda fluxes...")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    for e in soup.find_all("a"):
        # yearly datasets
        m = re.search(r"(nflx(\d{4})/index.html)", e.attrs["href"])
        if m:
            suburl, year = m.groups()
            print(f"-> year {year}")
            get_all_data(urljoin(page.url, suburl), year, overwrite, "flux tables")

            if include_seasonal:
                p = requests.get(urljoin(page.url, suburl))
                s = BeautifulSoup(p.content, "html.parser")
                links = s.find_all("a")
                for _e in links:
                    ms = re.search(r"index-\d{4}.html", _e.attrs["href"])
                    if ms:
                        suburl = urljoin(p.url, _e.attrs["href"])
                        get_all_data(suburl, year, overwrite, "seasonal fluxes")

            if include_production_height:
                p = requests.get(urljoin(page.url, suburl))
                s = BeautifulSoup(p.content, "html.parser")
                links = s.find_all("a")
                for _e in links:
                    ms = re.search(r"index-height.html", _e.attrs["href"])
                    if ms:
                        suburl = urljoin(p.url, _e.attrs["href"])
                        get_all_data(
                            suburl, year, overwrite, "production height tables"
                        )


def main():
    args = docopt(__doc__, version=km3flux.version)

    get_honda(
        include_seasonal=args["-x"],
        include_production_height=args["-p"],
        overwrite=args["-x"],
    )


if __name__ == "__main__":
    main()
