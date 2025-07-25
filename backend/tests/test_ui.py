import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)  # Add headless=False
        page = browser.new_page()
        yield page
        browser.close()


def test_visit_home(page):
    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")  # Wait for page to fully load
    assert (
        "Protect the Digital Advertising Ecosystem" in page.content()
    )  # Check if text exists in page HTML


def test_visit_dashboard(page):
    page.goto("http://localhost:3000/dashboard")
    page.wait_for_load_state("networkidle")  # Wait for page to fully load
    assert "Dashboard Controls" in page.content()  # Check if text exists in page HTML
