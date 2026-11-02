import pytest
import requests

# mock 服务器里真实存在的用户：Bret、Antonette（注意拼写）


@pytest.mark.parametrize("username", ["Bret", "Antonette"],ids = ["用户1","用户2"])
def test_para_users_found(base_url, username):
    """存在的用户：返回 200 且匹配到唯一一条"""
    resp = requests.get(f"{base_url}/users", params={"username": username}, timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["username"] == username


@pytest.mark.parametrize("username", ["Antonella", "不存在的用户"])
def test_para_users_not_found(base_url, username):
    """不存在的用户：返回 200 但列表为空"""
    resp = requests.get(f"{base_url}/users", params={"username": username}, timeout=10)
    assert resp.status_code == 200
    assert resp.json() == []