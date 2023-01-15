import re
import contextlib

from playwright.sync_api import sync_playwright



def download_recent_garmin_runs(garmin_connect_email, garmin_connect_password):
    with sync_playwright() as p:
        with contextlib.closing(p.chromium.launch(headless=False)) as browser:
            page = browser.new_page()

            page.goto("https://connect.garmin.com/signin")
            login_iframe = page.frame_locator("#gauth-widget-frame-gauth-widget")
            login_iframe.get_by_label("Email").fill(garmin_connect_email)
            login_iframe.get_by_label("Password").fill(garmin_connect_password)
            login_iframe.get_by_role("button", name="Sign In").click()

            page.wait_for_timeout(10000)
            page.goto("https://connect.garmin.com/modern/activities?activityType=running")
            page.wait_for_timeout(5000)
            links = page.get_by_role("link").element_handles()
            links = [link for link in links if link.get_attribute("href") and re.match(r"^/modern/activity/\d+$", link.get_attribute("href"))]

            link_hrefs = [link.get_attribute("href") for link in links]
            link_hrefs = [href for href in link_hrefs if href and re.match(r"^/modern/activity/\d+$", href)]
            run_ids = [href[17:] for href in link_hrefs]

            for run_id in run_ids:
                page.goto(f"https://connect.garmin.com/modern/activity/{run_id}")
                page.get_by_role("button", name="More...").click()
                with page.expect_download() as download_info:
                    page.get_by_text("Export to TCX").click()
                download = download_info.value
                download.save_as(f"garmin_runs/{run_id}.tcx")
                break

            browser.close()

