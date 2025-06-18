#!/bin/env python
'''
%(prog)s git clone https://github.com/owner/repo.git   # temporary use github.com mirror
%(prog)s https://github.com/owner/repo/releases/latest or download/...   # list: replace `github.com` with mirror site
%(prog)s ./install.sh   # replace `github.com` with mirror site in install script, and try to run it
%(prog)s --set git pip...   # set mirrors for these commands
%(prog)s --set      # set all mirrors
%(prog)s -r         # remove all global mirrors
%(prog)s -l         # list all mirrors
%(prog)s -l git     # list git mirrors

ENV VARS 可用的环境变量:
- TIMEOUT: int = 10  # default timeout for network requests
- CONCURRENT: int = 12  # default concurrent threads
'''
import os
import re
import sys
import shlex
import shutil
import logging
import argparse
import subprocess
from random import shuffle
from urllib.request import urlopen
from datetime import datetime, timezone
from typing import Callable, Iterable, Literal, Sequence
IS_DEBUG = os.getenv('GITHUB_ACTIONS', None) or os.getenv('LOG', None)
_LEVEL = logging.DEBUG if IS_DEBUG else logging.INFO
logging.basicConfig(level=_LEVEL, format='[%(asctime)s %(levelname)s] %(filename)s:%(lineno)s\t%(message)s', datefmt='%H:%M:%S')
_ID = -1
_EXE_CONDA = 'mamba' if shutil.which('mamba') else 'conda'
Log = logging.getLogger(__name__)
def version(): return (datetime.fromtimestamp(os.path.getmtime(__file__), tz=timezone.utc)).strftime('%Y.%m.%d.%H.%M')


__version__ = f'v{version()}'

