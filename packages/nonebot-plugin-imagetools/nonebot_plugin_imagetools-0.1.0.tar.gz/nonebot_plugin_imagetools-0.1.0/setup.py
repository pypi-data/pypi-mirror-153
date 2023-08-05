# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_imagetools']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'httpx>=0.19.0',
 'imageio>=2.12.0,<3.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-imageutils>=0.1.3,<0.2.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-imagetools',
    'version': '0.1.0',
    'description': 'Nonebot2 简单图片操作插件',
    'long_description': '# nonebot-plugin-imagetools\n\n[Nonebot2](https://github.com/nonebot/nonebot2) 插件，用于一些简单图片操作\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_imagetools\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_imagetools\n```\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n操作名 + [图片] 或 回复图片\n\n#### 支持的操作\n - 水平翻转/左翻/右翻\n - 竖直翻转/上翻/下翻\n - 旋转 + 角度\n - 缩放 + 尺寸或百分比，如：`缩放 100x100`；`缩放 200x`；`缩放 150%`\n - 裁剪 + 尺寸或比例，如：`裁剪 100x100`；`裁剪 2:1`\n - 反相/反色\n - 轮廓\n - 浮雕\n - 模糊\n - 锐化\n - 像素化 + 像素尺寸，默认为 8\n - 颜色滤镜 + 16进制颜色代码 或 颜色名称，如：`颜色滤镜 #66ccff`；`颜色滤镜 green`\n - 纯色图 + 16进制颜色代码 或 颜色名称\n - gif倒放/倒放\n - gif分解\n - 九宫格\n - 文字转图 + 文字，支持少量BBcode\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-imagetools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
