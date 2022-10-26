# Tennga
 一个简单的源管理器

## 用法：

```python
from tennga import tennga
tennga.init() #在文件夹下初始化源srcf
tennga.listsrc() #打印所有源
tennga.add(url) #添加源
tennga.remove(url或者数字) #移除list出来的源
tennga.update() #更新与使用源 下载所有源文件到srcs下面
tennga.search(文件名和模糊搜索) #从srcs的源中查找文件
tennga.donwload(文件名,d回调函数=None) #从源搜索并下载文件，携带一个aop。自动将文件下载到srcf/内容1中。
#注意即使删除了源，srcf下的文件不会被自动移除
```

## d回调函数

```python
def callback(req :requests,param :dict) -> object:
    """
    用于处理下载的半成品源，默认是直接保存content。
    如果下载失败，则检查是否有离线文件。如果有就将就着，没有就报错。
    req: requests对象
    param: 源文件对应的所有参数，比如name，url以及其他
    """
    pass
```

## 源格式 utf-8 json

```json
{
    "内容1":[
        {"name":"文件1",
         "url":["http://www.baidu.com",
                "block://块名1/文件名"
               ]
         "xpath":"xxxxx",
         "time" : "2022/10/26"
        },
        ....
    ],
    "内容2":[
        
    ],
    "blocks":[
        {
            "name":"块名1",
            "url":"xxx",
        }
    ]
}
```

除了blocks以外，其他文件的源只有name和url是必须的。

文件存储在:

srcf/内容1/文件1/文件内容.txt

blocks是一个特殊的文件夹，用于存储block。实际上是tar文件。存储了一组数据。通常用于存储一组图片。blocks配置是固定不变的，只有name与url。为了使资源唯一，最好给块名加上一个id。使用block链接可以从block中解压出需要的资源放入对应文件夹下。

block的文件后缀为xx.bk。直接存储于block下面。

blocks文件夹也在srcf下面。