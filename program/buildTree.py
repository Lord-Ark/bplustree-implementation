import json
from pathlib import Path
import pdb

relation = ''
order = 1
attribute = ''

def read(path):
    f = open(path)
    return json.load(f)

# finding the position of attribute in the tupple


def findLocationOfAtrrInTupple(rel, att):
    schema = read("../data/schemas.txt")
    for item in schema:
        if (item[0] == str.capitalize(rel) and item[1] == att):
            return item[3]

def checkBtreeOnRelAndAtt(rel,att):
    direc = read("../index/directory.txt")
    rootpage = ''  
    for item in direc:
        if(item[0] == rel and item[1] == att):
            rootpage = item[2]
    return rootpage

def build(rel, att, odd):
    # pdb.set_trace()
    if(checkBtreeOnRelAndAtt(rel,att) != ''):
        print('B+ tree on <'+rel+','+att+'> already exist')
        return 
        
    global relation
    relation = rel
    global order
    order = odd
    global attribute
    attribute = att
    pagelink = "../data/"+rel+"/pageLink.txt"
    pageArray = read(pagelink)              # read the pagelink file
    pos = findLocationOfAtrrInTupple(rel, att)

    for i in range(len(pageArray)):
        page = read('../data/'+rel+'/'+pageArray[i])

        for j in range(len(page)):
            sk = page[j][pos]
            skval = pageArray[i]
            leafNodeReturn = findInTree(rel, att, sk)
            leafNode = leafNodeReturn['page']
            if(leafNode == ''):                 # No tree found
                nodeitem = {}
                nodeitem['key'] = sk
                nodeitem['value'] = [skval]
                npage = createLeafNode([nodeitem], '',{'left':'','right':''}, odd)
                direcmain = read("../index/directory.txt")
                direcmain.append([rel, att, npage])
                # insert tree in directory
                write(direcmain, "../index/directory.txt")
            else:
                leafNodeData = read("../index/"+leafNode['page'])
                newleaf = insertinleafnode(leafNodeData, sk, skval)
                if len(newleaf['nodevalue']) > (2*odd):  # if leaf node is full
                    splittheleaf(newleaf, odd, rel)
                else:
                    write(newleaf, "../index/"+newleaf['page'])

    return


def traverseInTree(pno, sk, traverseCost):
    # pdb.set_trace()
    page = read("../index/"+pno)
    traverseCost = traverseCost+1
    if(page['type'] == 'L'):
        return {'page': page,'cost':traverseCost}
    else:
        allval = page['nodevalue']
        for i in range(len(allval)):
            if(sk < allval[i]['key']):
                return traverseInTree(allval[i]['leftNode'], sk, traverseCost)
            elif((sk >= allval[i]['key'] and i == len(allval)-1) or (sk >= allval[i]['key'] and sk < allval[i+1]['key'])):
                return traverseInTree(allval[i]['rightNode'], sk, traverseCost)


def findInTree(rel, att, sk):
    # pdb.set_trace()
    direc = read("../index/directory.txt")
    rootpage = ''
    traverseCost = 0    #not working
    for item in direc:
        if(item[0] == rel and item[1] == att):
            rootpage = item[2]
    if(rootpage != ''):
        result = traverseInTree(rootpage, sk, traverseCost)
        return {'page': result['page'], 'cost': result['cost']}
    else:
        return {"page": rootpage, "cost": traverseCost}


def findKeyInNode(node, sk):
    # # pdb.set_trace()
    for nodeitem in node['nodevalue']:
        if(nodeitem['key'] == sk):
            return True
    return False


def insertinleafnode(leafNodeData, sk, skval):
    # pdb.set_trace()
    node = leafNodeData
    if(findKeyInNode(node, sk)):
        # append value in the array where key = sk
        for nodeitem in node['nodevalue']:
            if(nodeitem['key'] == sk):
                nodeitem['value'].append(skval)

    else:
        # insert in node
        tempnode = {}
        tempnode['key'] = sk
        tempnode['value'] = [skval]
        node['nodevalue'].append(tempnode)
        node['nodevalue'].sort(key=lambda x: x['key'])
        # node['value'][:node.index(sk)].append(skval)
        # insert in the node the key and value but in sorted manner

    return node


