# Python 基础速查笔记（接口自动化版）

> 配套代码：`tests/test_posts_api.py`。这份笔记只讲做接口自动化会用到的 Python，遇到不会的回来查。

## 0. 核心心智模型

接口测试 = **发请求 → 拿到 JSON → 翻译成 Python 对象 → 用 assert 检查**

JSON → Python 翻译对照表（`resp.json()` 自动完成）：

| JSON | Python | 取值方式 |
|------|--------|---------|
| `{ "id": 1 }` | 字典 dict | `data["id"]` |
| `[ ... ]` | 列表 list | `data[0]` |
| `"hello"` | 字符串 str | 直接比较 |
| `true` / `42` | bool / int | 直接比较 |

## 1. import：导入工具箱

```python
import requests          # 把整个工具箱搬进来
from collections import OrderedDict   # 只拿一件工具（以后会见到）
```

## 2. 变量：名字 = 值，不用声明类型

```python
BASE_URL = "https://jsonplaceholder.typicode.com"   # 全大写 = 常量约定
resp = requests.get(...)     # 变量可以存任何东西
```

## 3. f-string：字符串拼接

```python
f"{BASE_URL}/posts/1"        # {} 里放变量，自动替换
f"共 {len(data)} 条数据"      # {} 里也可以放表达式
```

## 4. 函数：def + 缩进

```python
def test_xxx():
    """docstring：函数说明"""
    代码...                   # 缩进 4 空格 = 属于这个函数
```

- 函数名 `test_` 开头 → pytest 自动收集为用例
- Python 用缩进分层，不用 `{}`，缩进错了语法就错了

## 5. 字典 dict：键值对柜子

```python
data = {"userId": 1, "id": 1, "title": "sunt aut facere"}

data["id"]           # → 1        取值（键必须加引号）
"title" in data      # → True     检查键是否存在
data.keys()          # → 所有键
data.get("xxx")      # → None     取不到也不报错（vs data["xxx"] 直接报 KeyError）
data["user"]["name"] # → 嵌套取值，一层层剥
```

## 6. 列表 list：有顺序的一串数据

```python
len(data)            # → 数量
data[0]              # → 第一个（从 0 开始数）
data[0]["id"]        # → 列表套字典，先取元素再取键
isinstance(data, list)   # → 类型检查：是不是列表
```

## 7. assert：断言（测试的灵魂）

```python
assert 条件                # 条件不成立 → 用例失败
assert a == b              # 相等（== 是比较，= 是赋值！）
assert a != b              # 不等
assert "x" in data         # 包含
assert isinstance(x, str)  # 类型
assert a == b, "失败提示语" # 逗号后是失败时显示的话
```

## 8. set()：验证字段结构

```python
assert set(data[0].keys()) == {"userId", "id", "title", "body"}
# set 转集合后无序，只比"字段名集合"是否一致，不管顺序
```

## 9. 字典字面量：手写请求体

```python
payload = {
    "title": "标题",
    "body": "内容",
    "userId": 1,
}
```

## 10. 关键字参数：带名字的参数

```python
requests.post(url, json=payload, timeout=10)     # 请求体
requests.get(url, params={"k": "v"}, timeout=10) # 拼成 ?k=v
requests.get(url, headers={"token": "..."})      # 请求头
```

requests 常用响应属性/方法：

| 写法 | 含义 |
|------|------|
| `resp.status_code` | 状态码（属性，不加括号） |
| `resp.json()` | 解析成 dict/list（方法，要加括号） |
| `resp.text` | 原始文本 |
| `resp.elapsed` | 耗时（测响应时间用） |

## 11. 新手常见坑

1. `==` 写成 `=`：`assert data["id"] = 1` 直接语法错误
2. 字典键忘加引号：`data[id]` → NameError（除非 id 是你定义过的变量）
3. 忘了 `resp.json()`：对 resp 对象直接 `resp["id"]` → TypeError
4. 缩进混用 Tab 和空格 → IndentationError
5. 从 0 开始数：`data[100]` 是第 101 个元素，`len(data)` 条数据的最后一个下标是 `len(data) - 1`

