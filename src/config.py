import os

import dataclasses


@dataclasses.dataclass(frozen=True)
class Config:
    garmin_connect_email: str = os.environ["GARMIN_CONNECT_EMAIL"]
    garmin_connect_password: str = os.environ["GARMIN_CONNECT_PASSWORD"]
    strava_email: str = os.environ["STRAVA_EMAIL"]
    strava_password: str = os.environ["STRAVA_PASSWORD"]
    n_activities: int = int(os.environ["GARMIN_STRAVA_SYNC_N_ACTIVITIES"])
