# coding: utf-8
#  -*- Mode: Python; -*-                                              
# 
#  internal.py     Low level interface to librosie for Python 3.x
# 
#  © Copyright IBM Corporation 2016, 2017, 2018.
#  © Copyright AUTHORS (see below) 2019, 2020, 2021.
#  LICENSE: MIT License (https://opensource.org/licenses/mit-license.html)
#  AUTHOR: Jamie A. Jennings

# TODO:
# - replace magic error code numbers with constants

from cffi import FFI
import sys, platform, os, json
assert( sys.version_info.major == 3 )

ffi = FFI()

# See librosie.h
ffi.cdef("""

typedef uint8_t * byte_ptr;

typedef struct rosie_string {
     uint32_t len;
     byte_ptr ptr;
} str;

typedef struct rosie_matchresult {
     str data;
     int leftover;
     int abend;
     int ttotal;
     int tmatch;
} match;

str *rosie_string_ptr_from(byte_ptr msg, size_t len);
void rosie_free_string_ptr(str *s);
void rosie_free_string(str s);

void *rosie_new(str *errors);
void rosie_finalize(void *L);
int rosie_libpath(void *L, str *newpath);
int rosie_alloc_limit(void *L, int *newlimit, int *usage);
int rosie_config(void *L, str *retvals);
int rosie_compile(void *L, str *expression, int *pat, str *errors);
int rosie_free_rplx(void *L, int pat);
int rosie_match(void *L, int pat, int start, char *encoder, str *input, match *match);
int rosie_matchfile(void *L, int pat, char *encoder, int wholefileflag,
		    char *infilename, char *outfilename, char *errfilename,
		    int *cin, int *cout, int *cerr,
		    str *err);
int rosie_trace(void *L, int pat, int start, char *trace_style, str *input, int *matched, str *trace);
int rosie_load(void *L, int *ok, str *src, str *pkgname, str *errors);
int rosie_loadfile(void *e, int *ok, str *fn, str *pkgname, str *errors);
int rosie_import(void *e, int *ok, str *pkgname, str *as, str *actual_pkgname, str *messages);
int rosie_read_rcfile(void *e, str *filename, int *file_exists, str *options, str *messages);
int rosie_execute_rcfile(void *e, str *filename, int *file_exists, int *no_errors, str *messages);

int rosie_expression_refs(void *e, str *input, str *refs, str *messages);
int rosie_block_refs(void *e, str *input, str *refs, str *messages);
int rosie_expression_deps(void *e, str *input, str *deps, str *messages);
int rosie_block_deps(void *e, str *input, str *deps, str *messages);
int rosie_parse_expression(void *e, str *input, str *parsetree, str *messages);
int rosie_parse_block(void *e, str *input, str *parsetree, str *messages);

void free(void *obj);

int rosie_match2 (void *e, uint32_t pat, char *encoder_name,
		  str *input, uint32_t startpos, uint32_t endpos,
		  match *match,
		  uint8_t collect_times);
""")

# Single instance of dynamic library
_lib = None

# Values of _librosie_path:
#
#   librosie_system --> Search for librosie in system-dependent directories,
#       (e.g. /usr/local/lib), which can be affected LD_LIBRARY_PATH and related
#       environment variables. 
#
#   librosie_local --> Load librosie from the same directory as this file,
#       internal.py.  Equivalent to using '//' as the argument.
#
#   path (string) --> Load librosie from the given path.  If the path
#       starts with '//' it is interpreted as relative to where this
#       file is installed.  A path starting with './' is relative to
#       the current directory of the process, and is discouraged.
#
#   None --> First try librosie_local, and if that fails, try librosie_system.

# Single instance of default path to use when loading librosie (see above)
_librosie_path = None       

