# coding: utf-8
#  -*- Mode: Python; -*-                                              
# 
#  rosie.py     An interface to librosie from Python 3.x
# 
#  © Copyright IBM Corporation 2016, 2017
#  © Copyright AUTHORS (see below) 2018, 2019, 2020, 2021.
#  LICENSE: MIT License (https://opensource.org/licenses/mit-license.html)
#  AUTHOR: Jenna N. Shockley
#  AUTHOR: Jamie A. Jennings

# Development environment (2021):
#
#   Mac OS Big Sur (11.1)
#   Python 3.9.4 (installed via homebrew)
#     cffi 1.14.5 (installed via pip3)
#

import sys, json
assert(sys.version_info.major == 3)

from . import decode
from . import internal

# We use bytes23() to allow the caller to supply string arguments in
# either the str or bytes form.
def bytes23(s):
    if isinstance(s, str):
        return bytes(s, encoding='UTF-8')
    elif isinstance(s, (bytes, memoryview)):
        return s
    else:
        raise TypeError('argument is not str, bytes, or memoryview: ' + repr(s))

# -----------------------------------------------------------------------------

def librosie_path():
    return internal._librosie_path

def librosie_system():
    return internal.librosie_system

def librosie_local():
    return internal.librosie_local

def load(path = None, **kwargs):
    return internal.load(path, kwargs)

# -----------------------------------------------------------------------------
# re package flags (for reference)
'''class RegexFlag(enum.IntFlag):
    ASCII = RE_FLAG_ASCII              # assume ascii "locale"
    IGNORECASE = RE_FLAG_IGNORECASE    # ignore case
    LOCALE = RE_FLAG_LOCALE            # assume current 8-bit locale
    UNICODE = RE_FLAG_UNICODE          # assume unicode "locale"
    MULTILINE = RE_FLAG_MULTILINE      # make anchors look for newline
    DOTALL = RE_FLAG_DOTALL            # make dot match newline
    VERBOSE = RE_FLAG_VERBOSE          # ignore whitespace and comments
    A = ASCII
    I = IGNORECASE
    L = LOCALE
    U = UNICODE
    M = MULTILINE
    S = DOTALL
    X = VERBOSE'''

# -----------------------------------------------------------------------------
# Rosie Engine

