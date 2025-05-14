from playwright.sync_api import Page, expect
from pages.components.ant_select import AntSelect

class StorageFacilityPage:
    def __init__(self, page: Page):
        self.page = page
        self.ant_select = AntSelect(page)
        self.new_button = page.get_by_role("button", name="New")
        self.room_number_input = page.get_by_role("textbox", name="* Room Number")
        self.room_input = page.locator('input[id="name"]')
        self.park_input = page.get_by_role("textbox", name="* Park")
        self.building_input = page.get_by_role("textbox", name="* Building")
        self.floor_input = page.get_by_role("textbox", name="* Floor")
        self.lab_safety_level_select = page.get_by_text("None")
        self.gxp_type_select = page.get_by_role("combobox", name="GXP Type")
        self.room_manaer_select = page.get_by_role("combobox", name="Room Manager")
        self.function_profile_input = page.get_by_role("textbox", name="Function Profile")
        self.room_image_upload = page.locator('.ant-upload[role="button"]')
        self.inventory_settings_switch = page.get_by_role("switch", name="On")
        self.management_method_select = page.get_by_role("combobox", name="* Management Method")
        self.inventory_admin_select = page.get_by_role("combobox", name="* Inventory Administrator")
        self.warehouse_type_select = page.get_by_role("combobox", name="* Warehouse Type")
        self.submit_button = page.get_by_role("button", name="Confirm")
        self.search_input = page.locator('.ant-input-group-wrapper .ant-input[placeholder="Keyword"]')
        self.search_button = page.locator('.ant-input-group-wrapper .ant-btn-icon-only')

    def navigate(self, request):
        self.page.goto(request.config.domain + '/inventory/locations/storageFacility')
        # 等待页面加载完成
        expect(self.new_button).to_be_visible(timeout=10000)

    def create_storage_facility(self, room_number: str, room: str, park: str, building: str, floor: str,
                              lab_safety_level: str = None, gxp_type: str = None, function_profile: str = None,
                              image_path: str = None, inventory_enabled: bool = True,
                              management_method: str = None, inventory_admin: str = None,
                              warehouse_type: str = None):
        # 点击New按钮
        expect(self.new_button).to_be_enabled(timeout=10000)
        self.new_button.click()

        # 等待页面跳转到创建页面
        self.page.wait_for_load_state('networkidle', timeout=10000)

        # 等待表单加载
        expect(self.room_number_input).to_be_visible(timeout=10000)
        expect(self.room_input).to_be_visible(timeout=10000)

        # 填写基本信息
        self.room_number_input.fill(room_number)
        self.room_input.fill(room)
        self.park_input.fill(park)
        self.building_input.fill(building)
        self.floor_input.fill(floor)

        # 选择实验室安全等级
        if lab_safety_level:
            self.ant_select.select_option(self.lab_safety_level_select, lab_safety_level)

        # 选择GXP类型
        if gxp_type:
            self.ant_select.select_option(self.gxp_type_select, gxp_type)

        # 填写功能简介
        if function_profile:
            self.function_profile_input.fill(function_profile)

        # 上传房间图片
        if image_path:
            self.room_image_upload.set_input_files(image_path)

        # 设置库存设置开关
        current_state = self.inventory_settings_switch.get_attribute('aria-checked') == 'true'
        if current_state != inventory_enabled:
            self.inventory_settings_switch.click()

        # 如果启用库存设置，填写相关信息
        if inventory_enabled:
            if management_method:
                self.ant_select.select_option(self.management_method_select, management_method)

            if management_method == "Administrator Management" and inventory_admin:
                self.ant_select.select_option(self.inventory_admin_select, inventory_admin)

            if warehouse_type:
                self.ant_select.select_option(self.warehouse_type_select, warehouse_type)

        # 提交表单
        expect(self.submit_button).to_be_enabled(timeout=10000)
        self.submit_button.click()
        # 等待提交完成
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def verify_storage_facility_created(self, room_number: str):
        # 等待页面刷新并加载数据
        self.page.wait_for_load_state('networkidle', timeout=10000)
        # 验证第一条数据的房间号是否匹配
        first_row_room_number = self.page.locator('.ant-table-row:first-child >> text=' + room_number)
        expect(first_row_room_number).to_be_visible(timeout=10000)
        assert first_row_room_number.text_content() == room_number

    def search_by_room_number(self, room_number: str):
        # 等待搜索框和按钮可见
        expect(self.search_input).to_be_visible(timeout=10000)
        expect(self.search_button).to_be_visible(timeout=10000)

        # 填写搜索关键字
        self.search_input.fill(room_number)

        # 点击搜索按钮
        self.search_button.click()

    def verify_search_result(self, room_number: str):
        # 等待搜索结果加载
        self.page.wait_for_load_state('networkidle', timeout=10000)

        # 验证搜索结果
        search_result = self.page.locator(f'.ant-table-row >> text={room_number}')
        expect(search_result).to_be_visible(timeout=10000)