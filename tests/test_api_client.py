"""
使用 API 客户端层的测试用例

对比旧写法，用例里不再出现 URL 拼接、params 组装、timeout 这些细节：
    旧：requests.get(f"{base_url}/users", params={"username": u}, timeout=5)
    新：user_api.list_users(u)

断言仍然写在用例层 —— 「检查什么」是用例的职责，「怎么发请求」是 api 层的职责。
"""

import pytest


# ---------------------------------------------------------------
# 文章接口：通过 post_api 客户端调用
# ---------------------------------------------------------------
def test_get_post_by_id(post_api):
    resp = post_api.get_post(1)

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] != ""


def test_list_posts(post_api):
    resp = post_api.list_posts()

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 100


def test_create_post(post_api):
    payload = {"title": "客户端层的用例", "body": "请求细节都收进 api 层了", "userId": 1}

    resp = post_api.create_post(payload)

    assert resp.status_code == 201
    assert resp.json()["id"] == 101


# ---------------------------------------------------------------
# 用户接口：参数化 + 客户端，两种已学技能组合
# ---------------------------------------------------------------
@pytest.mark.parametrize("username", ["Bret", "Antonette"])
def test_users_found(user_api, username):
    resp = user_api.list_users(username)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["username"] == username


@pytest.mark.parametrize("username", ["ghost_user", "不存在的用户"])
def test_users_not_found(user_api, username):
    resp = user_api.list_users(username)

    assert resp.status_code == 200
    assert resp.json() == []