GITHUB_RELEASE = [
    ['https://gh.h233.eu.org/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [@X.I.U/XIU2] 提供'],
    ['https://ghproxy.1888866.xyz/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [WJQSERVER-STUDIO/ghproxy] 提供'],
    ['https://gh.ddlc.top/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [@mtr-static-official] 提供'],
    ['https://slink.ltd/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [知了小站] 提供'],
    ['https://gh-proxy.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh-proxy.com] 提供'],
    ['https://cors.isteed.cc/github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [@Lufs\'s] 提供'],
    ['https://hub.gitmirror.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [GitMirror] 提供'],
    ['https://down.sciproxy.com/github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [sciproxy.com] 提供'],
    ['https://ghproxy.cfd/https://github.com', '美国', '[美国 洛杉矶] - 该公益加速源由 [@yionchilau] 提供'],
    ['https://github.boki.moe/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [blog.boki.moe] 提供'],
    ['https://github.moeyy.xyz/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [moeyy.cn] 提供'],
    ['https://gh-proxy.net/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh-proxy.net] 提供'],
    # ['https://github.yongyong.online/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [github.yongyong.online] 提供'],
    ['https://ghdd.862510.xyz/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [ghdd.862510.xyz] 提供'],
    ['https://gh.jasonzeng.dev/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.jasonzeng.dev] 提供'],
    ['https://gh.monlor.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.monlor.com] 提供'],
    ['https://fastgit.cc/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [fastgit.cc] 提供'],
    ['https://github.tbedu.top/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [github.tbedu.top] 提供'],
    ['https://gh-proxy.linioi.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh-proxy.linioi.com] 提供'],
    ['https://firewall.lxstd.org/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [firewall.lxstd.org] 提供'],
    ['https://mirrors.chenby.cn/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [mirrors.chenby.cn] 提供'],
    ['https://github.ednovas.xyz/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [github.ednovas.xyz] 提供'],
    ['https://ghfile.geekertao.top/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [ghfile.geekertao.top] 提供'],
    ['https://ghp.keleyaa.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [ghp.keleyaa.com] 提供'],
    ['https://github.wuzhij.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [github.wuzhij.com] 提供'],
    # ['https://gh.cache.cloudns.org/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.cache.cloudns.org] 提供'],
    ['https://gh.chjina.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.chjina.com] 提供'],
    ['https://ghpxy.hwinzniej.top/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [ghpxy.hwinzniej.top] 提供'],
    ['https://cdn.crashmc.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [cdn.crashmc.com] 提供'],
    ['https://git.yylx.win/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [git.yylx.win] 提供'],
    ['https://gitproxy.mrhjx.cn/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gitproxy.mrhjx.cn] 提供'],
    ['https://ghproxy.cxkpro.top/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [ghproxy.cxkpro.top] 提供'],
    ['https://gh.xxooo.cf/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.xxooo.cf] 提供'],
    ['https://ghproxy.xiaopa.cc/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [ghproxy.xiaopa.cc] 提供'],
    ['https://gh.944446.xyz/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.944446.xyz] 提供'],
    ['https://github.limoruirui.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [github.limoruirui.com] 提供'],
    ['https://api-gh.muran.eu.org/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [api-gh.muran.eu.org] 提供'],
    ['https://gh.idayer.com/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.idayer.com] 提供'],
    ['https://gh.zwnes.xyz/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.zwnes.xyz] 提供'],
    # ['https://gh.llkk.cc/https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [gh.llkk.cc] 提供'],
    ['https://down.npee.cn/?https://github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [npee社区] 提供'],
    ['https://raw.ihtw.moe/github.com', '美国', '[美国 Cloudflare CDN] - 该公益加速源由 [raw.ihtw.moe] 提供'],
    ['https://dgithub.xyz', '美国', '[美国 西雅图] - 该公益加速源由 [dgithub.xyz] 提供'],
    ['https://gh-proxy.ygxz.in/https://github.com', '美国', '[美国 洛杉矶] - 该公益加速源由 [@一个小站 www.ygxz.in] 提供'],
    ['https://gh.nxnow.top/https://github.com', '美国', '[美国 洛杉矶] - 该公益加速源由 [gh.nxnow.top] 提供'],
    ['https://gh-proxy.ygxz.in/https://github.com', '美国', '[美国 洛杉矶] - 该公益加速源由 [gh-proxy.ygxz.in] 提供'],
    ['https://gh.zwy.one/https://github.com', '美国', '[美国 洛杉矶] - 该公益加速源由 [gh.zwy.one] 提供'],
    ['https://ghproxy.monkeyray.net/https://github.com', '美国', '[美国 洛杉矶] - 该公益加速源由 [ghproxy.monkeyray.net] 提供'],
    ['https://gh.xx9527.cn/https://github.com', '美国', '[美国 洛杉矶] - 该公益加速源由 [gh.xx9527.cn] 提供'],
    # 为了缓解非美国公益节点压力（考虑到很多人无视前面随机的美国节点），干脆也将其加入随机
    ['https://ghproxy.net/https://github.com', '英国', '[英国伦敦] - 该公益加速源由 [ghproxy.net] 提供提示：希望大家尽量多使用美国节点（每次随机 负载均衡），避免流量都集中到亚洲公益节点，减少成本压力，公益才能更持久~'],
    ['https://ghfast.top/https://github.com', '其他', '[日本、韩国、新加坡、美国、德国等]（CDN 不固定） - 该公益加速源由 [ghproxy.link] 提供提示：希望大家尽量多使用美国节点（每次随机 负载均衡），避免流量都集中到亚洲公益节点，减少成本压力，公益才能更持久~'],
    # ['https://wget.la/https://github.com', '其他', '[中国香港、中国台湾、日本、美国等]（CDN 不固定） - 该公益加速源由 [ucdn.me] 提供提示：希望大家尽量多使用美国节点（每次随机 负载均衡），避免流量都集中到亚洲公益节点，减少成本压力，公益才能更持久~'],
    ['https://kkgithub.com', '其他', '[中国香港、日本、韩国、新加坡等] - 该公益加速源由 [help.kkgithub.com] 提供提示：希望大家尽量多使用美国节点（每次随机 负载均衡），避免流量都集中到亚洲公益节点，减少成本压力，公益才能更持久~'],
]
GIT = {
    'github.com': [
        # ['https://gitclone.com/github.com', '国内', '[中国 国内] - 该公益加速源由 [GitClone] 提供 - 缓存：有 - 首次比较慢，缓存后较快'],
        ['https://githubfast.com', '韩国', '[韩国] - 该公益加速源由 [Github Fast] 提供'],
        ['https://kkgithub.com', '香港', '[中国香港、日本、新加坡等] - 该公益加速源由 [help.kkgithub.com] 提供'],
        ['https://ghfast.top/https://github.com', '韩国', '[日本、韩国、新加坡、美国、德国等]（CDN 不固定） - 该公益加速源由 [ghproxy] 提供'],
        ['https://ghproxy.net/https://github.com', '日本', '[日本 大阪] - 该公益加速源由 [ghproxy.net] 提供'],
    ]
}
PIP = [
    'https://pypi.tuna.tsinghua.edu.cn/simple',  # 清华
    'https://mirrors.aliyun.com/pypi/simple',  # 阿里云
    'http://mirrors.cloud.tencent.com/pypi/simple/',  # 腾讯云
    'https://pypi.mirrors.ustc.edu.cn/simple/',  # 中国科学技术大学
]
CONDA = [
    {
        "https://anaconda.com/bioconda": ["https://mirrors.ustc.edu.cn/anaconda/cloud/bioconda"],
        "https://anaconda.com/conda-forge": ["https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge"],
        "https://anaconda.com/nvidia": ["https://mirrors.sustech.edu.cn/anaconda-extra/cloud/nvidia/"],
        "https://anaconda.com/pytorch": ["https://mirrors.ustc.edu.cn/anaconda/cloud/pytorch"],
        "https://repo.anaconda.com/pkgs/main": ["https://mirrors.ustc.edu.cn/anaconda/pkgs/main"],
        "https://repo.anaconda.com/pkgs/msys2": ["https://mirrors.ustc.edu.cn/anaconda/pkgs/msys2"],
        "https://repo.anaconda.com/pkgs/r": ["https://mirrors.ustc.edu.cn/anaconda/pkgs/r"],
    }
]
ALL = [GITHUB_RELEASE, GIT, PIP, CONDA]
_GITHUB_RELEASE = (v[0] for v in GITHUB_RELEASE)
_GIT = {k: [_[0] for _ in v] for k, v in GIT.items()}
_GIT = {k: iter(v) for k, v in _GIT.items()}
_PIP = iter(PIP)
__RE = {
    'symbol': r'[^\w_]+',
    'github': r'.*github\.com/([^/]+/[^/]+)',
}
_RE = {k: re.compile(v) for k, v in __RE.items()}
def _shlex_quote(args: Iterable[str]): return [shlex.quote(str(arg)) for arg in args]
def _get_cmd(cmds: Iterable[str] | str): return cmds if isinstance(cmds, str) else _shlex_quote(cmds)
def _get_domain(url: str): return url.split("://")[1].split("/")[0]
def _strip(s: str): return s.strip() if s else ''


