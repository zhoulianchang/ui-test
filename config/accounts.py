# 账号配置文件
import pytest

def get_account(request):
    """获取账号信息
    
    从pytest配置中获取账号信息：
    --username: 用户名（必填）
    --password: 密码（必填）
    --company: 公司名（可选，默认为Test-01）
    
    Args:
        request: pytest的request fixture
        
    Returns:
        dict: 包含username、password和company的字典
    """
    config = request.config.option
    
    return {
        "username": config.username,
        "password": config.password,
        "company": config.company
    }