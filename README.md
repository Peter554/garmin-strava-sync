# garmin strava sync

A small automation to sync my activities from Garmin Connect to Strava.

* Using https://playwright.dev/python/ for browser automation.
* Deployed as a GitHub action, manually triggerable using the workflow_dispatch trigger.

New Garmin activities will be posted to Strava. 
Updates and deletes on Garmin are not synced to Strava, since this is complex and offers me little benefit (updates/deletes are rare).

Triggering the sync using the GitHub API:

```
curl \
  -X POST \
  -u peter554:$TOKEN \
  https://api.github.com/repos/peter554/garmin-strava-sync/actions/workflows/sync.yml/dispatches \
  -d '{"ref": "master", "inputs": {"n_activities": "5"}}'
```