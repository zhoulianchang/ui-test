from playwright.sync_api import Page, expect

class EquipmentPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_button = page.locator('button:has-text("New")')
        self.asset_id_input = page.locator('#asset_number')
        self.equipment_name_input = page.locator('#name')
        self.type_select = page.locator('#first_asset_category_id')
        self.brand_select = page.locator('#asset_brand_id')
        self.model_select = page.locator('#asset_brand_model_id')
        self.status_select = page.locator('#status')
        self.owner_select = page.locator('#user_id')
        self.department_select = page.locator('#department_id')
        self.serial_number_input = page.locator('#factory_number')
        self.location_select = page.locator('#location_id')
        self.purchase_date_input = page.locator('#purchase_date')
        self.in_service_date_input = page.locator('#scrap_start_date')
        self.comments_input = page.locator('#remark')
        self.image_upload = page.locator('.ant-upload[role="button"]')
        self.submit_button = page.locator('.ant-btn.ant-btn-primary')
        self.search_input = page.locator('.ant-input-group-wrapper .ant-input[placeholder="Keyword"]')
        self.search_button = page.locator('.ant-input-group-wrapper .ant-btn-icon-only')

    def navigate(self, request):
        self.page.goto(request.config.domain + '/equipment/equipment/equipmentList')
        # 等待页面加载完成
        expect(self.new_button).to_be_visible(timeout=10000)

    def create_equipment(self, asset_id: str, equipment_name: str, equipment_type: str, brand: str, model: str, status: str, 
                         owner: str, department: str, serial_number: str, location: str, 
                         purchase_date: str, in_service_date: str, comments: str, image_path: str = None):
        # 点击New按钮
        expect(self.new_button).to_be_enabled(timeout=10000)
        self.new_button.click()

        # 等待页面跳转到创建设备页面
        self.page.wait_for_load_state('networkidle', timeout=10000)

        # 等待表单加载
        expect(self.asset_id_input).to_be_visible(timeout=10000)
        expect(self.equipment_name_input).to_be_visible(timeout=10000)
        expect(self.type_select).to_be_visible(timeout=10000)
        expect(self.location_select).to_be_visible(timeout=10000)

        # 填写表单
        self.asset_id_input.fill(asset_id)
        self.equipment_name_input.fill(equipment_name)

        # 选择品牌
        expect(self.brand_select).to_be_visible(timeout=10000)
        self.brand_select.click()
        self.page.wait_for_timeout(1000)  # 等待动画完成
        brand_option = self.page.locator(f'.ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option:has-text("{brand}")')
        expect(brand_option).to_be_visible(timeout=10000)
        brand_option.click()
        self.page.wait_for_timeout(2000)  # 等待动画完成
        # 选择型号
        expect(self.model_select).to_be_visible(timeout=10000)
        self.model_select.click()
        self.page.wait_for_timeout(1000)  # 等待动画完成
        self.page.locator('.ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option').first.click()

        # 选择设备状态
        expect(self.status_select).to_be_visible(timeout=10000)
        self.status_select.click()
        status_option = self.page.locator(f'.ant-select-item-option:has-text("{status}")')
        expect(status_option).to_be_visible(timeout=10000)
        status_option.click()

        # 选择负责人
        expect(self.owner_select).to_be_visible(timeout=10000)
        self.owner_select.click()
        # 等待下拉列表完全展开
        self.page.wait_for_selector('.ant-select-dropdown:not(.ant-select-dropdown-hidden)', state='visible', timeout=10000)
        self.page.wait_for_timeout(2000)  # 增加等待时间，确保选项完全加载
        # 选择指定的负责人
        owner_option = self.page.locator(f'.ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option:has-text("{owner}")')
        # 使用键盘上键滚动查找目标选项
        max_attempts = 10  # 最大尝试次数
        attempt = 0
        while attempt < max_attempts:
            if owner_option.is_visible():
                break
            self.page.keyboard.press('ArrowUp')
            self.page.wait_for_timeout(500)  # 等待滚动动画
            attempt += 1
        expect(owner_option).to_be_visible(timeout=10000)
        owner_option.click()


        # 选择部门
        if department:
            print(f"开始选择部门: {department}")
            expect(self.department_select).to_be_visible(timeout=10000)
            self.department_select.click()
            self.page.wait_for_timeout(1000)  # 等待动画完成
            # 等待下拉框完全展开
            self.page.wait_for_selector('.ant-cascader-menu', state='visible', timeout=10000)
            self.page.wait_for_timeout(1000)  # 等待动画完成
        
            # 分割部门路径并选择
            department_levels = department.split('/')
            print(f"部门层级: {department_levels}")
            for level in department_levels:
                print(f"正在选择部门层级: {level}")
                department_option = self.page.locator(f'.ant-cascader-menu >> text={level}').first
                is_visible = department_option.is_visible()
                print(f"部门选项 {level} 是否可见: {is_visible}")
                expect(department_option).to_be_visible(timeout=10000)
                department_option.click()
                print(f"已点击部门选项: {level}")
                self.page.wait_for_timeout(1000)  # 等待动画完成
            print("部门选择完成")


        # 选择设备类型
        self.type_select.click()
        # 等待下拉框完全展开
        self.page.wait_for_selector('.ant-cascader-menu', state='visible', timeout=10000)
        self.page.wait_for_timeout(1000)  # 等待动画完成

        # 等待并点击第一级 Analytical
        analytical_option = self.page.locator('.ant-cascader-menu >> text=Analytical').first
        expect(analytical_option).to_be_visible(timeout=10000)
        analytical_option.click()
        self.page.wait_for_timeout(1000)  # 等待动画完成

        # 等待并点击第二级 Chromatography
        chromatography_option = self.page.locator('.ant-cascader-menu >> text=Chromatography').first
        expect(chromatography_option).to_be_visible(timeout=10000)
        chromatography_option.click()
        self.page.wait_for_timeout(1000)  # 等待动画完成

        # 等待并点击第三级选项
        equipment_type_option = self.page.locator(f'.ant-cascader-menu >> text={equipment_type}').first
        expect(equipment_type_option).to_be_visible(timeout=10000)
        equipment_type_option.click()
        self.page.wait_for_timeout(1000)  # 等待动画完成
        
        # 填写序列号
        self.serial_number_input.fill(serial_number)

        # 选择位置
        expect(self.location_select).to_be_visible(timeout=10000)
        self.location_select.click()
        # 等待下拉列表完全展开
        self.page.wait_for_selector('.ant-select-dropdown:not(.ant-select-dropdown-hidden)', state='visible', timeout=10000)
        self.page.wait_for_timeout(2000)  # 增加等待时间，确保选项完全加载
        location_option = self.page.locator(f'.ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option:has-text("{location}")')
        expect(location_option).to_be_visible(timeout=10000)
        location_option.click()

        # 选择购买日期
        expect(self.purchase_date_input).to_be_visible(timeout=10000)
        self.purchase_date_input.click()
        # 等待日期选择面板显示并定位当前激活的面板中的today按钮
        today_button = self.page.locator('.ant-picker-dropdown:not(.ant-picker-dropdown-hidden) .ant-picker-today-btn')
        expect(today_button).to_be_visible(timeout=10000)
        today_button.click()
        self.page.wait_for_timeout(1000)  # 等待日期选择完成

        # 选择服务日期
        expect(self.in_service_date_input).to_be_visible(timeout=10000)
        self.in_service_date_input.click()
        # 等待日期选择面板显示并定位当前激活的面板中的today按钮
        today_button = self.page.locator('.ant-picker-dropdown:not(.ant-picker-dropdown-hidden) .ant-picker-today-btn')
        expect(today_button).to_be_visible(timeout=10000)
        today_button.click()
        self.page.wait_for_timeout(1000)  # 等待日期选择完成

        # 填写备注
        self.comments_input.fill(comments)

        # 上传图片
        if image_path:
            self.image_upload.set_input_files(image_path)

        # 提交表单
        expect(self.submit_button).to_be_enabled(timeout=10000)
        self.submit_button.click()
        # 等待提交完成
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def verify_equipment_created(self, asset_id: str):

        # 等待页面刷新并加载数据
        self.page.wait_for_load_state('networkidle', timeout=10000)
        # 验证第一条数据的Asset ID是否匹配
        first_row_asset_id = self.page.locator('.ant-table-row:first-child >> text=' + asset_id)
        expect(first_row_asset_id).to_be_visible(timeout=10000)
        assert first_row_asset_id.text_content() == asset_id

    def verify_search_result(self, asset_id: str):
        # 等待搜索结果加载
        self.page.wait_for_load_state('networkidle', timeout=10000)

        # 验证搜索结果
        search_result = self.page.locator(f'.ant-table-row >> text={asset_id}')
        expect(search_result).to_be_visible(timeout=10000)

    def search_by_asset_id(self, asset_id: str):
        # 等待搜索框和按钮可见
        expect(self.search_input).to_be_visible(timeout=10000)
        expect(self.search_button).to_be_visible(timeout=10000)

        # 填写搜索关键字
        self.search_input.fill(asset_id)

        # 点击搜索按钮
        self.search_button.click()

    def delete_equipment_by_asset_id(self, asset_id: str):
        # 先搜索指定的设备
        self.search_by_asset_id(asset_id)

        # 等待搜索结果加载并验证
        self.verify_search_result(asset_id)

        # 找到对应行的Delete按钮并点击
        delete_button = self.page.locator(f'.ant-table-row:has-text("{asset_id}") >> button:has-text("Delete")')
        expect(delete_button).to_be_visible(timeout=10000)
        delete_button.click()

        # 等待确认弹窗出现并点击OK按钮
        ok_button = self.page.locator('.ant-modal-content .ant-btn-primary')
        expect(ok_button).to_be_visible(timeout=10000)
        ok_button.click()

        # 等待删除操作完成
        self.page.wait_for_load_state('networkidle', timeout=10000)

        # 验证删除成功提示
        success_message = self.page.locator('.ant-message-notice-content:has-text("Deleted Successfully")')
        expect(success_message).to_be_visible(timeout=10000)