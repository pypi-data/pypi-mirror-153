# coding:utf-8

from setuptools import setup

def get_ver_from_readme(readme_path):
    with open("README.md", "r", encoding='utf-8') as fs:
        for line in fs.readlines():
            if "当前版本：" in line:
                return line.split("：")[1]
    exit(0)


with open("README.md", "r", encoding='utf-8') as fs:
    long_description = fs.read()


cur_ver = get_ver_from_readme("README.md")


setup(
    name = 'ibnsession',
    version = cur_ver,
    author = 'ZF',
    author_email = 'zofon@qq.com',
    description = "Library for IBN",
    packages=[
        "ibnsession",
        "ibnsession/core",
        "ibnsession/tool",
        ],
    # py_module=[""]
    long_description = long_description,
    long_description_content_type="text/markdown",

    platforms = ["windows or Linux"],
    keywords = ['ibn', 'ops'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">=3.6.0",
    install_requires=[
        "netmiko>=2.0.0",
    ],
)