class engine (object):

    '''
    A Rosie pattern matching engine is used to load/import RPL code
    (patterns) and to do matching.  Create as many engines as you need.
    '''

    _version = None

    def __init__(self):
        self._engine = internal.engine()
    
    # -----------------------------------------------------------------------------
    # Compile an expression
    # -----------------------------------------------------------------------------

    def compile(self, exp):
        pat, errs = self._engine.compile(bytes23(exp))
        if not pat:
            raise_rosie_error(errs)
        return rplx(self, exp, pat)


    # -----------------------------------------------------------------------------
    # Basic methods
    # included in python re
    # -----------------------------------------------------------------------------

    def match(self, pattern, string, **kwargs):
        """Try to apply the pattern at the start of the string, returning
        a match object, or None if no match was found."""
        pattern = self.compile(pattern)
        return pattern.match(string, **kwargs)
    
    def fullmatch(self, pattern, input, **kwargs):
        pattern = self.compile(pattern)
        return pattern.fullmatch(input, **kwargs)

    def trace(self, pattern, input, **kwargs):
        pattern = self.compile(pattern)
        return pattern.trace(input, **kwargs)

    def search(self, pattern, string, **kwargs):
        pattern = self.compile(pattern)
        return pattern.search(string, **kwargs)

    def findall(self, pattern, string, **kwargs):
        pattern = self.compile(pattern)
        return pattern.findall(string, **kwargs)

    def finditer(self, pattern, string, **kwargs):
        pattern = self.compile(pattern)
        return pattern.finditer(string, **kwargs)

    def sub(self, pattern, repl, string, **kwargs):
        pattern = self.compile(pattern)
        return pattern.sub(repl, string, **kwargs)

    def subn(self, pattern, repl, string, **kwargs):
        pattern = self.compile(pattern)
        return pattern.subn(repl, string, **kwargs)

    def purge(self):
        raise NotImplementedError(
            "purge is an 're' function that is not applicable to RPL."
        )


    # -----------------------------------------------------------------------------
    # Functions for loading statements/blocks/packages into an engine
    # this functionality not included in python re
    # -----------------------------------------------------------------------------

    def load(self, src):
        ok, pkgname, errs = self._engine.load(bytes23(src))
        if not ok:
            raise_rosie_error(errs)
        return pkgname

    def loadfile(self, filename):
        ok, pkgname, errs = self._engine.loadfile(bytes23(filename))
        if not ok:
            raise_rosie_error(errs)
        return pkgname

    def import_package(self, pkgname, as_name=None):
        ok, actual_pkgname, errs = self._engine.import_pkg(bytes23(pkgname),
                                                           as_name and bytes23(as_name))
        if not ok:
            raise_rosie_error(errs)
        return actual_pkgname

    # -----------------------------------------------------------------------------
    # Functions for reading and processing rcfile (init file) contents.
    # This functionality not included in python re.
    # -----------------------------------------------------------------------------
    
    def read_rcfile(self, filename=None):
        if isinstance(filename, str):
            filename = bytes(filename, encoding='UTF-8')
        return self._engine.read_rcfile(filename)

    def execute_rcfile(self, filename=None):
        if isinstance(filename, str):
            filename = bytes(filename, encoding='UTF-8')
        return self._engine.execute_rcfile(filename)

    # -----------------------------------------------------------------------------
    # Functions that return a parse tree or fragments of one.
    # This functionality not included in python re
    # -----------------------------------------------------------------------------

    def parse_expression(self, exp):
        return self._engine.parse_expression(exp)
        
    def parse_block(self, block):
        return self._engine.parse_block(block)
        
    def expression_refs(self, exp):
        return self._engine.expression_refs(exp)
        
    def block_refs(self, block):
        return self._engine.block_refs(block)
        
    def expression_deps(self, exp):
        return self._engine.expression_deps(exp)
        
    def block_deps(self, block):
        return self._engine.block_deps(block)

    # -----------------------------------------------------------------------------
    # Functions for reading and modifying various engine settings
    # this functionality not included in python re
    # -----------------------------------------------------------------------------

    def config(self):
        return json.loads(self._engine.config())

    # In theory, each engine can support a different version of Rosie,
    # although in practice (currently) we do not provide a way to
    # create engines that implement other versions.
    def version(self):
        if self._version: return self._version
        all_config = self.config()
        if not all_config: raise RunTimeError('failed to get rosie configuration')
        rosie_attributes = all_config[0]
        for item in rosie_attributes:
            if item['name']=='ROSIE_VERSION':
                self._version = item['value']
                break
        return self._version

    def libpath(self, libpath=None):
        return self._engine.libpath(libpath)

    def alloc_limit(self, newlimit=None):
        return self._engine.alloc_limit(newlimit)

    def __del__(self):
        self._engine = None


class RPLError (Exception):
    def __init__(self, violations):
        self.errs = violations
    def __str__(self):
        human_readable = "\n"
        for err in self.errs:
            if 'formatted' in err:
                human_readable += err['formatted']
            else:
                human_readable += "{} reports: {}\n".format(
                    (err['who'] or "<unknown component>"),
                    (err['message'] or "<missing error message>"))
        return human_readable

def raise_rosie_error(encoded_errors):
    try:
        errs = json.loads(encoded_errors)
    except:
        raise RuntimeError('Unexpected RPL error format:\n{}'.format(errstring))
    raise RPLError(errs)


def raise_halt_error():
    raise RuntimeError('Matching aborted due to pattern containing halt pattern')


