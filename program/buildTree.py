import json


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
            leafNodeReturn =json.loads(findInTree(rel, att, sk)) 
            leafNode = leafNodeReturn['page']
            if(leafNode == ''):                 # No tree found
                npage = createLeafNode('L', rel, att, sk, skval, odd)
                direcmain = read("../index/directory.txt")
                direcmain.append([rel, att, npage])
                # insert tree in directory
                write(direcmain, "../index.directory.txt")
            else:
                leafNodeData = read("../index/"+leafNode)
                if leafNode:  # if leaf node is full
                    splittheleaf(leafNode)
                else:
                    insertinleafnode(leafNodeData, sk, skval)

    return


def traverseInTree(pno, sk, traverseCost):

    page = read("../index/"+pno)
    traverseCost = traverseCost+1
    if(page.type == 'L'):
        return page
    else:
        allval = page.value
        for i in range(len(allval)):
            if(sk < allval[i].key):
                traverseInTree(allval[i].leftNode, sk)
            elif((sk >= allval[i].key and sk < allval[i+1].key) or (sk >= allval[i].key and i == len(allval)-1)):
                traverseInTree(allval[i].rightNode, sk)


def findInTree(rel, att, sk):
    direc = read("../index/directory.txt")
    rootpage = ''
    traverseCost = 0
    for item in direc:
        if(item[0] == rel and item[1] == att):
            rootpage = item[2]
    if(rootpage != ''):
        page = traverseInTree(rootpage, sk, traverseCost)
        return json.dumps({'page': page, 'cost': traverseCost})
    else:
        return json.dumps({'page': rootpage, 'cost': traverseCost})


def findKeyInNode(node,sk):
    for nodeitem in node['value']:
        if(nodeitem['key'] == sk):
            return True
    return False

def insertinleafnode(leafNodeData, sk, skval):
    node = leafNodeData
    if(findKeyInNode(node,sk)):
        print('insert in node')
        tempnode ={}
        tempnode['key'] = sk
        tempnode['value'] = [skval]
        node['value'].append(tempnode)
        node['value'].sort(key=lambda x: x.key)
        # node['value'][:node.index(sk)].append(skval)
        # insert in the node the key and value but in sorted manner
    else:
        # node['key']
        print('append in value ')
        # append value in the array where key = sk

        # tempnode ={}
        # tempnode['key'] = sk
        # tempnode['value'] = skval
        # # node.
        # node.append(tempnode)

    return


def createLeafNode(rel, att, sk, skval, odd):
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    nodep = {}
    print('new leaf')
    nodep['type'] = 'L'
    nodep['value'] = []
    node = {}
    node['leftNode'] = None
    node['rightNode'] = None
    node['key'] = sk
    node['value'] = [skval]
    nodep['value'].append(node)
    # create a leaf node and write the lpage in the indexfolder
    json.dumps(nodep)
    write(nodep, lpage)
    return lpage
    # create a internal node and write the lpage in the indexfolder


def createInternalNode(rel, att, sk, ln, rn, odd):
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    nodep = {}
    print('new internal node')
    nodep['type'] = 'I'
    nodep['value'] = []
    node = {}
    node['leftNode'] = ln
    node['rightNode'] = rn
    node['key'] = sk
    nodep['value'].append(node)
    json.dumps(nodep)
    write(nodep, lpage)
    return lpage


def splittheleaf(leafNode):
    #
    return


def write(text, page):
    f = open(page, 'w')
    f.write(json.dump(text))


# build('Products', 'pid', 2)
