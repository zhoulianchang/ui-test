import pytest
from pages.utils.login_utils import login_with_request
from playwright.sync_api import Page, expect

def test_example(page, request):
    login_with_request(page, request)
    # 进行其他测试Debug步骤
    page.goto("https://console.scioneaitest.local.ilabservice.cloud/inventory/locations/storageFacility")
    page.get_by_role("button", name="New").click()
    page.get_by_text("None").click()
    page.get_by_text("None").nth(1).click()
    page.get_by_role("combobox", name="GXP Type").click()
    page.get_by_text("None").nth(2).click()
    page.get_by_role("combobox", name="Room Manager").click()
    page.get_by_title("Mr.Zhou").click()
    page.get_by_role("combobox", name="* Management Method").click()
    page.get_by_title("Administrator Management").locator("div").click()
    page.get_by_role("combobox", name="* Inventory Administrator").click()
    page.get_by_text("pp.wu").nth(1).click()
    page.get_by_role("combobox", name="* Warehouse Type").click()
    page.get_by_title("Warehouse", exact=True).click()
    page.wait_for_timeout(5000)
