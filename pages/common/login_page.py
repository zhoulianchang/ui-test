from playwright.sync_api import Page, expect
from config.accounts import get_account

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('button[type="submit"]')
        self.error_message = page.locator('.ant-form-item-explain-error')

    def navigate(self, request):
        self.page.goto(request.config.domain + '/user/login')
        # 等待页面加载完成，增加超时时间
        expect(self.username_input).to_be_visible(timeout=10000)
        expect(self.password_input).to_be_visible(timeout=10000)
        expect(self.login_button).to_be_visible(timeout=10000)

    def login(self, request, username: str = None, password: str = None):
        # 如果没有提供用户名和密码，从配置中获取
        account = get_account(request)
        # 区分None和空字符串的情况
        username = account["username"] if username is None else username
        password = account["password"] if password is None else password
        # 确保元素可交互，增加超时时间
        expect(self.username_input).to_be_editable(timeout=10000)
        self.username_input.fill(username)
        expect(self.password_input).to_be_editable(timeout=10000)
        self.password_input.fill(password)
        expect(self.login_button).to_be_enabled(timeout=10000)
        self.login_button.click()
        # 等待页面响应
        self.page.wait_for_load_state('networkidle', timeout=30000)
        self.choice_company(account["company"])

    def get_api_error(self) -> str:
        # 检查接口返回的错误消息
        api_error = self.page.locator('.ant-message-notice-content')
        if api_error.count() > 0:
            expect(api_error.first).to_be_visible(timeout=10000)
            return api_error.first.text_content()
        return ""

    def get_form_error(self) -> str:
        # 检查表单验证的错误消息
        form_error = self.error_message.first
        expect(form_error).to_be_visible(timeout=10000)
        error_messages = [msg.text_content() for msg in self.error_message.all()]
        return ' '.join(error_messages)

    def get_error_message(self) -> str:
        # 优先检查API错误
        api_error = self.get_api_error()
        if api_error:
            return api_error
        # 如果没有API错误，则检查表单验证错误
        return self.get_form_error()
    def choice_company(self, company_name: str):
        # 检查是否存在公司选择弹窗
        company_modal = self.page.locator('.ant-modal-content')
        if company_modal.count() > 0:
            # 等待弹窗完全显示并确保内容加载
            expect(company_modal).to_be_visible(timeout=15000)
            self.page.wait_for_load_state('networkidle', timeout=15000)
            
            # 等待公司列表加载完成，点击下拉框
            select_company = self.page.locator('.ant-select-selector')
            expect(select_company).to_be_visible(timeout=15000)
            select_company.click()
            self.page.wait_for_load_state('networkidle', timeout=5000)

            # 等待选择公司的选项加载完成，点击指定公司
            company_option = self.page.locator(f'.ant-select-item-option-content:has-text("{company_name}")')
            expect(company_option).to_be_visible(timeout=15000)
            company_option.click()
            self.page.wait_for_load_state('networkidle', timeout=5000)
            # 等待选择公司的按钮加载完成，点击登录按钮
            select_company_button = self.page.locator('.ant-modal-content .ant-btn-primary')
            expect(select_company_button).to_be_visible(timeout=15000)
            select_company_button.click()
            self.page.wait_for_load_state('networkidle', timeout=5000)
    def verify_login_success(self, request):
        # 等待页面加载完成
        self.page.wait_for_load_state('networkidle', timeout=15000)
        # 验证是否成功跳转到home页面
        expect(self.page).to_have_url(request.config.domain + '/home', timeout=15000)