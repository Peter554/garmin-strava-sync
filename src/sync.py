import os
import contextlib

from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

from download_recent_garmin_runs import download_recent_garmin_runs
from upload_garmin_runs_to_strava import upload_garmin_runs_to_strava


def main():
    load_dotenv()
    sync_dir = "garmin_runs"
    with sync_playwright() as p:
        with contextlib.closing(p.chromium.launch(headless=False)) as browser:
            page = browser.new_page()

            download_recent_garmin_runs(
                page,
                os.getenv("GARMIN_CONNECT_EMAIL"),
                os.getenv("GARMIN_CONNECT_PASSWORD"),
                sync_dir,
            )

            upload_garmin_runs_to_strava(
                page,
                os.getenv("STRAVA_EMAIL"),
                os.getenv("STRAVA_PASSWORD"),
                sync_dir,
            )


if __name__ == "__main__":
    main()
