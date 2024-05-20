# -*- coding:utf-8 -*-
# @FileName : tmp.py
# @Time : 2024/5/19 21:15
# @Author : fiv

class MyClass:
    def __init__(self):
        self.x = 10
        self.y = 20

    def add(self):
        self.z = self.x + self.y
        print(self.z)

    def execute_code(self, code):
        # 将 self 传递给 exec 的局部命名空间
        local_context = {'self': self}
        exec("""
self.add()
""", {}, local_context)


# 创建类的实例
obj = MyClass()

# 定义要执行的代码
code = """
self.z = self.x + self.y
print(self.z)
"""

# 执行代码
obj.execute_code(code)

# 验证 self.z 是否被正确地设置
print(obj.z)  # 输出: 30
