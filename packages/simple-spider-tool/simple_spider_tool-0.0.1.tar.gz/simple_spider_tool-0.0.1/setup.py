# -*- coding: utf-8 -*-
# @Time : 2022/5/30 22:04
# @Author : xic
# @File : setup.py
# @Description : None
# @Software : PyCharm
import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = '\n' + f.read()

setuptools.setup(
    name="simple_spider_tool",
    version="0.0.1",
    author="xingc",
    author_email="xingcys@gmail.com",
    description="一些简易、好用的爬虫工具，减少重复代码与文件冗余",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.0.0",
    install_requires=["jsonpath"],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
