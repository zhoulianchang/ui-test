import pytest
from playwright.sync_api import Page, expect
from pages.common.login_page import LoginPage
from pages.equipment.reservation_page import ReservationPage
from pages.utils.login_utils import login_with_request

def test_equipment_reservation(page: Page, request):
    """测试设备预约流程：登录 -> 跳转到预约页面 -> 搜索设备 -> 预约"""
    # 步骤1：登录系统
    print("步骤1：登录系统")
    login_with_request(page, request)
    
    # 步骤2：跳转到预约设备页面
    print("步骤2：跳转到预约设备页面")
    reservation_page = ReservationPage(page)
    reservation_page.navigate(request)
    
    # 步骤3：输入设备ID并搜索
    asset_id = "01001"  # 使用您提供的第二行资产ID
    print(f"步骤3：搜索资产ID {asset_id}")
    reservation_page.search_by_asset_id(asset_id)
    
    # 步骤4：预约指定资产ID的设备（更精确的定位方式）
    print(f"步骤4：预约资产ID {asset_id} 的设备")
    reservation_page.reserve_equipment_by_asset_id(asset_id)
    
    # 步骤5：选择预约日期和时间
    print("步骤5：选择预约日期和时间")
    reservation_page.select_next_available_date()
    reservation_page.select_time_slot("00:00:00")  # 选择凌晨时间段
    # 计算次日的预约时间
    from datetime import datetime, timedelta
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.strftime("%Y-%m-%d") + " 10:00"
    end_time = tomorrow.strftime("%Y-%m-%d") + " 11:30"
    reservation_page.set_reservation_time(start_time, end_time)
   
    # 步骤6：验证预约成功
    print("步骤6：验证预约成功")
    reservation_page.verify_reservation_success()
    print("测试完成")