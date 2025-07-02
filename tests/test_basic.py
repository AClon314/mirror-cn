import os
import re
import pytest
from mirror_cn import git, run, try_script, get_latest_release_tag
from logging import getLogger
Log = getLogger(__name__)
IS_ACTION = os.environ.get('GITHUB_ACTIONS', None)


@pytest.mark.skipif(bool(IS_ACTION), reason="test manually")
@pytest.mark.parametrize(
    "cmds",
    [
        ['sleep', '1'],
        ['sleep', '3'],
        'sleep 1',
    ]
)
def test_run(cmds):
    # TODO: `yes` command will stuck python process, because it will output amounts of 'y'
    p = run(cmds, timeout=2)
    Log.info(f'{p.__dict__=}')


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
    if not os.path.exists(path):
        assert False, "Failed to install pixi"
