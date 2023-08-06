# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia',
 'graia.amnesia',
 'graia.amnesia.builtins',
 'graia.amnesia.json',
 'graia.amnesia.json.backend',
 'graia.amnesia.message',
 'graia.amnesia.transport',
 'graia.amnesia.transport.common',
 'graia.amnesia.transport.common.http',
 'graia.amnesia.transport.common.websocket']

package_data = \
{'': ['*']}

install_requires = \
['launart>=0.1.0,<0.2.0',
 'loguru>=0.6.0,<0.7.0',
 'statv>=0.1.0,<0.2.0',
 'yarl>=1.7.2,<2.0.0']

extras_require = \
{'orjson': ['orjson>=3.6.7,<4.0.0'], 'ujson': ['ujson>=5.2.0,<6.0.0']}

setup_kwargs = {
    'name': 'graia-amnesia',
    'version': '0.5.0',
    'description': 'a collection of shared components for graia',
    'long_description': '<div align="center">\n\n# Amnesia\n\n_A collection of common components for Graia Project._\n\n> 于是明天仍将到来.\n\n> 每一天都会带来新的邂逅, 纵使最终忘却也不会害怕明天到来.\n\n</div>\n\n<p align="center">\n  <img alt="PyPI" src="https://img.shields.io/pypi/v/graia-amnesia" />\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="code_style" />\n  <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" />\n  <a href="https://results.pre-commit.ci/latest/github/GraiaProject/Amnesia/master">\n    <img src="https://results.pre-commit.ci/badge/github/GraiaProject/Amnesia/master.svg" />\n  </a>\n\n</p>\n\n## 简述\n\nAmnesia 是一系列共用组件的集合, 包含了以下内容:\n\n - 消息链 `MessageChain`, 沿袭自 Avilla 实现和 Ariadne 部分方法实现;\n - `Element` 基类和 `Text` 消息元素实现;\n - `Launch API`: 程序生命周期管理, 提供准备(`prepare`), 主线(`mainline`) 与 清理(`cleanup`) 三个时间节点; 支持依赖编排;\n - 轻量化实现的 `Service`;\n - 轻量化的内存缓存实现 `Memcache`, 原版本由 @ProgramRipper 实现, 沿袭自 Avilla;\n - `Transport API`: 职权分派, 交互主导的网络通信封装;\n   - `uvicorn`: ASGI Runner;\n   - `starlette`: ASGI Application;\n   - `aiohttp`: Http & WebSocket Client.\n\n通过 Amnesia, 我们希望能更加轻量化第三方库的依赖, 并籍此促进社区的发展.\n\n - `MessageChain` 可以让 Avilla, Ariadne, Alconna 等共用统一实现, 并使其泛用性扩大;\n - `Launch API` 可以优化应用的启动流程, 适用于 `Saya` 或是单纯的 `Broadcast Control` 应用;\n - `Service` 使维护和访问资源的流程更加合理;\n - ...或许还会有更多?\n\n## 协议\n\n本项目以 MIT 协议开源.\n',
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