class rplx (object):            # A compiled pattern  

    def __init__(self, engine, exp, internal_rplx):
        self.pattern = exp      # bytes or str
        self._internal_rplx = internal_rplx
        self.engine = engine
    
    def valid(self):
        return self._internal_rplx.valid
    
    def match(self, string, pos=1, endpos=None, **kwargs):
        encoder = kwargs['encoder'] if 'encoder' in kwargs else 'byte'
        posonly = kwargs['posonly'] if 'posonly' in kwargs else False
        m, l, a, ttotal, tmatch = self._internal_rplx.engine.match(
            self._internal_rplx,
            bytes23(string),    # if str type, convert it
            pos,
            endpos,
            bytes23(encoder))
        # Was matching halted by abend without any partial match being found?
        if a and (m == False):
            raise_halt_error()
        elif m == False:
            return None
        if 'encoder' in kwargs:
            dict_return = {'match':m, 'leftover':l, 'abend':a}
            return dict_return
        else:
            match_value = decode.decode(m, (None if posonly else string))
            matchObject = Match(match_value, self, string, a, pos, endpos)
            return matchObject

    def fullmatch(self, string, pos=1, endpos=None, **kwargs):
        encoder = kwargs['encoder'] if 'encoder' in kwargs else 'byte'
        posonly = kwargs['posonly'] if 'posonly' in kwargs else False
        m, l, a, ttotal, tmatch = self._internal_rplx.engine.match(
            self._internal_rplx,
            bytes23(string),
            pos,
            endpos,
            bytes23(encoder))
        # If matching was halted and no partial match was found, then signal error
        if a and (m == False):
            raise_halt_error()
        elif (m == False) or (l != 0):
            return None
        if 'encoder' in kwargs:
            dict_return = {'match':m, 'leftover':l, 'abend':a}
            return dict_return
        else:
            match_value = decode.decode(m, (None if posonly else string))
            matchObject = Match(match_value, self, string, a, pos, endpos)
            return matchObject

    def trace(self, string, pos=1, endpos=None, **kwargs):
        encoder = kwargs['encoder'] if 'encoder' in kwargs else 'json'
        matched, trace_data = self._internal_rplx.engine.trace(
            self._internal_rplx,
            bytes23(string),
            pos,
            bytes23(encoder))
        if 'encoder' in kwargs:
            return {'matched': matched, 'trace': trace_data}
        else:
            trace_value = json.loads(trace_data)
            return Trace(matched, trace_value)

    # TODO: Doesn't the 'grep' command in the CLI use an API that
    # applies 'find' to a pattern at the AST level?  We should be
    # using that!
    def search(self, string, pos=1, endpos=None, **kwargs):
        pattern = "find:{{({})}}".format(self.pattern)
        rplx_object = self.engine.compile(pattern)
        match_object = rplx_object.match(string, pos, endpos, **kwargs)
        if match_object is None:
            return None
        m = match_object.rosie_match
        for s in m['subs']:
            return Match(s, rplx_object, string, match_object.abend(), pos, endpos)

    def findall(self, string, pos=1, endpos=None, **kwargs):
        pattern = "findall:{{({})}}".format(self.pattern)
        rplx_object = self.engine.compile(pattern)
        match_object = rplx_object.match(string, pos, endpos, **kwargs)
        if match_object is None:
            return None
        m = match_object.rosie_match
        subs = []
        if 'subs' in m:
            for s in m['subs']:
                subs.append(s['data'])
        return subs

    def finditer(self, string, pos=1, endpos=None, **kwargs):
        pattern = "findall:{{({})}}".format(self.pattern)
        rplx_object = self.engine.compile(pattern)
        match_object = rplx_object.match(string, pos, endpos, **kwargs)
        if match_object is None:
            return None
        m = match_object.rosie_match
        subs = []
        if 'subs' in m:
            for s in m['subs']:
                subs.append(s['data'])
        return iter(subs)
    
    # TODO: This is a quadratic time impl that also makes unnecessary
    # string allocations.  FIXME!
    def sub(self, repl, string, count = 0):
        pattern = "find:{{({})}}".format(self.pattern)
        rplx_object = self.engine.compile(pattern)
        match_object = rplx_object.match(string)
        found = (match_object != None)
        while (found):
            m = match_object.rosie_match['subs'][0]
            string = string[0:m['s'] - 1] + repl + string[(m['e'] - 1):]
            match_object = rplx_object.match(string)
            found = (match_object != None)
        return string

    # TODO: This is a quadratic time impl that also makes unnecessary
    # string allocations.  FIXME!
    # And it shares code with sub() above.  Combine them!
    def subn(self, repl, string, count = 0):
        pattern = "find:{{({})}}".format(self.pattern)
        rplx_object = self.engine.compile(pattern)
        count_of_subs = 0
        match_object = rplx_object.match(string)
        found = (match_object != None)
        while (found):
            m = match_object.rosie_match['subs'][0]
            string = string[0:m['s'] - 1] + repl + string[(m['e'] - 1):]
            count_of_subs += 1
            match_object = rplx_object.match(string)
            found = (match_object != None)
        return (string, count_of_subs)



class Trace (object):
    def __init__(self, matchedValue, trace):
        self.matchedValue = matchedValue
        self.trace = trace

    def trace_value(self):
        return self.trace

    def matched(self):
        return self.matchedValue


