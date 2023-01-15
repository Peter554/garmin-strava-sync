import os


import dotenv

from download_recent_garmin_runs import download_recent_garmin_runs


def main():
    dotenv.load_dotenv()
    download_recent_garmin_runs(
        os.getenv("GARMIN_CONNECT_EMAIL"),
        os.getenv("GARMIN_CONNECT_PASSWORD"),
        "garmin_runs",  # TODO
    )


if __name__ == "__main__":
    main()
