import os

from playwright.sync_api import TimeoutError


def upload_garmin_runs_to_strava(page, strava_email, strava_password, garmin_runs_dir):
    login(page, strava_email, strava_password)
    for tcx_file_path in os.listdir(garmin_runs_dir):
        upload_tcx_to_strava(page, f"{garmin_runs_dir}/{tcx_file_path}")


def login(page, strava_email, strava_password):
    page.goto("https://www.strava.com/login")
    page.get_by_placeholder("Your Email").fill(strava_email)
    page.get_by_placeholder("Password").fill(strava_password)
    page.get_by_role("button", name="Log In").click()


def upload_tcx_to_strava(page, tcx_file_path):
    page.goto("https://www.strava.com/upload/select")
    page.locator(".files").set_input_files(tcx_file_path)
    while True:
        try:
            page.get_by_text("duplicate of activity").wait_for(timeout=1000)
            return
        except TimeoutError:
            ...

        try:
            save_button = page.get_by_role("button", name="Save & View").element_handle(
                timeout=1000
            )
        except TimeoutError:
            ...
        else:
            if save_button.is_disabled():
                page.wait_for_timeout(1000)
            else:
                return  # No need to click save_button, activity is already saved.
