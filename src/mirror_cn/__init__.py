'''
See [pixi.py](https://github.com/AClon314/mocap-wrapper/tree/master/src/mocap_wrapper/install/pixi.py) for more usage
```python
from mirror_cn import Shuffle, is_need_mirror, set_mirror, reset_mirror, global_pixi, try_script
Shuffle()           # randomize mirrors
IS_MIRROR = is_need_mirror()  # check if need mirror
set_mirror()        # set mirrors for all programs

for process in try_script('./install.sh'):
  if process.returncode == 0:
    break
```
'''
from mirror_cn.mirror_cn import *
