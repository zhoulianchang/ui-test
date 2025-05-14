import pytest
from playwright.sync_api import Page, expect
from pages.common.login_page import LoginPage
from pages.inventory.storage_facility_page import StorageFacilityPage
from pages.utils.login_utils import login_with_request

def test_create_storage_facility(page: Page, request):
    """测试库房设施创建流程：登录 -> 跳转到库房设施页面 -> 创建库房 -> 验证创建成功"""
    # 步骤1：登录系统
    print("步骤1：登录系统")
    login_with_request(page, request)
    
    # 步骤2：跳转到库房设施页面
    print("步骤2：跳转到库房设施页面")
    storage_facility_page = StorageFacilityPage(page)
    storage_facility_page.navigate(request)
    
    # 步骤3：创建新的库房设施
    print("步骤3：创建新的库房设施")
    storage_facility_page.create_storage_facility(
        room_number="TEST001",
        room="测试房间",
        park="测试园区",
        building="测试大楼",
        floor="1",
        lab_safety_level="None",
        gxp_type="None",
        function_profile="测试用库房",
        inventory_enabled=True,
        management_method="Administrator Management",
        inventory_admin="Jack",
        warehouse_type="Warehouse"
    )
    
    # 步骤4：验证库房创建成功
    print("步骤4：验证库房创建成功")
    storage_facility_page.verify_storage_facility_created(room_number)
    
    # 步骤5：搜索并验证创建的库房
    print("步骤5：搜索并验证创建的库房")
    storage_facility_page.search_by_room_number(room_number)
    storage_facility_page.verify_search_result(room_number)
    
    print("测试完成")