import logging
import os


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
        login_to_garmin(page, garmin_connect_email, garmin_connect_password)
        login_to_strava(page, strava_email, strava_password)
        context.storage_state(path="context.json")
    return browser.new_context(storage_state="context.json")


def login_to_garmin(page, garmin_connect_email, garmin_connect_password):
    logging.info("logging in to garmin")
    page.goto("https://connect.garmin.com/signin")
    login_iframe = page.frame_locator("#gauth-widget-frame-gauth-widget")
    login_iframe.get_by_label("Email").fill(garmin_connect_email)
    login_iframe.get_by_label("Password").fill(garmin_connect_password)
    login_iframe.get_by_role("button", name="Sign In").click()
    page.locator(".signed-in").wait_for()
    logging.info("logged in to garmin")


def login_to_strava(page, strava_email, strava_password):
    logging.info("logging in to strava")
    page.goto("https://www.strava.com/login")
    page.get_by_placeholder("Your Email").fill(strava_email)
    page.get_by_placeholder("Password").fill(strava_password)
    page.get_by_role("button", name="Log In").click()
    page.locator(".logged-in").wait_for()
    logging.info("logged in to strava")
