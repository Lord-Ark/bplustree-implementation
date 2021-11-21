import json
import pdb
import os
from display import traverseAllNode

def write(text, page):
    with open(page, 'w') as f:
        json.dump(text, f)


def read(path):
    f = open(path)
    return json.load(f)

def removeTree(rel, att):
    direc = read("../index/directory.txt")
    # pdb.set_trace()
    rootpage = ''
    for item in direc:
        if(item[0] == rel and item[1] == att):
            rootpage = item[2]
            direc.remove(item)
            write(direc,"../index/directory.txt")

    if(rootpage != ''):
        print('append the value and delete')
        allitem = traverseAllNode(rootpage)
        seen_pages = set()
        new_list = []
        for obj in allitem:
            if obj['page'] not in seen_pages:
                new_list.append(obj)
                seen_pages.add(obj['page'])

        pagepool = read("../index/pagePool.txt")        
        for item in new_list:
            os.remove("../index/"+item['page'])
            pagepool.append(item['page'])

        write(pagepool,"../index/pagePool.txt")    
        # traverse all nodes and delete them
        print(len(allitem))
    return;




removeTree('Testsuppliers', 'sid')