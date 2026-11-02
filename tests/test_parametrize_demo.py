"""
参数化测试 demo：@pytest.mark.parametrize

核心思想：一份用例逻辑 + 一张数据表 = N 条独立用例
- 数据表里的每一行，pytest 都会单独跑一次
- 任何一行失败，只影响那一条，其他照常执行
- 报告里能清楚看出是哪一行数据挂了

Python 知识点：@ 开头的东西叫「装饰器」
它不改动函数本身的代码，而是给函数"附加"一层能力。
这里是给测试函数附加"我要按这张表跑多次"的能力。
"""

import pytest
import requests


# ---------------------------------------------------------------
# 场景 1：同一个接口，测多个有效 id
# ---------------------------------------------------------------
@pytest.mark.parametrize("post_id", [1, 2, 50, 100])
def test_get_post_by_id(base_url, post_id):
    """4 个有效 id → pytest 自动跑 4 条用例

    参数说明：
    - "post_id"      : 参数名，必须和函数里的形参同名
    - [1, 2, 50, 100]: 数据列表，每个元素跑一次
    """
    resp = requests.get(f"{base_url}/posts/{post_id}", timeout=5)

    assert resp.status_code == 200
    assert resp.json()["id"] == post_id


# ---------------------------------------------------------------
# 场景 2：异常数据 —— 一次测所有非法 id
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    "post_id",
    [0, -1, 101, 999999],
    ids=["id为0", "id为负数", "id超出范围", "id不存在"],
)
def test_get_post_invalid_id(base_url, post_id):
    """4 种非法 id 都应该返回 404

    ids= 是给每条用例起个可读的名字。
    不加 ids 时，pytest 会用原始数据当名字（比如 test_get_post_invalid_id[-1]），
    中文项目里加上 ids 报告会好读很多。
    """
    resp = requests.get(f"{base_url}/posts/{post_id}", timeout=5)

    assert resp.status_code == 404


# ---------------------------------------------------------------
# 场景 3：多个参数组合 —— 一次传两个参数
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    "post_id, expect_keys",
    [
        (1, {"userId", "id", "title", "body"}),
        (100, {"userId", "id", "title", "body"}),
    ],
    ids=["第一篇", "最后一篇"],
)
def test_post_structure(base_url, post_id, expect_keys):
    """一次传两个参数：数据表里每行是一个元组，按顺序对应参数名

    这种写法在"同一个字段结构，不同数据"时特别顺手。
    """
    resp = requests.get(f"{base_url}/posts/{post_id}", timeout=5)

    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == expect_keys
    assert data["title"] != ""


# ---------------------------------------------------------------
# 场景 4：参数化 POST 请求体 —— 测多种创建场景
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    "payload",
    [
        {"title": "正常标题", "body": "正常内容", "userId": 1},
        {"title": "很长的标题" * 20, "body": "很长的内容" * 50, "userId": 2},
        {"title": "带特殊字符 <>&'\"", "body": "emoji 也要能存", "userId": 3},
    ],
    ids=["普通数据", "超长数据", "特殊字符"],
)
def test_create_post_with_various_payloads(base_url, payload):
    """同一个接口用 3 组不同的请求体测，验证服务器都能正确处理

    payload 是字典，可以直接当参数传；表里每个元素就是一组数据。
    """
    resp = requests.post(f"{base_url}/posts", json=payload, timeout=5)

    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["id"] == 101
