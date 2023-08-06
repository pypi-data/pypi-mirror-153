# coding: utf-8
#  -*- Mode: Python; -*-                                              
#
# This file is part of the tests for the Python interface to librosie.
# After all unit tests pass, confirming that the basics of rosie.py
# are all working ok, the tests in this file can be run.
#
# What this file does
#
# Process each package in the RPL standard library, extracting the RPL
# unit tests and running them without using the `rosie test` CLI.
#
# E.g. the file 'net.rpl' contains unit tests like:
#   -- test fqdn accepts "ibm.com:443", "ibm.com.:80"
#
# We would first extract these lines (using rosie, of course), and
# then run each of the tests through Python, as follows:
#
# For each package:
#   Read the source RPL code from its file, e.g. 'net.rpl'
#   Extract all the tests of public patterns (so, not "test local ...")
#   Run the tests by calling rosie through the Python interface
#     Import the package
#     Prefix each pattern being tested with its package name
#     Compile the pattern
#     Test the pattern against all the test input strings 
#
# AUTHOR Jamie A. Jennings

import unittest
import sys, os, glob

# We want to test the rosie package in the parent directory, not any
# rosie package that happens to be visible to Python.  There must be
# an idiomatic way to do this, because this way is a hack.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import rosie

assert( sys.version_info.major == 3 )

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

test_patterns = '''
	 identifier = rpl.identifier           -- rename
	 quoted_string = rpl.quoted_string
	 includesKeyword = "includes" / "excludes"
	 includesClause = includesKeyword identifier
	 testKeyword = "accepts" / "rejects"
	 test_local = "local"
	 test_line = ("--test" / "-- test")
	             test_local?
	             identifier 
	             (testKeyword / includesClause) 
		     (quoted_string ("," quoted_string)*)?
'''

def is_local_test(test_line_match):
    return test_line_match.rosie_match['subs'][0]['type']=="test_local"

def test_identifier(test_line_match):
    index = 0
    if is_local_test(test_line_match): index = 1
    item = test_line_match.rosie_match['subs'][index]
    assert(item['type']=='identifier')
    return item['data']

def test_type(test_line_match):
    index = 1
    if is_local_test(test_line_match): index = 2
    t = test_line_match.rosie_match['subs'][index]
    if t['type'] == 'testKeyword':
        return t['data']
    elif t['type'] == 'includesClause':
        return t['subs'][0]['data']
    else:
        raise ValueError('cannot parse test line match {}'.format(t))

def test_included_type(test_line_match):
    kind = test_type(test_line_match)
    if kind == 'includes' or kind == 'excludes':
        index = 1
        if is_local_test(test_line_match): index = 2
        t = test_line_match.rosie_match['subs'][index]
        assert(t['subs'][1]['type'] == 'identifier')
        return t['subs'][1]['data']
    else:
        raise ValueError('invalid test type (expected includes/excludes test): {}'.format(test_line_match))

def test_strings(test_line_match):
    index = 2
    if is_local_test(test_line_match): index = 3
    strings = []
    for item in test_line_match.rosie_match['subs'][index:]:
        assert(item['type'] == 'quoted_string')
        assert('subs' in item)
        assert(item['subs'][0]['type']=='rpl.literal')
        strings.append(item['subs'][0]['data'])
    return strings

def extract_package(package_decl, line):
    m = package_decl.match(line)
    if m: return m.groups()[1]

# -----------------------------------------------------------------------------
# Find all the files in the RPL standard library
# -----------------------------------------------------------------------------

