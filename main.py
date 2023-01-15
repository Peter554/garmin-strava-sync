import time
import re

from playwright.sync_api import sync_playwright

GARMIN_CONNECT_EMAIL = "byfield554@gmail.com"
GARMIN_CONNECT_PASSWORD = ""

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://connect.garmin.com/signin")
        login_iframe = page.frame_locator("#gauth-widget-frame-gauth-widget")
        login_iframe.get_by_label("Email").fill(GARMIN_CONNECT_EMAIL)
        login_iframe.get_by_label("Password").fill(GARMIN_CONNECT_PASSWORD)
        login_iframe.get_by_role("button", name="Sign In").click()
        
        page.wait_for_timeout(10000)        
        page.goto("https://connect.garmin.com/modern/activities?activityType=running")
        page.wait_for_timeout(5000)
        links = page.get_by_role("link").element_handles()

        links = [link for link in links if link.get_attribute("href") and re.match(r"^/modern/activity/\d+$", link.get_attribute("href"))]
        links[0].hover()
        for _ in range(10):
            page.mouse.wheel(0, 5000)
            page.wait_for_timeout(3000)

        links = page.get_by_role("link").element_handles()

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

        browser.close()

if __name__ == "__main__":
    main()