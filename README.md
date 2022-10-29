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
tennga.find(文件夹，文件名，uuid) #从srcs的源中查找文件
tennga.install(文件夹，文件名) #从源搜索并下载文件，携带一个aop。自动将文件下载到srcf/内容1中。
tennga.uninstall(文件夹，文件名)
tennga.freeze(文件夹) #freeze会返回已经安装的所有文件信息
tennga.getfile(文件夹，文件名) #获得文件目录
tennga.getfiles(文件夹) #获得虚文件下所有文件目录
```



## 源格式 utf-8 json

```json
{
    "目录1":[
        {"name":"文件1",
         "urls":["http://www.baidu.com",
                "block://块名1/文件名"
               ]
         "uuid" : "f0645603-2fc6-4007-82e6-b731b8920b5b"
        },
    ],
    "目录2":[
        
    ],
    "blocks":[
        {
            "name":"块名1",
            "url":"http://www.baidu.com/xx.block",
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

## block文件

以tar归档的文件。不能包含文件夹，是多个文件被裸归档的。

block链接：block://block名/文件名.扩展名

其中，程序会先从blocks目录中查找block块，如果没有，会尝试从源中下载对应block。然后再从block中获取文件。通常用于应对过于散碎的批量文件，比如一个源中全是图片。

block是固定的。也就是说同名block只能上传一次。下次如果要更改请制作新的block。因为程序会主动检查是否存在对应block。如果压缩错了重新修改上传了，也不会被重新下载。因此建议如果修改，请使用新的block。

## 源制作器

```python
from tennga import srcmake
srcmake.openSourceFile(name)
srcmake.addFile(srcfile, floder, filename)
srcmake.addLink(srcfile, floder, filename, link)
srcmake.addKV(srcfile, floder, filename, key, value)
srcmake.addBlock(srcfile, blockname)
srcmake.addBlockLink(srcfile, blockname, link)
srcmake.save(name,srcfile)
```



## 预计功能（v2.0.0）

提供一个源管理器和制作器的UI

使用：

python -m tennga

可以导出两个文件:

tennga.html #这是tennga管理器页面，放在static目录下即可

tennga.py #这是flask的蓝图，可以直接注册使用

可以使用iframe导入tennga集成到flask软件中使用。