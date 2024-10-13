from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


class WebParser:
    def __init__(self, link):
        self.link = link
        self.driver = webdriver.Chrome()
        self.data = {
            "vacancy_title": [],
            "company_title": [],
            "grade": [],
            "vacancy": [],
            "skills": [],
        }

    def _get_html(self):
        """This methode get html code for parsing"""
        self.driver.get(self.link)
        return self.driver.page_source

    def _parse_page(self):
        """Methode parses an Internet page"""
        soup = BeautifulSoup(self._get_html(), features="html.parser")

        # methode retrieves all necessary information from page
        vacancy_title = soup.find_all(class_="vacancy-card__title")
        self.data["vacancy_title"].extend([title.text for title in vacancy_title])

        company_title = soup.find_all(class_="vacancy-card__company-title")
        self.data["company_title"].extend([company.text for company in company_title])

        skills_data = soup.find_all(class_="vacancy-card__skills")
        for skills in skills_data:
            skill = skills.text.split(" • ")

            try:
                vacancy, grade = skill[0].split(", ")
            except ValueError:
                vacancy, grade = skill[0], "Не указан"

            self.data["vacancy"].append(vacancy)
            self.data["grade"].append(grade)
            self.data["skills"].append(skill[1:])

    def parse(self):
        """Methode that parses, scrolls page and clicks a button to move to another page"""
        while True:
            # parses page
            self._parse_page()
            # scrolls page
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # finds button to click
            elems = self.driver.find_elements(
                By.XPATH, '//div[@class="with-pagination__side-button"]'
            )
            try:
                self.link = (
                    elems[1].find_element(By.TAG_NAME, "a").get_attribute("href")
                )
                # clicks on a button to move to another page
                elems[1].click()
            except NoSuchElementException:
                print("Last page reached")
                break
        # closes selenium window and quits selenium driver
        self.driver.close()
        self.driver.quit()

    def get_data(self):
        """Methode helps to create a pandas dataframe with collected data"""
        return pd.DataFrame(self.data)
