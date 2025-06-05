

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
    def indices(self):
        # assumes the key is complete and valid
        return {**{self.index : self}, **self.lchild.indices(), **self.rchild.indices()}
    
    
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
    def indices(self):
        return {self.index : self}
    
class Leaf:
    def __init__(self,title,data):
        self.title=title
        self.data=data
    
class Key:
    def __init__(self,root_node=None):
        self.leaves = []
        self.indices = []
        self.root = root_node
        
    def insert_node(self,node,parent):
        # TODO: type validation
        return
    def replace_node(self,old_node,new_node):
        return
    def grow_leaves(self):    
        self.leaves = self.root.leaves()
        return
    def grow_indices(self):    
        self.indices = self.root.indices()
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
    def print_node(self,node):
        print(node.index,'   ',node.description)
        try:
            print(node.leaf.title,'   ',node.leaf.data)
        except AttributeError:
            pass
    def print_index(self,index):
        node=self.indices[index]
        try:
            print(index,'   ',node.description)
            print('..... ',node.leaf.title,'   ',node.leaf.data)
        except AttributeError:
            pass

    def path_to_root(self,node):
        if node==self.root:
            return [node]
        return [node] + self.path_to_root(node.parent)
    
    def nearest_common_ancestor(self,node_a,node_b):
        path_a = self.path_to_root(node_a)
        path_a.reverse()
        path_b = self.path_to_root(node_b)
        path_b.reverse()
        previous = None
        for i, node in enumerate(path_a):
            if path_a[i] != path_b[i]:
                return previous
            previous = node
        return previous # if this return is used, node_a == node_b 
