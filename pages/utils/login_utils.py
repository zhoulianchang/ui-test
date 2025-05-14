from playwright.sync_api import Page
from pages.common.login_page import LoginPage

def login_with_request(page: Page, request) -> None:
    """通用的登录方法，处理页面导航、登录和验证
    
    Args:
        page: Playwright的Page对象
        request: pytest的request对象，包含配置信息
    """
    login_page = LoginPage(page)
    login_page.navigate(request)
    login_page.login(request)  # 使用命令行参数中的用户名和密码
    login_page.verify_login_success(request)