def _call(cmd: Sequence[str] | str, Print=True):
    '''⚠️ Strongly recommended use list[str] instead of str to pass commands,
    to avoid shell injection risks for online service.'''
    global _ID
    _ID += 1
    prefix = f'{cmd[0]}_{_ID}'
    shell = True if isinstance(cmd, str) else False
    cmd = _get_cmd(cmd) if shell else cmd
    Log.info(f'{prefix}🐣❯ {cmd}') if Print else None
    try:
        process = subprocess.run(cmd, shell=shell, text=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        process = e
    if Print:
        stdout = _strip(process.stdout)
        stderr = _strip(process.stderr)
        Log.info(f'{prefix}❯ {stdout}') if stdout else None
        Log.error(f'{prefix}❯ {stderr}') if stderr else None
    return process


def _next(iterable, default=None):
    try:
        return next(iterable)
    except StopIteration:
        Log.error(f'{iterable=}已耗尽。')
        return default


def git(*args: str, retry=True) -> str | None:
    '''2.49.0'''
    _args = list(args)
    idxs = [i for i, a in enumerate(args) if a.startswith('https://github.com')]
    if idxs:
        url = _args[idxs[0]]
        owner_repo = _get_owner_repo(url)
        mirror = _next(_GIT['github.com'])
        if mirror is None:
            return
        _url = f'{mirror}/{owner_repo}'
        for i in idxs:
            _args[i] = _url
        p = _call(['git', *_args])
        if any([err in p.stderr for err in ('The requested URL returned error', 'not found', 'not accessible')]):
            return git(*args) if retry else None

        repo = owner_repo.split('/')[-1]
        to_local = repo.replace('.git', '')
        os.chdir(to_local)
        p = _call(['git', 'remote', 'set-url', '--push', 'origin', url])
        return _url
    else:
        Log.warning(f'Git URL 不包含 github.com，无法使用镜像源: {locals()=}')
        _call(['git', *args])


def global_git(
    to_mirror: str | None = None,
    from_domain='github.com',
    loc: Literal['system', 'global', 'local', 'worktree', 'file'] = 'global'
) -> str | None:
    if to_mirror is None:
        mirror = _next(_GIT[from_domain])
    if mirror is None:
        return
    m = git('clone', 'AClon314/mirror-cn', retry=False)
    if m:
        _call(f'git config --{loc}  url."{mirror}".insteadOf "https://{from_domain}"')
        # call(f'git config --{loc}  url."git@{to_mirror}:".insteadOf "git@{from_domain}:"')
        return mirror
    else:
        return global_git()


def reset_git(
    loc: Literal['system', 'global', 'local', 'worktree', 'file'] = 'global'
):
    for mirror in GIT['github.com']:
        mirror = mirror[0]
        cmd = f'git config --{loc} --unset url."{mirror}".insteadOf'
        p = _call(cmd)


def uv(*args: str):
    '''0.7.13'''
    _args = list(args)
    if all([s in _args for s in ('python', 'install')]):
        mirror = _next(_GITHUB_RELEASE)
        if mirror is None:
            return
        mirror += '/astral-sh/python-build-standalone/releases/download/'
        cmds = ['uv', _get_cmd(args), '--mirror', mirror]
    else:
        index = _next(_PIP)
        cmds = ['uv', _get_cmd(args), '--index', index]
    _uv_env()
    return _call(cmds)


def global_uv(): return _uv_env()


def reset_uv():
    env = _uv_env()
    for k in env.keys():
        os.environ.pop(k, None)


def pip(*args: str):
    '''24.3.1'''
    mirror = _next(_PIP)
    cmds = ['pip', _get_cmd(args), '-i', mirror, '--timeout', TIMEOUT]
    return _call(cmds)


def global_pip(to_mirror: str | None = None):
    if to_mirror is None:
        to_mirror = _next(_PIP)
    if to_mirror is None:
        return
    _call(f'pip config set global.index-url {to_mirror}')
    _call(f'pip config set global.trusted-host {_get_domain(to_mirror)}')


def reset_pip():
    _call('pip config unset global.index-url')
    _call('pip config unset global.trusted-host')


def pixi(*args: str):
    '''0.48.1'''
    _uv_env()
    cmds = ['pixi', _get_cmd(args)]
    return _call(cmds)


def global_pixi(pypi: list[str] = PIP, toml_path: str | None = None):
    _args = [f'--manifest-path {toml_path}'] if toml_path else ['--global']
    pixi_prefix = 'pixi config set'.split(' ')
    index_main = pypi.pop(0)    # TODO
    cmds = {
        'pypi-config.index-url': index_main,
        'pypi-config.extra-index-urls': str(pypi).replace("'", '"'),
        'mirrors': str(CONDA[0]).replace("'", '"'),
    }
    for k, v in cmds.items():
        _call(pixi_prefix + _args + [k, v])


def reset_pixi(toml_path: str | None = None):
    _args = [f'--manifest-path {toml_path}'] if toml_path else ['--global']
    pixi_prefix = 'pixi config unset'.split(' ')
    cmds = [
        'pypi-config.index-url',
        'pypi-config.extra-index-urls',
        'mirrors',
    ]
    for cmd in cmds:
        _call(pixi_prefix + _args + [cmd])


def global_conda(urls: dict | None = None):
    _call(f'{_EXE_CONDA} clean -i')
    if urls is None:
        urls = CONDA[0]
    main: list[str] = urls.pop('main', [])
    custom: dict[str, list[str]] = urls
    for url in main:
        _call(f'{_EXE_CONDA} config prepend channels {url}')
    for channel, _urls in custom.items():
        for url in _urls:
            _call(f'{_EXE_CONDA} config prepend channels {url}')


def _get_global_funcs(prefix='global_'): return {
    name.replace(prefix, ''): func for name, func in globals().items()
    if name.startswith(prefix) and callable(func)}


_GLOBAL_FUNCS = _get_global_funcs()
_RESET_FUNCS = _get_global_funcs(prefix='reset_')
_FUNCS = {
    name: func for name, func in globals().items()
    if callable(func) and not name.startswith('_') and name not in _GLOBAL_FUNCS.keys() and name not in _RESET_FUNCS.keys()}


def _get_owner_repo(url):
    owner_repo = _RE['github'].match(url)
    if not owner_repo:
        raise Exception(f'Git URL 格式错误，无法解析 owner/repo: {url}')
    owner_repo = str(owner_repo.group(1))
    return owner_repo


def _uv_env():
    _pip = _next(_PIP)
    _index = {'UV_DEFAULT_INDEX': _pip} if _pip else {}
    env = {
        'UV_HTTP_TIMEOUT': str(TIMEOUT),
        'UV_REQUEST_TIMEOUT': str(TIMEOUT),
        'UV_INSECURE_HOST': _get_domain(PIP[0]),
        **_index,
    }
    for k, v in env.items():
        os.environ[k] = v
    return env


def Shuffle():
    for key in GIT.keys():
        shuffle(GIT[key])
    shuffle(PIP)
    shuffle(CONDA)
    shuffle(GITHUB_RELEASE)


def is_need_mirror(url='https://www.google.com', timeout=4.0):
    Log.info("检查是否需要镜像...")
    try:
        with urlopen(url, timeout=timeout) as response:
            if response.status != 200:
                raise Exception(f"{url} is not reachable")
            else:
                GITHUB_RELEASE.insert(0, ['https://github.com', '美国', '[官方Github]'])
        return False
    except:
        Log.info("🪞 使用镜像")
        return True


def replace_github_with_mirror(file='./install.sh'):
    ''' replace https://github.com to mirror site, return the replaced file path & shell invoke commands '''
    with open(file, mode='rb') as f:
        raw = f.read()
    _dir = os.path.dirname(file)
    _file = f'_{os.path.basename(file)}'
    _file = os.path.join(_dir, _file)
    github_com = b'https://github.com'
    while github_mirror := _next(_GITHUB_RELEASE):
        Log.info(f'{github_mirror=}')
        _github_mirror = github_mirror.encode('utf-8')
        changed = raw.replace(github_com, _github_mirror)
        with open(_file, mode='wb') as f:
            f.write(changed)
        os.chmod(_file, 0o755)
        yield _file, github_mirror


def build_shell_cmds(file: str):
    if file.endswith('.sh'):
        cmds = ['sh', '-c', file]
    elif file.endswith('.ps1'):
        cmds = ['powershell', '-ExecutionPolicy', 'ByPass', '-File', file]
    elif file.endswith('.bat') or file.endswith('.cmd'):
        cmds = ['cmd', '/c', file]
    else:
        Log.error(f'Unsupported script suffix: {file}')
        return
    return cmds


def get_latest_release_tag(owner_repo='prefix-dev/pixi') -> str:
    import json
    url = f"https://api.github.com/repos/{owner_repo}/releases/latest"
    Log.debug(f'{url=}')
    with urlopen(url, timeout=TIMEOUT) as response:
        data = json.loads(response.read().decode('utf-8'))
        return data['tag_name']


def try_script(file: str):
    ''' for process in try_script('./install.sh') '''
    for _file, mirror in replace_github_with_mirror(file):
        cmds = build_shell_cmds(_file)
        if cmds is None:
            return
        yield _call(cmds)


CONCURRENT = 12
TIMEOUT = 10


def argParser():
    Log.info(f'{__name__} {__version__}') if not IS_DEBUG else None
    parser = argparse.ArgumentParser(description=f'国内镜像源助手 Mirror CN 🧙🪄 🪞 🌐, 支持 {" ".join(_GLOBAL_FUNCS.keys())}', usage=__doc__)
    parser.add_argument(
        '-y', '--smart', action='store_true', help=f'⭐ 无人值守智能判断，仅当访问谷歌超过4秒时设置镜像')
    parser.add_argument(
        '-s', '--set', action='store_true', help='仅设置选定的全局镜像源 Set global mirrors for selected programs')
    parser.add_argument(
        '-r', '--reset', '--remove', action='store_true', help='移除全局镜像源，走官方源 Remove(reset) mirrors in global config')
    parser.add_argument(
        '-l', '--list', action='store_true', help='镜像列表 Mirrors list')
    # parser.add_argument(
    #     '--test', '--rank', **_KW_PARSE, help='测试最快镜像 Test mirrors and rank them by speed')
    ns, args = parser.parse_known_args()
    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)
    return ns, args


