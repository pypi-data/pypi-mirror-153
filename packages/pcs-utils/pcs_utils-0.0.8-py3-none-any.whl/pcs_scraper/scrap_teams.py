from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from .base import init_driver
from selenium import webdriver

BASE_URL: str = "https://www.procyclingstats.com/teams.php?{args}"
TEAMS_BY_YEAR_URL: str = BASE_URL.format(args="year={year}")


def scrap_teams_by_year(year: int) -> list:
    driver: webdriver = init_driver()

    url = TEAMS_BY_YEAR_URL.format(year=year)
    driver.get(url)

    elements = driver.find_elements(By.XPATH, "//ul[contains(@class, 'list') and contains(@class, 'fs14') and "
                                              "contains(@class, 'columns2') and contains(@class, 'mob_columns1')]")

    # Get the teams from each category
    teams = list()
    for uci_category in elements:
        for team_element in uci_category.find_elements(By.XPATH, ".//li"):
            team = dict()
            link = team_element.find_element(By.XPATH, ".//a")
            team['link'] = link.get_attribute('href')
            team['name'] = link.text
            team['riders'] = list()
            teams.append(team)

    # Get the img and the riders from each team
    for team in teams:
        driver.get(team['link'])
        team_img_candidates = driver.find_elements(By.XPATH, "//ul[contains(@class, 'infolist')]")
        if len(team_img_candidates) == 1:
            team['img'] = team_img_candidates[0].find_element(By.XPATH, ".//img").get_attribute('src')
        else:
            for infolist_element in team_img_candidates:
                if 'Shirt:' in infolist_element.text:
                    team['img'] = infolist_element.find_element(By.XPATH, ".//img").get_attribute('src')

        riders = driver.find_element(By.XPATH, "//ul[contains(@class, 'list') and contains(@class, 'pad2')]") \
            .find_elements(By.XPATH, ".//li")
        for rider_element in riders:
            rider = dict()
            rider_link = rider_element.find_element(By.XPATH, ".//a")
            rider['link'] = rider_link.get_attribute('href')
            rider['preferred_name'] = rider_link.get_attribute('innerHTML')
            team['riders'].append(rider)

    # Get the information of each rider
    for team in teams:
        for rider in team['riders']:
            driver.get(rider['link'])
            try:
                rider['img'] = driver.find_element(By.XPATH, "//div[contains(@class, 'rdr-img-cont')]") \
                    .find_element(By.XPATH, ".//img").get_attribute('src')
            except NoSuchElementException:
                print("Could not find img for '" + rider["preferred_name"] + "' in '" + rider["link"] + "'")
            rider['country'] = driver.find_element(By.XPATH, "//div[contains(@class, 'rdr-info-cont')]") \
                .find_element(By.XPATH, ".//a[contains(@class, 'black')]").get_attribute('innerHTML')

    # Close the driver
    driver.close()

    return teams
