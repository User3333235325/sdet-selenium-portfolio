# SDET Portfolio: Selenium UI Tests

A project built with Python, Selenium, and Pytest. It uses the Page Object Model to keep tests clear and easy to read.

The tests cover login, shopping cart actions, and form submission.

## Test sites

- [The Internet](https://the-internet.herokuapp.com/) — valid and invalid login.
- [Sauce Demo](https://www.saucedemo.com/) — login and add a product to the cart.
- [EvilTester Test Pages](https://testpages.eviltester.com/pages/forms/html-form/) — complete and submit an HTML form.

`standard_user` and `secret_sauce` are public Sauce Demo credentials. They are not real account details.

## What this project shows

- Page objects keep locators and browser actions out of the tests.
- Explicit waits replace fixed `sleep` calls.
- Each test starts with a new Chrome browser session.
- A failed test saves a screenshot and page HTML in `artifacts/`.
- Environment variables can change the test site URL and browser mode.
- GitHub Actions runs the smoke tests on pushes and pull requests.

## Project structure

```text
.
├── src/
│   ├── config/settings.py        # Test settings
│   └── pages/                    # Page objects
│       ├── base_page.py
│       ├── the_internet_login_page.py
│       ├── secure_area_page.py
│       ├── sauce_login_page.py
│       ├── inventory_page.py
│       ├── cart_page.py
│       └── html_form_page.py
├── tests/
│   ├── conftest.py               # Browser setup and failure files
│   ├── test_the_internet_login.py
│   ├── test_sauce_demo_shopping.py
│   └── test_html_form_submission.py
├── .github/workflows/ui-tests.yml
├── requirements.txt
└── pytest.ini
```

## Run the tests

### Requirements

- Python 3.11 or newer
- Google Chrome
- Internet access

Selenium Manager downloads the matching browser driver on the first run.

### Install and run in PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest -m smoke
```

Tests run in headless Chrome by default. Use this command to watch the browser:

```powershell
$env:HEADLESS = "false"
pytest -m smoke
```

Run all tests or one test file:

```powershell
pytest
pytest tests/test_the_internet_login.py
pytest tests/test_html_form_submission.py
```

## Settings

The project has defaults for all test sites.

| Variable | Default | Use |
| --- | --- | --- |
| `HEADLESS` | `true` | Set to `false` to see the browser. |
| `BROWSER` | `chrome` | Browser to run. |
| `THE_INTERNET_URL` | `https://the-internet.herokuapp.com` | The Internet URL. |
| `SAUCE_DEMO_URL` | `https://www.saucedemo.com` | Sauce Demo URL. |
| `FORM_TEST_URL` | `https://testpages.eviltester.com/pages/forms/html-form/` | HTML form test URL. |

Example:

```powershell
$env:HEADLESS = "false"
pytest -m smoke
```

## Test coverage

| Area | Test | Check |
| --- | --- | --- |
| Login | Valid The Internet login | The secure area and success message appear. |
| Login | Invalid The Internet login | An error message appears. |
| Shopping cart | Sauce Demo add to cart | The selected product appears in the cart. |
| Form | HTML form submission | The submitted values and success message appear. |

## Failure files

When a test fails, the project saves a PNG screenshot and the page HTML in `artifacts/`. These files help with bug reports and test failures.

## Design

- Tests are independent. Each test uses a new browser session.
- Tests contain the checks. Page objects contain browser actions.
- Locators use stable IDs and clear text where possible.
- `BasePage` contains the shared wait and interaction methods.

## About this repository

This repository was created as an SDET portfolio project. It shows Python code, Selenium test design, and use of Git and GitHub Actions.
