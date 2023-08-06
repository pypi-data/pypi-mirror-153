# coding: utf-8
#  -*- Mode: Python; -*-                                              
#
# python test.py
# 
#  AUTHOR Jenna N. Shockley
#  AUTHOR Jamie A. Jennings

# TODO:
# - replace magic error code numbers with constants
#

import unittest
import sys, os, json

# We want to test the rosie package in the parent directory, not any
# rosie package that happens to be visible to Python.  There must be
# an idiomatic way to do this, because this way is a hack.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import rosie

assert( sys.version_info.major == 3 )

# -----------------------------------------------------------------------------
# Tests for Engine class
# -----------------------------------------------------------------------------

class RosieEngineTest(unittest.TestCase):

    def setUp(self):
        rosie.load(librosiedir, quiet=True)
        self.engine = rosie.engine()
        pass

    def tearDown(self):
        pass

    def testInit(self):
        assert(self.engine)
        path = rosie.librosie_path()
        assert(path)

    def testConfig(self):
        cfg = self.engine.config()
        self.assertTrue(cfg)
        # Config list is 3 lists:
        #   rosie installation attributes, engine attributes, encoder parms
        self.assertTrue(len(cfg)==3)
        ver = None
        libpath = None
        for item in cfg[0]:
            if item['name']=='ROSIE_VERSION':
                ver = item['value']
            if item['name']=='ROSIE_LIBPATH':
                libpath = item['value']
        self.assertIsInstance(ver, str)
        self.assertTrue(self.engine.version() == ver)

    def testLoad(self):
        try:
            pkgname = self.engine.load(b'package x; foo = "foo"')
            self.assertTrue(pkgname == b"x")
        except RuntimeError:
            self.fail()

        try:
            b = self.engine.compile(b"x.foo")
            self.assertTrue(b.valid())
        except RuntimeError:
            self.fail()

        try:
            bb = self.engine.compile(b"[:digit:]+")
            self.assertTrue(bb.valid())
        except RuntimeError:
            self.fail()

        b2 = None
        try:
            b2 = self.engine.compile(b"[:foobar:]+")
            self.fail()
        except rosie.RPLError as e:
            self.assertTrue(not b2)
            self.assertIsInstance(e.errs, list)
            self.assertTrue(len(e.errs) > 0)
            self.assertTrue('who' in e.errs[0])
            self.assertTrue('message' in e.errs[0])
            self.assertTrue(e.errs[0]['who']=='compiler')
            self.assertTrue(e.errs[0]['message'].startswith('unknown named charset'))
        try:
            b = None                       # trigger call to librosie to gc the compiled pattern
            b = self.engine.compile(b"[:digit:]+")
        except RuntimeError:
            self.fail()

        num_int = None
        try:
            num_int = self.engine.compile(b"num.int")
            self.fail()
        except rosie.RPLError as e:
            self.assertTrue(not num_int)
            self.assertIsInstance(e.errs, list)
            self.assertTrue('who' in e.errs[0])
            self.assertTrue('message' in e.errs[0])
            self.assertTrue(e.errs[0]['who']=='compiler')
            self.assertTrue(e.errs[0]['message'].startswith('undefined identifier'))

        try:
            pkgname = self.engine.load(b'foo = "')
            self.fail()
        except rosie.RPLError as e:
            self.assertTrue(str(e))
            #todo fix
            self.assertEqual(str(e), str(e))

        engine2 = rosie.engine()
        self.assertTrue(engine2)
        self.assertTrue(engine2 != self.engine)
        engine2 = None          # triggers call to librosie to gc the engine

    def testLibpath(self):
        path = self.engine.libpath()
        self.assertIsInstance(path, bytes)
        newpath = b"foo bar baz"
        self.engine.libpath(newpath)
        testpath = self.engine.libpath()
        self.assertIsInstance(testpath, bytes)
        self.assertTrue(testpath == newpath)
        
    def testAllocLimit(self):
        limit, usage = self.engine.alloc_limit()
        self.assertIsInstance(limit, int)
        self.assertTrue(limit == 0)
        limit, usage = self.engine.alloc_limit(0)
        limit, usage = self.engine.alloc_limit()
        self.assertTrue(limit == 0)
        limit, usage = self.engine.alloc_limit(8199)
        self.assertTrue(limit == 8199)
        with self.assertRaises(ValueError):
            limit, usage = self.engine.alloc_limit(8191) # too low
        limit, usage = self.engine.alloc_limit()
        self.assertTrue(limit == 8199)
            
    def testImport(self):
        try:
            pkgname = self.engine.import_package(b'net')
            self.assertTrue(pkgname == b'net')
        except RuntimeError:
            self.fail()

        try:
            pkgname = self.engine.import_package(b'net', b'foobar')
            self.assertTrue(pkgname == b'net') # actual name inside the package
        except RuntimeError:
            self.fail()

        net_any = None
        try:
            net_any = self.engine.compile(b"net.any")
            self.assertTrue(net_any)
        except RuntimeError:
            self.fail()

        try:
            foobar_any = self.engine.compile(b"foobar.any")
            self.assertTrue(foobar_any)
        except RuntimeError:
            self.fail()
        
        m = net_any.match(b"1.2.3.4", 1, encoder = b"color")
        self.assertTrue(m)
        m = net_any.match(b"Hello, world!", 1, encoder = b"color")
        self.assertTrue(not m)

        try:
            pkgname = self.engine.import_package(b'THISPACKAGEDOESNOTEXIST')
        except rosie.RPLError as e:
            self.assertTrue(e)
            self.assertIsInstance(e.errs, list)
    
    def testLoadFile(self):
        try:
            pkgname = self.engine.loadfile('test.rpl')
            self.assertTrue(pkgname == bytes(b'test'))
        except RuntimeError:
            self.fail()

    def testMatch(self):
        # test short match
        try:
            m = self.engine.match(b"[:digit:]+", "321")
            self.assertTrue(m)
            self.assertTrue(m.rosie_match['data'] != None) # NOT posonly
            self.assertTrue(m.start() == 1)     # match started at char 2
            self.assertTrue(m.end() == 4)
            self.assertTrue(m.group() == "321")
            self.assertTrue(m.abend() == False)
        except:
            self.fail()

        # test short match with option to get positions only in the match object
        try:
            m = self.engine.match(b"[:digit:]+", "321", posonly=True)
            self.assertTrue(m)
            self.assertTrue(m.rosie_match['data'] == None) # posonly
            self.assertTrue(m.start() == 1)     # match started at char 2
            self.assertTrue(m.end() == 4)
            self.assertTrue(m.group() == None)  # posonly means no data field
            self.assertTrue(m.abend() == False)
        except:
            self.fail()

        # test no match
        try:
            m = self.engine.match(b"[:digit:]+", b"xyz")
            self.assertTrue(m == None)
        except:
            self.fail()

        # test long match
        inp = "889900112233445566778899100101102103104105106107108109110xyz"
        linp = len(inp)

        try:
            m = self.engine.match(b"[:digit:]+", inp)
            self.assertTrue(m)
            self.assertTrue(m.start() == 1)
            self.assertTrue(m.end() == linp-3+1) # due to the "xyz" at the end
            self.assertTrue(m.group() == inp[0:-3])
            self.assertTrue(m.abend() == False)
        except:
            self.fail()

    def testFullMatch(self):
        # test short match, with data fields in match object
        try:
            m = self.engine.fullmatch(b"[:digit:]+", "321")
            self.assertTrue(m)
            self.assertTrue(m.rosie_match['data'] != None) # NOT posonly
            self.assertTrue(m.start() == 1)     # match started at char 2
            self.assertTrue(m.end() == 4)
            self.assertTrue(m.group() == "321")
            self.assertTrue(m.abend() == False)
        except:
            self.fail()

        # test short match with option to get positions only in the match object
        try:
            m = self.engine.fullmatch(b"[:digit:]+", "321", posonly=True)
            self.assertTrue(m)
            self.assertTrue(m.rosie_match['data'] == None) # posonly
            self.assertTrue(m.start() == 1)     # match started at char 2
            self.assertTrue(m.end() == 4)
            self.assertTrue(m.group() == None)  # posonly means no data field
            self.assertTrue(m.abend() == False)
        except:
            self.fail()

        try:
            pkgname = self.engine.load(b'package year; d = [0-9]')
        except:
            self.fail()

        # input has str type
        m = self.engine.fullmatch(b'year.d{4}', "1998")
        self.assertTrue(m)
        self.assertEqual(m.group(), "1998")

        m = self.engine.fullmatch(b'year.d{4}', "1998 Year")
        self.assertTrue(m == None)

        # input has bytes type
        m = self.engine.fullmatch(b'year.d{4}', b"1998")
        self.assertTrue(m)
        self.assertEqual(m.group(), b"1998")

        m = self.engine.fullmatch(b'year.d{4}', b"1998 Year")
        self.assertTrue(m == None)

        # input has memoryview type
        backing_store = b"1998"
        inp = memoryview(backing_store)
        m = self.engine.fullmatch(b'year.d{4}', inp)
        self.assertTrue(m)
        self.assertEqual(m.group(), inp)

        backing_store = b"1998 Year"
        inp = memoryview(backing_store)
        m = self.engine.fullmatch(b'year.d{4}', inp)
        self.assertTrue(m == None)
        
    def testTrace1(self):
        pkgname = self.engine.import_package(b'net')
        self.assertTrue(pkgname)

        # First, try varying the type of the input.  Later, vary the encoder.

        # Input type is str
        d = self.engine.trace(b'net.fqdn_strict', "a.b.c", encoder=b"condensed")
        self.assertTrue(d['matched'] == True)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)

        # Input type is bytes
        d = self.engine.trace(b'net.fqdn_strict', b"a.b.c", encoder=b"condensed")
        self.assertTrue(d['matched'] == True)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)

        # Input type is memoryview
        backing_store = b"a.b.c"
        inp = memoryview(backing_store)
        d = self.engine.trace(b'net.fqdn_strict', inp, encoder=b"condensed")
        self.assertTrue(d['matched'] == True)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)

        # Using bytes as input type, vary the trace encoder.
        
        d = self.engine.trace(b"net.fqdn_strict", b"a.b.c", encoder=b"condensed")
        self.assertTrue(d['matched'] == True)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)

        d = self.engine.trace(b'net.fqdn_strict', b"a.b.c", encoder=b"full")
        self.assertTrue(d['matched'] == True)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)
        self.assertTrue(d['trace'].find(b'Matched 5 chars') != -1)

        try:
            d = self.engine.trace(b'net.fqdn_strict', b"a.b.c", encoder=b"no_such_trace_style")
            # Force a failure in case the previous line does not throw an exception:
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(repr(e).find('invalid trace style') != -1)

        trace_object = self.engine.trace(b'net.fqdn_strict', b"a.b.c")
        self.assertTrue(trace_object.trace_value())
        self.assertTrue(len(trace_object.trace_value()) > 0)
        self.assertTrue('match' in trace_object.trace_value())
        self.assertTrue(trace_object.trace_value()['match'])
        self.assertTrue('nextpos' in trace_object.trace_value())
        self.assertTrue(trace_object.trace_value()['nextpos'] == 6)
    
    def testSearch(self):
        try:
            pkgname = self.engine.load(b'package year; d = [0-9]')
        except:
            self.fail()

        m = self.engine.search('year.d{4}', "info 1998 23 2006 time 1876")
        self.assertEqual(m.group(), "1998")

    def testFindall(self):
        try:
            pkgname = self.engine.load(b'package year; d = [0-9]')
        except:
            self.fail()

        matches = self.engine.findall('year.d{4}', "info 1998 23 2006 time 1876")
        self.assertTrue("1998" in matches)
        self.assertTrue("2006" in matches)
        self.assertTrue("1876" in matches)
        self.assertTrue("23" not in matches)

    def testSub(self):
        self.assertEqual(self.engine.sub('[0-9]{4}', 'time', 'the year of 1956 and 1957'), 'the year of time and time')

    def testSubn(self):
        self.assertEqual(self.engine.subn('[0-9]{4}', 'time', 'the year of 1956 and 1957'), ('the year of time and time', 2))

    def testReadRCFile(self):
        result, messages = self.engine.read_rcfile("This file does not exist")
        self.assertTrue(result is None)
        if testdir:
            options, messages = self.engine.read_rcfile("rcfile1")
            self.assertIsInstance(options, list)
            self.assertTrue(messages is None)
            options, messages = self.engine.read_rcfile("rcfile2")
            self.assertTrue(messages[0].find("Syntax errors in rcfile") != -1)
            self.assertTrue(options is False)
            options, messages = self.engine.read_rcfile(b"This file does not exist")
            self.assertTrue(options is None)
            self.assertTrue(messages[0].find("Could not open rcfile") != -1)
            
    def testExecuteRCFile(self):
        result, messages = self.engine.execute_rcfile("This file does not exist")
        self.assertTrue(result is None)
        if testdir:
            result, messages = self.engine.execute_rcfile("rcfile1")
            self.assertFalse(result)
            self.assertTrue(messages[0].find("Failed to load another-file") != -1)
            result, messages = self.engine.execute_rcfile("rcfile2")
            self.assertFalse(result)
            self.assertTrue(messages[0].find("Syntax errors in rcfile") != -1)
            result, messages = self.engine.execute_rcfile("rcfile3")
            self.assertFalse(result)
            self.assertTrue(messages[0].find("Failed to load nofile_mod1.rpl") != -1)
            result, messages = self.engine.execute_rcfile("rcfile6")
            self.assertTrue(result)
            self.assertTrue(messages is None)

    def testDeps(self):
        # Expression
        result, messages = self.engine.expression_deps(b'"xyz" A')
        self.assertTrue(result is None)
        self.assertTrue(messages is None)
        #pt = json.loads(result)
        #self.assertTrue(len(pt) == 0)
        result, messages = self.engine.expression_deps(b'A / "hello" / B.c [:digit:]+ p.mac:#hi')
        def check_deps(result, messages, index=None):
            self.assertFalse(result is None)
            self.assertTrue(messages is None)
            pt = json.loads(result)
            if index: pt = pt[index]
            self.assertTrue(len(pt) == 2)
            self.assertTrue(pt[0] == 'B')
            self.assertTrue(pt[1] == 'p')
        check_deps(result, messages)
        result, messages = self.engine.expression_deps(b"A // B.c") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)
        # Block
        result, messages = self.engine.block_deps(b"x = A / B.c; y=[:alpha:] p.mac:#tagname")
        check_deps(result, messages, 'implicit')
        result, messages = self.engine.block_deps(b"import F as G, H; x = A / B.c; y=[:alpha:] p.mac:#tagname")
        check_deps(result, messages, 'implicit')
        pt = json.loads(result)
        pt = pt['explicit']
        self.assertTrue(len(pt) == 2)
        self.assertTrue('as_name' in pt[0])
        self.assertTrue(pt[0]['as_name'] == 'G')
        self.assertTrue('importpath' in pt[0])
        self.assertTrue(pt[0]['importpath'] == 'F')
        self.assertTrue(not 'as_name' in pt[1])
        self.assertTrue('importpath' in pt[1])
        self.assertTrue(pt[1]['importpath'] == 'H')
        result, messages = self.engine.block_deps(b" = A / B.c; y=[:alpha:]") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)

    def testRefs(self):
        # Expression
        result, messages = self.engine.expression_refs(b"A")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue(len(pt) == 1)
        self.assertTrue('ref' in pt[0])
        self.assertTrue('localname' in pt[0]['ref'])
        self.assertTrue(pt[0]['ref']['localname'] == "A")
        result, messages = self.engine.expression_refs(b'A / "hello" / B.c [:digit:]+ mac:#hi')
        def check_refs(result, messages):
            self.assertFalse(result is None)
            self.assertTrue(messages is None)
            pt = json.loads(result)
            self.assertTrue(len(pt) == 3)
            self.assertTrue('ref' in pt[0])
            self.assertTrue(pt[0]['ref']['localname'] == "A")
            self.assertTrue('ref' in pt[1])
            self.assertTrue(pt[1]['ref']['packagename'] == "B")
            self.assertTrue(pt[1]['ref']['localname'] == "c")
            self.assertTrue('ref' in pt[2])
            self.assertTrue(pt[2]['ref']['localname'] == "mac")
        check_refs(result, messages)
        result, messages = self.engine.expression_refs(b"A // B.c") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)
        # Block
        result, messages = self.engine.block_refs(b"x = A / B.c; y=[:alpha:] mac:#tagname")
        check_refs(result, messages)
        result, messages = self.engine.block_refs(b" = A / B.c; y=[:alpha:]") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)

    def testParse(self):
        # Parse expression
        result, messages = self.engine.parse_expression(b"A")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue('ref' in pt)
        self.assertTrue('localname' in pt['ref'])
        self.assertTrue(pt['ref']['localname'] == "A")
        result, messages = self.engine.parse_expression(b"A / B.c")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue('choice' in pt)
        self.assertTrue('exps' in pt['choice'])
        second_exp = pt['choice']['exps'][1]
        self.assertTrue('ref' in second_exp)
        self.assertTrue(second_exp['ref']['packagename'] == "B")
        self.assertTrue(second_exp['ref']['localname'] == "c")
        result, messages = self.engine.parse_expression(b"A // B.c") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)
        # Parse block
        result, messages = self.engine.parse_block(b"x = A / B.c; y=[:alpha:]")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue('block' in pt)
        self.assertTrue('stmts' in pt['block'])
        binding1 = pt['block']['stmts'][0]
        binding2 = pt['block']['stmts'][1]
        def check_binding(b, boundname):
            self.assertTrue('binding' in b)
            self.assertTrue('ref' in b['binding'])
            self.assertTrue('ref' in b['binding']['ref'])
            self.assertTrue('localname' in b['binding']['ref']['ref'])
            self.assertTrue(b['binding']['ref']['ref']['localname'] == boundname)
        check_binding(binding1, 'x')
        check_binding(binding2, 'y')
        result, messages = self.engine.parse_block(b" = A / B.c; y=[:alpha:]") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)

