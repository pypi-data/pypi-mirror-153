#  -*- Mode: Python; -*-                                                   
#  -*- coding: utf-8; -*-
# 
#  decode.py
# 
#  © Copyright Jamie A. Jennings 2019, 2020, 2021.
#  LICENSE: MIT License (https://opensource.org/licenses/mit-license.html)
#  AUTHOR: Jamie A. Jennings

import sys
assert(sys.version_info.major == 3)

def _decode_short(b, i):
    n = b[i] + (b[i+1]<<8)
    if n > 32767:
        n = n - 65536
    return n, i+2

def _decode_int(b, i):
    n = b[i] + (b[i+1]<<8) + (b[i+2]<<16) + (b[i+3]<<24)
    if n > 2147483647:
        n = n - 4294967296
    return n, i+4

#
# About decode:
#
# When 'inputstring' argument is None, the decoder will return a parse
# tree without any 'data' fields.  It will have 'type', 's', and 'e'
# fields only, where s and e are start/end and are 1-based.
#
# When the `inputstring` argument is a bytes or str object, the
# decoder returns a parse tree whose nodes include a 'data' field
# containing a COPY (of type bytes or str, depending on the type of
# inputstring) of inputstring[s-1, e-1].
#
# When the `inputstring` argument is a memoryview object, the
# decoder returns a parse tree whose nodes include a 'data' field
# containing a memoryview slice of inputstring[s-1, e-1].
#
def decode(bytestring, inputstring):
    i = 0                       # bytestring index
    current = [[]]              # stack
    while True:
        position, i = _decode_int(bytestring, i)
        if position > 0:
            # Found a match end position, not a new start position.
            # Find the open match, the one where 'e' is None:
            while True:
                assert(current)
                # If current list of subs is empty, pop the stack
                if not current[-1]:
                    current.pop()
                    continue
                # Check if last match in current list is open
                match = current[-1][-1]
                assert(match and (match['s'] is not None))
                if match['e']:
                    # No open match in this list of subs, so pop the stack
                    current.pop()
                    continue
                else:
                    # Found the open match that needs this end position
                    break
            match['e'] = position

            # Set data field, if we have an inputstring. Note: if data
            # field already set, it was a "constant capture".

            if (inputstring is not None) and (match['data'] is None):
                # Adjust for rosie's 1-based indexing.
                match['data'] = inputstring[match['s']-1:position-1]
            # Did we just close up the outermost match?
            if len(current) == 1:
                return match
            # Back to top of the loop, to read the next position from
            # the encoded data
            continue

        # Else position < 0, indicating the start of a sub-match
        typelen, i = _decode_short(bytestring, i)
        after_typename = i + (typelen if typelen >= 0 else -typelen)
        # Assumes typename will be valid UTF-8, which Rosie should enforce
        typename = str(bytestring[i:after_typename], encoding='UTF-8')
        i = after_typename

        match = {'type': typename,
                 'data': None,
                 'subs': list(),
                 's': - position,
                 'e': None}

        # Add the new match to the end of the list we are building,
        # which is at the end of the 'current' list
        current[-1].append(match)
        current.append(match['subs'])

        # Is this a "constant capture" (user-provided string embedded in RPL pattern)?
        if typelen < 0:
            # Constant capture means data is in the bytestring (the
            # match result), not the inputstring.
            datalen, i = _decode_short(bytestring, i)
            assert( datalen >= 0 )
            # Assumes typename will be valid UTF-8, which Rosie should enforce.
            match['data'] = str(bytestring[i:i+datalen], encoding='UTF-8')
            i = i + datalen

        # Else we found a regular capture, so the data is a substring
        # of the input.  We don't have the end position for the
        # capture, yet.  Before we can get it, we may have to process
        # some sub-matches.

        # Go to top of loop where we decode the next position, which
        # may be the start of a sub-match or the end of the current
        # "open" match.
        continue


'''
def dict_diff(a, b):
    ak = a.keys()
    bk = b.keys()
    if ak != bk:
        return ("different keys", a, b)
    for k in ak:
        if type(a[k]) is dict:
            if type(b[k]) is dict:
                diff = dict_diff(a[k], b[k])
                if diff is None: continue
                else: return diff
            else: return ("only a is dict", a[k], b[k])
        elif type(a[k]) is list:
            if type(b[k]) is list:
                if len(a[k]) != len(b[k]):
                    return ("different list lengths", a[k], b[k])
                for pair in zip(a[k], b[k]):
                    diff = dict_diff(pair[0], pair[1])
                    if diff is None: continue
                    else: return diff
            else:
                return ("only a is a list", a[k], b[k])
        else:
            if a[k]==b[k]: continue
            else: return ("non-dicts not equal", a[k], b[k])
    return None
'''


