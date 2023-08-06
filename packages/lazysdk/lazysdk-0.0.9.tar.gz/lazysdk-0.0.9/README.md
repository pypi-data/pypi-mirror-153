# lazysdk
![](https://img.shields.io/badge/Python-3.8.6-green.svg)


#### 介绍
基于Python3的懒人包

#### 软件架构
软件架构说明
- lazysdk.lazyprocess
  - 多进程控制

- lazysdk.lazywebhook
  - webhook推送
  
#### 安装教程
1.  使用pip安装
- 普通方式安装
```shell script
pip3 install lazysdk
```

- 使用阿里镜像加速安装
```shell script
pip3 install lazysdk -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1. lazyprocess
```python3
import lazysdk

task_list = [1,2,3,4,5,6,7,8]
def process_task(
        task_index, 
        task_info
):
    print(f'task_index:{task_index}, task_info:{task_info}')
    
    
lazysdk.lazyprocess.run(
    task_list=task_list,
    task_function=process_task,
    subprocess_limit=2
)
```

2. lazywebhook
- 目前仅支持企业微信
```python3
from lazysdk import lazywebhook
    
lazywebhook.send_text(
    webhook='webhook url'
)
```


## Links
- PyPI Releases: https://pypi.org/project/lazysdk/
