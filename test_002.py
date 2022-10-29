import json
from tennga import srcmake
from pytest_mock import MockerFixture
import logging


#测试打开文件
def test_open(mocker: MockerFixture):
    j = mocker.spy(json, "loads")
    js = srcmake.openSourceFile("test.json")
    logging.info(js)
    assert j.called


def test_addFile():
    js = srcmake.openSourceFile("test.json")
    sa = srcmake.addFile(js, "拉拉", "已奔赴")
    logging.info(sa)


def test_addLink():
    js = srcmake.openSourceFile("test.json")
    sa = srcmake.addFile(js, "拉拉", "已奔赴")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu.com")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu2.com")
    logging.info(sa)


def test_addKV():
    js = srcmake.openSourceFile("test.json")
    sa = srcmake.addFile(js, "拉拉", "已奔赴")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu.com")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu2.com")
    sa = srcmake.addKV(sa, "拉拉", "已奔赴", "吃饭", 15)
    sa = srcmake.addKV(sa, "拉拉", "已奔赴", "睡觉", 16)
    logging.info(sa)


def test_addBlock():
    js = srcmake.openSourceFile("test.json")
    sa = srcmake.addFile(js, "拉拉", "已奔赴")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu.com")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu2.com")
    sa = srcmake.addKV(sa, "拉拉", "已奔赴", "吃饭", 15)
    sa = srcmake.addKV(sa, "拉拉", "已奔赴", "睡觉", 16)
    sa = srcmake.addBlock(sa, "波波")
    logging.info(sa)


def test_addBlockLink():
    js = srcmake.openSourceFile("test.json")
    sa = srcmake.addFile(js, "拉拉", "已奔赴")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu.com")
    sa = srcmake.addLink(sa, "拉拉", "已奔赴", "http://www.baidu2.com")
    sa = srcmake.addKV(sa, "拉拉", "已奔赴", "吃饭", 15)
    sa = srcmake.addKV(sa, "拉拉", "已奔赴", "睡觉", 16)
    sa = srcmake.addBlock(sa, "波波")
    sa = srcmake.addBlockLink(sa, "波波", "http://www.xx.cc")
    logging.info(sa)


def test_save(mocker: MockerFixture):
    js = srcmake.openSourceFile("test.json")
    sa = srcmake.addFile(js, "目录1", "软件1")
    sa = srcmake.addLink(sa, "目录1", "软件1", "http://www.baidu.com")
    sa = srcmake.addLink(sa, "目录1", "软件1", "http://www.baidu2.com")
    sa = srcmake.addLink(sa, "目录1", "软件1", "block://波波/xx.jpg")
    sa = srcmake.addKV(sa, "目录1", "软件1", "吃饭", 15)
    sa = srcmake.addKV(sa, "目录1", "软件1", "睡觉", 16)
    sa = srcmake.addFile(sa, "目录2", "软件2")
    sa = srcmake.addLink(sa, "目录2", "软件2", "http://www.baidu.com")
    sa = srcmake.addLink(sa, "目录2", "软件2", "http://www.baidu2.com")
    sa = srcmake.addBlock(sa, "块1")
    sa = srcmake.addBlockLink(sa, "块1", "http://www.xx.cc/xx.block")
    logging.info(sa)
    sj = mocker.spy(json, "dumps")
    srcmake.save("test.json",sa)
    assert sj.called
