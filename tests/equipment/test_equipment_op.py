# 导入pytest测试框架
import pytest
from pages.common.login_page import LoginPage
from pages.equipment.equipment_page import EquipmentPage
from pages.utils.login_utils import login_with_request

def test_create_equipment(page, request):
    # 先登录
    login_with_request(page, request)

    # 创建设备
    equipment_page = EquipmentPage(page)
    equipment_page.navigate(request)
    equipment_page.create_equipment(
        asset_id="TEST001",
        equipment_name="测试设备001",
        equipment_type="Gas Chromatograph",
        brand="Altamira Instruments（AMI）",
        model="Others",
        status="Operational",
        owner="赵立鹏",
        department="Test-01/研发部",
        serial_number="SN001",
        location="Room01",
        purchase_date="2024-03-28",
        in_service_date="2024-03-28",
        comments="测试设备创建"
    )
    equipment_page.verify_equipment_created("TEST001")

def test_search_equipment(page, request):
    # 先登录
    login_with_request(page, request)
    # 搜索并验证设备
    equipment_page = EquipmentPage(page)
    equipment_page.navigate(request)
    equipment_page.search_by_asset_id("TEST001")
    equipment_page.verify_search_result("TEST001")

def test_delete_equipment(page, request):
    # 先登录
    login_with_request(page, request)
    # 创建一个测试设备
    equipment_page = EquipmentPage(page)
    equipment_page.navigate(request)
    # 删除设备
    equipment_page.delete_equipment_by_asset_id("TEST001")