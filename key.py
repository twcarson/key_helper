

class Node:
    def __init__(self,index,description,parent):
        self.index = index
        self.description = description
        self.parent = parent
    def set_parent(self,parent):
        if self.parent is None:
            self.parent = parent
            return 0
        return 1

class NonTerminalNode(Node):
    def __init__(self,index,description='',parent=None,lchild=None,rchild=None):
        super().__init__(index,description,parent)
        self.lchild = lchild
        self.rchild = rchild
    def attach_child(self,child_node,position=-1):
        return_val = 0
        match position:
            case 0: # attach lchild
                if self.lchild is None:
                    self.lchild=child_node
                else:
                    return_val = 1
            case 1: # attach rchild
                if self.rchild is None:
                    self.rchild=child_node
                else:
                    return_val = 1
            case _:
                if self.lchild is None:
                    self.lchild=child_node
                elif self.rchild is None:
                    self.rchild=child_node
                else:
                    return_val=1
        if return_val == 0:
            return_val = child_node.set_parent(self)
        # 0 is OK.  1 is failure
        return return_val
        
    def leaves(self):
        # assumes the key is complete and valid
        return self.lchild.leaves() + self.rchild.leaves()
    
    
class TerminalNode(Node):
    def __init__(self,index,description='',parent=None,leaf=None):
        super().__init__(index,description,parent)
        self.leaf=leaf
    def attach_leaf(self,leaf):
        if self.leaf is None:
            self.leaf=leaf
            return 0
        return 1
    def leaves(self):
        return [self.leaf]
    
class Leaf:
    def __init__(self,title,data):
        self.title=title
        self.data=data
    
class Key:
    def __init__(self,root_node=None):
        self.leaves = []
        self.root = root_node
        
    def insert_node(self,node,parent):
        # TODO: type validation
        return
    def replace_node(self,old_node,new_node):
        return
    def grow_leaves(self):    
        self.leaves = self.root.leaves()
        return
    def print_key(self):
        self.print_branch(self.root,0)
        return
    def print_branch(self,node,depth=0):
        # assumes the branch is complete and valid
        try:
            print(node.index, '-'*depth, node.description)
            self.print_branch(node.lchild,depth+1)
            self.print_branch(node.rchild,depth+1)
        except AttributeError:
            print('  ', '-'*2*depth, node.leaf.title)
            

def plaintext_file_to_key(key_file):
    with open(key_file,'r') as inf:
        # read in file.  get rid of extraneous whitespace
        lines = [l.strip() for l in list(filter(None,inf.read().split('\n')))]
    # grab genus name
    genus = lines[0].split()[-1]
    # throw away all lines not part of the numbered key
    lines = [l for l in list(filter(lambda x : x[0].isdigit(), lines))]

    # as far as I can tell, all jepson key pages have at least two taxa
    root = NonTerminalNode('0.',genus,None,None,None)    
    key = Key(root)
    index_stack = [root]
    for l in lines:
        index,rest = l.split(' ', 1)
        parts = rest.split(' ..... ')
        if len(parts) == 1: # non-terminal
            node=NonTerminalNode(index,rest,None,None,None)
        elif len(parts) == 2: # terminal node, taxon follows "....."
            leaf=Leaf(parts[1],'')
            node=TerminalNode(index,parts[0],None,leaf)
        position = 1 if index.endswith("'") else 0 
        node.set_parent(index_stack[-1])
        index_stack[-1].attach_child(node,position)
        if position == 1:
            index_stack.pop()
        if len(parts) == 1:
            index_stack.append(node)
    key.grow_leaves()
    return key

