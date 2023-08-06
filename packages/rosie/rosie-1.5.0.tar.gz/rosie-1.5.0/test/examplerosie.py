# coding: utf-8
#  -*- Mode: Python; -*-                                              
#
# python examplerosie.py
#  AUTHOR Jenna N. Shockley

# TODO:
# - replace magic error code numbers with constants
#
import unittest
import sys, os

# We want to test the rosie package in the parent directory, not any
# rosie package that happens to be visible to Python.  There must be
# an idiomatic way to do this, because this way is a hack.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import rosie

assert( sys.version_info.major == 3 )

str23 = lambda s: str(s, encoding='UTF-8')
bytes23 = lambda s: bytes(s, encoding='UTF-8')

# -----------------------------------------------------------------------------
# Tests for Engine class
# -----------------------------------------------------------------------------

class RosieExampleTest(unittest.TestCase):

    def setUp(self):
        rosie.load(librosiedir, quiet=True)
        self.engine = rosie.engine()
        pass

    def tearDown(self):
        pass

    def test(self):
        # -----------------------------------------------------------------------------
        # Rosie Engine Functionality
        # -----------------------------------------------------------------------------
        
        # Load
        pkgname = self.engine.load(b'package email; x1 = [a-z]+; x2 = [a-z]+; x3 = [a-z]+')
            
        # Compile
        b = self.engine.compile(b'email.x1[@]email.x2[.]email.x3')

        # Search
        match_object = self.engine.search('[0-9]{4}', "The year is 2018")
        self.assertEqual(match_object.group(), "2018")

        # Match
        match_object = self.engine.match('[0-9]{4}', "1998 was the year I was born")
        self.assertEqual(match_object.group(), "1998")

        # Fullmatch
        match_object = self.engine.fullmatch('[0-9]{4}', "1998")
        self.assertEqual(match_object.group(), "1998")

        # Findall
        list = self.engine.findall('[0-9]{4}', "1998 was the year I was born. 2018 is the current year")
        self.assertEqual(list, ["1998", "2018"])


        # Sub
        string = self.engine.sub('[0-9]{4}', "time", "the year of 1998")
        self.assertEqual(string, "the year of time")

        # Subn
        tuple = self.engine.subn('[0-9]{4}', "time", "the year of 1998 and 2004")
        self.assertEqual(tuple, ("the year of time and time", 2))

        # -----------------------------------------------------------------------------
        # Pattern Object Functionality
        # -----------------------------------------------------------------------------

        # Compile
        b = self.engine.compile('[0-9]{4}')

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

        # Load
        pkgname = self.engine.load(b'package email2; x1 = [a-z]+; x2 = [a-z]+; x3 = [a-z]+')
            
        # Compile
        b = self.engine.compile(b'email2.x1[@]email2.x2[.]email2.x3')

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
        dict = {'*': 'user@ncsu.edu', 'x1': 'user', 'x2': 'ncsu', 'x3': 'edu'}
        self.assertEqual(m.groupdict(), dict)

        # Start
        self.assertEqual(m.start(1), 1)

        # End
        self.assertEqual(m.end('x1'), 5)

        # Span
        self.assertEqual(m.span('x1'), (1,5))

        # Pos
        self.assertEqual(m.pos, 1)

        # Endpos
        self.assertEqual(m.endpos, 13)

        # Last Index
        self.assertEqual(m.lastindex(), 3)

        # Last Group
        self.assertEqual(m.lastgroup(), 'x3')

        # re
        self.assertEqual(m.re, b)

        # String
        self.assertEqual(m.string, "user@ncsu.edu")

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) != 1:
        sys.exit("Error: ignoring spurious command-line parameters (none are expected)")
    testdir = os.path.abspath(__file__)
    librosiedir = rosie.librosie_system()
    print("Loading librosie from system library path")
    unittest.main()
    
