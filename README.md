# mirror-cn

git pip pixi 临时/永久镜像加速 mirrors server site to accelerate.

无依赖项，可作为python包被python调用。

## Install 安装
```sh
pip install git+http://github.com/AClon314/mirror-cn
```

```sh
curl -o ./mirror_cn.py https://raw.githubusercontent.com/AClon314/mirror-cn/refs/heads/main/src/mirror_cn/mirror_cn.py
# 国内可使用如下地址：
# https://gitee.com/aclon314/mirror-cn/raw/main/src/mirror_cn/mirror_cn.py
python ./mirror_cn.py --help
```

## Usage 用法
```sh
mirror git clone http://github.com/AClon314/mirror-cn   # 临时走镜像
mirror git pip pixi conda   # 等价于 mirror --all，永久设置镜像
mirror --reset  # 移除镜像设置
mirror --list
mirror --help
```

See [pixi.py](https://github.com/AClon314/mocap-wrapper/tree/master/src/mocap_wrapper/install/pixi.py) or [test.py](./tests/test_basic.py) for more usage

```python
from mirror_cn import Shuffle, is_need_mirror, set_mirror, reset_mirror, try_script
Shuffle() # randomize mirrors
IS_MIRROR = is_need_mirror()        # check if need mirror
set_mirror() if IS_MIRROR else None # set mirrors for all programs

for process in try_script('./install.sh'):
  if process.returncode == 0:
    break # Successfully executed './_install.sh'
  else:
    err = process.stderr.strip()
    if 'not found' in err:
      with open('./install.sh', 'w') as f:
        f.write() # Your fail logic here
        ...
```

## As module 单文件模块

Download mirror_cn.py in the same folder with your python script, then import relatively.
在同目录下下载mirror_cn.py文件即可相对导入。

```python
try:
    from mirror_cn import *
except ImportError:
    if os.path.exists('mirror_cn.py'):
        raise
    Log.debug('❗ mirror_cn module not found, fixing...')
    download('https://gitee.com/aclon314/mirror-cn/raw/main/src/mirror_cn/mirror_cn.py', 'mirror_cn.py')
    os.execvp('python', ['python','mirror_cn.py'])
```