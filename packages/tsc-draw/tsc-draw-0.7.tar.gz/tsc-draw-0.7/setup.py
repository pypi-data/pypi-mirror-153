# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

if os.path.exists('readme.md'):
    long_description = open('readme.md', 'r', encoding='utf8').read()
else:
    long_description = '代码: https://github.com/aitsc/tsc-draw'

setup(
    name='tsc-draw',
    version='0.7',
    description="绘图",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='tanshicheng',
    license='GPLv3',
    url='https://github.com/aitsc/tsc-draw',
    keywords='tools',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        # 'matplotlib>=3.1.3,<=3.2.3',
        'matplotlib>=3.1.3',  # 雷达图形状 用不了, 但是所有电脑可以安装, 防止高版本python装不了
        'numpy>=1.18.1',
        'scipy>=1.4.1',
        'statsmodels>=0.12.2',
    ],
    python_requires='>=3.6',
)
