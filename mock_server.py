"""
本地 mock 服务器：模仿 JSONPlaceholder 的行为

为什么需要它？
- 外网练习 API（jsonplaceholder.typicode.com）在国内访问不稳定，经常超时
- 接口自动化的最佳实践：测试跑在稳定、可控的环境里，不打真实外网
- 数据存在内存里，每次启动都是干净的，测试之间互不干扰

跑测试时不用手动启动它 —— conftest.py 里的 fixture 会自动把它拉起来。
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------- 准备假数据（模仿 JSONPlaceholder 的数据规则） ----------

# 100 篇文章，id 从 1 到 100
POSTS = {
    i: {
        "userId": (i - 1) // 10 + 1,
        "id": i,
        "title": f"title {i}",
        "body": f"body of post {i}",
    }
    for i in range(1, 101)
}

# 用户列表，模仿真实返回的字段结构
USERS = [
    {"id": 1, "name": "Leanne Graham", "username": "Bret", "email": "bret@april.biz"},
    {"id": 2, "name": "Ervin Howell", "username": "Antonette", "email": "ervin@melissa.tv"},
]

# ---------- 接口定义 ----------


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    """获取单篇文章，不存在返回 404"""
    post = POSTS.get(post_id)
    if post is None:
        return jsonify({"message": "Not Found"}), 404
    return jsonify(post)


@app.get("/posts")
def list_posts():
    """获取全部文章列表"""
    return jsonify(list(POSTS.values()))


@app.post("/posts")
def create_post():
    """创建文章：返回 201，并分配新 id=101"""
    data = request.get_json()
    new_post = {**data, "id": 101}   # **data 是字典解包：把 data 的键值对摊进来
    return jsonify(new_post), 201


@app.get("/users")
def list_users():
    """获取用户列表，支持 ?username=xxx 过滤"""
    username = request.args.get("username")
    if username:
        result = [u for u in USERS if u["username"] == username]
    else:
        result = USERS
    return jsonify(result)
