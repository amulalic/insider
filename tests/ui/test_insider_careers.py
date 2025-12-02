import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_jobs_page import QAJobsPage


def test_insider_careers(driver):
    """
    1. Visit https://useinsider.com/ and check Insider home page is opened or not
    2. Select the 'Company' menu in the navigation bar, select 'Careers' and check Career page, its Locations, Teams, and Life at Insider blocks are open or not
    3. Go to https://useinsider.com/careers/quality-assurance/, click 'See all QA jobs', filter jobs by Location: 'Istanbul, Turkiye', and Department: 'Quality Assurance', check the presence of the job list
    4. Check that all jobs' Position contains 'Quality Assurance', Department contains 'Quality Assurance', and Location contains 'Istanbul, Turkiye'
    5. Click the 'View Role' button and check that this action redirects us to the Lever Application form page
    """

    print("Visit https://useinsider.com/")
    home_page = HomePage(driver)
    home_page.open()

    print("Check Insider home page is opened or not")
    assert home_page.is_opened(), "Home page is not opened"

    print("Select the 'Company' menu in the navigation bar, select 'Careers'")
    home_page.navigate_to_careers()

    print("Check Career page")
    careers_page = CareersPage(driver)
    assert careers_page.is_opened(), "Careers page is not opened"
    assert careers_page.get_big_title().text == "Ready to disrupt?", "Wrong big title"

    print("Check Locations, Teams, and Life at Insider blocks are open or not")
    assert (
        careers_page.is_locations_block_visible()
    ), "The block 'Location' is not shown"
    assert careers_page.is_teams_block_visible(), "The block 'Teams' is not shown"
    assert (
        careers_page.is_life_at_insider_block_visible()
    ), "The block 'Life at Insider' is not shown"

    print("Go to https://useinsider.com/careers/quality-assurance/")
    qa_jobs_page = QAJobsPage(driver)
    qa_jobs_page.open()

    print("Click 'See all QA jobs'")
    qa_jobs_page.click_see_all_qa_jobs()

    print("Filter jobs by Department: 'Quality Assurance'")
    qa_jobs_page.wait_for_deparment_filter_population()
    qa_jobs_page.wait_for_jobs_to_load()

    print("Filter jobs by Location: 'Istanbul, Turkiye'")
    qa_jobs_page.filter_by_location("Istanbul, Turkiye")

    print("Check the presence of the job list")
    qa_jobs_page.wait_for_jobs_to_load()

    print(
        "Check that all jobs' Position contains 'Quality Assurance', Department contains 'Quality Assurance', and Location contains 'Istanbul, Turkiye'"
    )
    assert qa_jobs_page.verify_all_jobs(), "Some jobs do not meet the criteria"

    print("Click the 'View Role' button of the first job")
    qa_jobs_page.click_view_role_for_first_job()

    print("Check that this action redirects us to the Lever Application form page")
    assert (
        qa_jobs_page.verify_lever_application_page()
    ), "Not redirected to Lever Application form page"
