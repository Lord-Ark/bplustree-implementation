import json
from pathlib import Path


def read(path):
    f = open(path)
    return json.load(f)

# finding the position of attribute in the tupple


def findLocationOfAtrrInTupple(rel, att):
    schema = read("../data/schemas.txt")
    for item in schema:
        if (item[0] == str.capitalize(rel) and item[1] == att):
            return item[3]


def build(rel, att, odd):
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
                nodeitem['value'] = sk
                npage = createLeafNode([nodeitem], '', odd)
                direcmain = read("../index/directory.txt")
                direcmain.append([rel, att, npage])
                print(direcmain)
                # insert tree in directory
                write(direcmain, "../index/directory.txt")
            else:
                leafNodeData = read("../index/"+leafNode['page'])
                newleaf = insertinleafnode(leafNodeData, sk, skval)
                if len(newleaf['nodevalue']) > (2*odd):  # if leaf node is full
                    splittheleaf(newleaf, odd, rel)
                else:
                    print('writing in leaf')
                    write(newleaf, "../index/"+newleaf['page'])

    return


def traverseInTree(pno, sk, traverseCost):

    page = read("../index/"+pno)
    traverseCost = traverseCost+1
    if(page['type'] == 'L'):
        return page
    else:
        allval = page['nodevalue']
        for i in range(len(allval)):
            if(sk < allval[i]['key']):
                traverseInTree(allval[i]['leftNode'], sk)
            elif((sk >= allval[i]['key'] and sk < allval[i+1]['key']) or (sk >= allval[i]['key'] and i == len(allval)-1)):
                traverseInTree(allval[i]['rightNode'], sk)


def findInTree(rel, att, sk):
    direc = read("../index/directory.txt")
    rootpage = ''
    traverseCost = 0
    for item in direc:
        if(item[0] == rel and item[1] == att):
            rootpage = item[2]
    if(rootpage != ''):
        page = traverseInTree(rootpage, sk, traverseCost)
        return {'page': page, 'cost': traverseCost}
    else:
        return {"page": rootpage, "cost": traverseCost}


def findKeyInNode(node, sk):
    for nodeitem in node['nodevalue']:
        if(nodeitem['key'] == sk):
            return True
    return False


def insertinleafnode(leafNodeData, sk, skval):
    node = leafNodeData
    if(findKeyInNode(node, sk)):
       # node['key']
        print('append in value ')
        # append value in the array where key = sk

        # tempnode ={}
        # tempnode['key'] = sk
        # tempnode['value'] = skval
        # # node.
        # node.append(tempnode)
    else:
        print('insert in node')
        tempnode = {}
        tempnode['key'] = sk
        tempnode['value'] = [skval]
        node['nodevalue'].append(tempnode)
        node['nodevalue'].sort(key=lambda x: x['key'])
        # node['value'][:node.index(sk)].append(skval)
        # insert in the node the key and value but in sorted manner

    return node


def insertininternalnode(internalnode, nodeitem, odd, rel):
    node = internalnode
    node['nodevalue'].append(nodeitem)
    node['nodevalue'].sort(key=lambda x: x.key)
    # sort the nodevalue
    if(node['nodevalue'] > (2*odd)):
        print('split internal node')
        # split the internal node
        leftnode = node['nodevalue'][:odd]
        parent = node['parent']
        newLeftNode = node
        newLeftNode['nodevalue'] = leftnode
        write(newLeftNode, "../index/"+newLeftNode['page'])

        rightnode = node['nodevalue'][-odd:]
        npage = createInternalNode(rightnode, parent, odd)
        copyToParent(node['nodevalue'][odd+1], parent,
                     newLeftNode['page'], npage, rel, odd)
    else:
        write(node, "../index/"+node['page'])

    return node


def createLeafNode(leafitems, parent, odd):
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    write(pagepool,"../index/pagePool.txt")
    nodep = {}
    print('new leaf')
    nodep['page'] = lpage
    nodep['parent'] = parent
    nodep['type'] = 'L'
    nodep['nodevalue'] = []
    for item in leafitems:
        node = {}
        node['key'] = item['key']
        node['value'] = item['value']
        nodep['nodevalue'].append(node)
    # create a leaf node and write the lpage in the indexfolder
    # newnode = json.dumps(nodep)
    write(nodep, "../index/"+lpage)
    return lpage
    # create a internal node and write the lpage in the indexfolder


def createInternalNode(nodeitems, parent, odd):
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    nodep = {}
    print('new internal node')
    nodep['page'] = lpage
    nodep['parent'] = parent
    nodep['type'] = 'I'
    nodep['nodevalue'] = []
    for item in nodeitems:
        node = {}
        node['leftNode'] = item['ln']
        node['rightNode'] = item['rn']
        node['key'] = item['sk']
        nodep['nodevalue'].append(node)
    # newnode = json.dumps(nodep)
    write(nodep, "../index/"+lpage)
    return lpage


def splittheleaf(leafNode, odd, rel):
    #
    lstodd = odd+1
    leftleaf = leafNode['nodevalue'][:odd]
    parent = leafNode['parent']
    newLeftLeaf = leafNode
    newLeftLeaf['nodevalue'] = leftleaf
    write(newLeftLeaf, "../index/"+newLeftLeaf['page'])

    rightleaf = leafNode['nodevalue'][-lstodd:]
    npage = createLeafNode(rightleaf, parent, odd)

    copyElem = rightleaf['nodevalue'][0]['key']

    copyToParent(copyElem, parent, newLeftLeaf['page'], npage, rel, odd)
    return


def copyToParent(elem, parent, ln, rn, rel, odd):
    inode = read('../data/'+rel+'/'+parent)
    nodeitem = {}
    nodeitem['key'] = elem
    nodeitem['leftNode'] = ln
    nodeitem['rightNode'] = rn
    insertininternalnode(inode, nodeitem, odd, rel)
    return


def write(text, page):
    with open(page, 'w') as f:
        json.dump(text, f)


build('Products', 'pid', 1)
