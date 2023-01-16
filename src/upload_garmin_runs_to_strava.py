import os
import logging

from playwright.sync_api import TimeoutError


def upload_garmin_runs_to_strava(
    page, strava_email, strava_password, garmin_activities_dir
):
    logging.info(f"uploading garmin runs from {garmin_activities_dir} to strava")
    login(page, strava_email, strava_password)
    activity_ids = sorted(
        [f[:-4] for f in os.listdir(garmin_activities_dir) if f.endswith(".tcx")],
        key=lambda f: int(f),
    )
    logging.info(f"found {len(activity_ids)} activities: {activity_ids}")
    for activity_id in activity_ids:
        upload_activity_file_to_strava(page, garmin_activities_dir, activity_id)


def login(page, strava_email, strava_password):
    logging.info("logging in to strava")
    page.goto("https://www.strava.com/login")
    page.get_by_placeholder("Your Email").fill(strava_email)
    page.get_by_placeholder("Password").fill(strava_password)
    page.get_by_role("button", name="Log In").click()
    page.locator(".logged-in").wait_for()
    logging.info("logged in to strava")


def upload_activity_file_to_strava(page, garmin_activities_dir, activity_id):
    logging.info(f"uploading activity to strava: {activity_id}")
    page.goto("https://www.strava.com/upload/select")
    page.locator(".files").set_input_files(f"{garmin_activities_dir}/{activity_id}.tcx")
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
