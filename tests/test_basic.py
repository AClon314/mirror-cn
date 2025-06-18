import re
import pytest
from mirror_cn import git, try_script, get_latest_release_tag, Shuffle
from logging import getLogger
Log = getLogger(__name__)


@pytest.mark.parametrize(
    "url",
    [
        'https://github.com/AClon314/mirror-cn',
    ]
)
def test_git(url: str):
    mirror_url = git('clone', url)
    assert mirror_url is not None


def test_pixi():
    import os
    import shutil
    import socket
    from urllib.request import urlretrieve
    socket.setdefaulttimeout(10)
    if not shutil.which('pixi'):
        file, _ = urlretrieve('https://pixi.sh/install.sh', filename='./install.sh')
        Log.info(f'{file=}')
        tag = get_latest_release_tag()
        os.environ['PIXI_VERSION'] = tag
        for p in try_script(file):
            if p.returncode == 0:
                break
    path = re.search(r"is installed into '(/.*?)'", p.stdout)
    path = path.group(1) if path else None
    if not path:
        assert False, "Failed to extract path from stdout"
    Log.info(f'{path=}')
    # warn: Could not detect shell type.
    # Please permanently add '/root/.pixi/bin' to your $PATH to enable the 'pixi' command.
    if p and 'PATH' in p.stderr:
        _export = f'export PATH=$PATH:{path}'
        _bashrc = os.path.expanduser('~/.bashrc')
        if os.path.exists(_bashrc):
            with open(_bashrc, 'r') as f:
                content = f.read()
            if _export not in content:
                Log.info(f'Adding to {_bashrc}: {_export}')
        with open(_bashrc, 'a') as f:
            f.write(f'\n{_export}\n')
    if not os.path.exists(path):
        assert False, "Failed to install pixi"
