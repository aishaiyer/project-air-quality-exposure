## EPA AQS Daily PM2.5 Files Used
- daily_88101_2018.csv
- daily_88101_2019.csv
- daily_88101_2022.csv
- daily_88101_2023.csv 
- daily_88101_2024.csv

Notes:
- Parameter code 88101 corresponds to PM2.5 local conditions (FRM/FEM).
- COVID-19 period years (2020–2021) were intentionally excluded.
- Spatial filtering to DC and Maryland will be applied during preprocessing.

## NOAA ISD-Lite Files Used (Meteorology)
Stations:
- DCA: 724050-13743
- BWI: 724060-93721
- IAD: 724030-93738

Years: 2018, 2019, 2022, 2023, 2024

Source: https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/

## Data Attribution and Use

All datasets used in this project are publicly available and provided by U.S.
government agencies.

### EPA Air Quality System (AQS)
U.S. Environmental Protection Agency (EPA).
Air Quality System (AQS) Data Mart.
https://www.epa.gov/aqs

Daily PM2.5 FRM/FEM (parameter code 88101) data were used for the years
2018–2019 and 2022–2024. Years 2020–2021 were excluded to avoid COVID-era
emission anomalies.

### NOAA Integrated Surface Database (ISD-Lite)
National Oceanic and Atmospheric Administration (NOAA),
National Centers for Environmental Information (NCEI).
Integrated Surface Database (ISD-Lite).
https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database

Daily meteorological summaries were used from ISD-Lite for the following stations:
- Washington Reagan National (DCA): 724050–13743
- Baltimore/Washington International (BWI): 724060–93721
- Washington Dulles International (IAD): 724030–93738
