# coding: utf-8
#  -*- Mode: Python; -*-                                              
#
# python examplere.py
#  AUTHOR Jenna N. Shockley

import unittest
import re

import sys
assert( sys.version_info.major == 3 )

class ReExampleTest(unittest.TestCase):

    def test(self):
        # -----------------------------------------------------------------------------
        # Re Functionality
        # -----------------------------------------------------------------------------
            
        # Compile
        b = re.compile(b'([a-z]+)[@]([a-z]+)[.]([a-z]+)')

        # Search
        match_object = re.search('[0-9]{4}', "The year is 2018")
        self.assertEqual(match_object.group(), "2018")

        # Match
        match_object = re.match('[0-9]{4}', "1998 was the year I was born")
        self.assertEqual(match_object.group(), "1998")

        # Fullmatch
        match_object = re.fullmatch('[0-9]{4}', "1998")
        self.assertEqual(match_object.group(), "1998")

        # Findall
        list = re.findall('[0-9]{4}', "1998 was the year I was born. 2018 is the current year")
        self.assertEqual(list, ["1998", "2018"])

        # Sub
        string = re.sub('[0-9]{4}', "time", "the year of 1998")
        self.assertEqual(string, "the year of time")

        # Subn
        tuple = re.subn('[0-9]{4}', "time", "the year of 1998 and 2004")
        self.assertEqual(tuple, ("the year of time and time", 2))

        # -----------------------------------------------------------------------------
        # Pattern Object Functionality
        # -----------------------------------------------------------------------------

        # Compile
        b = re.compile('[0-9]{4}')

        # Search
        match_object = b.search("The year is 2018")
        self.assertEqual(match_object.group(), "2018")

        # Match
        match_object = b.match("1998 was the year I was born")
        self.assertEqual(match_object.group(), "1998")
        
        # FullMatch
        match_object = b.fullmatch("1998")
        self.assertEqual(match_object.group(), "1998")

        # Findall
        list = b.findall("1998 was the year I was born. 2018 is the current year")
        self.assertEqual(list, ["1998", "2018"])

        # Sub
        string = b.sub("time", "the year of 1998")
        self.assertEqual(string, "the year of time")

        # Subn
        tuple = b.subn("time", "the year of 1998 and 2004")
        self.assertEqual(tuple, ("the year of time and time", 2))

        # Pattern
        self.assertEqual(b.pattern, '[0-9]{4}')

        # -----------------------------------------------------------------------------
        # Match Object Functionality
        # -----------------------------------------------------------------------------

        # Compile
        b = re.compile('(?P<x1>[a-z]+)[@](?P<x2>[a-z]+)[.](?P<x3>[a-z]+)')

        # Match
        m = b.match("user@ncsu.edu")

        # __getitem__
        self.assertEqual(m[1], "user")

        # Group
        self.assertEqual(m.group(), "user@ncsu.edu")

        # Group by number
        self.assertEqual(m.group(2), "ncsu")

        # Group by name
        self.assertEqual(m.group('x3'), "edu")

        # Group with multiple
        self.assertEqual(m.group('x1', 'x3'), ("user", "edu"))
        self.assertEqual(m.group(1,2,3), ('user', 'ncsu', 'edu'))

        # Groups
        self.assertEqual(m.groups(), ("user", "ncsu", "edu"))

        # Group dict
        dict = {'x1': 'user', 'x2': 'ncsu', 'x3': 'edu'}
        self.assertEqual(m.groupdict(), dict)

        # Start
        self.assertEqual(m.start(1), 0)

        # End
        self.assertEqual(m.end('x1'), 4)

        # Span
        self.assertEqual(m.span('x1'), (0,4))

        # Pos
        self.assertEqual(m.pos, 0)

        # Endpos
        self.assertEqual(m.endpos, 13)

        # Last Index
        self.assertEqual(m.lastindex, 3)

        # Last Group
        self.assertEqual(m.lastgroup, 'x3')

        # re
        self.assertEqual(m.re, b)

        # String
        self.assertEqual(m.string, "user@ncsu.edu")

        # Expand
        self.assertEqual(m.expand(r"hello \1 is done"), "hello user is done")
        self.assertEqual(m.expand(r'\1 is done'), "user is done")
        self.assertEqual(m.expand(r'username: \1 email: \2 end: \3'), "username: user email: ncsu end: edu")
        self.assertEqual(m.expand(r'username: \g<1> email: \g<2> end: \g<3>'), "username: user email: ncsu end: edu")
        self.assertEqual(m.expand(r'username: \g<x1> email: \g<x2> end: \g<x3>'), "username: user email: ncsu end: edu")

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
    
