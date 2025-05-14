import pytest
from pages.common.login_page import LoginPage
from pages.inventory.locations_page import LocationsPage
from datetime import datetime
import random

def test_create_location(page, request):
    # 生成唯一的location_number
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    location_number = f"LOC{timestamp}"

    # 登录
    login_page = LoginPage(page)
    login_page.navigate(request)
    login_page.login(request)
    login_page.verify_login_success(request)

    # 导航到locations页面并点击new按钮
    locations_page = LocationsPage(page)
    locations_page.navigate(request)
    locations_page.click_new_button()

    # 创建新位置
    locations_page.create_location(
        location_number=location_number,
        room="Room01",
        equipment="zlc",
        layer=str(random.randint(1, 50)),
        grid=str(random.randint(1, 50))
    )
    # 验证位置创建成功
    locations_page.verify_location_created(location_number)
    

def test_edit_location(page, request):
    # 生成唯一的location_number
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    location_number = f"LOC{timestamp}"

    # 登录
    login_page = LoginPage(page)
    login_page.navigate(request)
    login_page.login(request)
    login_page.verify_login_success(request)

    # 导航到locations页面并点击new按钮
    locations_page = LocationsPage(page)
    locations_page.navigate(request)
    locations_page.click_new_button()

    # 创建新位置
    locations_page.create_location(
        location_number=location_number,
        room="Room01",
        equipment="zlc",
        layer=str(random.randint(1, 50)),
        grid=str(random.randint(1, 50))
    )
    # 验证位置创建成功
    locations_page.verify_location_created(location_number)
    # 点击编辑按钮
    locations_page.click_edit_button(location_number)
    # 修改layer值并获取新的值
    new_layer = locations_page.edit_location()
    # 验证修改成功
    locations_page.verify_location_edited(location_number, new_layer)