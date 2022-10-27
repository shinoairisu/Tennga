from tennga import tennga

if __name__ =="__main__":
    tennga.init()
    # tennga.add("http://www.baidu.com/xx.json")
    # tennga.add("http://www.baidu.com/xx2.json")
    # tennga.add("http://localhost:8000/test.json")
    # tennga.add("http://localhost:8000/test.json")
    f = tennga.listsrc()
    for i,j in enumerate(f):
        print(i,j)
    result = tennga.update()
    # print(result)
    # s=tennga.search("vv","2022/10/26")
    # print(s)
    print(tennga.donwload("vv5"))

    