## 12. 装饰器 @ —— 给函数附加能力

```python
@pytest.mark.parametrize("post_id", [1, 2, 50, 100])
def test_get_post_by_id(base_url, post_id):
    ...
```

`@xxx` 写法叫装饰器：不修改函数代码，给函数附加一层额外行为。这里的效果是"按数据表跑多次"。
你还会见到 `@pytest.fixture`（声明这个是夹具）、`@pytest.mark.skip`（跳过用例）。

## 13. 参数化 parametrize —— 一份逻辑跑 N 组数据

```python
# 单参数
@pytest.mark.parametrize("post_id", [1, 2, 50, 100])
def test_xxx(base_url, post_id): ...

# 单参数 + 可读名字
@pytest.mark.parametrize("post_id", [0, -1, 101], ids=["零", "负数", "超范围"])
def test_yyy(base_url, post_id): ...

# 多参数（每行是元组，按位置对应）
@pytest.mark.parametrize("post_id, expect_keys", [
    (1,  {"userId", "id", "title", "body"}),
    (100, {"userId", "id", "title", "body"}),
], ids=["第一篇", "最后一篇"])
def test_zzz(base_url, post_id, expect_keys): ...

# 参数是字典（测不同请求体）
@pytest.mark.parametrize("payload", [
    {"title": "普通", "body": "内容", "userId": 1},
    {"title": "超长" * 20, "body": "内容" * 50, "userId": 2},
], ids=["普通数据", "超长数据"])
def test_create(base_url, payload): ...
```

**铁律**：装饰器里字符串写的参数名，必须和函数形参**完全一致**，否则报 `fixture 'xxx' not found`。

输出里 `test_xxx[1]`、`test_xxx[id为0]` 的方括号内容就是当前这行数据，一眼能看出哪条挂了。

Windows 终端中文显示成 `\u4e3a0`：设环境变量 `PYTHONIOENCODING=utf-8` 即可，不影响测试结果。

## 14. 读失败报告的三个信息点

```
tests\test_posts_api.py:65: in test_post_not_found     ← 出错文件:行号
    assert resp.status_code == 200                     ← 出错的断言
E   assert 404 == 200                                  ← 实际值 vs 期望值
E    +  where 404 = <Response [404]>.status_code        ← 实际值来源
```

排查顺序：**先看实际值对不对（服务器问题？）→ 再看期望值写对没（断言问题？）→ 最后看环境（网络/数据）**。

## 15. 类与对象 —— 封装 API 客户端的语法

```python
class PostApi(BaseApi):              # 定义类；括号里是父类（继承它的能力）
    def __init__(self, base_url):    # 构造方法：PostApi("http://...") 时自动执行
        self.base_url = base_url     # self.xxx = 把数据挂到"这个对象自己"身上

    def get_post(self, post_id):     # 方法：第一个参数固定是 self
        return self.get(f"/posts/{post_id}")   # self.get = 用父类的方法

# 使用：
api = PostApi("http://127.0.0.1:5001")   # 类名(...) 造出一个对象
resp = api.get_post(1)                   # 对象.方法() 调用
```

三个关键理解：
- **类是模板，对象是实例**：`PostApi(base_url)` 执行一次就造一个对象，数据存在各自的 self 上
- **self 就是"这个对象自己"**：方法里通过 self 拿到对象身上的数据和方法
- **继承**：`class PostApi(BaseApi)` 表示 PostApi 自动拥有 BaseApi 的 get/post/session，自己只写业务方法

## 16. 分层设计的价值（面试要点）

```
tests/ 用例层      → 只写「测什么 + 断言什么」，读起来像需求文档
api/  客户端层     → 一个接口一个方法，URL 只出现一次，返回 Response
BaseApi 基础层     → base_url/timeout/Session/日志/重试，改一处全局生效
conftest fixture   → 把对象自动"递"给用例，用例不用关心对象怎么造
```

好处：接口路径改动只改 api 层一处；加日志/鉴权只改 BaseApi 一处；用例作者不需要懂 requests 细节。
