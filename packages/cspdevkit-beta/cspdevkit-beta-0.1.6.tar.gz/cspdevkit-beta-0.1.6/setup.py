#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/25 14:48
# @Author  : xgy
# @Site    : 
# @File    : setup.py.py
# @Software: PyCharm
# @python version: 3.7.4
"""

from setuptools import setup, find_packages

setup(
    # name='cspdevkit',
    name='cspdevkit-beta',
    # py_modules=["cspdevkit"],
    version='0.1.6',
    packages=find_packages(where='src', exclude=[]),
    package_dir={'': 'src'},
    include_package_data=True,
    # install_requires=['Click', 'requests', 'PyYAML==5.4.1', 'docker==5.0.3', 'tqdm', 'imageio==2.19.1', 'scipy==1.7.3', 'chardet==3.0.4', 'terminaltables', 'numpy==1.21.5', 'Pillow==9.1.0','matplotlib', 'pandas==1.3.4', 'imgaug', 'opencv-python', 'lxml', 'openpyxl', 'zipp==3.7.0', 'loguru'],
    install_requires=['Click', 'requests', 'PyYAML==5.4.1', 'tqdm', 'scipy==1.7.3', 'chardet==3.0.4', 'terminaltables', "Pillow==9.1.0", 'numpy==1.21.5', 'matplotlib==3.5.1', 'pandas==1.3.4', 'lxml', 'openpyxl', 'zipp==3.7.0', 'loguru'],
    entry_points={'console_scripts': ['CSP=cspdevkit.command.cli_all:csptools']},
    classifiers=[
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # 开发的目标用户
        'Intended Audience :: Developers',

        # 属于什么类型
        'Topic :: Software Development :: Build Tools',

        # 许可证信息
        'License :: OSI Approved :: MIT License',

        # 目标 Python 版本
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)
