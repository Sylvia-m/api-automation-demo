"""
BaseApi：所有接口客户端的父类

这一层的职责：把「怎么发请求」的通用细节收拢到一处 ——
- base_url 怎么拼
- 超时设多少
- 用 Session 复用连接（几十条用例跑下来比每次 requests.get 快不少）
- 统一的 get/post 入口，以后要加日志、重试、鉴权头，改这里一个文件就行

Python 知识点（本课重点）：
- class 定义类，类是"模板"，对象是按模板造出来的实例
- __init__ 是构造方法：PostApi(base_url) 这一行会自动调用它
- self 指"当前这个对象自己"，对象的数据都挂在 self.xxx 上
"""

import requests


class BaseApi:

    def __init__(self, base_url, timeout=5):
        # self.xxx = ... 表示"把这个数据存到对象身上"，对象存活期间随时可取
        self.base_url = base_url.rstrip("/")   # 去掉末尾多余的 /，防止拼出 //posts
        self.timeout = timeout
        # Session 会复用底层 TCP 连接：同一服务器的多次请求更快
        self.session = requests.Session()

    def get(self, path, **kwargs):
        """统一的 GET 入口。**kwargs 把额外参数（如 params=）原样转交给 requests"""
        return self.session.get(self.base_url + path, timeout=self.timeout, **kwargs)

    def post(self, path, **kwargs):
        """统一的 POST 入口"""
        return self.session.post(self.base_url + path, timeout=self.timeout, **kwargs)
