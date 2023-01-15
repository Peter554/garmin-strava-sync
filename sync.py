import os
import contextlib

import dotenv
from playwright.sync_api import sync_playwright

from download_recent_garmin_runs import download_recent_garmin_runs


def main():
    dotenv.load_dotenv()

    headless = os.getenv("HEADLESS", "").lower() in ("1", "true")
    sync_dir = os.getenv("SYNC_DIR")

    with sync_playwright() as p:
        with contextlib.closing(p.chromium.launch(headless=headless)) as browser:
            download_recent_garmin_runs(
                browser,
                os.getenv("GARMIN_CONNECT_EMAIL"),
                os.getenv("GARMIN_CONNECT_PASSWORD"),
                sync_dir,
            )

            # upload_garmin_runs_to_strava(
            #     browser,
            #     os.getenv("STRAVA_EMAIL"),
            #     os.getenv("STRAVA_PASSWORD"),
            #     sync_dir
            # )


if __name__ == "__main__":
    main()
