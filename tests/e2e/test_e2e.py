# tests/e2e/test_e2e.py

import pytest
from playwright.sync_api import expect


@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage displays "Hello World".

    This verifies that the FastAPI server is running
    and serving the correct HTML template.
    """

    # Navigate to the homepage
    page.goto("http://localhost:8000")

    # Verify the homepage heading
    expect(page.locator("h1")).to_have_text("Hello World")


@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """
    Test the addition functionality of the calculator.

    This test simulates a user entering two numbers,
    clicking Add, and checking the displayed result.
    """

    # Navigate to the calculator
    page.goto("http://localhost:8000")

    # Enter the first number
    page.fill("#a", "10")

    # Enter the second number
    page.fill("#b", "5")

    # Click the Add button
    page.click('button:text("Add")')

    # Wait for the calculation result and verify it
    expect(page.locator("#result")).to_have_text(
        "Calculation Result: 15"
    )


@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """
    Test division by zero.

    This verifies that the calculator displays an
    appropriate error message when dividing by zero.
    """

    # Navigate to the calculator
    page.goto("http://localhost:8000")

    # Enter the first number
    page.fill("#a", "10")

    # Enter zero as the second number
    page.fill("#b", "0")

    # Click the Divide button
    page.click('button:text("Divide")')

    # Wait for the error message and verify it
    expect(page.locator("#result")).to_have_text(
        "Error: Cannot divide by zero!"
    )