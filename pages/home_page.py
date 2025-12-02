from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import ConfigUI


class HomePage(BasePage):

    ACCEPT_ALL_BUTTON = (By.ID, "wt-cli-accept-all-btn")
    COMPANY_LINK = (By.LINK_TEXT, "Company")
    CAREERS_LINK = (By.LINK_TEXT, "Careers")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = ConfigUI.BASE_URL

    def open(self):
        self.navigate_to(self.url)
        self.handle_cookie_popup()

    def handle_cookie_popup(self):
        try:
            self.click(self.ACCEPT_ALL_BUTTON)
        except:
            pass

    def is_opened(self):
        return "useinsider.com" in self.get_current_url()

    def navigate_to_careers(self):
        self.hover_over_element_by_locator(self.COMPANY_LINK)
        self.click(self.CAREERS_LINK)
