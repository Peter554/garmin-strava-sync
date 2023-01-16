# garmin strava sync

A small automation to sync my activities from Garmin Connect to Strava.

* Using https://playwright.dev/python/ for browser automation.
* Using a scheduled GitHub action to run the automation on a schedule.

New Garmin activities will be posted to Strava. 
Updates and deletes on Garmin are not synced to Strava, since this is complex and offers me little benefit. 
