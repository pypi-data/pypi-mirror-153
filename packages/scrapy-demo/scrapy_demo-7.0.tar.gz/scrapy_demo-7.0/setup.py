# -*- coding: utf-8 -*-
# @Author : zhy
# @Time   : 2022-05-30
# @File   : setup.py
from setuptools import setup,find_packages

setup(
    name='scrapy_demo',
    version='7.0',
    description='scrapy通用爬虫',
    include_package_data=True,  # 是否允许上传资源文件
    packages=find_packages(),#包的目录
    author='zhy',  # 作者
    author_email='191517137@qq.com',  # 作者邮件
    python_requires='==3.7.5',#设置python版本要求
    install_requires=['scrapy']#安装所需要的库
)
