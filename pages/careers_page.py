from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CareersPage(BasePage):

    BIG_TITLE = (By.CLASS_NAME, "big-title")
    LOCATIONS_BLOCK = (By.ID, "career-our-location")
    TEAMS_BLOCK = (By.ID, "career-find-our-calling")
    LIFE_AT_INSIDER_BLOCK = (By.XPATH, "//section[contains(., 'Life at Insider')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)

    def is_opened(self):
        self.wait_for_url_contains("careers")
        return "careers" in self.get_current_url().lower()

    def get_big_title(self):
        return self.find_element(self.BIG_TITLE)

    def is_locations_block_visible(self):
        try:
            self.scroll_to_element_by_locator(self.LOCATIONS_BLOCK)
            self.wait.until(EC.visibility_of_element_located(self.LOCATIONS_BLOCK))
            return True
        except:
            return False

    def is_teams_block_visible(self):
        try:
            self.scroll_to_element_by_locator(self.TEAMS_BLOCK)
            self.wait.until(EC.visibility_of_element_located(self.TEAMS_BLOCK))
            return True
        except:
            return False

    def is_life_at_insider_block_visible(self):
        try:
            self.scroll_to_element_by_locator(self.LIFE_AT_INSIDER_BLOCK)
            self.wait.until(
                EC.visibility_of_element_located(self.LIFE_AT_INSIDER_BLOCK)
            )
            return True
        except:
            return False
