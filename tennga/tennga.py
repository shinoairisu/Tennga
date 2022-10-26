import requests

def init():
    """
    新建文件夹srcf,srcf/blocks,srcf/srcs,srcf/src.json
    """
    pass

def listsrc() -> list:
    """
    返回src按顺序
    """
    pass

def add(url) -> str:
    """
    将一个源加入src.json
    """
    pass

def remove(url) -> str:
    """
    url可以是链接，也可以是list返回的数字
    删除源从src.json
    删除源文件从srcf/srcs
    """
    pass

def update() -> str:
    """
    更新与使用源 下载所有源文件到srcf/srcs下面
    返回所有失败以及成功
    """
    pass

def search(name) -> list:
    """
    name 是一个模糊查询。list 返回name以及对应源url。
    返回空就是失败
    """
    pass

def donwload(name,dcallback=None) -> str:
    """
    name 是绝对文件名,一个字不能差
    dcallback  用于处理下载的半成品源,默认是直接保存content
    返回所有失败以及相关内容
    """
    pass