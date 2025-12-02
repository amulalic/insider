from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class QAJobsPage(BasePage):

    SEE_ALL_QA_JOBS_BUTTON = (By.LINK_TEXT, "See all QA jobs")
    LOCATION_FILTER = (By.ID, "select2-filter-by-location-container")
    DEPARTMENT_FILTER = (By.ID, "select2-filter-by-department-container")
    JOB_LIST = (By.CSS_SELECTOR, ".position-list-item")
    DEPARTMENT_SEARCH = (By.XPATH, "//li[text()='Quality Assurance']")
    POSITION_TITLE = (By.CSS_SELECTOR, ".position-title")
    POSITION_LOCATION = (By.CSS_SELECTOR, ".position-location")
    POSITION_DEPARTMENT = (By.CSS_SELECTOR, ".position-department")
    POSITION_VIEW_ROLE = (By.LINK_TEXT, "View Role")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)
        self.url = "https://useinsider.com/careers/quality-assurance/"

    def wait_for_count_to_stabilize(
        self, element_id="deneme", stability_duration=3, timeout=30
    ):
        element = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))

        start_time = time.time()
        last_value = None
        last_change_time = time.time()

        while time.time() - start_time < timeout:
            current_value = element.text

            if current_value != last_value:
                # Value changed, reset the stability timer
                last_value = current_value
                last_change_time = time.time()
            else:
                # Value hasn't changed, check if it's been stable long enough
                if time.time() - last_change_time >= stability_duration:
                    return current_value

            # Short sleep to avoid excessive CPU usage
            time.sleep(0.1)

        raise TimeoutError(
            f"Element #{element_id} did not stabilize within {timeout} seconds"
        )

    def open(self):
        self.navigate_to(self.url)

    def click_see_all_qa_jobs(self):
        self.scroll_to_element_by_locator(self.SEE_ALL_QA_JOBS_BUTTON)
        self.click(self.SEE_ALL_QA_JOBS_BUTTON)
        self.wait_for_url_contains("open-positions")

    def wait_for_jobs_to_load(self):
        self.wait_for_count_to_stabilize()
        self.find_elements(self.JOB_LIST)

    def wait_for_deparment_filter_population(self):
        self.wait.until(
            EC.text_to_be_present_in_element_attribute(
                self.DEPARTMENT_FILTER, "title", "Quality Assurance"
            )
        )

    def filter_by_location(self, location):
        self.click(self.LOCATION_FILTER)
        self.click((By.XPATH, f"//li[text()='{location}']"))
        self.wait_for_jobs_to_load()

    def get_job_listings(self):
        return self.find_elements(self.JOB_LIST)

    def get_job_details(self, job_element):
        try:
            position = job_element.find_element(*self.POSITION_TITLE).text
            department = job_element.find_element(*self.POSITION_DEPARTMENT).text
            location = job_element.find_element(*self.POSITION_LOCATION).text

            print(position)
            print(department)
            print(location)

            return {
                "position": position,
                "department": department,
                "location": location,
            }
        except Exception as e:
            print(f"Error extracting job details: {e}")
            return None

    def verify_job_criteria(
        self,
        job_details,
        expected_department="Quality Assurance",
        expected_location="Istanbul, Turkiye",
    ):
        if not job_details:
            return False

        position_match = expected_department in job_details["position"]
        department_match = expected_department in job_details["department"]
        location_match = expected_location in job_details["location"]

        return position_match and department_match and location_match

    def verify_all_jobs(self):
        jobs = self.get_job_listings()

        for i, job in enumerate(jobs, 1):
            job_details = self.get_job_details(job)

            if not job_details:
                print(f"\nJob {i}: Could not extract job details")
                continue

            print(f"\nJob {i}:")
            print(f"  Position: {job_details['position']}")
            print(f"  Department: {job_details['department']}")
            print(f"  Location: {job_details['location']}")

            is_valid = self.verify_job_criteria(job_details)

            if is_valid:
                print(f"Valid")
            else:
                print(f"Invalid")
                return False

        return True

    def click_view_role_for_first_job(self):
        jobs = self.get_job_listings()
        if jobs:
            self.scroll_to_element(jobs[0])
            self.hover_over_element(jobs[0])
            self.click(self.POSITION_VIEW_ROLE)
            self.wait_for_number_of_windows(2)

            return True
        return False

    def verify_lever_application_page(self):
        if self.wait_for_number_of_windows(2):
            self.switch_to_window(1)

        # Wait for Lever page to load
        self.wait.until(
            lambda driver: "lever.co" in driver.current_url
            or "jobs.lever.co" in driver.current_url
        )

        current_url = self.get_current_url()
        return "lever.co" in current_url or "jobs.lever.co" in current_url
