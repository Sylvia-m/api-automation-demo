# api-automation-demo

接口自动化测试入门 demo：Python + requests + pytest + Flask mock server。

测试跑在**本地 mock 服务器**（127.0.0.1:5001）上，不依赖外网，稳定且速度快。
mock 服务器模仿了 [JSONPlaceholder](https://jsonplaceholder.typicode.com) 的行为。

## 项目结构

```
api-automation-demo/
├── api/                     # 接口客户端层（分层设计）
│   ├── base_api.py          # BaseApi 基类：URL/超时/Session 统一管理
│   ├── post_api.py          # 文章接口客户端：一个接口一个方法
│   └── user_api.py          # 用户接口客户端
├── tests/
│   ├── test_posts_api.py    # 基础用例（直接用 requests 的教学版）
│   ├── test_parametrize_demo.py  # 参数化教学 demo
│   ├── test_paratrize_demo.py    # 参数化练习
│   └── test_api_client.py   # 使用客户端层的推荐写法
├── conftest.py              # base_url / post_api / user_api fixture（自动启停 mock 服务器）
├── mock_server.py           # Flask mock 服务器（内存数据，模仿 JSONPlaceholder）
├── requirements.txt
├── pytest.ini
└── docs/
    └── python-basics-notes.md   # Python 基础速查笔记
```

## 覆盖的测试点

| 用例 | 方法 | 场景 | 验证点 |
|------|------|------|--------|
| test_get_single_post | GET | 查询单篇文章 | 状态码、字段存在性、字段类型 |
| test_get_all_posts | GET | 查询列表 | 返回数量、数据结构 |
| test_create_post | POST | 创建资源 | 201 状态码、服务端回显 |
| test_post_not_found | GET | 异常场景 | 404 状态码 |
| test_get_users_with_params | GET | 带查询参数 | 参数过滤生效 |

## 快速开始

```bash
# 1. 创建并激活虚拟环境（Windows PowerShell）
python -m venv venv
.\venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行全部测试（conftest 会自动启动 mock 服务器，无需手动启动）
pytest

# 4. 只运行某一条用例
pytest tests/test_posts_api.py::test_create_post -v
```

## 架构说明

- **conftest.py 中的 `base_url` fixture**：测试前用 `make_server` 把 Flask 应用启动在后台线程，`yield` 出地址给所有用例共享（`scope="session"` 全程只启动一次），测试结束后 `shutdown` 自动关闭。
- **mock_server.py**：用 Flask 定义了 4 个接口（查单篇、查列表、POST 创建、用户过滤），数据存内存，每次启动都是干净状态。