def main():
    global CONCURRENT, TIMEOUT
    ns, args = argParser()
    CONCURRENT = int(os.environ.get('concurrent', CONCURRENT))
    TIMEOUT = int(os.environ.get('timeout', TIMEOUT))
    Log.debug(f'{os.environ=}\t{locals()=}')
    Shuffle()
    if ns.smart:
        IS_MIRROR = is_need_mirror()
        set_mirror() if IS_MIRROR else Log.info('不需要镜像源。No need to set mirrors.')
        return
    if ns.list:
        import json
        is_pretty = '--list' in sys.argv
        kw = {'ensure_ascii': False, 'indent': 2}
        if args:
            for exe in args:
                _LIST = globals().get(exe.upper(), {})
                _LIST = json.dumps(_LIST, **kw) if is_pretty else _LIST
                Log.info(f'{exe} 镜像源 Mirrors: {_LIST}') if _LIST else exit(404)
        else:
            _ALL = json.dumps(ALL, **kw) if is_pretty else ALL
            Log.info(f'所有镜像源 All mirrors: {_ALL}')
    if ns.reset:
        Log.debug('reset')
        reset_mirror(*args)
    # if ns.test:
    #     for exe in args:
    #         ...
    if ns.set:
        Log.debug('set')
        set_mirror(*args)
        return
    if len(args) == 1:
        url = args[0]
        if os.path.exists(url):
            Log.debug(f'try_script')
            for p in try_script(url):
                if p.returncode == 0:
                    return
        elif args[0].startswith('https://github.com'):
            Log.debug(f'github releases')
            if 'latest' in url:
                owner_repo = _get_owner_repo(url)
                tag = get_latest_release_tag(owner_repo)
                url = url.replace('/latest', '').replace('download', f'download/{tag}')
            while github_mirror := _next(_GITHUB_RELEASE):
                _url = url.replace('https://github.com', github_mirror)
                print(_url)
    elif len(args) > 0:
        Log.debug('temp')
        func = globals().get(args[0], None)
        if func and callable(func):
            func(*args[1:])
        else:
            Log.error(f'{args[0]}: 暂未支持或拼写错误。Unimplemented or check your spelling?')


