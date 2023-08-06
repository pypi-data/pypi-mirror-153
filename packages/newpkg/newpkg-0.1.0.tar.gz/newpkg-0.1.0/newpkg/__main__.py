import os
import sys
setuppy = """
from setuptools import setup, find_packages

# 读取readme.md作为项目的描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{name}", # 包名
    version="0.0.1", # 版本号
    author="{author}", # 作者
    author_email="{author_email}", # 作者邮箱
    description="{description}", # 简短描述
    long_description=long_description, # 长描述
    long_description_content_type="text/markdown", # 长描述类型
    classifiers=[ # 分类
        "Programming Language :: Python :: 3", # 编程语言
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)", # 许可证
        "Operating System :: OS Independent", # 操作系统
    ],
    license="GPL-3.0", # 许可证
    install_requires=[{install_requires}], # 安装依赖
    packages=find_packages(),
    python_requires=">=3.6",
    {entry_points}
)
"""

entrypoints = """entry_points = {
        # 通过命令行执行的入口
        "console_scripts": [
            "{name} = {name}.__main__:main"
        ]
}"""

readme = """
# {name}

{description}

(Created by newpkg)
"""

mainpy = """
def main():
    print("{name}")

if __name__ == "__main__":
    main()
"""

def output(text):
    print("\033[44m NewPKG \033[0m " + text)

def print_done(text):
    output("\033[42m 搞定 \033[0m " + text)

def print_error(text):
    output("\033[41m 错误 \033[0m " + text)

def run_cmd(cmd):
    output("\033[45m 执行命令 \033[0m " + cmd)
    os.system(cmd)

def cli_choice(choice_list):
    print()
    for i in range(len(choice_list)):
        print("\033[44m " + str(i+1)+" \033[0m "+choice_list[i])
    choice = input("\n请输入编号 \033[44m 1-"+str(len(choice_list))+" \033[0m: ")
    if choice.isdigit() and (1 <= int(choice) <= len(choice_list)):
        return int(choice)
    else:
        print_error("输入有误，请重试")
        return cli_choice(choice_list)

def create_package(name="", description="", author="", author_email="", install_requires="", is_cli=False):
    # 创建setup.py
    with open("setup.py", "w", encoding="utf-8") as fh:
        if is_cli:
            entrypointsStr = entrypoints.format(name=name)
        else:
            entrypointsStr = ""
        setup = setuppy.format(
            name=name,
            description=description,
            author=author,
            author_email=author_email,
            install_requires=install_requires,
            entry_points=entrypointsStr
        )
        fh.write(setup)
    
    # 创建README.md
    with open("README.md", "w", encoding="utf-8") as fh:
        fh.write(readme.format(
            name=name,
            description=description
        ))

    # 判断是否存在名为name的文件夹
    if not os.path.exists(name):
        # 创建一个名为name的文件夹
        os.mkdir(name)

        # 创建一个名为__init__.py的文件
        with open(name+"/__init__.py", "w", encoding="utf-8") as fh:
            fh.write("")
        
        # 创建一个名为__main__.py的文件
        with open(name+"/__main__.py", "w", encoding="utf-8") as fh:
            fh.write(mainpy.format(name=name))
        
def create_new():
    name = input("请输入包名：")
    description = input("请输入包描述：")
    author = input("请输入作者：")
    author_email = input("请输入作者邮箱：")
    install_requires = input("请输入依赖包（用英文逗号隔开，没有请留空）：")
    is_cli = input("是否将这个包注册为命令行工具（y/n）：")
    if is_cli == "y":
        is_cli = True
    else:
        is_cli = False
    create_package(name, description, author, author_email, install_requires, is_cli)
    print_done("创建成功")
    if is_cli:
        output("您选择了将这个包注册为命令行工具")
        output("安装这个包后，在终端输入 " + name + " 可以执行" + name + ".__main__.py中的main()函数")
    else:
        output("安装这个包后即可使用import " + name + "来使用这个包")

def main():
    output("new package! by xuanzhi33")
    c = cli_choice([
        "创建一个新包",
        "发布当前目录下的包到pypi",
        "退出 (ctrl+c)"
    ])
    if c == 1:
        create_new()
    elif c == 2:
        run_cmd("spkg patch")
    else:
        output("程序退出")

if __name__ == '__main__':
    main()
