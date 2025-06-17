'''
See [pixi.py](https://github.com/AClon314/mocap-wrapper/tree/master/src/mocap_wrapper/install/pixi.py) or [test.py](https://github.com/AClon314/mirror-cn/blob/main/tests/test_basic.py) for more usage
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
'''
from mirror_cn.mirror_cn import *
