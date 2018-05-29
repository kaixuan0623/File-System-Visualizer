"""
=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
import os
from random import randint
import math


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    @type data_size: int
        The total size of all leaves of this tree.
    @type colour: (int, int, int)
        The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    @type _root: obj | None
        The root value of this tree, or None if this tree is empty.
    @type _subtrees: list[AbstractTree]
        The subtrees of this tree.
    @type _parent_tree: AbstractTree | None
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    def __init__(self, root, subtrees, data_size=0):
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.

        @type self: AbstractTree
        @type root: object
        @type subtrees: list[AbstractTree]
        @type data_size: int
        @rtype: None

        >>> t0 = AbstractTree(None, [])
        >>> t0.data_size
        0
        >>> t1 = AbstractTree(1, [], 10)
        >>> t1.data_size
        10
        >>> t2 = AbstractTree(2, [t1])
        >>> t1.data_size
        10
        >>> t3 = AbstractTree(3, [t2])
        >>> t3.data_size
        10
        >>> t4 = AbstractTree(4, [], 100)
        >>> tx = AbstractTree('x', [t3, t4])
        >>> tx.data_size
        110
        >>> t3._parent_tree is tx
        True
        >>> t0._parent_tree is None
        True
        >>> t1._parent_tree is t2
        True
        >>> t2._parent_tree is t3
        True
        >>> t2._parent_tree is tx
        False
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None

        # 1. Initialize self.colour and self.data_size。
        # 2. Properly set all _parent_tree attributes in self._subtrees

        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))

        if root is None:
            self.data_size = 0

        elif subtrees == []:
            self.data_size = data_size

        else:
            size = 0
            for tree in subtrees:
                size += tree.data_size
                tree._parent_tree = self
            self.data_size = size

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: AbstractTree
        @rtype: bool
        """
        return self._root is None

    def generate_treemap(self, rect):
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        x, y, width, height = rect

        if self.data_size == 0:
            # This represents an empty folder.
            return []

        elif len(self._subtrees) == 0:
            # <self> is a leaf in this case (ie. represents a single file).
            return [(rect, self.colour)]

        else:
            tree_map = []
            x_tree = x
            y_tree = y

            for tree in self._subtrees:
                portion = tree.data_size / self.data_size

                if width > height and tree != self._subtrees[-1]:
                    # <tree> is not the last tree in the list of subtree.
                    subtree_width = math.floor(portion * width)

                    subtree_rect = (x_tree, y_tree, subtree_width, height)

                    combine(tree.generate_treemap(subtree_rect), tree_map)

                    x_tree += subtree_width

                elif width > height and tree == self._subtrees[-1]:
                    subtree_width = width - (x_tree - x)
                    # NOTICE THAT, the meaning for (x_tree - x) is to change
                    # the starting x coordinate of current rectangle to the x
                    # coordinate with respect to the origin (0, 0).
                    # This is extremely important and easy to ignore.
                    # Since for the import rectangle <rect>, the top-left
                    # coordinate of <rect> is not always starts at (0, 0).

                    subtree_rect = (x_tree, y_tree, subtree_width, height)

                    combine(tree.generate_treemap(subtree_rect), tree_map)

                    x_tree += subtree_width

                elif width <= height and tree != self._subtrees[-1]:
                    subtree_height = math.floor(portion * height)

                    subtree_rect = (x_tree, y_tree, width, subtree_height)

                    combine(tree.generate_treemap(subtree_rect), tree_map)

                    y_tree += subtree_height

                elif width <= height and tree == self._subtrees[-1]:
                    subtree_height = height - (y_tree - y)

                    subtree_rect = (x_tree, y_tree, width, subtree_height)

                    combine(tree.generate_treemap(subtree_rect), tree_map)

                    y_tree += subtree_height

            return tree_map

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.

        @type self: AbstractTree
        @rtype: str
        """
        raise NotImplementedError

    def leaves(self):
        """Return a list containing all leaves of the tree <self> and don't
        contain the leaf has <data_size> equal to 0.

        NOTICE THAT,This is a special version of leaves method.

        @type self: AbstractTree | None
        @rtype: list[AbstractTree]

        >>> t_null = AbstractTree('null', [])
        >>> t0 = AbstractTree(0, [], 1)
        >>> t1 = AbstractTree('a', [], 10)
        >>> t2 = AbstractTree('b', [t0])
        >>> tx = AbstractTree('x', [t1, t2, t_null])
        >>> len(tx.leaves())
        2
        >>> tx.leaves()[0]._root
        'a'
        >>> tx.leaves()[1]._root
        0
        """
        leaves = []
        if self.is_empty():
            return []
        elif len(self._subtrees) == 0:
            return []
        else:
            for tree in self._subtrees:
                # NOTICE THAT, the empty folder is the same as a single file
                # from the view of regular leaves method. But here we need to
                # let this method distinguish empty folded and a single file.
                # The difference is an empty file has <data_size> equal to 0
                # While a single file <data_size> is not 0.
                if (len(tree.get_subtrees()) == 0) and (tree.data_size != 0):
                    leaves.append(tree)
                else:
                    leaves += tree.leaves()
            return leaves

    def get_leaf(self, rect, tree_rect):
        """Return a leaf(which is a AbstractTree object) according to its
        treemap rectangle representation.

        Given a rectangle representation of a leaf, we can find the
        corresponding leaf through this method. (ie, Convert (x, y, w, h) to
        a tree object (a leaf).

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            This is the pygame rectangle, the display area to fill, and has
            format: (x, y, width, height).
        @type tree_rect: (int, int, int, int)
            This is the rectangle representation of a leaf of <self> and
            its has the format: (x, y, width, height).
        @rtype: AbstractTree
            The leaf that corresponding to the given rectangle representation:
            <tree_rect>.

        Precondition: <tree_rect> is the first element of some element of
        self.generate_treemap(rect).

        >>> path = 'C:/Users/User/Desktop/csc148/assignments/a2/B'
        >>> t = FileSystemTree(path)
        >>> t.get_leaf((0, 0, 800, 1000), (0, 0, 400, 750))._root
        'f1.txt'
        >>> t.get_leaf((0, 0, 800, 1000), (400, 0, 133, 750))._root
        'f2.txt'
        >>> f4 = t.get_leaf((0, 0, 800, 1000), (0, 750, 800, 250))
        >>> f4._root
        'f4.txt'
        >>> isinstance(f4, AbstractTree)
        True
        >>> f4.generate_treemap((0, 0, 800, 1000))[0][0]
        (0, 0, 800, 1000)
        """
        leaves = self.leaves()
        # List of leaf (with <data_size> is not 0) of this tree <self>.
        tree_map = self.generate_treemap(rect)
        for item in tree_map:
            # <item> is in format: ((x, y, width, height), colour).
            if tree_rect == item[0]:
                index = tree_map.index(item)
                return leaves[index]

    def convert_to_rect(self, rect, leaf):
        """Return the rectangle representation of a leaf.

        Take a leaf, transfer it to its rectangle representation.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
        @type leaf: AbstractTree
        @rtype: list[(int, int, int, int), (int, int, int)]

        Precondition: <leaf> has no subtrees, ie it is a leaf. And its is
        not None.

        >>> path = 'C:/Users/User/Desktop/csc148/assignments/a2/B'
        >>> tree = FileSystemTree(path)
        >>> f1 = tree.get_leaf((0, 0, 800, 1000), (0, 0, 400, 750))
        >>> tree.convert_to_rect((0, 0, 800, 1000), f1)[0]
        (0, 0, 400, 750)
        >>> f4 = tree.get_leaf((0, 0, 800, 1000), (0, 750, 800, 250))
        >>> f4._root
        'f4.txt'
        >>> tree.convert_to_rect((0, 0, 800, 1000), f4)[0]
        (0, 750, 800, 250)
        """

        leaf_lst = self.leaves()
        treemap = self.generate_treemap(rect)
        for item in leaf_lst:
            # <item> is in format: ((x, y, width, height), colour).
            if item == leaf:
                index = leaf_lst.index(item)
                return treemap[index]

    def delete_leaf(self, leaf):
        """Delete the leaf <leaf> from this tree.

        Return True if <leaf> is deleted,
        return False (and do nothing else) if the item is not in this tree.


        Precondition: <self> is not empty, the tree has this <leaf> and the
        <leaf> does not have any subtree.

        @type self: AbstractTree
        @type leaf: AbstractTree
        @rtype: bool

        >>> t0 = AbstractTree('o', [])
        >>> t1 = AbstractTree('a', [])
        >>> t2 = AbstractTree('b', [])
        >>> t3 = AbstractTree('c', [])
        >>> t = AbstractTree('x', [t1, t2, t3])
        >>> t.delete_leaf(t1)
        True
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
        >>> f.delete_leaf(f3)
        True
        >>> len(f._subtrees)
        3
        >>> f._subtrees[2]._root
        '4'
        >>> f._subtrees[2]._subtrees
        []
        """
        if len(self._subtrees) == 0:
            if self is leaf:
                self._root = None
                return True
            else:
                return False

        else:
            for subtree in self._subtrees:
                if subtree.delete_leaf(leaf):
                    if subtree.is_empty():
                        self._subtrees.remove(subtree)
                    return True
            return False

    def compute_size(self):
        """Return the <data_size> attribute of this tree <self>.

        it is sum of all the <data_size> of its subtrees.

        @type self: AbstractTree
        @rtype: int

        >>> t1 = AbstractTree('a', [], 10)
        >>> t2 = AbstractTree('b', [], 100)
        >>> t3 = AbstractTree('c', [t1])
        >>> big_t = AbstractTree('big', [t2, t3])
        >>> t2.compute_size()
        100
        >>> t3.compute_size()
        10
        >>> big_t.compute_size()
        110
        >>> t0 = AbstractTree(0, [])
        >>> t0.compute_size()
        0
        """
        if self.is_empty():
            return 0
        elif len(self._subtrees) == 0:
            # This is the case for a single file or a single empty folder.
            return self.data_size
        else:
            count = 0
            for subtree in self._subtrees:
                count += subtree.compute_size()
            return count

    def complete_leaf_deletion(self, leaf):
        """The complete leaf deletion operation, it delete the <leaf> from this
        tree <self> and change the <data_size> attribute of <self> and its
        subtree.

        @type self: AbstractTree
        @type leaf: AbstractTree
        @rtype: None

        Precondition: <leaf> is some leaf of <self>. Otherwise, this method
        will do nothing.

        >>> t1 = AbstractTree('a', [], 10)
        >>> t2 = AbstractTree('b', [], 100)
        >>> t3 = AbstractTree('c', [t1])
        >>> t5 = AbstractTree('e', [], 1000)
        >>> t6 = AbstractTree('t6', [], 10000)
        >>> t4 = AbstractTree('d', [t5, t6])
        >>> big_t = AbstractTree('big', [t2, t3, t4])
        >>> t2.compute_size()
        100
        >>> t3.compute_size()
        10
        >>> big_t.compute_size()
        11110
        >>> big_t.complete_leaf_deletion(t1)
        >>> big_t.data_size
        11100
        >>> big_t.get_subtrees()[1].data_size
        0
        >>> len(big_t.get_subtrees())
        3
        >>> big_t.complete_leaf_deletion(t5)
        >>> big_t.data_size
        10100
        >>> t4.data_size
        10000
        >>> t3.data_size
        0
        >>> file1 = AbstractTree('file1', [], 8)
        >>> folder1 = AbstractTree('folder1', [file1])
        >>> folder1.complete_leaf_deletion(file1)
        >>> folder1.data_size
        0
        >>> folder1.get_subtrees()
        []
        """
        leaf.get_parent_tree().data_size -= leaf.data_size
        if self.delete_leaf(leaf):
            if len(self._subtrees) == 0:
                # This is the case that after deletion, <self> becomes a tree
                # with no subtree(ie.an empty folder).
                self.data_size = 0
            else:
                for subtree in self._subtrees:
                    subtree.data_size = subtree.compute_size()
                self.data_size = self.compute_size()

    def get_subtrees(self):
        """Return the <_subtrees> attribute of <self>.

        @type self: AbstractTree
        @rtype: list[AbstractTree]

        >>> t1 = AbstractTree('a', [], 10)
        >>> t2 = AbstractTree('b', [], 100)
        >>> t3 = AbstractTree('c', [t1])
        >>> big_t = AbstractTree('big', [t2, t3])
        >>> big_t.get_subtrees()[0]._root
        'b'
        """
        return self._subtrees

    def get_parent_tree(self):
        """Return the <_parent_tree> attribute of <self>

        @type self: AbstractTree
        @rtype: AbstractTree

        >>> t1 = AbstractTree('a', [], 10)
        >>> t2 = AbstractTree('b', [], 100)
        >>> t3 = AbstractTree('c', [t1])
        >>> big_t = AbstractTree('big', [t2, t3])
        >>> t1.get_parent_tree()._root
        'c'
        >>> t3.get_parent_tree()._root
        'big'
        """
        return self._parent_tree

    def increase_size(self):
        """Increase the <data_size> attribute of <self> by 1% of its current
        value and the increasing value should be rounded up.
        The <data_size> of all <self>'s ancestors will be updated.

        Pre-condition: <self> is a leaf. (ie.it has no subtree)

        @type self: AbstractTree
        @rtype: None

        >>> f1 = AbstractTree('f1', [], 10)
        >>> f2 = AbstractTree('f2', [], 100)
        >>> f3 = AbstractTree('f3', [], 1000)
        >>> folder0 = AbstractTree('folder0', [])
        >>> folder1 = AbstractTree('F1', [f1, f2, folder0])
        >>> folder_big = AbstractTree('big', [folder1, f3])
        >>> f1.increase_size()
        >>> f1.data_size
        11
        >>> f2.data_size
        100
        >>> f3.data_size
        1000
        >>> folder1.data_size
        111
        >>> folder_big.data_size
        1111
        >>> f2.increase_size()
        >>> folder_big.data_size
        1112
        """
        # First, we increase <data_size> of this leaf <self>.
        increase = math.ceil(self.data_size * 0.01)
        self.data_size += increase

        # Next, we change the <data_size> of all ancestors of this leaf <self>.
        parent = self
        # type parent: AbstractTree | None
        while parent.get_parent_tree() is not None:
            parent = parent.get_parent_tree()
            count = 0
            for subtree in parent.get_subtrees():
                count += subtree.data_size
            parent.data_size = count
            # or do: parent.data_size = parent.compute_size() directly.

    def decrease_size(self):
        """Decrease the <data_size> attribute of <self> by 1% of its current
        value and the decreasing value should be rounded up.
        The <data_size> of all <self>'s ancestors will be updated.

        Pre-condition: <self> is a leaf. (ie.it has no subtree)
        Post-conditions: A leaf's <data_size> cannot decrease below 1.

        @type self: AbstractTree
        @rtype: None

        >>> f1 = AbstractTree('f1', [], 10)
        >>> f2 = AbstractTree('f2', [], 100)
        >>> f3 = AbstractTree('f3', [], 1000)
        >>> folder0 = AbstractTree('folder0', [])
        >>> folder1 = AbstractTree('F1', [f1, f2, folder0])
        >>> folder_big = AbstractTree('big', [folder1, f3])
        >>> f2.decrease_size()
        >>> f1.data_size
        10
        >>> f2.data_size
        99
        >>> f3.data_size
        1000
        >>> folder_big.data_size
        1109
        >>> f1.decrease_size()
        >>> f1.data_size
        9
        >>> leaf1 = AbstractTree(1, [], 1)
        >>> leaf1.decrease_size()
        >>> leaf1.data_size
        1
        """
        decrease = math.ceil(self.data_size * 0.01)
        self.data_size -= decrease

        if self.data_size < 1:
            # This prevents the case when <data_size> of this leaf goes below 1.
            self.data_size = 1

        # Next, we change the <data_size> of all ancestors of this leaf <self>.
        parent = self
        # type parent: AbstractTree | None
        while parent.get_parent_tree() is not None:
            parent = parent.get_parent_tree()
            count = 0
            for subtree in parent.get_subtrees():
                count += subtree.data_size
            parent.data_size = count

    def get_root(self):
        """Return the root value of <self>

        @type self: AbstractTree
        @rtype: object
        """
        return self._root


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path):
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        @type self: FileSystemTree
        @type path: str
        @rtype: None

        >>> path1 = 'C:/Users/User/Desktop/csc148/assignments/a1'
        >>> t = FileSystemTree(path1)
        >>> t._root
        'a1'
        >>> t._subtrees[0]._root
        'starter_code'
        >>> t._subtrees[0]._subtrees[1]._parent_tree is t._subtrees[0]
        True
        """
        if not os.path.isdir(path):
            # <path> is pointing at a file(ie .py, .txt)
            size = os.path.getsize(path)
            name = os.path.basename(path)
            AbstractTree.__init__(self, name, [], size)

        else:
            name = os.path.basename(path)
            content = []
            for filename in os.listdir(path):
                subitem_path = os.path.join(path, filename)
                subitem = FileSystemTree(subitem_path)
                content.append(subitem)
            AbstractTree.__init__(self, name, content)

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        @type self: AbstractTree
        @rtype: str
        """

        # This is the case that this object is just an single file or an
        # empty folder. (ie. it does not have parent tree)
        if self._parent_tree is None:
            return self._root

        else:
            parent_path = self._parent_tree.get_separator()
            return os.path.join(parent_path, self._root)


##############################################################################
# Helper Function
##############################################################################


def combine(subtree_map, tree_map):
    """
    Mutate the <tree_map>, put all tuples in <subtree_map> into <tree_map>.

    @type subtree_map: list
    @type tree_map: list
    @rtype: None

    >>> lst1 = [1, 2, 3]
    >>> lst2 = [5, 6, 7]
    >>> combine(lst1, lst2)
    >>> lst2
    [5, 6, 7, 1, 2, 3]
    """
    for item in subtree_map:
        tree_map.append(item)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
