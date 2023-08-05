from selenium import webdriver
from selenium.webdriver.common.by import By

from .base import init_driver

BASE_URL: str = "https://www.procyclingstats.com/race/{args}"
STAGE_URL: str = BASE_URL.format(args="{race_name}/{year}/stage-{stage}")
STAGE_GC_URL: str = BASE_URL.format(args="{race_name}/{year}/stage-{stage}-gc")
FINAL_GC_URL: str = BASE_URL.format(args="{race_name}/{year}/gc")
FINAL_POINTS_URL: str = BASE_URL.format(args="{race_name}/{year}/stage-21-points")
FINAL_KOM_URL: str = BASE_URL.format(args="{race_name}/{year}/stage-21-kom")
FINAL_YOUTH_URL: str = BASE_URL.format(args="{race_name}/{year}/stage-21-youth")
FINAL_TEAMS_URL: str = BASE_URL.format(args="{race_name}/{year}/stage-21-teams")

STAGE_LEN = 20
STAGE_TTT_LEN = 3
STAGE_GC_LEN = 6
FINAL_GC_LEN = 25
FINAL_POINTS_LEN = 1
FINAL_KOM_LEN = 1
FINAL_YOUTH_LEN = 1
FINAL_TEAMS_LEN = 1


def scrap_items(url: str, results_len: int) -> list:
    driver: webdriver = init_driver()
    driver.get(url)
    result_items = driver.find_element(By.XPATH,
                                       "//div[contains(@class, 'result-cont') and not(contains(@class, 'hide'))]") \
        .find_element(By.XPATH, ".//table[contains(@class, 'basic') and contains(@class, 'results')]") \
        .find_element(By.XPATH, ".//tbody").find_elements(By.XPATH, ".//tr")
    results = list()
    for index in range(0, results_len):
        result_link = result_items[index].find_element(By.XPATH, ".//a")
        results.append({
            "name": result_link.get_attribute("innerHTML"),
            "link": result_link.get_attribute("href"),
            "position": index + 1
        })
    # Close the driver
    driver.close()
    print("Results scraped. Webdriver closed!")
    return results


def scrap_items_ttt(url: str, team_results_len: int) -> list:
    driver: webdriver = init_driver()
    driver.get(url)
    result_items = driver.find_element(By.XPATH,
                                       "//div[contains(@class, 'result-cont') and not(contains(@class, 'hide'))]") \
        .find_element(By.XPATH, ".//table[contains(@class, 'results-ttt')]") \
        .find_element(By.XPATH, ".//tbody").find_elements(By.XPATH, ".//tr")
    results = list()
    team_position = 0
    for item in result_items:
        if 'team' in item.get_attribute('class').split():
            if team_position >= team_results_len:
                break
            else:
                team_position += 1
                pass
        result_element = item.find_element(By.XPATH, ".//a")
        results.append({
            "name": result_element.get_attribute("innerHTML"),
            "link": result_element.get_attribute("href"),
            "position": team_position
        })
    # Close the driver
    driver.close()
    print("Results scraped. Webdriver closed!")
    return results


def scrap_stage(race_name: str, year: int, stage: int, length: int = STAGE_LEN) -> list:
    stage_url = STAGE_URL.format(race_name=race_name, year=year, stage=stage)
    return scrap_items(stage_url, length)


def scrap_stage_ttt(race_name: str, year: int, stage: int, length: int = STAGE_TTT_LEN) -> list:
    stage_url = STAGE_URL.format(race_name=race_name, year=year, stage=stage)
    return scrap_items_ttt(stage_url, length)


def scrap_stage_gc(race_name: str, year: int, stage: int, length: int = STAGE_GC_LEN) -> list:
    stage_gc_url = STAGE_GC_URL.format(race_name=race_name, year=year, stage=stage)
    return scrap_items(stage_gc_url, length)


def scrap_final_gc(race_name: str, year: int, length: int = FINAL_GC_LEN) -> list:
    final_gc_url = FINAL_GC_URL.format(race_name=race_name, year=year)
    return scrap_items(final_gc_url, length)


def scrap_final_points(race_name: str, year: int, length: int = FINAL_POINTS_LEN) -> list:
    final_points_url = FINAL_POINTS_URL.format(race_name=race_name, year=year)
    return scrap_items(final_points_url, length)


def scrap_final_kom(race_name: str, year: int, length: int = FINAL_KOM_LEN) -> list:
    final_kom_url = FINAL_KOM_URL.format(race_name=race_name, year=year)
    return scrap_items(final_kom_url, length)


def scrap_final_youth(race_name: str, year: int, length: int = FINAL_YOUTH_LEN) -> list:
    final_youth_url = FINAL_YOUTH_URL.format(race_name=race_name, year=year)
    return scrap_items(final_youth_url, length)


def scrap_final_teams(race_name: str, year: int, length: int = FINAL_TEAMS_LEN) -> list:
    final_teams_url = FINAL_TEAMS_URL.format(race_name=race_name, year=year)
    return scrap_items(final_teams_url, length)
