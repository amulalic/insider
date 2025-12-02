from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self.actions = ActionChains(driver)

    def navigate_to(self, url):
        self.driver.get(url)

    def wait_for_element_to_be_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_to_be_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        element = self.wait_for_element_to_be_clickable(locator)
        element.click()

    def get_current_url(self):
        return self.driver.current_url

    def hover_over_element_by_locator(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.actions.move_to_element(element).perform()

    def hover_over_element(self, element):
        element = self.wait.until(EC.visibility_of(element))
        self.actions.move_to_element(element).perform()

    def wait_for_url_contains(self, text):
        try:
            self.wait.until(EC.url_contains(text))
            return True
        except TimeoutException:
            return False

    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not found: {locator}")

    def find_elements(self, locator):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            return []

    def scroll_to_element_by_locator(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )

        # Wait for the browser to stop scrolling (Custom Wait)
        try:
            scroll_finished = self.wait.until(
                lambda driver: driver.execute_script(
                    """
                    let scrollingElement = document.scrollingElement || document.documentElement;
                    let initialScrollY = scrollingElement.scrollTop;
                    let currentScrollY = window.scrollY || document.documentElement.scrollTop;
                    return currentScrollY;
                    """
                )
            )

        except TimeoutException:
            print("Warning: Timed out waiting for smooth scrolling to fully finish.")

        self.wait.until(EC.visibility_of_element_located(locator))
        return element

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )

        # Wait for the browser to stop scrolling (Custom Wait)
        try:
            scroll_finished = self.wait.until(
                lambda driver: driver.execute_script(
                    """
                    let scrollingElement = document.scrollingElement || document.documentElement;
                    let initialScrollY = scrollingElement.scrollTop;
                    let currentScrollY = window.scrollY || document.documentElement.scrollTop;
                    return currentScrollY;
                    """
                )
            )

        except TimeoutException:
            print("Warning: Timed out waiting for smooth scrolling to fully finish.")

        self.wait.until(EC.visibility_of(element))
        return element

    def get_window_count(self):
        return len(self.driver.window_handles)

    def wait_for_number_of_windows(self, num_windows):
        try:
            self.wait.until(lambda driver: len(driver.window_handles) == num_windows)
            return True
        except TimeoutException:
            return False

    def switch_to_window(self, window_index):
        windows = self.driver.window_handles
        if len(windows) > window_index:
            self.driver.switch_to.window(windows[window_index])

    def wait_for_text_to_be_present_in_attribute(self, locator, text, attribute):
        self.wait.until(
            EC.text_to_be_present_in_element_attribute(locator, attribute, text)
        )
