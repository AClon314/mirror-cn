#!/bin/env mitmdump -s redirect.py -p 8080 --mode upstream:http://localhost:10808
'''
TODO: currently you need to install manually mitmproxy .pem certificate into system trust store
'''
import os
from mitmproxy import http, ctx
from mitmproxy.http import Response
Log = ctx.log
REMAP = {
    'https://github.com/actions/python-versions/releases/download/3.12.11-15433310049/python-3.12.11-linux-22.04-x64.tar.gz': '/home/n/download/python-3.12.11-linux-22.04-x64.tar.gz'
}


def request(flow: http.HTTPFlow) -> None:
    file = REMAP.get(flow.request.url, None)
    if file:
        Log.info(f"[Remap 🌐 →📄]\t{flow.request.url=}")
        try:
            # 读取本地文件内容
            with open(file, 'rb') as f:
                content = f.read()
            if len(content) == 0:
                Log.warn(f"Local {file=} is empty.")
                # 可选操作：返回空响应
                flow.response = Response.make(
                    204,  # 无内容
                    b"",
                    {"Content-Type": "text/plain"}
                )
                return

            # 构建响应
            flow.response = Response.make(
                200,  # 状态码
                content,  # 响应内容
                {"Content-Type": "application/octet-stream"}  # 响应头
            )
            Log.info(f"✅ {file=}")
        except Exception as e:
            Log.warn(e)
            # 可选操作：返回错误响应
            flow.response = Response.make(
                500,  # 内部服务器错误
                b"Failed to load local file",
                {"Content-Type": "text/plain"}
            )
    else:
        Log.info(f"[Direct]\t{flow.request.url=}")
