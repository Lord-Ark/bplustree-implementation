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

            # compare on the basis of operator and value provided in the function

            skval = pageArray[i]
            leafNode = findInTree(rel, att, sk)
            if(leafNode == ''):                 # No tree found
                npage = createLeafNode('L', rel, att, sk, skval, odd)
                direcmain = read("../index/directory.txt")
                direcmain.push([rel,att,npage]);
                write(direcmain,"../index.directory.txt")   # insert tree in directory
            else:
                leafNodeData = read("../index/"+leafNode)
                if leafNode:  # if leaf node is full
                    splittheleaf(leafNode)
                else:
                    insertinleafnode(leafNodeData, sk, skval)
    #
    #
    return

def traverseInTree(pno,sk):
    page = read("../index/"+pno)
    if(page.type=='L'):
        return page;
    else:
        allval=page.value;
        for i in range(len(allval)):
            if(sk < allval[i].key):
                traverseInTree(allval[i].leftNode,sk)
            elif((sk >= allval[i].key and sk < allval[i+1].key) or(sk>=allval[i].key and i==len(allval)-1)):
                traverseInTree(allval[i].rightNode,sk)


def findInTree(rel, att, sk):
    direc = read("../index/directory.txt")
    rootpage=''
    for item in direc:
        if(item[0] == rel and item[1] == att):
            rootpage = item[2]
    if(rootpage != ''):
        page = traverseInTree(rootpage,sk)
        return page
    else:
        return rootpage


def insertinleafnode(leafNodeData, sk, skval):
    node = leafNodeData
    if(node.index(sk)):
        node.value[:node.index(sk)].push(skval)
    else:
        node.key.push(sk)
        node.value.push(skval)

    return


def createLeafNode(rel, att, sk, skval, odd):
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    nodep = {}
    print('new leaf')
    nodep.type = 'L'
    nodep.value = []
    node = {}
    node.leftNode = None
    node.rightNode = None
    node.key = sk
    node.value = [skval]
    node.value.push(node)
    # create a leaf node and write the lpage in the indexfolder
    json.dumps(nodep)
    write(nodep, lpage)
    return lpage
    # create a internal node and write the lpage in the indexfolder


def createInternalNode(rel, att, sk, ln, rn, odd):
    pagepool = read("../index/pagePool.txt")
    lpage = pagepool.pop()
    nodep = {}
    print('new leaf')
    nodep.type = 'I'
    nodep.value = []
    node = {}
    node.leftNode = ln
    node.rightNode = rn
    node.key = sk
    node.value.push(node)
    json.dumps(nodep)
    write(nodep, lpage)
    return lpage


def splittheleaf(leafNode):
    #
    return


def write(text, page):
    f = open(page, 'w')
    f.write(json.dump(text))


build('Products', 'pid', 2)
