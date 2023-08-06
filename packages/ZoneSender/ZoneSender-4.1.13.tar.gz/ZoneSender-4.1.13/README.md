# ZoneSender4
ZoneSender4

## 1 项目介绍
ZoneSender4 是一个开放的汽车各种信号测试框架

## 2 软件架构
![软件架构](/Doc/design/架构设计/%E8%BF%9B%E7%A8%8B%E9%80%9A%E4%BF%A1%E5%9B%BE.png)

## 3 常用操作
### 3.1 代码拉取与初始化
ZoneSender4 使用 git submodule 来管理子项目具体步骤
所有的子项目都放在 ./Libs 中
``` bash
git clone http://47.103.0.123:8008/ZoneSwToolsDevelop/ZoneSender4.git
cd ZoneSender4
git submodule update --init --recursive
```

添加子仓库
``` bash
cd Libs
git submodule add -b master git.url
cc ..
```
### 3.2 编译
安装依赖，最好在虚拟环境下安装
``` bash
pip install -r requirements_dev.txt
```
#### 3.2.1 编译 dev
编译用于本地调试的应用
``` bash
cd {项目根目录}
python ./scripts/PyInstallerBuild.py dev
```
#### 3.2.2 编译 release
编译用于发布的应用
所有 Libs 中的 .py 文件将会编译成 .pyd
``` bash
cd {项目根目录}
python ./scripts/PyInstallerBuild.py release
```
编译完成后到 {项目根目录}/Release 中看结果
### 3.3 运行调试
代码拉下来后需要解压项目根目录的 emqx.zip 文件到根目录中
#### 3.3.1 单独程序手动调试方法
手动把 emqx 启动
``` bash
cd {项目根目录}
emqx/bin/emqx start
```
启动自己的程序
关闭 emqx
``` bash
cd {项目根目录}
emqx/bin/emqx stop
```
#### 3.3.2 整个程序调试方法
根据 3.2.1 中的说明把ZoneSender4编译
使用命令行启动 ZoneSender4
``` bash
cd {项目根目录}
python scripts/ZoneSender4Tool.py start -f Configs/start_config_dev.json
```

#### 3.3.2 前端调试
前端调试使用 Mock 程序
手动把 emqx 启动
``` bash
cd {项目根目录}
emqx/bin/emqx start
```
根据需要启动需要调试的 Mock 进程
``` bash
cd {项目根目录}
python mock/xx/xx.py
```

## 4 文档管理
### 4.1 Web 设计和需求
{项目根目录}/Doc/desion
