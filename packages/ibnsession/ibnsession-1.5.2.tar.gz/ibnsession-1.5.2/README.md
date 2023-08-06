网络自动化运维工具
=======
该工具包含了网络设备一些基础操作，极大的简化了编程难度，对国产设备有着良好的支持。

- account_verification() 检查账号是否具有config权限
- get_running_config() 获取设备的running config
- inspect_config() 检查指定的配置，就是 show run | in XXX
- inspect_session() 对于防火墙，可以用该方法检查防火墙session
- execute_script() 对设备进行配置


### 设备支持列表:
- 山石防火墙
- 华为路由交换设备
- 思科的asa防火墙，路由器


### 运行依赖
```
[root@local ~]# pip show netmiko
Metadata-Version: 1.1
Name: netmiko
Version: 2.0.2
```


## 编程示例
```
from collections import namedtuple

ac_info = namedtuple('ac_info', ['username', 'password', 'enable_pass'])
ac_info.username = "username"
ac_info.password = "password"
ac_info.enable_pass = "en_pass"

dev_info = namedtuple('dev_info', ["dev_ip", "dev_name"])
dev_info.dev_ip = "192.168.0.1"

# 这里的 hs_SG6000 指的是所支持的山石防火墙的型号
# 目前支持 huawei_S5720 , asa_5545, srx_550 等等
dev_ob = hs_SG6000(ac_info,dev_info)

# 可以进行账号校验，判断账号是否登录成功且具有config权限
if dev_ob.account_verification():
    print("账号校验成功，具有CONFIG权限")

# 可以配置脚本
cmd_lines = []
cmd_lines.append('address "TTTT_172.19.1.1"')
cmd_lines.append('  ip 172.19.1.1/32')
cmd_lines.append('exit')

dev_ob.execute_script(cmd_lines):
```

### 其他说明
1. 在执行 execute_script 函数之前最好先看一下配置
2. 有问题请联系 zofon@qq.com



### 版本记录

当前版本：1.5.2

#### 1.5.2
- 给linux增加一个get_running_config函数，可以用这个简单获取服务器的运行状态

#### 1.5.1
- ibnsession.__init__.py
- cisco -> cisco_ios

#### 1.5.0
- 重新调整设备的分类，和 netmiko 保持一致

#### 1.4.3
- 一些格式上的，兼容性优化



#### 1.4.2
- 更新 linux 主机相关的函数
- 优化 网络设备代码

#### 1.4.0
- 添加linux主机相关的函数，后续会陆续更新

#### 1.3.6
- 优化了一些输出的BUG

#### 1.3.5
- 调整所有支持型号的基类
- 示例中添加 ：from collections import namedtuple
- 细化README.md

#### 1.3.4
- 调整一下版本位置，在更新版本之前，应该先清空 dist 目录文件夹

#### 1.3.3
- 优化了 setup.py 文件，以后版本信息就通过这个位置自动获取了

#### 1.3.2
- 优化了山石防火墙的账号校验部分
- 添加中文的介绍，以后会优先更新中文
- 添加了一个思科路由器的型号 cisco_C3900，把原本的 asa_5545 变成基类
- setup 的版本和这个保持同步

#### 1.3.1 
- 添加华为的设备 
- 配置过程不在输出内容
- 添加一个参数：config_mode_tag

#### 1.0.0
- 添加 huawei.py
- 添加 cisco.py

#### 0.1.0
- SRX 防火墙功能更新
- 添加功能（还不完善）: generate_routing_script(self, route_info_list)
- 添加功能 : get_running_config(self)

#### 0.02 Add hillstone related update
- 添加功能（还不完善） : generate_access_script(self,basic_info,session_list)
- 添加功能（还不完善） : execute_access_script(self,access_script_list)

#### 0.01 Design this package
