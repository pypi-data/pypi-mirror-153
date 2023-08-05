### Overview

Selenium scraper for fetching information from the ProCyclingStats page.

### Setup

#### Setting up virtualenv

```
python3 -m pip install virtualenv
virtualenv .
source bin/activate
```

#### Installing requirements

```
pip install -r requirements.txt
sudo apt-get install xvfb
sudo apt-get install -y chromium-chromedriver
```

### Usage

```
import pcs_scraper

pcs_scraper.scrap_teams_by_year(2021)
pcs_scraper.scrap_stage('tour-de-france', 2020, 2)
pcs_scraper.scrap_stage_gc('tour-de-france', 2020, 2)
pcs_scraper.scrap_final_gc('tour-de-france', 2021)
pcs_scraper.scrap_final_points('tour-de-france', 2021)
pcs_scraper.scrap_final_kom('tour-de-france', 2021)
pcs_scraper.scrap_final_youth('tour-de-france', 2021)
pcs_scraper.scrap_final_teams('tour-de-france', 2021)
```

### Publishing to PyPy

https://packaging.python.org/en/latest/tutorials/packaging-projects/
