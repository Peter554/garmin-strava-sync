import contextlib
import tempfile
import logging
import os

import dotenv
from playwright.sync_api import sync_playwright


import config
import garmin
import strava


def login(
    browser,
    garmin_connect_email,
    garmin_connect_password,
    strava_email,
    strava_password,
):
    if os.path.exists("context.json"):
        # assumption: context is not stale
        logging.info("using existing auth context")
    else:
        logging.info("creating new auth context")
        context = browser.new_context()
        page = context.new_page()
        garmin.login(page, garmin_connect_email, garmin_connect_password)
        strava.login(page, strava_email, strava_password)
        context.storage_state(path="context.json")
    return browser.new_context(storage_state="context.json")


def main():
    dotenv.load_dotenv()  # support .env file for running locally.
    cfg = config.Config()

    logging.basicConfig(level=logging.INFO)

    with sync_playwright() as p:
        with contextlib.closing(p.chromium.launch(headless=False)) as browser:
            context = login(
                browser,
                cfg.garmin_connect_email,
                cfg.garmin_connect_password,
                cfg.strava_email,
                cfg.strava_password,
            )
            page = context.new_page()
            with tempfile.TemporaryDirectory() as sync_dir:
                garmin.download_recent_activity_fit_files(
                    page,
                    sync_dir,
                    cfg.n_activities,
                )
                strava.upload_fit_files_to_strava(
                    page,
                    sync_dir,
                )


if __name__ == "__main__":
    main()
