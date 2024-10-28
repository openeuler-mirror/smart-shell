from setuptools import setup, find_packages

# 定义项目所需的依赖
# install_requires = [
#     'click==8.1.7',
#     'distro==1.9.0',
#     'litellm==1.42.5',
#     'openai==1.36.1',
#     'rich==13.7.1',
#     'typer==0.12.3',
# ]

setup(
    name='smart_shell',

    version='1.0.0',

    author='Delthin',

    author_email='1059661071@qq.com',

    description='A smart command line tool for executing shell commands',

    long_description=open('README.md', encoding='utf-8').read(),

    url='https://gitee.com/Delthin/smart_shell',

    packages=find_packages(),

    # install_requires=install_requires,

    entry_points={
        'console_scripts': [
            'smsh=smsh.app:entry',  # 'smsh' 是命令 'app:main' 是你的应用模块和主函数
        ],
    },

    license='MulanPSL2.0',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mulan PSL v2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    # 项目所需的Python版本
    python_requires='>=3.9',
)