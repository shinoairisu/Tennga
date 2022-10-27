import glob
import json
import os
import shutil
import tarfile
import requests


def init():
    """
    新建文件夹srcf,srcf/blocks,srcf/srcs
    """
    os.makedirs("srcf/blocks", exist_ok=True)
    os.makedirs("srcf/srcs", exist_ok=True)
    if not os.path.exists("srcf/src.json"):
        with open("srcf/src.json", "w", encoding="utf-8") as f:
            f.write(json.dumps([]))


def listsrc() -> list:
    """
    返回src按顺序
    """
    srcs = None
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())
    return srcs


def add(url) -> str:
    """
    将一个源加入src.json
    比如 http://www.baidu.com/xxx.json
    """
    srcs = None
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())

    with open("srcf/src.json", "w", encoding="utf-8") as f:
        srcs.append(url)
        srcs = list(set(srcs))
        f.write(json.dumps(srcs))


def remove(url) -> str:
    """
    url可以是链接，也可以是list返回的数字
    删除源从src.json
    删除源文件从srcf/srcs
    """
    srcs = None
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())
    try:
        if isinstance(url, str):
            srcs.remove(url)
        elif isinstance(url, int):
            del srcs[url]
    except:
        print("删除内容不存在...")
        return
    with open("srcf/src.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(srcs))


def update() -> str:
    """
    更新与使用源 下载所有源文件到srcf/srcs下面
    返回所有失败以及成功
    """
    result = ""
    srcs = None
    shutil.rmtree("srcf/srcs")
    os.makedirs("srcf/srcs", exist_ok=True)
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())
    for i in srcs:
        try:
            res = requests.get(i)
        except:
            result += f"{i},failed\n"
            continue
        if res.status_code == 200:
            _, filename = os.path.split(i)
            with open(f"srcf/srcs/{filename}", "wb") as f:
                f.write(res.content)
            result += f"{i},ok\n"
        else:
            result += f"{i},failed\n"
    return result


def search(name: str, time: str = None) -> list:
    """
    name 是一个模糊查询
    time: 年/月/日 -> 这是一个类似id的标记
    list 返回所有name
    返回空就是失败
    """
    srcs = glob.glob("srcf/srcs/*.json")
    files = []
    for i in srcs:
        jswen = None
        with open(i, "r", encoding="utf-8") as f:
            jswen = json.loads(f.read())
            del jswen["blocks"]
        for j in jswen:
            for z in jswen[j]:
                if z["name"].find(name) > -1:
                    files.append([z["name"], "0/0/0"])
                if time != None:
                    if "time" in z and time == z["time"]:
                        files[-1][1] = z["time"]
                    else:
                        del files[-1]
                else:
                    if "time" in z:
                        files[-1][1] = z["time"]
    return files


def donwload(name, time=None, dcallback=None) -> str:
    """
    下载或更新
    name 是绝对文件名,一个字不能差
    dcallback  用于处理下载的半成品源,默认是直接保存content
    返回失败
    """
    srcs = glob.glob("srcf/srcs/*.json")
    for i in srcs:
        jswen = None
        blocks = None
        with open(i, "r", encoding="utf-8") as f:
            jswen = json.loads(f.read())
            blocks = jswen["blocks"] if "blocks" in jswen else None
            del jswen["blocks"]
            
        for j in jswen:
            for z in jswen[j]:
                if time != None:
                    if "time" in z and time == z["time"] and z["name"] == name:
                        
                        texts= __download(z,blocks,dcallback)
                        return texts
                else:
                    if z["name"] == name:
                        texts= __download(z,blocks,dcallback)
                        return texts
    return "failed"

def __download(filedic,blocks=None,dcallback=None) -> str:
    os.makedirs(f"srcf/{filedic['name']}", exist_ok=True)
    links = filedic['url']
    texts=""
    for i in links:
        link = i.strip()
        if link[0:4] == "http":
            _, filename = os.path.split(i)
            try:
                res = requests.get(link)
                if cont.status_code != 200:
                    texts+=f"{filename},failed\n"
                    continue
            except:
                if os.path.exists(f"srcf/{filedic['name']}/{filename}"):
                    texts+=f"{filename},ok\n"
                    continue
            cont = res.content
            if dcallback:
               cont = dcallback(res,filedic) #返回处理后的文件
            with open(f"srcf/{filedic['name']}/{filename}","wb") as f:
                f.write(cont)
                texts+=f"{filename},ok\n"
        elif link[0:5] == "block":
            cont,res = __blockReader(link,blocks)
            _, filename = os.path.split(i)
            if res == "ok":
                with open(f"srcf/{filedic['name']}/{filename}","wb") as f:
                    f.write(cont)
                texts+=f"{filename},ok\n"
            else:
                texts+=f"{filename},failed\n"
    return texts


def __blockReader(blockurl,blocks) -> "bytes,str":
    blockfile = __getmidstring(blockurl,"//","/")
    _, filename = os.path.split(blockurl)
    if not os.path.exists(f"srcf/blocks/{blockfile}.block"):
        co = 0
        for i in blocks:
            if i["name"] == blockfile:
                try:
                    cont = requests.get(i["url"])
                    if cont.status_code != 200:
                        return None,"failed"
                except:
                    return None,"failed"
                with open(f"srcf/blocks/{blockfile}.block","wb") as f:
                    f.write(cont.content)
                co+=1
                break
        if co==0:
            return None,"failed"
    tar = tarfile.open(f"srcf/blocks/{blockfile}.block")
    for i in tar.getmembers():
        if i.name == filename:
            f=tar.extractfile(i)
            content=f.read()
            return content,"ok"
    return None,"failed"


def __getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()