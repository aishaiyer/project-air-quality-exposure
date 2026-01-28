# Meteorology Plan (NOAA ISD)

## Stations (DMV backbone)
- DCA (Reagan National)
- BWI (Baltimore/Washington)
- IAD (Dulles)

## Variables
Daily features derived from station observations:
- air temperature
- dew point temperature
- wind speed
- sea-level pressure (optional)
- precipitation (optional)

## Merge Strategy (v1)
Assign each PM2.5 observation to a NOAA station by county-level mapping:
- DC counties → DCA
- Baltimore-area counties → BWI
- Western/VA-influenced counties → IAD

This will be refined in a later version using nearest-station matching (lat/lon).

## NOAA ISD Station Identifiers

The following USAF–WBAN station pairs are used:

- DCA (Washington Reagan National): 724050–13743
- BWI (Baltimore/Washington Intl): 724060–93721
- IAD (Washington Dulles Intl): 724030–93738

Data source: NOAA ISD-Lite daily summaries.
