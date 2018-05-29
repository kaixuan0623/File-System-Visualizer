if mouse_check:
    # This checks which rectangle is currently being clicked
    # by mouse.
    # Notice that left hand side is '<=', and right is '<'.

    selected_leaf = tree.get_leaf(rect0, t_rect[0])
    # Now, selected_leaf refer to a FileSystemTree object.
    data_size = '(' + str(selected_leaf.data_size) + ')'
    text = selected_leaf.get_separator() + ' ' + data_size
    render_display(screen, tree, text)
    break

elif ((curr_rect[0] <= x < (curr_rect[0] + curr_rect[2])) and (
        curr_rect[1] <= y < (curr_rect[1] + curr_rect[3]))) and (
    selected_leaf is not None):
    # This is the case that the user clicks again on the
    # currently-selected rectangle, and thus this rectangle
    # becomes unselected.
    selected_leaf = None
    text = ''
    render_display(screen, tree, text)
    break

elif (not ((curr_rect[0] <= x < (curr_rect[0] + curr_rect[2])) and (
        curr_rect[1] <= y < (curr_rect[1] + curr_rect[3])))) and (
    selected_leaf is not None):
    selected_leaf = tree.get_leaf(rect0, t_rect[0])
    data_size = '(' + str(selected_leaf.data_size) + ')'
    text = selected_leaf.get_separator() + ' ' + data_size
    render_display(screen, tree, text)
    break


def delete_leaf_version_2(leaf):
    """
    >>> t0 = AbstractTree('o', [])
    >>> t1 = AbstractTree('a', [])
    >>> t2 = AbstractTree('b', [])
    >>> t3 = AbstractTree('c', [])
    >>> t = AbstractTree('x', [t1, t2, t3])
    >>> delete_leaf_version_2(t1)
    >>> len(t._subtrees)
    2
    >>> t._subtrees[0]._root
    'b'
    >>> t._subtrees[1]._root
    'c'
    >>> f1 = AbstractTree(1, [])
    >>> f2 = AbstractTree(2, [])
    >>> f3 = AbstractTree(3, [])
    >>> f4 = AbstractTree('4', [f3])
    >>> f = AbstractTree('f', [f1, f2, f4])
    >>> delete_leaf_version_2(f3)
    >>> len(f._subtrees)
    3
    >>> f._subtrees[2]._root
    '4'
    >>> f._subtrees[2]._subtrees
    []
    """

    leaf._parent_tree._subtrees.remove(leaf)
