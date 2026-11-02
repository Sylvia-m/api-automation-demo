"""
本地 mock 服务器（127.0.0.1:5001）的接口自动化测试

被测对象由 conftest.py 里的 base_url fixture 提供：
- 测试函数把 base_url 写进参数表，pytest 自动注入
- 服务器在跑测试前自动启动、跑完后自动关闭

pytest 约定：
- 文件名必须以 test_ 开头，pytest 才会自动发现它
- 每个以 test_ 开头的函数就是一条测试用例
- 用 Python 自带的 assert 语句做断言
"""
from wsgiref.validate import assert_

import requests


def test_get_single_post(base_url):
    """用例 1：查询单篇文章 —— 最基本的 GET 接口测试"""
    resp = requests.get(f"{base_url}/posts/1", timeout=5)

    assert resp.status_code == 200                     # 状态码应该是 200（成功）
    data = resp.json()                                 # 把响应体解析成 Python 字典
    assert data["id"] == 1                             # id 字段应该是 1
    assert "title" in data                             # 应该包含 title 字段
    assert isinstance(data["title"], str)              # title 应该是字符串类型
    assert data["title"] != ""
    assert data["body"] != ""                          # title 不应该是空的


def test_get_all_posts(base_url):
    """用例 2：查询文章列表 —— 验证返回数量和结构"""
    resp = requests.get(f"{base_url}/posts", timeout=5)

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)          # 返回的应该是一个列表
    assert len(data) == 100                # mock 服务器固定有 100 篇文章
    # 验证第一项的字段结构是否完整
    assert set(data[0].keys()) == {"userId", "id", "title", "body"}


def test_create_post(base_url):
    """用例 3：创建文章 —— 最基本的 POST 接口测试"""
    payload = {
        "title": "我的第一篇自动化测试文章",
        "body": "这是用 requests + pytest 自动创建的",
        "userId": 1,
    }
    # POST 请求，json= 参数会自动把字典序列化成 JSON 并加上 Content-Type 头
    resp = requests.post(f"{base_url}/posts", json=payload, timeout=5)

    assert resp.status_code == 201                     # 创建成功，状态码应该是 201
    data = resp.json()
    assert data["id"] == 101                           # 服务器应该分配新 id=101
    assert data["title"] == payload["title"]           # 服务器应该原样返回我们传的字段
    assert data["body"] == payload["body"]


def test_post_not_found(base_url):
    """用例 4：异常场景 —— 查询不存在的资源，应该返回 404

    好的接口自动化不止测正常流程，异常流程同样重要。
    """
    resp = requests.get(f"{base_url}/posts/999999", timeout=5)

    assert resp.status_code == 404


def test_get_users_with_params(base_url):
    """用例 5：带查询参数的请求 —— GET /users?username=Bret"""
    resp = requests.get(
        f"{base_url}/users",
        params={"username": "Bret"},   # params= 会自动拼成 ?username=Bret
        timeout=5,
    )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1                  # 应该只匹配到 1 个用户
    assert data[0]["username"] == "Bret"

def test_get_post_2(base_url):

    resp = requests.get(f"{base_url}/posts/2", timeout=5)
    data = resp.json()
    assert data["id"] == 2