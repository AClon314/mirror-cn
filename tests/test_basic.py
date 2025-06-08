import pytest
from mirror_cn.mirror import git


@pytest.mark.parametrize(
    "url",
    [
        'https://github.com/AClon314/mirror-cn',
    ]
)
def test_git(url: str):
    mirror_url = git('clone', url=url)
    assert mirror_url is not None
