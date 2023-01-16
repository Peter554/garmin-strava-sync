import os
import logging

from playwright.sync_api import TimeoutError


def upload_garmin_runs_to_strava(page, strava_email, strava_password, garmin_runs_dir):
    logging.info(f"uploading garmin runs from {garmin_runs_dir} to strava")
    login(page, strava_email, strava_password)
    tcx_files = [f for f in os.listdir(garmin_runs_dir) if f.endswith(".tcx")]
    logging.info(f"found {len(tcx_files)} TCX files: {tcx_files}")
    for tcx_file in tcx_files:
        upload_tcx_to_strava(page, f"{garmin_runs_dir}/{tcx_file}")


def login(page, strava_email, strava_password):
    logging.info("logging in to strava")
    page.goto("https://www.strava.com/login")
    page.get_by_placeholder("Your Email").fill(strava_email)
    page.get_by_placeholder("Password").fill(strava_password)
    page.get_by_role("button", name="Log In").click()
    page.locator(".logged-in").wait_for()
    logging.info("logged in to strava")


def upload_tcx_to_strava(page, tcx_file_path):
    logging.info(f"uploading TCX file to strava: {tcx_file_path}")
    page.goto("https://www.strava.com/upload/select")
    page.locator(".files").set_input_files(tcx_file_path)
    while True:
        try:
            page.get_by_text("duplicate of activity").wait_for(timeout=100)
            logging.info("activity already exists, skipping (duplicate)")
            return
        except TimeoutError:
            ...

        try:
            save_button = page.get_by_role("button", name="Save & View").element_handle(
                timeout=100
            )
        except TimeoutError:
            ...
        else:
            if save_button.is_disabled() or "disabled" in save_button.evaluate(
                "node => node.className"
            ):
                # upload still in progress
                logging.info("waiting...")
                page.wait_for_timeout(3000)
            else:
                # No need to click save_button, activity is already saved.
                logging.info("upload complete")
                return
