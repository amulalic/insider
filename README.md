# Insider Testing Framework

A Python-based automated testing framework for validating Insider Careers Page and Pet API endpoint.

## Prerequisites

- Python 3.8+
- pip
- Chrome/Firefox browser (for UI tests)
- JMeter

## Installation

```bash
# Clone the repository
git clone https://github.com/amulalic/insider.git
cd insider

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
insider/
├── tests/
│   ├── ui/                    # UI tests for Insider Careers page
│   └── api/                   # API tests for Pet endpoint
├── bugs/                      # Video recordings of bugs found
├── config/                    # Configuration files
├── api/                       # API Object Models
├── pages/                     # Page Object Models
├── utils/                     # Helper functions and utilities
├── reports/                   # Generated test reports
├── screenshots/               # Screenshots of failed tests
├── jmeter/                    # JMeter files
│   ├── *.jmx                  # JMeter test plan file
│   └── *.csv                  # Test data for JMeter
├── requirements.txt
└── README.md
```

## Running Tests

```bash
# Run all tests (in Chrome by default)
pytest

# Run specific test suite
pytest tests/api/
pytest tests/ui/

# Run in Firefox
pytest --browser "firefox"

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run with verbose output
pytest -v
```

## Test Coverage

### Insider Careers Page
1. Visit https://useinsider.com/ and check Insider home page is opened or not
2. Select the 'Company' menu in the navigation bar, select 'Careers' and check Career page, its Locations, Teams, and Life at Insider blocks are open or not
3. Go to https://useinsider.com/careers/quality-assurance/, click 'See all QA jobs', filter jobs by Location: 'Istanbul, Turkiye', and Department: 'Quality Assurance', check the presence of the job list
4. Check that all jobs' Position contains 'Quality Assurance', Department contains 'Quality Assurance', and Location contains 'Istanbul, Turkiye'
5. Click the 'View Role' button and check that this action redirects us to the Lever Application form page

### Pet API Endpoint
- CRUD operations (Create, Read, Update, Delete)

### Search module on n11.com
- Load tests for search module