def insertininternalnode(internalnode, nodeitem,ln,rn, odd, rel):
    # pdb.set_trace()
    node = internalnode
    # sort the nodevalue
    node['nodevalue'].append(nodeitem)
    node['nodevalue'].sort(key=lambda x: x['key'])
    leftleaf = read('../index/'+ln)
    leftleaf['parent'] = node['page']
    write(leftleaf,'../index/'+ln)
    rightleaf = read('../index/'+rn)
    rightleaf['parent'] = node['page']
    write(rightleaf,'../index/'+rn)
    
    if(len(node['nodevalue']) > (2*odd)):
        # split the internal node
        source_list = node['nodevalue']
        N = odd
        new_left_list = []
        for index in range(0, N):
            new_left_list.append(source_list[index])
        new_right_list = []
        for index in range(N+1, len(node['nodevalue'])):
            new_right_list.append(source_list[index])

        parent = node['parent']

        leftinternal ={};
        leftinternal['parent'] = parent
        leftinternal['page']=node['page']
        leftinternal['type'] ='I'
        leftinternal['nodevalue']= new_left_list   
        
        write(leftinternal, "../index/"+node['page'])

        npage = createInternalNode(new_right_list, parent, odd)

        copyToParent(source_list[N]['key'], parent,node['page'], npage, rel, odd)
    else:
        write(node, "../index/"+node['page'])

    return node


def createLeafNode(leafitems, parent, siblings, odd):
    # pdb.set_trace()
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    write(pagepool,"../index/pagePool.txt")
    nodep = {}
    nodep['page'] = lpage
    nodep['parent'] = parent
    nodep['type'] = 'L'
    nodep['nodevalue'] = []
    if(siblings):
        nodep['leftSibiling'] = siblings['left']
        nodep['rightSibiling'] = siblings['right']
    else:
        nodep['leftSibiling'] = ''
        nodep['rightSibiling'] = ''

    for item in leafitems:
        node = {}
        node['key'] = item['key']
        node['value'] = item['value']
        nodep['nodevalue'].append(node)
    # create a leaf node and write the lpage in the indexfolder
    write(nodep, "../index/"+lpage)
    return lpage
    # create a internal node and write the lpage in the indexfolder


def createInternalNode(nodeitems, parent, odd):
    # pdb.set_trace()
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    write(pagepool,"../index/pagePool.txt")
    nodep = {}
    nodep['page'] = lpage
    nodep['parent'] = parent
    nodep['type'] = 'I'
    nodep['nodevalue'] = []
    for item in nodeitems:
        node = {}
        node['leftNode'] = item['leftNode']
        # change the parent of the leaf nodes
        leftNode = read("../index/"+item['leftNode'])
        leftNode['parent']=lpage
        write(leftNode,"../index/"+item['leftNode'])
        node['rightNode'] = item['rightNode']
        rightNode = read("../index/"+item['rightNode'])
        rightNode['parent']=lpage
        write(rightNode,"../index/"+item['rightNode'])
        node['key'] = item['key']
        nodep['nodevalue'].append(node)
    write(nodep, "../index/"+lpage)
    return lpage


def splittheleaf(leafNode, odd, rel):

    # pdb.set_trace()
    source_list = leafNode['nodevalue']
    N = odd
    new_left_list = []
    for index in range(0, N):
        new_left_list.append(source_list[index])
    new_right_list = []
    for index in range(N, len(leafNode['nodevalue'])):
        new_right_list.append(source_list[index])
    
    parent = leafNode['parent']

    leftleaf ={};
    leftleaf['page']=leafNode['page']
    leftleaf['parent'] = leafNode['parent']
    leftleaf['type'] ='L'
    leftleaf['nodevalue']= new_left_list
    leftleaf['leftSibiling'] = leafNode['leftSibiling']
    
    npage = createLeafNode(new_right_list, parent,{'left':leftleaf['page'],'right': ''}, odd)
    
    leftleaf['rightSibiling'] = npage
    write(leftleaf, "../index/"+leftleaf['page'])

    

    copyElem = new_right_list[0]['key']

    copyToParent(copyElem, parent, leftleaf['page'], npage, rel, odd)
    return


def copyToParent(elem, parent, ln, rn, rel, odd):
    # pdb.set_trace()
    if(parent == ""):
        nodeitem={};
        nodeitem['key'] = elem
        nodeitem['leftNode'] = ln
        nodeitem['rightNode'] = rn
        parentpage = createInternalNode([nodeitem], parent, odd)
        leftleaf = read('../index/'+ln)
        leftleaf['parent'] = parentpage
        write(leftleaf,'../index/'+ln)
        rightleaf = read('../index/'+rn)
        rightleaf['parent'] = parentpage
        write(rightleaf,'../index/'+rn)

        directoryelem = read("../index/directory.txt")
        for item in directoryelem:
            if(item[0]==relation and item[1]==attribute):
                item[2] = parentpage
        write(directoryelem,"../index/directory.txt")
        #change the rootpage in directory
    else:
        inode = read('../index/'+parent)
        nodeitem = {}
        nodeitem['key'] = elem
        nodeitem['leftNode'] = ln
        nodeitem['rightNode'] = rn
        insertininternalnode(inode, nodeitem,ln,rn, odd, rel)
    return


def write(text, page):
    with open(page, 'w') as f:
        json.dump(text, f)


# build('Supply', 'pid', 2)
