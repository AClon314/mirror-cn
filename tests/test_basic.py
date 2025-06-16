import pytest
from mirror_cn import git, try_script


@pytest.mark.parametrize(
    "url",
    [
        'https://github.com/AClon314/mirror-cn',
    ]
)
def test_git(url: str):
    mirror_url = git('clone', url=url)
    assert mirror_url is not None


def test_pixi():
    import shutil
    import socket
    from urllib.request import urlretrieve
    socket.setdefaulttimeout(10)
    file, _ = urlretrieve('https://pixi.sh/install.sh', filename='./install.sh')
    for p in try_script(file):
        if p.returncode == 0:
            break
    if not shutil.which('pixi'):
        assert False, "pixi command not found"
