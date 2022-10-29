import logging
import os
import shutil
from tennga import tennga
import pytest
from pytest_mock import MockerFixture

logging.basicConfig(level=logging.DEBUG)

#测试初始化
def test_init():
    tennga.init()
    pytest.assume(os.path.exists("srcf/blocks"))
    pytest.assume(os.path.exists("srcf/srcs"))
    pytest.assume(os.path.exists("srcf/src.json"))



#测试添加源
def test_add():
    tennga.add("http://localhost:8000/test.json")
    res = tennga.listsrc()
    pytest.assume("http://localhost:8000/test.json" in res)

#测试列出源
def test_listsrc():
    tennga.add("http://localhost:8000/test.json")
    tennga.add("http://localhost:8000/test2.json")
    tennga.add("http://localhost:8000/test3.json")
    res = tennga.listsrc()
    pytest.assume("http://localhost:8000/test.json" in res)
    pytest.assume("http://localhost:8000/test2.json" in res)
    pytest.assume("http://localhost:8000/test3.json" in res)


#测试删除源
def test_remove():
    tennga.remove("http://localhost:8000/test.json")
    tennga.remove("http://localhost:8000/test2.json")
    tennga.remove("http://localhost:8000/test3.json")
    res = tennga.listsrc()
    pytest.assume("http://localhost:8000/test.json" not in res)
    pytest.assume("http://localhost:8000/test2.json" not in res)
    pytest.assume("http://localhost:8000/test3.json" not in res)

#测试更新源
def test_update():
    tennga.add("http://localhost:8000/test.json")
    tennga.update()
    pytest.assume(os.path.exists("srcf/srcs/test.json"))
    tennga.add("http://localhost:8000/test3.json")
    res = tennga.update()
    pytest.assume(res.find("failed")>-1)

#测试查找
def test_find():
    log = logging.getLogger('test_find')
    tennga.add("http://localhost:8000/test.json")
    tennga.update()
    res = tennga.find("vv")
    for i in res:
        log.info(i)
    pytest.assume(len(res)>0)
    res = tennga.find("kk")
    pytest.assume(len(res)==0)

#测试安装
def test_install():
    log = logging.getLogger('test_install')
    tennga.add("http://localhost:8000/test.json")
    tennga.update()
    res = tennga.install("目录1","vv")
    log.info("正常数据:"+res)
    pytest.assume(res.find("failed")==-1)
    pytest.assume(os.path.exists("srcf/目录1/vv"))
    res = tennga.install("目录2","vvx")
    log.info("不应该下载数据:"+res)
    pytest.assume(res.find("failed")>-1)
    pytest.assume(not os.path.exists("srcf/目录2/vvx"))
    res = tennga.install("目录2","vvz")
    log.info(res)
    pytest.assume(res.find("failed")>-1)
    pytest.assume(os.path.exists("srcf/目录2/vvz"))
    

#测试列出安装
def test_freeze():
    files = tennga.freeze("目录1")
    logging.info("1:")
    for i in files:
        logging.info(i)
    assert len(files)>0
    files = tennga.freeze()
    logging.info("2:")
    for i in files:
        logging.info(i)
    assert len(files)>0

#测试删除
def test_uninstall(mocker:MockerFixture):
    sh = mocker.spy(shutil,"rmtree")
    tennga.uninstall("目录1","vv")
    assert sh.called

#测试获取文件
def test_getfile():
    tennga.install("目录1","vv")
    pa = tennga.getfile("目录1","vv")
    logging.info(pa)
    assert pa!=None
    pa = tennga.getfile("目录1","vv")
    logging.info(pa)
    assert pa!=None
    pa = tennga.getfile("目录1","vv2")
    assert pa==None

#测试获取虚目录下文件
def test_getfiles():
    pa = tennga.getfiles("目录1")
    for i in pa:
        logging.info(i)
    assert len(pa)>0