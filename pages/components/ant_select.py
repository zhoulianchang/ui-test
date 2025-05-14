from playwright.sync_api import Page, expect

class AntSelect:
    def __init__(self, page: Page):
        self.page = page

    def select_option(self, select_element, option_value: str):
        """通用的Ant Design单选下拉框选择方法
        
        Args:
            select_element: 下拉框元素的Locator
            option_value: 要选择的选项值
        """
        # 确保下拉框可见并可点击
        expect(select_element).to_be_visible(timeout=10000)
        select_element.click()
    
        # 等待下拉框完全展开并确保是可见的（不包含hidden类）
        self.page.wait_for_selector('.ant-select-dropdown:not(.ant-select-dropdown-hidden)', timeout=10000)
        
        # 使用更精确的选择器定位选项，只在可见的下拉框中查找
        # 首先找到当前激活的下拉框
        active_dropdown = self.page.locator('.ant-select-dropdown:not(.ant-select-dropdown-hidden)').first
        
        # 在当前激活的下拉框中查找选项
        option = active_dropdown.locator(f'.ant-select-item-option[title="{option_value}"]').first
        
        # 确保元素可点击
        expect(option).to_be_enabled(timeout=10000)
        self.page.wait_for_timeout(500)
        option.click(force=True)