"""
PostApi：文章相关接口的客户端

这一层的规矩：**每个接口一个方法，URL 只允许出现在这里**。
- 方法名用业务语言（get_post / create_post），读用例像读需求
- 参数用业务参数（post_id、payload），不再出现 path 拼接细节
- 返回值统一返回 Response 对象，断言交给用例层做

继承自 BaseApi，所以自动拥有 self.get / self.post / self.session。
"""

from api.base_api import BaseApi


class PostApi(BaseApi):

    def get_post(self, post_id):
        """获取单篇文章"""
        return self.get(f"/posts/{post_id}")

    def list_posts(self):
        """获取全部文章列表"""
        return self.get("/posts")

    def create_post(self, payload):
        """创建文章，payload 是 dict"""
        return self.post("/posts", json=payload)
