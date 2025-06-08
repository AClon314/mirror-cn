# mirror-cn

临时/永久镜像加速 mirrors server site to accelerate.

无依赖项，可作为python包被python调用。

## Install 安装
```sh
pip install git+http://github.com/AClon314/mirror-cn
```

## Usage 用法
```sh
mirror git clone http://github.com/AClon314/mirror-cn   # 临时走镜像
mirror git pip pixi conda   # 等价于 mirror --all，永久设置镜像
mirror --reset  # 移除镜像设置
mirror --list
mirror --help
```