class _librosie_config(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return name

librosie_system = _librosie_config('*system*')
librosie_local = _librosie_config('*local*')

# Single instance of default library name, where None means:
# (1) the base file name will be 'librosie', and
# (2) the file name extension will be set based on the OS.
_librosie_name = None

# Single instance flag indicating if the version of librosie that we
# loaded has a definition for rosie_match2 (August, 2021).
_have_rosie_match2 = False

# -----------------------------------------------------------------------------
# ffi utilities

# The _new_cstr() function creates a Rosie string struct that points
# to the Python storage for the 'string' argument.  No copying
# occurs. The Rosie struct will be freed automatically when no longer
# needed, thanks to ffi.gc().

def free_cstr_ptr(local_cstr_obj):
    _lib.rosie_free_string(local_cstr_obj[0])

def _new_cstr(string=None):
    if string is None:
        obj = ffi.new("struct rosie_string *")
        return ffi.gc(obj, free_cstr_ptr)
    elif isinstance(string, (bytes, bytearray)):
        obj = _lib.rosie_string_ptr_from(string, len(string))
        return ffi.gc(obj, _lib.free)
    elif isinstance(string, memoryview):
        obj = _lib.rosie_string_ptr_from(ffi.from_buffer(string), len(string))
        return ffi.gc(obj, _lib.free)
    raise ValueError("Unsupported argument type: " + str(type(string)))

# The _read_cstr() function returns a COPY of the data in its Rosie
# string struct argument.

def _read_cstr(cstr_ptr):
    if cstr_ptr.ptr == ffi.NULL:
        return None
    else:
        # The call to bytes() makes a copy of the ffi buffer data
        return bytes(ffi.buffer(cstr_ptr.ptr, cstr_ptr.len)[:])

# -----------------------------------------------------------------------------

def load(path = None, quiet = False):
    global _lib
    if _lib:
        # librosie already loaded via cffi, and can only load it once
        if quiet:
            return
        else:
            raise RuntimeError('librosie already loaded from ' + _librosie_path)
    if path == None:
        # Try current directory first, then system directories
        if _load_from('//') or _load_from(''): return
    elif path == librosie_system:
        if  _load_from(''): return
    elif path == librosie_local:
        if _load_from('//'): return
    else:
        if _load_from(path): return
    raise RuntimeError('Failed to load librosie.  Check that rosie is installed?')


def _load_from(path_string):
    global _librosie_name, _librosie_path, _lib, _have_rosie_match2
    if not _librosie_name:
        ostype = platform.system()
        if ostype=="Darwin":
            _librosie_name = "librosie.dylib"
        else:
            _librosie_name = "librosie.so"
    if path_string[0:2]=='//':
        # Try to find librosie at a path relative to this python file
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               path_string[2:],
                               _librosie_name)
    else:
        # Try to find librosie at an absolute filesystem path, where
        # an empty path tells cffi to look in all the system directories
        libpath = os.path.join(path_string, _librosie_name)
    try:
        _lib = ffi.dlopen(libpath, ffi.RTLD_LAZY | ffi.RTLD_GLOBAL)
    except OSError as err:
        # Indicate failure
        return False
    # Success
    _librosie_path = libpath

    try:
        ffi.addressof(_lib, "rosie_match2")
        _have_rosie_match2 = True
    except AttributeError as err:
        _have_rosie_match2 = False
    return True


def librosie_path():
    return _librosie_path