class RosieRPLLibraryTest(unittest.TestCase):

    def setUp(self):
        assert(librosiedir)
        rosie.load(librosiedir, quiet=True)
        self.engine = rosie.engine()
        assert(self.engine)

        # Extract some rosie installation configuration info
        config = self.engine.config()
        for item in config[0]:
            if item['name']=='ROSIE_LIBDIR':
                self.libpath = item['value']
                break
        for item in config[1]:
            if item['name']=='RPL_VERSION':
                self.rpl_version = item['value']
        assert(self.libpath)
        assert(self.rpl_version)

        # Make sure we can find the file that defines the version of
        # RPL for this rosie engine
        rpl_defn_file = os.path.join('rosie',
                                     'rpl_' + '_'.join(str.split(self.rpl_version, sep='.')))
        rpl_defn_path = os.path.join(self.libpath, rpl_defn_file + '.rpl')
        assert(os.path.exists(rpl_defn_path))

        # Load and compile the RPL expression for extracting the unit
        # tests from the RPL files
        pkgname = self.engine.import_package(rpl_defn_file, "rpl")
        assert(pkgname)
        self.engine.load(test_patterns)
        self.test_pattern = self.engine.compile("test_line")
        assert(self.test_pattern)

        self.package_decl = self.engine.compile('~rpl.package_decl')
        assert(self.package_decl)

        # Build a list of rpl files from the standard library, which
        # will be the source of all our tests
        self.files = glob.glob(os.path.join(self.libpath, "*.rpl"))


    def tearDown(self):
        pass


    def testExtractor(self):
        assert(self.test_pattern)
        m = self.test_pattern.match('-- test fqdn accepts "ibm.com:443", "ibm.com.:80"')
        self.assertTrue(m)
        self.assertTrue(test_identifier(m) == 'fqdn')
        self.assertTrue(not is_local_test(m))
        strings = test_strings(m)
        self.assertTrue(len(strings)==2)
        self.assertTrue(strings[0]=='ibm.com:443')
        self.assertTrue(strings[1]=='ibm.com.:80')
        self.assertTrue(test_type(m)=='accepts')

        m = self.test_pattern.match('-- test local letter rejects "7"')
        self.assertTrue(m)
        self.assertTrue(test_identifier(m) == 'letter')
        assert(is_local_test(m))
        strings = test_strings(m)
        self.assertTrue(len(strings)==1)
        self.assertTrue(strings[0]=='7')
        self.assertTrue(test_type(m)=='rejects')

        m = self.test_pattern.match('-- test ipv6 includes ipv4 "::192.9.5.5"')
        self.assertTrue(m)
        self.assertTrue(test_identifier(m) == 'ipv6')
        strings = test_strings(m)
        self.assertTrue(len(strings)==1)
        self.assertTrue(strings[0]=='::192.9.5.5')
        self.assertTrue(test_type(m)=='includes')
        self.assertTrue(test_included_type(m)=='ipv4')
        
        m = self.test_pattern.match('-- test ipv6 excludes ipv4 "1080::8:800:200C:417A", "x"')
        self.assertTrue(m)
        self.assertTrue(test_identifier(m) == 'ipv6')
        strings = test_strings(m)
        self.assertTrue(len(strings)==2)
        self.assertTrue(strings[1]=='x')
        self.assertTrue(test_type(m)=='excludes')
        self.assertTrue(test_included_type(m)=='ipv4')

    def testFiles(self):
        assert(self.test_pattern)
        assert(self.files)
        filecount = 0
        stringcount = 0
        for filename in self.files:
            tests = []
            pkg = None
            with open(filename) as f:
                filecount += 1
                other_testcount = 0
                lineno = 0
                for line in f:
                    lineno += 1
                    pkg = pkg or extract_package(self.package_decl, line)
                    m = self.test_pattern.match(line)
                    if not m:
                        # No tests on this line
                        continue
                    if is_local_test(m):
                        # Cannot access local patterns from outside package
                        other_testcount += 1
                        continue
                    ttype = test_type(m)
                    if (ttype=='accepts') or (ttype=='rejects'):
                        tests.append({ 'file': filename,
                                       'package': pkg,
                                       'line': lineno,
                                       'pattern': test_identifier(m),
                                       'action': ttype,
                                       'strings': test_strings(m)
                                      })
                    else:
                        other_testcount += 1
                print("File {} has {} accept/reject tests and {} other tests".format(
                    filename, len(tests), other_testcount))
            # Prepare to run tests
            e = rosie.engine()
            self.assertTrue(e)
            e.loadfile(filename)
            scount = 0
            for test in tests:
                pat = e.compile(test['package'] + '.' + test['pattern'])
                self.assertTrue(pat)
                for string in test['strings']:
                    scount += 1
                    m = pat.fullmatch(string)
                    if test['action']=='accept':
                        self.assertTrue(m)
                    elif test['action']=='reject':
                        self.assertTrue(m is None)
            print("Processed file {} with {} accept/reject tests and {} total test strings".format(
                filename, len(tests), scount))
            stringcount += scount
        print("\nProcessed {} files with a total of {} strings tested".format(
            filecount, stringcount))


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    librosiedir = None
    if len(sys.argv) == 1:
        librosiedir = rosie.librosie_system()
        print("Loading librosie from system library path")
    elif len(sys.argv) == 2:
        librosiedir = sys.argv[1]
        print("Loading librosie from path given on command line: " + librosiedir)
    else:
        sys.exit("Error: spurious command-line parameters (one or none are expected)")
    testdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(testdir)                 # To find files needed for testing
    unittest.main(argv=[sys.argv[0]]) # F'ing Python

    

