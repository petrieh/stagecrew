Importer requirements implementation
------------------------------------

Importer requirements can be implemented via global configuration file system.
Proposed name for the configuration file is *confimporter.py*. There can be
multiple *confimporter.py* files which are read during the import process.
These are read when the associated package is handled in find_module call. The
*confimporter.py* file is executed by the importer (without registering the
modules) as a first package import operation.

The configuration may contain for example:

 - addition of the module rules - requirements map - addition of explicit
   dependencies

     - explicit dependencies are not always found during import process. For
       example the modules imported in functions should be configured via
       explicit dependencies


Module rules optimization
-------------------------

.. note::

  This feature does not optimize essentially the import process. Instead,
  it would be better to use cache.


Module rules can be optimized via first grouping consecutive Include,
RecursiveInclude, Exclude and RecursiveExclude rules into a single rule. For
that purpose we create a module rule tree. Nodes are module path parts (like in
'foo.bar.foobar' rule path has nodes 'foo' -> 'bar' -> 'foobar'). Each node
contains the default value which is usually Tribool() but in case the node is
the base node of the recursive rule, then either Tribool(False) or
Tribool(True) if the rule is RecursiveExclude or RecursiveInclude rule
respectively.

This can be further optimized by grouping rules in the requirements map (i.e.
map from module rules to requirements) by adding diagonal_contains_obj function
(this can be a static method of ContainsBase) This conceptually is just an
n-dimensional diagonal map from Python objects composed with
*contains_as_tribool* function  of each TriboolSet of module rules keys::

    class ContainsMap:
         def __init__(self, contains, callable):
              self._contains = contains
              self._callable = callable

         def __call__(self, obj):
            return self._callable(self._contains(obj))

    ...

    class ContainsBase:
        ...

        @staticmethod
        def diagonal_contains_obj(obj, *containsmaps):
            return (m(obj) for m in containsmaps)


As in the code excerpt above, For convenience this is further then mapped to
Python objects (which in this case are requirements generators).  Using
diagonal map we can compute simultaneously optimized fashion matching of all
keys (provided the rules are based on these above mentioned four rules). As
this all is string manipulation, it is not usually time consuming. However, in
the large requirements set (containing hundreds of requirements) combined with
large number of imported files (containing again hundreds of modules), then
this likely gives some milliseconds benefit. As this is rather trivial to
implement, it is still feasible to do. The only trick here is to override the
trivial implementation of the static method *diagonal_contains_obj* so that it
uses the common extended module rule tree.

The requirements can be also combined so that the required modules are grouped.
The requirements are the following::

    class RequirementsBase:
        def __init__(self, *required_modules)
            self._required_modules = required_modules
            self._modules = {}


        def check(self):
            self._try_to_get_modules(self)
            self._check()

        @abc.abstractmethod
        def _check(self):
            """Implement actual requirements check.
            """


    class ModuleRequirements(RequirementsBase):
        def _check(self):
            pass


Registration process of Python 2 + 3
-------------------------------------

Registration process can be optimized in Python 3 by wrapping each finder is
sys.meta_path.  Unfortunately, Python 2 relies on implicit importer so that
this cannot be used.

Especially, we can cache each registered module dependencies. The cache has to
be refreshed only if sys.path changes or if namespace package paths are
changed.

It would be useful to monkeypatch during registration the sys.modules to
return only excluded modules (like standard libraries). The __setitem__ could
be overridden to void.

Requirements notes
------------------

Importer shall raise *ImportError* in case requirements are not met. Import
process is used in two different scenarios:

   1. Creation of the package
   2. Extracting of the package

There is no need in 1. for successful import in case there are other means to
to get the source code of the module. Therefore, there shall be handling for
*ImportError* in packaging case in order to we can use the same importer in both
cases. The other option is to use differently configured importers. In the case
2. *ImnportError* shall not be handled if requirements are not met.