# -----------------------------------------------------------------------------
# Tests for RPLX class
# -----------------------------------------------------------------------------

class RosieRPLXTest(unittest.TestCase):

    engine = None
    
    def setUp(self):
        rosie.load(librosiedir, quiet=True)
        self.engine = rosie.engine()

    def tearDown(self):
        pass

    def test_match_object(self):
        b = None
        try:
            pkgname = self.engine.load('package email; x1 = [a-z]+; x2 = [a-z]+; x3 = [a-z]+')
            b = self.engine.compile('email.x1[@]email.x2[.]email.x3')
            self.assertTrue(b.valid())
        except:
            self.fail()

        m = b.match("user@ncsu.edu")
        self.assertTrue(m)
        self.assertTrue(m.start() == 1)     # match started at char 1
        self.assertEqual(m.end(), 14)
        self.assertEqual(m.group(), "user@ncsu.edu")
        self.assertEqual(m.groupdict(), {'*': 'user@ncsu.edu', 'x1': 'user', 'x2': 'ncsu', 'x3': 'edu'})
        self.assertEqual(m.group('x1', 'x2'), ("user", "ncsu"))
        self.assertEqual(m.group('x1'), "user")
        self.assertEqual(m['x1'], "user")
        self.assertEqual(m.start('x1'), 1)
        self.assertEqual(m.subs('x1'), ['user'])
        self.assertEqual(m.start(1), 1)
        self.assertEqual(m.end('x1'), 5)
        self.assertEqual(m.end(1), 5)
        self.assertEqual(m.span('x1'), (1,5))
        self.assertEqual(m.lastindex(), 3)
        self.assertEqual(m.lastgroup(), 'x3')
        self.assertEqual(m.group(0), "user@ncsu.edu")
        self.assertEqual(m.group(1), "user")
        self.assertEqual(m.group(2), "ncsu")
        self.assertEqual(m[2], "ncsu")
        self.assertEqual(m.group(3), "edu")
        self.assertEqual(m.group(1,2,3), ('user', 'ncsu', 'edu'))
        self.assertTrue(m.abend() == False)

    def testSub(self):
        b = None
        b = self.engine.compile('[0-9]{4}')
        self.assertEqual(b.sub('time', 'the year of 1956 and 1957'), 'the year of time and time')

    def testSubn(self):
        b = None
        b = self.engine.compile('[0-9]{4}')
        self.assertEqual(b.subn('time', 'the year of 1956 and 1957'), ('the year of time and time', 2))

    def testFindIter(self):
        b = None
        b = self.engine.compile('[0-9]{4}')
        iter = b.finditer('the year of 1956 and 1957 and 1988', 1)
        li = [s for s in iter]
        self.assertEqual(len(li), 3)
        self.assertEqual(li[0], "1956")
        self.assertEqual(li[1], "1957")
        self.assertEqual(li[2], "1988")

    def testFullMatch(self):
        b = None
        try:
            pkgname = self.engine.load(b'package year; d = [0-9]')
            b = self.engine.compile(b'year.d{4}')
            self.assertTrue(b.valid())
        except:
            self.fail()

        m = b.fullmatch(b"1998", 1)
        self.assertTrue(m)
        self.assertEqual(m.group(), b"1998")

        m = b.fullmatch(b"1998 Year", 1)
        self.assertTrue(m == None)

        m = b.fullmatch(b"1998 Year", 1, 5)
        self.assertTrue(m)
        self.assertEqual(m.group(), b"1998")
        

    def testMatch(self):
        b = self.engine.compile(b"[:digit:]+")
        self.assertTrue(b.valid())

        # test short match
        m = b.match("321", 2)
        self.assertTrue(m)
        self.assertTrue(m.start() == 2)     # match started at char 2
        self.assertTrue(m.end() == 4)
        self.assertTrue(m.group() == "21")
        self.assertTrue(m.abend() == False)

        m = b.match("3x", encoder='status')
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        self.assertTrue(m['leftover'] == 1)

        m = b.match("3x", 2, encoder='status')
        self.assertTrue(m is None)

        m = b.match("321", 2, encoder='status')
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        self.assertTrue(m['leftover'] == 0)

        m = b.match("321", 3, encoder='status')
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        self.assertTrue(m['leftover'] == 0)
        
        # test no match
        m = b.match("xyz", 1)
        self.assertTrue(m == None)
        m = b.match("xyz", 1, encoder='status')
        self.assertTrue(m == None)

        # test long match (input is str type)
        inp = "889900112233445566778899100101102103104105106107108109110xyz"
        self.assertTrue(isinstance(inp, str))
        linp = len(inp)

        m = b.match(inp, 1)
        self.assertTrue(m)
        self.assertTrue(m.start() == 1)
        self.assertTrue(m.end() == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m.group() == inp[0:-3])
        self.assertTrue(m.abend() == False)

        m = b.match(inp, 10)
        self.assertTrue(m)
        self.assertTrue(m.start() == 10)
        self.assertTrue(m.end() == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m.group() == inp[9:-3])
        self.assertTrue(m.abend() == False)

        # test long match (input is bytes type)
        inp = b"889900112233445566778899100101102103104105106107108109110xyz"
        self.assertTrue(isinstance(inp, bytes))
        linp = len(inp)

        m = b.match(inp, 1)
        self.assertTrue(m)
        self.assertTrue(m.start() == 1)
        self.assertTrue(m.end() == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m.group() == inp[0:-3])
        self.assertTrue(m.abend() == False)

        m = b.match(inp, 10)
        self.assertTrue(m)
        self.assertTrue(m.start() == 10)
        self.assertTrue(m.end() == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m.group() == inp[9:-3])
        self.assertTrue(m.abend() == False)

        # test long match (input is memoryview type)
        backing_store = b"889900112233445566778899100101102103104105106107108109110xyz"
        self.assertTrue(isinstance(backing_store, bytes))
        inp = memoryview(backing_store)
        linp = len(inp)

        m = b.match(inp, 1)
        self.assertTrue(m)
        self.assertTrue(m.start() == 1)
        self.assertTrue(m.end() == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m.group() == inp[0:-3])
        self.assertTrue(m.abend() == False)

        m = b.match(inp, 10)
        self.assertTrue(m)
        self.assertTrue(m.start() == 10)
        self.assertTrue(m.end() == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m.group() == inp[9:-3])
        self.assertTrue(m.abend() == False)

        # test other encoders
        m = b.match(inp, 1, encoder=b"line")
        self.assertTrue(m['match'])
        self.assertTrue(m['abend'] == False)

        m = b.match(inp, 1, encoder=b"status")
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        self.assertTrue(m['match'] == True)
        self.assertTrue(m['abend'] == False)

        m = b.match(inp, linp-3, encoder=b"status")
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        self.assertTrue(m['match'] == True)
        self.assertTrue(m['abend'] == False)

        m = b.match(inp, linp-2, encoder=b"status")
        self.assertTrue(m is None)

        m = b.match(inp, 1, encoder="color")
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        # Checking only the first two chars, looking for the start of
        # ANSI color sequence
        self.assertTrue(m['match'][0:1] == b'\x1B')
        self.assertTrue(m['match'][1:2] == b'[')
        self.assertTrue(m['abend'] == False)

        m = b.match(inp, 1, encoder="line")
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        self.assertTrue(m['match'] == inp)
        self.assertTrue(m['abend'] == False)
        
        m = b.match(inp, 1, encoder="json")
        self.assertTrue(m)
        self.assertIsInstance(m, dict)
        self.assertTrue(m['match'])
        self.assertTrue(m['abend'] == False)
        match = json.loads(m['match'])
        self.assertTrue(match['type'] == "*")
        self.assertTrue(match['s'] == 1)
        self.assertTrue(match['e'] == 58)
        self.assertIsInstance(match['data'], str)
        self.assertTrue(match['data'] == str(inp[:-3], encoding='UTF-8'))
        
        with self.assertRaises(ValueError) as ctx:
            m = b.match(inp, 1, encoder="foo_no_such_encoder_foo")
        self.assertTrue("invalid output encoder" in str(ctx.exception))

    def testMatch_pos_errs(self):
        pat = self.engine.compile(b"[:digit:]*")
        self.assertTrue(pat.valid())
        inp = "12345"

        # Supplying neither start nor end positions should produce a match
        m = pat.match(inp)
        self.assertTrue(m)
        self.assertTrue(m.pos == 1)
        self.assertTrue(m.endpos == len(inp))
        self.assertTrue(m.span() == (1, len(inp)+1)) # 1-based, semi-open

        # Supplying valid start and end positions should produce a match
        m = pat.match(inp, 2, 4)
        self.assertTrue(m)
        self.assertTrue(m.pos == 2)
        self.assertTrue(m.endpos == 4)
        self.assertTrue(m.span() == (2, 4)) # 1-based, semi-open

        # Supplying same start and end positions makes input string empty
        m = pat.match(inp, 3, 3)
        self.assertTrue(m)
        self.assertTrue(m.pos == 3)
        self.assertTrue(m.endpos == 3)
        self.assertTrue(m.span() == (3, 3)) # 1-based, semi-open
        self.assertTrue(m.group() == "")

        # Supplying same start and end positions makes input string empty
        m = pat.match(inp, 2, 2)
        self.assertTrue(m)
        self.assertTrue(m.pos == 2)
        self.assertTrue(m.endpos == 2)
        self.assertTrue(m.span() == (2, 2)) # 1-based, semi-open
        self.assertTrue(m.group() == "")

        # A start position at input length is treated as input length
        m = pat.match(inp, 5, 5)
        self.assertTrue(m)
        self.assertTrue(m.span() == (5, 5)) # 1-based, semi-open

        # A start position beyond input length is treated as input length
        m = pat.match(inp, 6)
        self.assertTrue(m)
        self.assertTrue(m.span() == (6, 6)) # 1-based, semi-open

        # An end position beyond input length is treated as input length
        m = pat.match(inp, 3, 7)
        self.assertTrue(m)
        self.assertTrue(m.span() == (3, 6)) # 1-based, semi-open

        # Both positions beyond input length are treated as input length
        m = pat.match(inp, 76, 76)
        self.assertTrue(m)
        self.assertTrue(m.span() == (6, 6)) # 1-based, semi-open

        # Out of order positions are treated as if both are startpos
        #   Try out of order where startpos is beyond end of input
        m = pat.match(inp, 7, 1)
        self.assertTrue(m)
        self.assertTrue(m.span() == (6, 6)) # 1-based, semi-open
        #   Try out of order where startpos is within the input
        m = pat.match(inp, 3, 2)
        self.assertTrue(m)
        self.assertTrue(m.span() == (3, 3)) # 1-based, semi-open


    # TODO: run this test with a variety of encoders and a variety of
    # input types (str, bytes, memoryview).
    def testMatch_with_pos_args(self):
        pat = self.engine.compile(b"{!<[:digit:] [:digit:]+}")
        self.assertTrue(pat.valid())

        expected_matches = ((1,"8"), (3,"89"), (6,"900"), (10,"1122"),
                            (15,"33445"), (21,"566778"), (28,"8991001"),
                            (40, "1"))
        inp = "8 89 900 1122 33445 566778 8991001 xyz 1"
        self.assertTrue(len(inp) == 40)

        m = pat.match(inp)
        self.assertTrue(m)
        self.assertTrue(m.pos == 1)
        self.assertTrue(m.endpos == len(inp))
        self.assertTrue(m.span() == (1, 2)) # 1-based, semi-open

        # control debugging output
        debug = False
        # test startpos argument, leaving endpos as default
        index = 0
        for i in range(1, len(inp)):
            expected_pos, expected_match = expected_matches[index]
            if debug:
                print("Looking for match ({}, {})".format(expected_pos, expected_pos+len(expected_match)))
            m = pat.match(inp, i) # varying only startpos
            if m:
                # Check that that actual match is the expected match
                self.assertTrue(m.pos == i)
                self.assertTrue(m.endpos == len(inp))
                if debug:
                    print("Match ({}, {}); group = '{}'".format(m.start(), m.end(), m.group()))
                self.assertTrue(m.start() == expected_pos)
                self.assertTrue(m.end() == expected_pos + len(expected_match))
                self.assertTrue(m.group() == inp[expected_pos-1 : expected_pos+len(expected_match)-1])
                index += 1
            else:
                # We have not yet reached the next expected match
                self.assertTrue(i < expected_pos)

        # test endpos argument for various values of startpos
        index = 0
        for start in range(1, len(inp)):
            expected_pos, expected_match = expected_matches[index]
            found_entire_match = False
            if debug:
                print("Looking for match ({}, {})".format(expected_pos, expected_pos+len(expected_match)))
            for endpos in range(start, len(inp)):
                if debug:
                    print("Testing start={}, endpos={}".format(start, endpos))
                m = pat.match(inp, start, endpos)
                if m:
                    # Check that that actual match is the expected match
                    self.assertTrue(m.pos == start)
                    self.assertTrue(m.endpos == endpos)
                    if debug:
                        print("Match ({}, {}); group = '{}'".format(m.start(), m.end(), m.group()))
                    self.assertTrue(m.start() == expected_pos)
                    expected_end = min(expected_pos + len(expected_match), endpos)
                    if debug:
                        print("endpos = {}, m.end() = {}, expected_end = {}".format(endpos, m.end(), expected_end))
                    self.assertTrue(m.end() == expected_end)
                    self.assertTrue(m.group() == inp[expected_pos-1 : expected_end-1])
                    found_entire_match = expected_end < endpos
            if found_entire_match: index += 1
                
    def testMatchDecoding(self):
        b = None
        try:
            self.engine.load('int = [:digit:]+')
            b = self.engine.compile('findall:int')
            self.assertTrue(b.valid())
        except:
            self.fail()

        try:
            # Start the match at second character, i.e. '1'
            m = b.match("Z1 22 333 4444 55555 X", 2)
            self.assertTrue(m)
            self.assertTrue(m.start() == 2)     # rosie uses 1-based indexing
            self.assertTrue(m.end() == 21)
            self.assertTrue(m.span() == (2, 21))
            self.assertTrue(m.pos == 2)
            self.assertTrue(m.endpos == 22)
            self.assertTrue(m.group() == "1 22 333 4444 55555")
            self.assertTrue(m.groups() == ('1', '22', '333', '4444', '55555'))
            self.assertTrue(m.lastindex() == 5)
            self.assertTrue(m.abend() == False)
        except:
            self.fail()

    def testMatchConstCapture(self):
        b = None
        try:
            self.engine.load('int = { [:digit:]+ message:#foo }')
            b = self.engine.compile('findall:int')
            self.assertTrue(b.valid())
        except:
            self.fail()

        try:
            # Start the match at second character, i.e. '1'
            m = b.match("Z1 22 333 4444 55555 X", 2)
            self.assertTrue(m)
            self.assertTrue(m.start() == 2)     # rosie uses 1-based indexing
            self.assertTrue(m.end() == 21)
            self.assertTrue(m.span() == (2, 21))
            self.assertTrue(m.pos == 2)
            self.assertTrue(m.endpos == 22)
            self.assertTrue(m.group() == "1 22 333 4444 55555")
            # Test result depends on a bug in Rosie 1.2 that was fixed in 1.3
            ver = self.engine.version()
            self.assertIsInstance(ver, str)
            versions = ver.split('.')
            self.assertTrue(len(versions) >= 2)
            self.assertTrue(versions[0] == '1')
            minor = int(versions[1])
            if minor < 3:
                self.assertTrue(m.groups() == ('1', '<search>',
                                               '22', '<search>',
                                               '333', '<search>',
                                               '4444', '<search>',
                                               '55555', '<search>'))
            else:
                # Correct behavior, as of Rosie 1.3.0
                self.assertTrue(m.groups() == ('1', 'foo',
                                               '22', 'foo',
                                               '333', 'foo',
                                               '4444', 'foo',
                                               '55555', 'foo'))
            self.assertTrue(m.lastindex() == 10)
            self.assertTrue(m.abend() == False)
        except:
            self.fail()

    def testTrace2(self):
        pkgname = self.engine.import_package(b'net')
        self.assertTrue(pkgname)
        self.net_any = self.engine.compile(b'net.any')
        self.assertTrue(self.net_any)

        d = self.net_any.trace(b"a.b.c", 1, encoder=b"condensed")
        self.assertTrue(d['matched'] == True)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)

        net_ip = self.engine.compile(b"net.ip")
        self.assertTrue(net_ip)
        d = net_ip.trace(b"a.b.c", 1, encoder=b"condensed")
        self.assertTrue(d['matched'] == False)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)

        d = self.net_any.trace(b"a.b.c", 1, encoder=b"full")
        self.assertTrue(d['matched'] == True)
        self.assertTrue(d['trace'])
        self.assertTrue(len(d['trace']) > 0)
        self.assertTrue(d['trace'].find(b'Matched 5 chars') != -1)

        try:
            d = self.net_any.trace(b"a.b.c", 1, encoder=b"no_such_trace_style")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(repr(e).find('invalid trace style') != -1)

        trace_object = self.net_any.trace(b"a.b.c", 1)
        self.assertTrue(trace_object.trace_value())
        self.assertTrue(len(trace_object.trace_value()) > 0)
        self.assertTrue('match' in trace_object.trace_value())
        self.assertTrue(trace_object.trace_value()['match'])
        self.assertTrue('nextpos' in trace_object.trace_value())
        self.assertTrue(trace_object.trace_value()['nextpos'] == 6)

    def testSearch(self):
        b = None
        try:
            pkgname = self.engine.load(b'package year; d = [0-9]')
            b = self.engine.compile('year.d{4}')
            self.assertTrue(b.valid())
        except:
            self.fail()

        m = b.search("info 1998 23 2006 time 1876", 1)
        self.assertEqual(m.group(), "1998")

    def testFindall(self):
        b = None
        try:
            pkgname = self.engine.load(b'package year; d = [0-9]')
            b = self.engine.compile('year.d{4}')
            self.assertTrue(b.valid())
        except:
            self.fail()

        matches = b.findall("info 1998 23 2006 time 1876", 1)
        self.assertTrue("1998" in matches)
        self.assertTrue("2006" in matches)
        self.assertTrue("1876" in matches)
        self.assertTrue("23" not in matches)



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
