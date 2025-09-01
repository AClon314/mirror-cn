#!/bin/env mitmdump -s redirect.py -p 3378
"""
mitmweb -s redirect.py -p 3378 --mode local --mode upstream:http://localhost:10808
TODO: currently you need to install manually mitmproxy .pem certificate into system trust store
"""
from pathlib import Path

PORT = 3378
PROG = "mitmweb"
ARGS = ["-s", __file__, "-p", str(PORT)]
REMAP = {
    f"http://127.0.0.1:{PORT}/builds/chromium/1187/chromium-win64.zip": Path(
        r"D:\Downloads\chromium-win64.zip"
    ),
    f"http://127.0.0.1:{PORT}/builds/chromium/1187/chromium-headless-shell-win64.zip": Path(
        r"D:\Downloads\chromium-headless-shell-win64.zip"
    ),
}
import os
import logging
from mitmproxy import http
from mitmproxy.http import Response

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d\t%(message)s",
)
Log = logging.getLogger(__name__)
BLANK_RESPONSE_HEADER = {"Content-Type": "text/plain"}


def request(flow: http.HTTPFlow) -> None:
    src = flow.request.url
    dst = REMAP.get(src, None)
    if isinstance(dst, Path):
        return redir_file(flow, dst)
    else:
        return redir_url(flow)


def redir_url(flow: http.HTTPFlow):
    src = flow.request.url
    if (
        src.startswith("http://mirror-pypi.cn/raw-proxy-tsinghua-cargo")
        and flow.request.method == "HEAD"
    ):
        flow.request.method = "GET"
        Log.info(f"[Method Change] HEAD → GET for {flow.request.url}")
        return
    Log.info(f"[Direct]\t{flow.request.method}\t{src=}")


def redir_file(flow: http.HTTPFlow, file: Path):
    Log.info(f"[Remap 🌐 →📄]\t{flow.request.url=}")
    if file.exists():
        MSG = f"FileNotFoundError: {file=}"
        Log.warning(MSG)
        flow.response = Response.make(404, MSG, BLANK_RESPONSE_HEADER)
        return
    try:
        with open(file, "rb") as f:
            content = f.read()
    except Exception as e:
        Log.error("", exc_info=e)
        flow.response = Response.make(500, f"FileException: {e}", BLANK_RESPONSE_HEADER)
    if len(content) == 0:
        Log.warning(f"{file=} is empty.")
        flow.response = Response.make(204, b"", BLANK_RESPONSE_HEADER)
        return
    flow.response = Response.make(200, content, BLANK_RESPONSE_HEADER)
    Log.info(f"[File]\t{file=}")


def parse():
    import argparse

    parser = argparse.ArgumentParser(
        description="适用于离线安装,对于硬编码的程序极为有效"
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    Log.setLevel(logging.DEBUG) if args.verbose else None
    return parser.parse_known_args()


def main():
    ns, args = parse()
    args += ARGS
    Log.debug(f"{locals()=}")
    os.execlp(PROG, PROG, *args)


if __name__ == "__main__":
    main()
