#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-09-18 00:15:21
@LastEditors    : yanyongyu
@LastEditTime   : 2021-03-16 16:59:22
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from typing import Dict, List

import psutil


def cpu_status() -> float:
    return psutil.cpu_percent(interval=1)  # type: ignore


def per_cpu_status() -> List[float]:
    return psutil.cpu_percent(interval=1, percpu=True)  # type: ignore


def memory_status() -> float:
    return psutil.virtual_memory().percent


def disk_usage() -> Dict[str, psutil._common.sdiskusage]:
    disk_parts = psutil.disk_partitions()
    disk_usages = {
        d.mountpoint: psutil.disk_usage(d.mountpoint) for d in disk_parts
    }
    return disk_usages


async def md_to_pic(
    md: str = None, md_path: str = None, css_path: str = None, width: int = 500
) -> bytes:
    """markdown 转 图片

    Args:
        md (str, optional): markdown 格式文本
        md_path (str, optional): markdown 文件路径
        css_path (str,  optional): css文件路径. Defaults to None.
        width (int, optional): 图片宽度，默认为 500

    Returns:
        bytes: 图片, 可直接发送
    """
    from os import getcwd
    from pathlib import Path
    import aiofiles
    import jinja2
    import markdown
    from jinja2.environment import Template
    from nonebot.log import logger
    from typing import Optional
    from .browser import get_new_page

    TEMPLATES_PATH = str(Path(__file__).parent / "templates")
    env = jinja2.Environment(
    extensions=["jinja2.ext.loopcontrols"],
    loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    enable_async=True,
)
    template = env.get_template("markdown.html")
    if not md:
        if md_path:
            md = await read_file(md_path)
        else:
            raise "必须输入 md 或 md_path"
    logger.debug(md)
    md = markdown.markdown(
        md,
        extensions=[
            "pymdownx.tasklist",
            "tables",
            "fenced_code",
            "codehilite",
            "mdx_math",
        ],
        extension_configs={"mdx_math": {"enable_dollar_delimiter": True}},
    )

    logger.debug(md)
    extra = ""
    if "math/tex" in md:
        katex_css = await read_tpl("katex/katex.min.b64_fonts.css")
        katex_js = await read_tpl("katex/katex.min.js")
        mathtex_js = await read_tpl("katex/mathtex-script-type.min.js")
        extra = (
            f'<style type="text/css">{katex_css}</style>'
            f"<script defer>{katex_js}</script>"
            f"<script defer>{mathtex_js}</script>"
        )

    if css_path:
        css = await read_file(css_path)
    else:
        css = await read_tpl("github-markdown-light.css") + await read_tpl(
            "pygments-default.css"
        )

    return await html_to_pic(
        template_path=f"file://{css_path if css_path else TEMPLATES_PATH}",
        html=await template.render_async(md=md, css=css, extra=extra),
        viewport={"width": width, "height": 10},
    )


if __name__ == "__main__":
    print(cpu_status())
    print(memory_status())
    print(disk_usage())
