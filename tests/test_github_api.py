"""
对着 GitHub 真实接口写的测试（真实数据，不是 mock）

被测接口的"说明书"：
- https://api.github.com/users/用户名   → 返回这个用户的公开资料（GET，"看数据"）
- https://api.github.com/users/用户名/repos → 返回这个用户所有的公开仓库列表
- 查一个不存在的用户 → GitHub 返回 404（"没这个人"）

注：公司里真实项目也是这么测的，只是接口地址是公司自己的。
"""

import requests

BASE_URL = "https://api.github.com"


def test_get_real_user():
    """查一个真实存在的用户 octocat（GitHub 的吉祥物账号）"""
    resp = requests.get(f"{BASE_URL}/users/octocat", timeout=15)

    assert resp.status_code == 200                  # 成功
    data = resp.json()
    assert data["login"] == "octocat"               # 用户名必须是 octocat
    assert isinstance(data["followers"], int)       # 粉丝数是数字（今天 24888，明天可能变，所以只验类型不验具体值）
    assert data["followers"] > 0


def test_user_repos_are_real():
    """查 octocat 的仓库列表，验证每个仓库都有名字"""
    resp = requests.get(f"{BASE_URL}/users/octocat/repos", timeout=15)

    assert resp.status_code == 200
    repos = resp.json()                             # 返回的是一个列表
    assert isinstance(repos, list)
    assert len(repos) > 0                           # octocat 有 8 个公开仓库，至少有内容
    for repo in repos[:3]:                          # 抽查前 3 个仓库
        assert "name" in repo                       # 每个仓库都有名字字段


def test_user_not_found():
    """查一个几乎不可能存在的用户名 → 404"""
    resp = requests.get(f"{BASE_URL}/users/zzz-no-such-user-9527xyz", timeout=15)

    assert resp.status_code == 404


def test_search_repositories():
    """搜索接口：在全 GitHub 搜带 pytest 关键字的仓库"""
    resp = requests.get(
        f"{BASE_URL}/search/repositories",
        params={"q": "pytest"},                     # 搜索关键词，拼成 ?q=pytest
        timeout=15,
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["total_count"] > 100                # 全网 pytest 仓库肯定超过 100 个
    assert isinstance(data["items"], list)
