import unittest
import os
from tree_data import AbstractTree, FileSystemTree
from random import randint
import math

class FirstTest(unittest.TestCase):
    def test1(self):
        path1 = 'C:\\Users\\User\\Desktop\\csc148\\assignments\\a1'
        t = FileSystemTree(path1)



if __name__ == '__main__':
    unittest.main(exit=False)
