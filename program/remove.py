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

def removeTable(rel):

    if(os.path.isdir('../data/'+rel)):     
        pagelink = read("../data/"+rel+"/pageLink.txt")
        
        # remove pages from rel and add in pagepool
        pagepool = read("../data/pagePool.txt")        
        for pageno in pagelink:
            os.remove("../data/"+rel+"/"+pageno)
            pagepool.append(pageno)
            write(pagepool,"../data/pagePool.txt")
        
        
        #remove from schema
        schema = read("../data/schemas.txt")
        newschema = list(schema)
        if(schema):
            for item in schema:
                if (item[0] == rel):
                    newschema.remove(item)
            
            write(newschema, "../data/schemas.txt")

        os.remove("../data/"+rel+"/pageLink.txt")
        os.rmdir("../data/"+rel)
    else:
        print('No such Table found as '+ rel)

    

# removeTree("Supply", "pid")
# removeTable('Join-Suppliers-Supply')
# removeTable('Projection-sname-Select-Suppliers-sid')