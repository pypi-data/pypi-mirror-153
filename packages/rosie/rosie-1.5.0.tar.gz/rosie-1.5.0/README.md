# A Python Module for Rosie Pattern Language

This module can be installed using `pip install rosie`.  It requires a Rosie 
installation, which is done separately.  
(See the [Rosie repository](https://gitlab.com/rosie-pattern-language/rosie).)

## Documentation

This module follows the API established by the Python `re` module where possible,
and extends it where necessary.

### Obtaining a rosie matching engine

### Defining patterns in an engine's memory

### Using a pattern for matching

### Compiling a pattern ahead of time is faster

### The result of matching is a "parse tree"

### Debugging a pattern by tracing its execution

### Best practice: Define patterns in rpl files

* create packages (namespaces)
* use unit tests
* "fail fast" by compiling named patterns during initialization of your
  application

### Performance tips

* always compile patterns ahead of time
* use output encoder `bool` when possible
* supply `posonly=True` unless you need most of the data fields (use `TO BE
  DETERMINED` function to get the data field for a specific match when needed)



## Examples

You can find some examples of using `rosie` to do some of the same things that
you might do with `re` in the following files:
* [examplere](https://gitlab.com/rosie-community/clients/python/blob/master/test/examplere.py) 
and 
* [examplerosie](https://gitlab.com/rosie-community/clients/python/blob/master/test/examplerosie.py) 

See also the tests in
[test/test.py](https://gitlab.com/rosie-community/clients/python/blob/master/test/test.py). 


## Thanks

Many thanks to the original author of this Python binding, Jenna Shockley!



## This is how the PyPI package was created

The package was created on MacOS 11.1, using Python 3.9.4 and cffi 1.14.5.  The
package contains only Python source code, so it should work across platforms.
(Also, it is tested on various Linux distributions using Docker.)

(1) Test the installation locally:

	pip3 install -e .

(2) Build the source distribution:

    python3 setup.py sdist

(3) Upload to PyPI:

	twine upload dist/*

