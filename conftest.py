"""
conftest.py —— pytest 的共享配置文件（文件名固定，pytest 自动识别）

本课重点：fixture（测试夹具）
- @pytest.fixture 装饰的函数 = 一件"可借用的装备"
- 测试函数把这个 fixture 的名字写成参数，pytest 就会自动把装备递进来
- scope="session" 表示整个测试会话只启动一次服务器，所有用例共用
- yield 之前的代码 = 测试前的准备工作（启动服务器）
- yield 之后的代码 = 测试后的清理工作（关闭服务器）
"""

import threading

import pytest
from werkzeug.serving import make_server

from api.post_api import PostApi
from api.user_api import UserApi
from mock_server import app


@pytest.fixture(scope="session")
def base_url():
    """启动本地 mock 服务器，返回它的地址，测试结束后自动关闭"""
    # make_server: 把 Flask 应用绑到 127.0.0.1:5001 上
    server = make_server("127.0.0.1", 5001, app)
    # 服务器要在后台线程里跑，不然会卡住测试
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield "http://127.0.0.1:5001"   # <-- 所有用例在这里"借"到服务器地址

    server.shutdown()               # 测试全部跑完后执行，优雅关闭服务器


@pytest.fixture(scope="session")
def post_api(base_url):
    """文章接口客户端：造一个对象，全程共用一个"""
    return PostApi(base_url)


@pytest.fixture(scope="session")
def user_api(base_url):
    """用户接口客户端"""
    return UserApi(base_url)