def set_mirror(*programes: str): return _run_funcs(_get_funcs(programes, _GLOBAL_FUNCS))
def reset_mirror(*programes: str): return _run_funcs(_get_funcs(programes, _RESET_FUNCS))
def _run_funcs(funcs: Iterable[Callable]): return [func() for func in funcs]


def _get_funcs(keys: Iterable[str], KEYS_FUNCS: dict = _GLOBAL_FUNCS) -> list[Callable]:
    '''check: ignore argparse unsupported

    Args:
        keys: user input as group A. **Fallback to `KEYS_FUNCS.keys()` if `keys` is empty**
        KEYS_FUNCS: compared group B. You MUST check **ALL FUNCS are callable**!
    '''
    KEYS = KEYS_FUNCS.keys()
    keys = _filter_exist_programs(keys if keys else KEYS)
    names = set(keys).intersection(set(KEYS))
    funcs = [KEYS_FUNCS[name] for name in names]
    Log.debug(f'{locals()=}')
    return funcs


def _filter_exist_programs(programes: Iterable[str]):
    _progs = [prog for prog in programes if shutil.which(prog)]
    not_found = set(programes) - set(_progs)
    if not_found:
        Log.warning(f'Ignored due to not in PATH: {not_found}')
    Log.debug(f'Exist programes: {_progs}')
    return _progs


if __name__ == '__main__':
    main()

Log.debug(f'{__name__} {__version__}')
