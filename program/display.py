
from buildTree import read
from buildTree import write
from buildTree import traverseAllNode
import json

def displayTree(filename):
    if(filename != ''):
        allitem = traverseAllNode(filename)
        seen_pages = set()
        new_list = []
        for obj in allitem:
            if obj['page'] not in seen_pages:
                new_list.append(obj)
                seen_pages.add(obj['page'])
       
        direc = read("../index/directory.txt")
        treeitem = ''  
        for item in direc:
            if(item[2] == filename):
                treeitem = item

        if(treeitem != ''):
            f = open("../treePic/"+treeitem[0]+"_"+treeitem[1]+".txt", "w")
            for item in new_list:
                if(item['type']=='I' and item['parent'] !=''):
                    f.write('\t')
                if(item['type']=='L'):
                    f.write('\t')
                    f.write('\t')    
                f.write(str(item))
                f.write('\n')
            f.close()

def displayTable(relName):
    if(relName!= ''):
        pagelink = "../data/"+relName+"/pageLink.txt"
        pageArray = read(pagelink)          

        results=[]
        for pages in pageArray:
            pageitem = read("../data/"+relName+"/"+pages)
            results.append(pageitem)
        
        page = "../queryOutput/queryResult.txt"
        with open(page, 'a') as f:
            f.write('\n')
            for item in results:
                json.dump(item, f)
                f.write("\n")
            f.write("\n\n\n")
            f.write("------------------------------------------------------------")
            f.write("\n")

# displayTree('pg30.txt')