# -*- coding: utf-8 -*-
# @time    : 22-1-12 下午8:28
# @author  : yangzhaowei
# @email   : yangzw_@outlook.com
# @file    : setup.py.py

# Always prefer setuptools over distutils，导入模块
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('README.md', encoding='utf-8') as fp:
    long_description = fp.read()

with open('requirements.txt', encoding='utf-8') as fp:
    install_requires = fp.read()

setup(name='DeepSignalLibrary',version='0.0.5',
    description='Adversarial Signal Library',

    # 项目的详细介绍，我这填充的是README.md的内容
    long_description=long_description,

    # README的格式，支持markdown，应该算是标准了
    long_description_content_type='text/markdown',

    # 项目的地址
    url='https://github.com/whatparty/advsignals',

    # 项目的作者
    author='yangzhaowei',

    # 作者的邮箱地址
    author_email='yangzw_@outlook.com',

    # Classifiers，
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],

    # 项目的关键字
    keywords='Adversarial Signal Library',

    # 打包时需要加入的模块，调用find_packages方法实现，简单方便
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'build', 'dist','data']),

    # 项目的依赖库，读取的requirements.txt内容
    install_requires=install_requires,

    # 数据文件都写在了MANIFEST.in文件中
    include_package_data=True,

    # entry_points 指明了工程的入口，在本项目中就是facialattendancerecord模块下的main.py中的main方法
    # 我这是命令行工具，安装成功后就是执行的这个命令

    entry_points={
        'console_scripts': [
            'FacialAttendanceRecord=facialattendancerecord.main:main',
        ],
    },
    license="MIT",
)
