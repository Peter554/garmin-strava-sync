import os
import contextlib
import tempfile
import logging

import dotenv
from playwright.sync_api import sync_playwright

from login import login
from download_recent_garmin_runs import download_recent_garmin_runs
from upload_garmin_runs_to_strava import upload_garmin_runs_to_strava


def main():
    dotenv.load_dotenv()  # support .env file for running locally.
    logging.basicConfig(level=logging.INFO)

    with sync_playwright() as p:
        with contextlib.closing(p.chromium.launch(headless=False)) as browser:
            context = login(
                browser,
                os.getenv("GARMIN_CONNECT_EMAIL"),
                os.getenv("GARMIN_CONNECT_PASSWORD"),
                os.getenv("STRAVA_EMAIL"),
                os.getenv("STRAVA_PASSWORD"),
            )
            page = context.new_page()
            with tempfile.TemporaryDirectory() as sync_dir:
                download_recent_garmin_runs(
                    page,
                    sync_dir,
                    int(os.getenv("GARMIN_STRAVA_SYNC_MAX_ACTIVITIES")),
                )
                upload_garmin_runs_to_strava(
                    page,
                    sync_dir,
                )


if __name__ == "__main__":
    main()
