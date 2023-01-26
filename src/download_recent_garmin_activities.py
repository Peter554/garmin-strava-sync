import re
import logging
import zipfile
import os


def download_recent_garmin_activities(page, out_dir, n_activities):
    logging.info(f"downloading recent garmin activities to {out_dir} ({n_activities})")
    activity_ids = get_recent_activity_ids(page, n_activities)
    for activity_id in activity_ids:
        download_activity_fit_file(page, activity_id, out_dir)


# note: case where n_activities exceeds the paging (20?) is not handled.
def get_recent_activity_ids(page, n_activities):
    logging.info("fetching recent activity IDs")
    page.goto("https://connect.garmin.com/modern/activities")

    # assumption: the user has at least 1 activity
    while not (activity_links := get_activity_links(page)):
        page.wait_for_timeout(500)

    activity_ids = [get_activity_id(activity_link) for activity_link in activity_links]
    activity_ids = activity_ids[:n_activities]
    logging.info(f"fetched {len(activity_ids)} recent activity IDs: {activity_ids}")
    return activity_ids


def get_activity_links(page):
    return [link for link in page.get_by_role("link").all() if is_activity_link(link)]


def is_activity_link(link):
    href = link.get_attribute("href")
    return href is not None and re.match(r"^/modern/activity/\d+$", href)


def get_activity_id(activity_link):
    return activity_link.get_attribute("href")[17:]


def download_activity_fit_file(page, activity_id, out_dir):
    logging.info(f"downloading activity FIT file: {activity_id}")
    page.goto(f"https://connect.garmin.com/modern/activity/{activity_id}")
    page.get_by_role("button", name="More...").click()
    with page.expect_download() as download_info:
        page.get_by_text("Export Original").click()
    download = download_info.value
    with zipfile.ZipFile(download.path(), "r") as zip_:
        zip_.extract(f"{activity_id}_ACTIVITY.fit", path=out_dir)
        os.rename(
            f"{out_dir}/{activity_id}_ACTIVITY.fit", f"{out_dir}/{activity_id}.fit"
        )
    logging.info("download complete")
