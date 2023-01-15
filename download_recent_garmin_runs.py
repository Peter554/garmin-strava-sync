import re
import contextlib

from playwright.sync_api import sync_playwright


def download_recent_garmin_runs(
    garmin_connect_email, garmin_connect_password, out_folder
):
    with sync_playwright() as p:
        with contextlib.closing(p.chromium.launch(headless=False)) as browser:
            page = browser.new_page()
            login(page, garmin_connect_email, garmin_connect_password)
            activity_ids = get_recent_activity_ids(page)
            for activity_id in activity_ids:
                download_activity_tcx(page, activity_id, out_folder)


def login(page, garmin_connect_email, garmin_connect_password):
    page.goto("https://connect.garmin.com/signin")
    login_iframe = page.frame_locator("#gauth-widget-frame-gauth-widget")
    login_iframe.get_by_label("Email").fill(garmin_connect_email)
    login_iframe.get_by_label("Password").fill(garmin_connect_password)
    login_iframe.get_by_role("button", name="Sign In").click()
    page.get_by_role("link", name="Profile & Account").wait_for()


def get_recent_activity_ids(page):
    page.goto("https://connect.garmin.com/modern/activities?activityType=running")
    page.wait_for_load_state("networkidle")
    activity_links = [
        link
        for link in page.get_by_role("link").element_handles()
        if is_activity_link(link)
    ]
    activity_ids = [get_activity_id(activity_link) for activity_link in activity_links]
    return activity_ids


def is_activity_link(link):
    href = link.get_attribute("href")
    return href is not None and re.match(r"^/modern/activity/\d+$", href)


def get_activity_id(activity_link):
    return activity_link.get_attribute("href")[17:]


def download_activity_tcx(page, activity_id, out_folder):
    page.goto(f"https://connect.garmin.com/modern/activity/{activity_id}")
    page.get_by_role("button", name="More...").click()
    with page.expect_download() as download_info:
        page.get_by_text("Export to TCX").click()
    download = download_info.value
    download.save_as(f"{out_folder}/{activity_id}.tcx")