class engine (object):
    '''
    A Rosie pattern matching engine is used to load/import RPL code
    (patterns) and to do matching.  Create as many engines as you need.
    '''
    def __init__(self):
        global _lib
        if not _lib: load()
        Cerrs = _new_cstr()
        self.engine = _lib.rosie_new(Cerrs)
        if self.engine == ffi.NULL:
            raise RuntimeError("librosie: " + str(_read_cstr(Cerrs)))
        self.Cmatch = ffi.new("struct rosie_matchresult *")

    def compile(self, exp):
        Cerrs = _new_cstr()
        Cexp = _new_cstr(exp)
        pat = rplx(self)
        ok = _lib.rosie_compile(self.engine, Cexp, pat.id, Cerrs)
        if ok != 0:
            raise RuntimeError("compile() failed (please report this as a bug)")
        if pat.id[0] == 0:
            pat = None
        return pat, _read_cstr(Cerrs)

    # -----------------------------------------------------------------------------
    # Functions for loading statements/blocks/packages into an engine
    # -----------------------------------------------------------------------------

    def load(self, src):
        Cerrs = _new_cstr()
        Csrc = _new_cstr(src)
        Csuccess = ffi.new("int *")
        Cpkgname = _new_cstr()
        ok = _lib.rosie_load(self.engine, Csuccess, Csrc, Cpkgname, Cerrs)
        if ok != 0:
            raise RuntimeError("load() failed (please report this as a bug)")
        errs = _read_cstr(Cerrs)
        pkgname = _read_cstr(Cpkgname)
        return Csuccess[0], pkgname, errs

    def loadfile(self, fn):
        Cerrs = _new_cstr()
        Cfn = _new_cstr(fn)
        Csuccess = ffi.new("int *")
        Cpkgname = _new_cstr()
        ok = _lib.rosie_loadfile(self.engine, Csuccess, Cfn, Cpkgname, Cerrs)
        if ok != 0:
            raise RuntimeError("loadfile() failed (please report this as a bug)")
        errs = _read_cstr(Cerrs)
        pkgname = _read_cstr(Cpkgname)
        return Csuccess[0], pkgname, errs

    def import_pkg(self, pkgname, as_name=None):
        Cerrs = _new_cstr()
        if as_name:
            Cas_name = _new_cstr(as_name)
        else:
            Cas_name = ffi.NULL
        Cpkgname = _new_cstr(pkgname)
        Cactual_pkgname = _new_cstr()
        Csuccess = ffi.new("int *")
        ok = _lib.rosie_import(self.engine, Csuccess, Cpkgname, Cas_name, Cactual_pkgname, Cerrs)
        if ok != 0:
            raise RuntimeError("import() failed (please report this as a bug)")
        actual_pkgname = _read_cstr(Cactual_pkgname)
        errs = _read_cstr(Cerrs)
        return Csuccess[0], actual_pkgname, errs

    # -----------------------------------------------------------------------------
    # Functions for matching and tracing (debugging)
    # -----------------------------------------------------------------------------

    # TODO: Reuse Cinput to avoid this repeated allocation?

    # Breaking change from older versions:
    #   * startpos and endpos must be >= 0 (0 indicates "use default")
    #   * if startpos > input length, it is treated as input length
    #   * if endpos < startpos, it is treated as startpos,
    #     giving a zero-length (empty) input string
    def match(self, pat, string, startpos, endpos, encoder):
        if (pat is None) or (pat.id[0] == 0):
            raise ValueError("invalid compiled pattern")
        # Clamp to length of input in 1-based system
        if (startpos > len(string)): startpos = len(string)+1
        # Default to length of input, and clamp to length of input
        # Out of order is treated as if startpos and endpos are same
        if (endpos is None): endpos = 0
        elif (endpos > len(string)): endpos = 0
        elif (endpos < startpos): endpos = startpos
        if _have_rosie_match2:
            Cinput = _new_cstr(string)
            ok = _lib.rosie_match2(self.engine, pat.id[0], encoder,
                                   Cinput, startpos, endpos,
                                   self.Cmatch,
                                   0) # TODO: Collect times or not?
            if ok != 0:
                raise RuntimeError("match2() failed (please report this as a bug)")
        else: # Else use the older API rosie_match, which does not support endpos.
            # Avoid copying the input string if possible.
            # We could adjust the len field in Cinput, but we really
            # don't want Python code to be responsible for such low
            # level fiddling.
            if endpos == 0:
                input_data = string
            else:
                input_data = string[:endpos - 1] # Rosie is 1-based
            Cinput = _new_cstr(input_data)
            ok = _lib.rosie_match(self.engine, pat.id[0], startpos, encoder, Cinput, self.Cmatch)
            if ok != 0:
                raise RuntimeError("match() failed (please report this as a bug)")
        left = self.Cmatch.leftover
        abend = self.Cmatch.abend
        ttotal = self.Cmatch.ttotal
        tmatch = self.Cmatch.tmatch
        if self.Cmatch.data.ptr == ffi.NULL:
            if self.Cmatch.data.len == 0:
                return False, left, abend, ttotal, tmatch
            elif self.Cmatch.data.len == 1:
                return True, left, abend, ttotal, tmatch
            elif self.Cmatch.data.len == 2:
                raise ValueError("invalid output encoder")
            elif self.Cmatch.data.len == 4:
                raise ValueError("invalid compiled pattern")
            else:
                raise ValueError("error ({}) reported by librosie".format(self.Cmatch.data.len))
        data = _read_cstr(self.Cmatch.data)
        return data, left, abend, ttotal, tmatch

    def trace(self, pat, string, start, style):
        if pat.id[0] == 0:
            raise ValueError("invalid compiled pattern")
        Cmatched = ffi.new("int *")
        Cinput = _new_cstr(string)
        Ctrace = _new_cstr()
        ok = _lib.rosie_trace(self.engine, pat.id[0], start, style, Cinput, Cmatched, Ctrace)
        if ok != 0:
            raise RuntimeError("trace() failed (please report this as a bug): " + str(_read_cstr(Ctrace)))
        if Ctrace.ptr == ffi.NULL:
            if Ctrace.len == 2:
                raise ValueError("invalid trace style")
            elif Ctrace.len == 1:
                raise ValueError("invalid compiled pattern")
        matched = False if Cmatched[0]==0 else True
        trace = _read_cstr(Ctrace)
        return matched, trace

    # Not currently exposed to the user, matchfile() is a performance
    # hack.  It *should* be a little faster than writing the
    # equivalent code in Python, because some per-match calculations
    # are done only once at the start of the matchfile()
    # implementation in librosie, and of course matchfile() avoids the
    # overhead of bouncing between Python, C, and Lua for every line
    # of the input file.
    #
    # Note that matchfile() writes results to outfile and errfile.
    # The outfile and errfile arguments default to the standard output
    # and error, respectively.  Supply "/dev/null" to suppress output.
    #
    # Is this even useful?  Perhaps with popen()?  Importantly, what
    # should a method like this return?
    def matchfile(self, pat, encoder,
                  infile=None,  # stdin
                  outfile=None, # stdout
                  errfile=None, # stderr
                  wholefile=False):
        if pat.id[0] == 0:
            raise ValueError("invalid compiled pattern")
        Ccin = ffi.new("int *")
        Ccout = ffi.new("int *")
        Ccerr = ffi.new("int *")
        wff = 1 if wholefile else 0
        Cerrmsg = _new_cstr()
        ok = _lib.rosie_matchfile(self.engine,
                                  pat.id[0],
                                  encoder,
                                  wff,
                                  infile or b"",
                                  outfile or b"",
                                  errfile or b"",
                                  Ccin, Ccout, Ccerr, Cerrmsg)
        if ok != 0:
            raise RuntimeError("matchfile() failed: " + str(_read_cstr(Cerrmsg)))

        if Ccin[0] == -1:       # Error occurred
            if Ccout[0] == 2:
                raise ValueError("invalid encoder")
            elif Ccout[0] == 3:
                raise ValueError(str(_read_cstr(Cerrmsg))) # file i/o error
            elif Ccout[0] == 4:
                raise ValueError("invalid compiled pattern (already freed?)")
            else:
                raise ValueError("unknown error caused matchfile to fail")
        return Ccin[0], Ccout[0], Ccerr[0]

    # -----------------------------------------------------------------------------
    # Functions for reading and processing rcfile (init file) contents
    # -----------------------------------------------------------------------------

    def read_rcfile(self, filename=None):
        Cfile_exists = ffi.new("int *")
        if filename is None:
            filename_arg = _new_cstr()
        else:
            filename_arg = _new_cstr(filename)
        Coptions = _new_cstr()
        Cmessages = _new_cstr()
        ok = _lib.rosie_read_rcfile(self.engine, filename_arg, Cfile_exists, Coptions, Cmessages)
        if ok != 0:
            raise RuntimeError("read_rcfile() failed (please report this as a bug)")
        messages = _read_cstr(Cmessages)
        messages = messages and json.loads(messages)
        if Cfile_exists[0] == 0:
            return None, messages
        # else file existed and was read
        options = _read_cstr(Coptions)
        if options:
            return json.loads(options), messages
        # else: file existed, but some problems processing it
        return False, messages

    def execute_rcfile(self, filename=None):
        Cfile_exists = ffi.new("int *")
        Cno_errors = ffi.new("int *")
        if filename is None:
            filename_arg = _new_cstr()
        else:
            filename_arg = _new_cstr(filename)
        Cmessages = _new_cstr()
        ok = _lib.rosie_execute_rcfile(self.engine, filename_arg, Cfile_exists, Cno_errors, Cmessages)
        if ok != 0:
            raise RuntimeError("execute_rcfile() failed (please report this as a bug)")
        messages = _read_cstr(Cmessages)
        messages = messages and json.loads(messages)
        if Cfile_exists[0] == 0:
            return None, messages
        # else: file existed
        if Cno_errors[0] == 1:
            return True, messages
        # else: some problems processing it
        return False, messages

    # -----------------------------------------------------------------------------
    # Functions that return a parse tree or fragments of one
    # -----------------------------------------------------------------------------

    def parse_expression(self, exp):
        Cexp = _new_cstr(exp)
        Cparsetree = _new_cstr()
        Cmessages = _new_cstr()
        ok = _lib.rosie_parse_expression(self.engine, Cexp, Cparsetree, Cmessages)
        if ok != 0:
            raise RuntimeError("parse_expression failed (please report this as a bug)")
        return _read_cstr(Cparsetree), _read_cstr(Cmessages)
        
    def parse_block(self, block):
        Cexp = _new_cstr(block)
        Cparsetree = _new_cstr()
        Cmessages = _new_cstr()
        ok = _lib.rosie_parse_block(self.engine, Cexp, Cparsetree, Cmessages)
        if ok != 0:
            raise RuntimeError("parse_block failed (please report this as a bug)")
        return _read_cstr(Cparsetree), _read_cstr(Cmessages)
        
    def expression_refs(self, exp):
        Cexp = _new_cstr(exp)
        Crefs = _new_cstr()
        Cmessages = _new_cstr()
        ok = _lib.rosie_expression_refs(self.engine, Cexp, Crefs, Cmessages)
        if ok != 0:
            raise RuntimeError("expression_refs failed (please report this as a bug)")
        return _read_cstr(Crefs), _read_cstr(Cmessages)
        
    def block_refs(self, block):
        Cexp = _new_cstr(block)
        Crefs = _new_cstr()
        Cmessages = _new_cstr()
        ok = _lib.rosie_block_refs(self.engine, Cexp, Crefs, Cmessages)
        if ok != 0:
            raise RuntimeError("block_refs failed (please report this as a bug)")
        return _read_cstr(Crefs), _read_cstr(Cmessages)
        
    def expression_deps(self, exp):
        Cexp = _new_cstr(exp)
        Cdeps = _new_cstr()
        Cmessages = _new_cstr()
        ok = _lib.rosie_expression_deps(self.engine, Cexp, Cdeps, Cmessages)
        if ok != 0:
            raise RuntimeError("expression_deps failed (please report this as a bug)")
        return _read_cstr(Cdeps), _read_cstr(Cmessages)
        
    def block_deps(self, block):
        Cexp = _new_cstr(block)
        Cdeps = _new_cstr()
        Cmessages = _new_cstr()
        ok = _lib.rosie_block_deps(self.engine, Cexp, Cdeps, Cmessages)
        if ok != 0:
            raise RuntimeError("block_deps failed (please report this as a bug)")
        return _read_cstr(Cdeps), _read_cstr(Cmessages)

    # -----------------------------------------------------------------------------
    # Functions for reading and modifying various engine settings
    # -----------------------------------------------------------------------------

    def config(self):
        Cresp = _new_cstr()
        ok = _lib.rosie_config(self.engine, Cresp)
        if ok != 0:
            raise RuntimeError("config() failed (please report this as a bug)")
        resp = _read_cstr(Cresp)
        return resp

    def libpath(self, libpath=None):
        if libpath:
            libpath_arg = _new_cstr(libpath)
        else:
            libpath_arg = _new_cstr()
        ok = _lib.rosie_libpath(self.engine, libpath_arg)
        if ok != 0:
            raise RuntimeError("libpath() failed (please report this as a bug)")
        return _read_cstr(libpath_arg) if libpath is None else None

    def alloc_limit(self, newlimit=None):
        limit_arg = ffi.new("int *")
        usage_arg = ffi.new("int *")
        if newlimit is None:
            limit_arg[0] = -1   # query
        else:
            if (newlimit != 0) and (newlimit < 8192):
                raise ValueError("new allocation limit must be 8192 KB or higher (or zero for unlimited)")
            limit_arg = ffi.new("int *")
            limit_arg[0] = newlimit
        ok = _lib.rosie_alloc_limit(self.engine, limit_arg, usage_arg)
        if ok != 0:
            raise RuntimeError("alloc_limit() failed (please report this as a bug)")
        return limit_arg[0], usage_arg[0]

    def __del__(self):
        if hasattr(self, 'engine') and (self.engine != ffi.NULL):
            e = self.engine
            self.engine = ffi.NULL
            _lib.rosie_finalize(e)

# -----------------------------------------------------------------------------

class rplx(object):    
    def __init__(self, engine):
        self.id = ffi.new("int *")
        self.engine = engine
        
    def __del__(self):
        if self.id[0] and self.engine.engine:
            _lib.rosie_free_rplx(self.engine.engine, self.id[0])

    def maybe_valid(self):
        return self.id[0] != 0

    def valid(self):
        return self.maybe_valid() and \
            self.engine.engine and \
            isinstance(self.engine, engine)
    
# -----------------------------------------------------------------------------




