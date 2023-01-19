import os

import dataclasses


def from_env(key: str, f):
    return dataclasses.field(default_factory=lambda: f(os.environ[key]))


def str_from_env(key: str):
    return from_env(key, lambda x: x)


@dataclasses.dataclass(frozen=True)
class Config:
    garmin_connect_email: str = str_from_env("GARMIN_CONNECT_EMAIL")
    garmin_connect_password: str = str_from_env("GARMIN_CONNECT_PASSWORD")
    strava_email: str = str_from_env("STRAVA_EMAIL")
    strava_password: str = str_from_env("STRAVA_PASSWORD")
    n_activities: int = from_env("GARMIN_STRAVA_SYNC_N_ACTIVITIES", int)
