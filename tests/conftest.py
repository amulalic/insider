import datetime
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import os
from api.pet_api import PetAPI
from utils.test_data import TestDataFactory, PetDataBuilder


def pytest_addoption(parser):
    """Command line options for browser selection"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox",
    )


@pytest.fixture(scope="function")
def driver(request):
    """Initialize and return WebDriver based on browser parameter"""
    browser = request.config.getoption("--browser").lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )
        driver.maximize_window()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test failure and take screenshot"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Create screenshots directory if not exists
            screenshots_dir = "screenshots"
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)

            # Generate screenshot filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)

            # Take screenshot
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")


@pytest.fixture(scope="session")
def pet_api():
    """Create PetAPI instance for the test session"""
    api = PetAPI()
    yield api
    api.close()


@pytest.fixture(scope="function")
def cleanup_pet(pet_api):
    """Fixture for cleaning up pets after test"""
    pets_to_cleanup = []

    def _add_pet(pet_id):
        pets_to_cleanup.append(pet_id)

    yield _add_pet

    # Cleanup after test
    for pet_id in pets_to_cleanup:
        try:
            pet_api.delete_pet(pet_id)
        except:
            pass


@pytest.fixture(scope="module")
def valid_pet_data():
    """Get valid pet data"""
    return TestDataFactory.valid_pet()


@pytest.fixture(scope="module")
def created_pet(pet_api, valid_pet_data):
    """Create a pet and return its data"""
    response = pet_api.create_pet(valid_pet_data)
    pet_data = response.json()
    yield pet_data
    # Cleanup
    try:
        pet_api.delete_pet(pet_data["id"])
    except:
        pass


@pytest.fixture(scope="function")
def pet_for_deletion(pet_api):
    """Create a pet specifically for deletion tests"""
    pet_data = (
        PetDataBuilder()
        .with_id()
        .with_name("PetToDelete")
        .with_status("available")
        .build()
    )

    response = pet_api.create_pet(pet_data)
    return response.json()
