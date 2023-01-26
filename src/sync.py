import contextlib
import tempfile
import logging

import dotenv
from playwright.sync_api import sync_playwright

from login import login
from config import Config
from download_recent_garmin_activities import download_recent_garmin_activities
from upload_garmin_activities_to_strava import upload_garmin_activities_to_strava


def main():
    dotenv.load_dotenv()  # support .env file for running locally.
    config = Config()

    logging.basicConfig(level=logging.INFO)

    with sync_playwright() as p:
        with contextlib.closing(p.chromium.launch(headless=False)) as browser:
            context = login(
                browser,
                config.garmin_connect_email,
                config.garmin_connect_password,
                config.strava_email,
                config.strava_password,
            )
            page = context.new_page()
            with tempfile.TemporaryDirectory() as sync_dir:
                download_recent_garmin_activities(
                    page,
                    sync_dir,
                    config.n_activities,
                )
                upload_garmin_activities_to_strava(
                    page,
                    sync_dir,
                )


if __name__ == "__main__":
    main()
