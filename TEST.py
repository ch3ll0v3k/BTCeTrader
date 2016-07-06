

import sys

class A:
    def __init__(self):
        print __file__
        print self.__class__.__name__
        print sys._getframe().f_code.co_name


    def M_1(self):

        print sys._getframe().f_code.co_name
    def M_2(self):

        print sys._getframe().f_code.co_name
    def M_3(self):

        print sys._getframe().f_code.co_name



a = A()

a.M_2()
a.M_1()
a.M_3()
a.M_1()


"""


TEST.py
A
__init__
M_2
M_1
M_3
M_1



"""