from playwright.sync_api import Page, expect

class ReservationPage:
    def __init__(self, page: Page):
        self.page = page
        self.asset_id_input = page.locator('input[placeholder="Please search for the Asset ID and Equipment Name"]')
        self.search_button = page.locator('button.ant-btn.ant-btn-default.ant-btn-icon-only.ant-input-search-button')
        

    def navigate(self, request):
        """导航到设备预约页面"""
        self.page.goto(request.config.domain + '/equipment/reservations/makeReservations')
        # 等待页面加载完成
        expect(self.asset_id_input).to_be_visible(timeout=10000)
        expect(self.search_button).to_be_visible(timeout=10000)

    def search_by_asset_id(self, asset_id: str):
        """通过资产ID搜索设备"""
        # 确保输入框可见并可编辑
        expect(self.asset_id_input).to_be_visible(timeout=10000)
        expect(self.asset_id_input).to_be_editable(timeout=10000)

        # 清空输入框并填入资产ID
        self.asset_id_input.clear()
        self.asset_id_input.fill(asset_id)

        # 点击搜索按钮
        expect(self.search_button).to_be_enabled(timeout=10000)
        self.search_button.click()

        # 等待搜索结果加载
        self.page.wait_for_load_state('networkidle', timeout=10000)
        
        # 等待表格体加载完成
        table_body = self.page.locator('.ant-table-tbody')
        expect(table_body).to_be_visible(timeout=10000)

    def reserve_equipment_by_asset_id(self, asset_id: str):
        """通过资产ID预约特定设备"""
        # 等待表格加载
        table_body = self.page.locator('.ant-table-tbody')
        expect(table_body).to_be_visible(timeout=10000)
        
        # 使用XPath直接定位包含特定asset_id的行
        row_locator = self.page.locator(f'//tr[contains(., "{asset_id}")]')
        
        # 检查是否找到行
        if row_locator.count() == 0:
            raise Exception(f"没有找到包含资产ID {asset_id} 的行")
        
        # 如果找到多行，选择第一行
        target_row = row_locator.first
        print(f"找到包含资产ID {asset_id} 的行: {target_row.inner_html()}")
        
        # 在该行中找到最后一列，通常包含操作按钮
        last_cell = target_row.locator('td:last-child')
        
        if last_cell.count() == 0:
            raise Exception(f"行中没有找到单元格")
        
        print(f"最后一列内容: {last_cell.inner_html()}")
        
        # 在最后一列中寻找Reserve按钮或链接
        reserve_button = None
        
        # 尝试不同的定位方式
        selectors = [
            'a:has-text("Reserve")',
            'button:has-text("Reserve")',
            '.ant-btn:has-text("Reserve")',
            ':text("Reserve")'
        ]
        
        for selector in selectors:
            elements = last_cell.locator(selector).all()
            if len(elements) > 0:
                reserve_button = elements[0]
                print(f"使用选择器 '{selector}' 找到Reserve按钮")
                break
        
        # 如果没有在最后一列找到，尝试在整行中查找
        if reserve_button is None:
            for selector in selectors:
                elements = target_row.locator(selector).all()
                if len(elements) > 0:
                    reserve_button = elements[0]
                    print(f"在整行中使用选择器 '{selector}' 找到Reserve按钮")
                    break
        
        # 如果仍然没找到，尝试直接使用XPath
        if reserve_button is None:
            try:
                # 直接在页面级别使用XPath查找
                xpath_selector = f'//tr[contains(., "{asset_id}")]//a[contains(., "Reserve")] | //tr[contains(., "{asset_id}")]//button[contains(., "Reserve")]'
                reserve_elements = self.page.locator(xpath_selector).all()
                if len(reserve_elements) > 0:
                    reserve_button = reserve_elements[0]
                    print("使用XPath找到Reserve按钮")
            except Exception as e:
                print(f"XPath定位失败: {e}")
        
        # 最后的尝试：直接点击文本为"Reserve"的元素
        if reserve_button is None:
            # 打印整行HTML用于调试
            print(f"无法找到Reserve按钮，行HTML: {target_row.inner_html()}")
            # 尝试截图
            try:
                target_row.screenshot(path=f"row_{asset_id}.png")
                print(f"已保存行截图到 row_{asset_id}.png")
            except Exception as e:
                print(f"截图失败: {e}")
                
            # 尝试直接点击文本
            try:
                self.page.click(f'text=Reserve', timeout=5000)
                print("通过直接文本点击Reserve")
                # 等待操作完成
                self.page.wait_for_load_state('networkidle', timeout=10000)
                return
            except Exception as e:
                print(f"直接文本点击失败: {e}")
                raise Exception(f"未能找到或点击资产ID为 {asset_id} 对应的Reserve按钮")
        
        # 如果找到了按钮，点击它
        print("点击Reserve按钮")
        reserve_button.click()
        
        # 等待预约操作完成
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def reserve_first_equipment(self):
        """预约搜索结果中的第一个设备"""
        # 等待表格加载
        table_body = self.page.locator('.ant-table-tbody')
        expect(table_body).to_be_visible(timeout=10000)
        
        # 获取第一行
        rows = self.page.locator('.ant-table-tbody tr').all()
        if len(rows) == 0:
            raise Exception("表格中没有找到任何行")
            
        first_row = rows[0]
        
        # 在第一行中找到最后一列，通常包含操作按钮
        last_cell = first_row.locator('td:last-child')
        
        if last_cell.count() == 0:
            raise Exception("行中没有找到单元格")
        
        # 在最后一列中寻找Reserve按钮或链接
        reserve_button = None
        
        # 尝试不同的定位方式
        selectors = [
            'a:has-text("Reserve")',
            'button:has-text("Reserve")',
            '.ant-btn:has-text("Reserve")',
            ':text("Reserve")'
        ]
        
        for selector in selectors:
            elements = last_cell.locator(selector).all()
            if len(elements) > 0:
                reserve_button = elements[0]
                break
        
        # 如果没有在最后一列找到，尝试在整行中查找
        if reserve_button is None:
            for selector in selectors:
                elements = first_row.locator(selector).all()
                if len(elements) > 0:
                    reserve_button = elements[0]
                    break
        
        # 如果仍然没找到，抛出异常
        if reserve_button is None:
            # 打印整行HTML用于调试
            print(f"无法找到Reserve按钮，行HTML: {first_row.inner_html()}")
            
            # 尝试直接点击文本
            try:
                self.page.click('text=Reserve', timeout=5000)
                print("通过直接文本点击Reserve")
            except Exception as e:
                print(f"直接文本点击失败: {e}")
                raise Exception("未能找到或点击第一行的Reserve按钮")
        else:
            # 如果找到了按钮，点击它
            reserve_button.click()
        
        # 等待预约操作完成
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def select_time_slot(self, time_str: str):
        """在日历视图中选择指定的时间段
        Args:
            time_str: 时间字符串，格式为"HH:mm:ss"，例如"00:00:00"
        """
        # 等待时间表格加载完成
        self.page.wait_for_selector('.fc-timegrid-slot', timeout=10000)
        self.page.wait_for_timeout(1000)  # 等待时间表格完全渲染
        
        # 构建选择器，定位具有特定data-time属性的td元素，只匹配具有fc-timegrid-slot和fc-timegrid-slot-lane两个class的元素
        time_slot = self.page.locator(f'td.fc-timegrid-slot.fc-timegrid-slot-lane[data-time="{time_str}"]')
        
        # 确保时间槽元素可见且可交互
        expect(time_slot).to_be_visible(timeout=10000)
        expect(time_slot).to_be_enabled(timeout=10000)
        self.page.wait_for_timeout(500)  # 等待元素稳定
        
        # 点击时间槽
        time_slot.click()
        
        # 等待可能出现的弹窗或其他UI响应
        self.page.wait_for_load_state('networkidle', timeout=10000)
        self.page.wait_for_timeout(1000)  # 等待弹窗完全显示

    def verify_reservation_success(self):
        """验证预约是否成功"""
        # 检查是否有成功提示信息
        reservation_success_message = self.page.locator('.ant-message-notice-content')
        expect(reservation_success_message).to_be_visible(timeout=10000)
        success_message = reservation_success_message.text_content()
        assert success_message == "Operate Successfully"
        
        return success_message

    def select_next_available_date(self):
        """选择预约日期，选择今天之后的第一个可用日期"""
        # 等待日历加载完成
        calendar = self.page.locator('.fc')
        expect(calendar).to_be_visible(timeout=10000)
        self.page.wait_for_timeout(1000)  # 等待日历完全渲染

        # 找到今天的日期元素
        today = self.page.locator('.fc-day-today')
        expect(today).to_be_visible(timeout=10000)
        self.page.wait_for_timeout(500)  # 等待日期元素稳定

        # 找到今天之后的第一个可用日期的顶部区域
        next_available_date_top = self.page.locator('.fc-day-today + .fc-day-future .fc-daygrid-day-top').first
        expect(next_available_date_top).to_be_visible(timeout=10000)
        expect(next_available_date_top).to_be_enabled(timeout=10000)  # 确保元素可交互

        # 点击日期顶部区域
        next_available_date_top.click()
        
        # 等待日期选择完成
        self.page.wait_for_load_state('networkidle', timeout=10000)
        self.page.wait_for_timeout(1000)  # 等待UI更新完成

    def set_reservation_time(self, start_datetime: str, end_datetime: str):
        """设置预约的开始时间和结束时间
        Args:
            start_datetime: 开始时间字符串，格式为"YYYY-MM-DD HH:mm"，例如"2025-04-11 01:30"
            end_datetime: 结束时间字符串，格式为"YYYY-MM-DD HH:mm"，例如"2025-04-11 02:30"
        """
        def set_datetime_in_picker(input_locator: str, datetime_str: str):
            """在日期时间选择器中设置日期和时间
            Args:
                input_locator: 输入框的定位器
                datetime_str: 日期时间字符串
            """
            # 点击输入框打开选择器
            input_element = self.page.locator(input_locator)
            expect(input_element).to_be_visible(timeout=10000)
            input_element.click()
            self.page.wait_for_timeout(500)  # 等待选择器打开

            # 等待并获取当前激活的选择器面板
            picker = self.page.locator('.ant-picker-dropdown:not(.ant-picker-dropdown-hidden)').first
            expect(picker).to_be_visible(timeout=10000)

            # 解析日期时间
            date_str, time_str = datetime_str.split(' ')
            year, month, day = map(int, date_str.split('-'))
            hour, minute = map(int, time_str.split(':'))

            # 设置年份
            header = picker.locator('.ant-picker-date-panel .ant-picker-header-view')
            expect(header).to_be_visible(timeout=10000)
            header.click()
            self.page.wait_for_timeout(500)

            year_panel = picker.locator('.ant-picker-year-panel')
            expect(year_panel).to_be_visible(timeout=10000)
            year_cell = year_panel.locator(f'td[title="{year}"]')
            expect(year_cell).to_be_visible(timeout=10000)
            year_cell.click()
            self.page.wait_for_timeout(500)
            
            # 设置月份
            month_btn = picker.locator('.ant-picker-month-btn')
            month_btn.click()
            self.page.wait_for_timeout(500)
            month_panel = picker.locator('.ant-picker-month-panel')
            expect(month_panel).to_be_visible(timeout=10000)
            month_cell = month_panel.locator(f'td[title="{year}-{month:02d}"]')
            expect(month_cell).to_be_visible(timeout=10000)
            month_cell.click()
            self.page.wait_for_timeout(500)

            # 设置日期
            date_panel = picker.locator('.ant-picker-date-panel')
            expect(date_panel).to_be_visible(timeout=10000)
            date_cell = date_panel.locator(f'td[title="{year}-{month:02d}-{day:02d}"]')
            expect(date_cell).to_be_visible(timeout=10000)
            date_cell.click()
            self.page.wait_for_timeout(500)

            # 设置时间
            time_panel = picker.locator('.ant-picker-time-panel')
            expect(time_panel).to_be_visible(timeout=10000)

            # 设置小时
            hour_column = time_panel.locator('.ant-picker-time-panel-column').first
            expect(hour_column).to_be_visible(timeout=10000)
            hour_cell = hour_column.locator(f'.ant-picker-time-panel-cell-inner:text-is("{hour:02d}")')
            expect(hour_cell).to_be_visible(timeout=10000)
            hour_cell.click()
            self.page.wait_for_timeout(500)

            # 设置分钟
            minute_column = time_panel.locator('.ant-picker-time-panel-column').nth(1)
            expect(minute_column).to_be_visible(timeout=10000)
            minute_cell = minute_column.locator(f'.ant-picker-time-panel-cell-inner:text-is("{minute:02d}")')
            expect(minute_cell).to_be_visible(timeout=10000)
            minute_cell.click()
            self.page.wait_for_timeout(500)

            # 点击确定
            ok_button = picker.locator('.ant-picker-ok button')
            expect(ok_button).to_be_visible(timeout=10000)
            ok_button.click()
            self.page.wait_for_timeout(500)

        # 等待预约弹窗加载完成
        modal = self.page.locator('.ant-modal-content')
        expect(modal).to_be_visible(timeout=10000)

        # 设置开始时间
        set_datetime_in_picker('#leaseStartTime', start_datetime)

        # 设置结束时间
        set_datetime_in_picker('#leaseEndTime', end_datetime)
        # 使用更精确的选择器定位确认按钮
        confirm_button = modal.locator('.ant-modal-footer button.ant-btn.ant-btn-primary')
        expect(confirm_button).to_be_visible(timeout=10000)
        confirm_button.click()
        # 等待时间设置完成
        self.page.wait_for_load_state('networkidle', timeout=10000)