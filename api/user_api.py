"""
UserApi：用户相关接口的客户端
"""

from api.base_api import BaseApi


class UserApi(BaseApi):

    def list_users(self, username=None):
        """获取用户列表；传 username 则按用户名过滤

        username=None 是"默认参数"：调用时不传就用 None。
        None 表示"没有这个参数"，此时不给 requests 传 params，查全量。
        """
        params = {"username": username} if username else None
        return self.get("/users", params=params)
