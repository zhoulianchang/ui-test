from playwright.sync_api import Page, expect
import random

class LocationsPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_button = page.locator('button:has-text("New")')
        # 定位新建位置弹窗中的元素
        self.location_number_input = page.locator('input[id="number"]')
        self.room_select = page.locator('input[id="roomId"]')
        self.equipment_select = page.locator('input[id="deviceId"]')
        self.by_user_radio = page.locator('label:has-text("By User")')
        self.layer_input = page.locator('input[id="storey"]')
        self.grid_input = page.locator('input[id="division"]')
        self.confirm_button = page.locator('button:has-text("Confirm")').first

    def navigate(self, request):
        # 导航到locations页面
        self.page.goto(request.config.domain + '/inventory/locations/locations')
        # 等待页面加载完成
        expect(self.new_button).to_be_visible(timeout=10000)

    def click_new_button(self):
        # 点击New按钮
        expect(self.new_button).to_be_enabled(timeout=10000)
        self.new_button.click()
        # 等待页面响应
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def create_location(self, location_number: str, room: str, equipment: str, layer: str = None, grid: str = None):
        # 填写Location Number
        self.location_number_input.fill(location_number)

        # 选择Room
        expect(self.room_select).to_be_visible(timeout=10000)
        self.room_select.click()
        self.page.wait_for_load_state('networkidle', timeout=5000)
        room_option = self.page.locator(f'div[title="{room}"]')
        expect(room_option).to_be_visible(timeout=10000)
        room_option.click()
        self.page.wait_for_load_state('networkidle', timeout=5000)

        # 选择Equipment
        self.equipment_select.click()
        self.page.locator(f'div[title="{equipment}"]').click()

        # 填写Layer和Grid，使用随机数，并处理Grid重复的情况
        random_layer = str(random.randint(1, 50))
        max_retries = 5  # 最大重试次数
        success = False
        
        # 填写Layer
        self.layer_input.fill(random_layer if layer is None else layer)
        
        # 循环尝试不同的Grid值，直到成功或达到最大重试次数
        for attempt in range(max_retries):
            try:
                # 清空Grid输入框
                self.grid_input.click()
                self.grid_input.press('Control+a')
                self.grid_input.press('Backspace')
                self.page.wait_for_timeout(1000)  # 等待清空操作完成

                # 使用更大范围的随机数
                random_grid = str(random.randint(1, 50))  # 扩大随机数范围
                self.grid_input.fill(random_grid if grid is None else grid)
                self.page.wait_for_timeout(1000)  # 等待填充完成
                
                # 等待所有输入完成并验证
                expect(self.location_number_input).to_have_value(location_number, timeout=10000)
                expect(self.layer_input).to_have_value(random_layer if layer is None else layer, timeout=10000)
                expect(self.grid_input).to_have_value(random_grid if grid is None else grid, timeout=10000)
                
                # 确保表单数据已完全准备好
                self.page.wait_for_timeout(2000)
                success = True
                break
            except Exception as e:
                if "Grid already exists" in str(e) and attempt < max_retries - 1:
                    print(f"Grid {random_grid} already exists, trying another value...")
                    continue
                else:
                    raise e
        
        if not success:
            raise Exception("Failed to find an available Grid value after multiple attempts")
        
        # 点击确认按钮
        self.page.wait_for_load_state('networkidle', timeout=5000)
        self.confirm_button.wait_for(state='visible', timeout=10000)
        expect(self.confirm_button).to_be_enabled(timeout=10000)
        self.confirm_button.click()
        # 等待页面响应
        self.page.wait_for_load_state('networkidle', timeout=10000)
        # 等待提交成功的提示消息
        success_message = self.page.locator('.ant-message-notice-content:has-text("Success")')
        expect(success_message).to_be_visible(timeout=10000)

    def verify_location_created(self, location_number: str):
        # 验证位置是否创建成功
        location_cell = self.page.locator(f'text={location_number}')
        expect(location_cell).to_be_visible(timeout=10000)

    def refresh_page(self):
        # 刷新页面
        self.page.reload()
        # 等待页面加载完成
        expect(self.new_button).to_be_visible(timeout=10000)
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def click_edit_button(self, location_number: str):
        # 找到对应记录的编辑按钮并点击
        self.page.wait_for_load_state('networkidle', timeout=10000)
        # 使用更可靠的定位器
        edit_button = self.page.locator(f'tr:has-text("{location_number}") button:has-text("Edit")')
        expect(edit_button).to_be_visible(timeout=10000)
        edit_button.click()
        # 等待页面响应
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def edit_location(self):
        # 等待页面加载完成
        self.page.wait_for_load_state('networkidle', timeout=10000)
        # 修改layer字段，使用更精确的定位器
        layer_input = self.page.locator('input[placeholder="Enter"]').nth(1)
        expect(layer_input).to_be_visible(timeout=10000)
        expect(layer_input).to_be_enabled(timeout=10000)
        # 确保输入框可以交互
        self.page.wait_for_timeout(1000)
        layer_input.click()
        # 清空输入框
        layer_input.press('Control+a')
        layer_input.press('Backspace')
        # 生成1-50的随机数作为新的layer值
        random_layer = str(random.randint(1, 50))
        # 填写新值
        layer_input.fill(random_layer)
        # 验证输入值是否正确
        expect(layer_input).to_have_value(random_layer, timeout=10000)
        # 等待一段时间确保值已更新
        self.page.wait_for_timeout(2000)
        # 再次验证输入值
        expect(layer_input).to_have_value(random_layer, timeout=10000)
        # 点击确认按钮
        expect(self.confirm_button).to_be_visible(timeout=10000)
        expect(self.confirm_button).to_be_enabled(timeout=10000)
        self.confirm_button.click()
        # 等待页面响应
        self.page.wait_for_load_state('networkidle', timeout=10000)
        # 等待提交成功的提示消息
        success_message = self.page.locator('.ant-message-notice-content:has-text("Success")')
        expect(success_message).to_be_visible(timeout=10000)
        # 返回随机生成的layer值供验证使用
        return random_layer

    def verify_location_edited(self, location_number: str, expected_layer: str):
        # 刷新页面以确保获取最新数据
        self.refresh_page()
        # 等待页面完全加载
        self.page.wait_for_load_state('networkidle', timeout=10000)
        # 验证位置是否修改成功
        location_row = self.page.locator(f'tr:has-text("{location_number}")')
        expect(location_row).to_be_visible(timeout=10000)
        # 使用更精确的定位器来定位layer列，通过表头文本定位列索引
        headers = self.page.locator('thead th')
        layer_index = -1
        for i in range(headers.count()):
            if 'Layer' in headers.nth(i).text_content():
                layer_index = i
                break
        assert layer_index >= 0, "Layer column not found in table headers"
        
        # 使用找到的列索引定位layer单元格
        layer_cell = location_row.locator('td').nth(layer_index)
        expect(layer_cell).to_be_visible(timeout=10000)
        # 等待一段时间确保数据已更新
        self.page.wait_for_timeout(2000)
        # 验证文本内容
        actual_layer = layer_cell.text_content().strip()
        # 打印实际值和期望值以便调试
        print(f"Actual layer value: {actual_layer}")
        print(f"Expected layer value: {expected_layer}")
        assert actual_layer == expected_layer, f"Layer value mismatch. Expected: {expected_layer}, Actual: {actual_layer}"