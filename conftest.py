import pytest
from playwright.sync_api import Page, expect
from datetime import datetime

def pytest_html_report_title(report):
    report.title = "Login Test Report"

def pytest_addoption(parser):
    parser.addoption(
        "--username",
        action="store",
        default=None,
        help="用户名"
    )
    parser.addoption(
        "--password",
        action="store",
        default=None,
        help="密码"
    )
    parser.addoption(
        "--company",
        action="store",
        default="Test-01",
        help="公司名称，默认为Test-01"
    )
    parser.addoption(
        "--domain",
        action="store",
        default=None
        help="测试域名"
    )

def pytest_configure(config):
    # 生成报告文件名
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    config.option.htmlpath = f"reports/login_{current_time}.html"
    
    # 将命令行参数添加到pytest配置中
    config.username = config.getoption("--username")
    config.password = config.getoption("--password")
    config.company = config.getoption("--company")
    config.domain = config.getoption("--domain")
    # 验证必填参数
    if not config.username or not config.password:
        pytest.exit("Error: --username and --password are required arguments")

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False,
        "args": [
            "--start-maximized",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None,  # 设置为None以允许浏览器窗口最大化
        "screen": {
            "width": 1920,
            "height": 1080
        }
    }

@pytest.fixture(scope="function")
def page(page: Page):
    page.set_default_timeout(60000)  # 设置默认超时时间为60秒
    page.set_default_navigation_timeout(60000)  # 设置默认导航超时时间为60秒
    yield page