class Match (object):

    def __init__(self, rosie_match, rplx_object, stringObject, a, position, endposition):
        self.re = rplx_object
        self.string = stringObject
        self.rosie_match = rosie_match
        self.a = a
        self.matches = []
        self.pos = position
        if (endposition == None):
            self.endpos = len(self.string)
        else:
            self.endpos = endposition

    # Convert subs tree into list
    def _convertSubsToGroups(self, m):
        list = []
        match = Match(m,self.re,self.string,self.a,self.pos,self.endpos)
        list.append(match)
        if 'subs' in m:
            for s in m['subs']:
                list.extend(self._convertSubsToGroups(s))
        return list

    def _set_matches(self):
        # One-time (lazy) conversion from rosie_match
        if not self.matches:
            assert(type(self.matches) is list)
            self.matches.extend(self._convertSubsToGroups(self.rosie_match))

    def expand(self, template):
        raise NotImplementedError(
            "expand is an 're' function that is not applicable to RPL."
        )

    def __getitem__(self, groupIdentifier):
        return self.group(groupIdentifier)

    def group(self, *args):
        if (not args):
            # Return original match
            return self.rosie_match['data']
        self._set_matches()
        # Find capture by number
        if isinstance(args[0], int):
            if (len(args) == 1):
                m = self.matches[args[0]]
                return m.rosie_match['data']
            list = []
            for groupIndex in args:
                m = self.matches[groupIndex]
                list.append(m.rosie_match['data'])
            return tuple(list)
        # Find capture by name
        # Assume that args[0] is str, unicode, or bytes
        if (len(args) == 1):
            for match in self.matches:
                if match.rosie_match['type'] == args[0]:
                    return match.rosie_match['data']
            return None
        list = []
        for namedCapture in args:
            found = False
            for match in self.matches:
                if match.rosie_match['type'] == namedCapture:
                    list.append(match.rosie_match['data'])
                    found = True
            if found is False:
                list.append(None)
        return tuple(list)
            

    def groups(self):
        '''Return a tuple containing all the subgroups of the match, from 1 up to however many groups are in the pattern. 
        The default argument is used for groups that did not participate in the match; it defaults to None'''
        self._set_matches()
        list = []
        for match in self.matches:
            list.append(match.rosie_match['data'])
        del list[0]
        return tuple(list)

    def groupdict(self):
        '''Return a dictionary containing all the named subgroups of the match, keyed by the subgroup name. 
        The default argument is used for groups that did not participate in the match; it defaults to None.'''
        self._set_matches()
        dict_return = {}
        for match in self.matches:
            dict_return[match.rosie_match['type']] = match.rosie_match['data']
        return dict_return

    def subs(self, *args):
        self._set_matches()

        if (not args):
            # Return a list of all the matched strings
            subs = []
            for match in self.matches:
                subs.append(match.rosie_match['data'])
            return subs

        if (len(args) != 1):
            raise_rosie_error("too many arguments")

        # Find capture by number
        if isinstance(args[0], int):
            if (len(args) == 1):
                if (len(args[0].matches) == 0):
                    args[0].matches.extend(args[0]._convertSubsToGroups(args[0].rosie_match))
            subs = []
            for match in args[0].matches:
                subs.append(match.rosie_match['data'])
            return subs

        # Find capture by name
        # Assume args[0] is str or similar
        if (len(args) == 1):
            for match in self.matches:
                if match.rosie_match['type'] == args[0]:
                    if (len(match.matches) == 0):
                        match.matches.extend(match._convertSubsToGroups(match.rosie_match))
                    subs = []
                    for submatch in match.matches:
                        subs.append(submatch.rosie_match['data'])
                    return subs
            return None


    def start(self, *args):
        if (not args):
            return self.rosie_match['s']
        self._set_matches()
        if isinstance(args[0], int):
            if (len(args) == 1):
                m = self.matches[args[0]]
                return m.rosie_match['s']
            else:
                raise_rosie_error("too many arguments")
        # Assume args[0] is str, unicode, bytes, or similar
        if (len(args) == 1):
            for match in self.matches:
                if match.rosie_match['type'] == args[0]:
                    return match.rosie_match['s']
        else:
            raise_rosie_error("too many arguments")

    def end(self, *args):
        if (not args):
            return self.rosie_match['e']
        if (len(args) != 1):
            raise_rosie_error("too many arguments")
        self._set_matches()
        if isinstance(args[0], int):
            m = self.matches[args[0]]
            return m.rosie_match['e']
        # Assume args[0] is str
        for match in self.matches:
            if match.rosie_match['type'] == args[0]:
                return match.rosie_match['e']

    def span(self, *args):
        if (not args):
            return (self.start(), self.end())
        else:
            return (self.start(*args), self.end(*args))

    def lastindex(self):
        # Integer index of the last matched capturing group, or None
        # if no group was matched at all
        self._set_matches()
        return len(self.matches) - 1

    def lastgroup(self):
        # Name of the last matched capturing group, or None if the
        # group didn’t have a name, or if no group was matched at all
        self._set_matches()
        return self.matches[len(self.matches) - 1].rosie_match['type']

    def abend(self):
        return self.a

    
    




