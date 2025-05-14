import pytest
from pages.common.login_page import LoginPage

def test_successful_login_company(page, request):
    login_page = LoginPage(page)
    login_page.navigate(request)
    login_page.login(request)
    login_page.verify_login_success(request)

def test_failed_login_with_invalid_credentials(page, request):
    login_page = LoginPage(page)
    login_page.navigate(request)
    login_page.login(request, "invalid_user", "invalid_password")
    error_message = login_page.get_error_message()
    assert "Account does not exist" in error_message

def test_empty_credentials(page, request):
    login_page = LoginPage(page)
    login_page.navigate(request)
    login_page.login(request, "", "")
    error_messages = login_page.get_error_message()
    assert "This field is required" in error_messages