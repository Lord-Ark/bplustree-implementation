# bplustree-implementation

This project is the immplementation of a hypothetic database system that consists of the
simplified versions for three relational algebra operations, select, project and join, a limited form
for B+_tree index, and a few other utility functions. The language is Python. The following is a list
of functions and description for their functionalities:

• select(rel, att, op, val): Select tuples from relation rel which meet a select condition. The
select condition is formed by att, op, and val, where att is an attribute in rel, op is one of
the five strings, ‘<’, ‘<=’, ‘=’, ‘>’, ‘>=’, corresponding respectively to the comparison
operators, <, ≤, =, >, , and val is a value. Returns the name of the resulting relation. The
schema for the resulting relation is identical to that for rel.

• project(rel, attList): project relation rel on attributes in attList, which is a list of strings,
corresponding to a list of attributes in relation rel. Return the name of the resulting
relation. The schema for the resulting relation is the set of attributes in attList.

• join(rel1, att1, rel2, att2): join two relations rel1 and rel2 based on join condition rel.att1
= rel2.att2. Returns the name of the resulting relation, with schema being the union of
the schemas for rel1 and rel2, minus either att1 or att2.

• build(rel, att, od): build a B+ tree with an order of od on search key att of relation rel.
Returns a reference to the root page of the constructed B+_tree.

• removeTree(rel, att): remove the B+-tree on rel.att from the system. Its entry in the
directory is deleted and all the pages occupied are returned to the page pool. If the
B+_tree does not exist, do nothing.

• removeTable(rel): Remove the relation rel from the system. Its entry in the catalog is
deleted and all the pages occupied are returned to the page pool. If the relation does not
exist, do nothing.

• displayTree(fname): display the structure of the B+_tree with root file fname. The
parameter fname is a plain file name under index folder. Return the plain file name for
the file under treePic folder where the tree is displayed. Note that you are not required
to plot a B+_tree like the ones plotted in the lecture notes. The looking can be similar to
a nested directory hierarchy. Refer to the sample in Section 4.
• displayTable(rel, fname): display the relation instance for rel in a file with name fname.

Pre-requisites: Python 


