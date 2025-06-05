import key as k

def plaintext_file_to_key(key_file):
    with open(key_file,'r') as inf:
        # read in file.  get rid of extraneous whitespace
        lines = [l.strip() for l in list(filter(None,inf.read().split('\n')))]
    # grab genus name
    genus = lines[0].split()[-1]
    # throw away all lines not part of the numbered key
    lines = [l for l in list(filter(lambda x : x[0].isdigit(), lines))]

    # as far as I can tell, all jepson key pages have at least two taxa
    root = k.NonTerminalNode('0.','',None,None,None)    
    key = k.Key(genus,'',root)
    index_stack = [root]
    for l in lines:
        index,rest = l.split(' ', 1)
        parts = rest.split(' ..... ')
        if len(parts) == 1: # non-terminal
            node=k.NonTerminalNode(index,rest,None,None,None)
        elif len(parts) == 2: # terminal node, taxon follows "....."
            node=k.TerminalNode(index,parts[0],None,None)
            leaf=k.Leaf(parts[1],'',node)
            node.attach_leaf(leaf)
        position = 1 if index.endswith("'") else 0 
        node.set_parent(index_stack[-1])
        index_stack[-1].attach_child(node,position)
        if position == 1:
            index_stack.pop()
        if len(parts) == 1:
            index_stack.append(node)
    key.grow_leaves()
    key.grow_indices()
    return key

