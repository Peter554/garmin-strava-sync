import os
import logging

from playwright.sync_api import TimeoutError


def login(page, strava_email, strava_password):
    logging.info("logging in to strava")
    page.goto("https://www.strava.com/login")
    page.get_by_placeholder("Your Email").fill(strava_email)
    page.get_by_placeholder("Password").fill(strava_password)
    page.get_by_role("button", name="Log In").click()
    page.locator(".logged-in").wait_for()
    logging.info("logged in to strava")


def upload_fit_files(page, fit_files_dir):
    logging.info(f"uploading FIT files from {fit_files_dir} to strava")
    fit_files = sorted(
        [f for f in os.listdir(fit_files_dir) if f.endswith(".fit")],
        key=lambda f: int(f[:-4]),
    )
    logging.info(f"found {len(fit_files)} FIT files: {fit_files}")
    for fit_file in fit_files:
        upload_fit_file(page, fit_files_dir, fit_file)


def upload_fit_file(page, fit_files_dir, fit_file):
    logging.info(f"uploading FIT file to strava: {fit_file}")
    page.goto("https://www.strava.com/upload/select")
    page.locator(".files").set_input_files(f"{fit_files_dir}/{fit_file}")
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
                save_button.click()
                page.wait_for_url("**/activities/*", wait_until="networkidle")
                logging.info("upload complete")
                return
