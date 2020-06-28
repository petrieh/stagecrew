.. Copyright (C) 2020, Nokia

Importer
--------

The basic idea is that the modules are stored *sys.modules* according to their
paths in the local file system. This ensures good enough uniqueness even though
it cannot be extended to *setuptools* like package management.  Partial
implementation for this importer is in issue-13_.

Another way is to write a completely new importer similarly than described in
`importer protocol`_ and in `python imports`_.

The basic idea is to re-import the required module with the new name created
from the full file path of the module. The modules which should be imported
along with the given module are informed via *__deps__* global variable in the
module.  In more detail, *__deps__* contains list of the functions, classes or
modules imported via import statements. After creating the module from the
source, this *__deps__* is checked and the associated modules are imported
recursively.  The associated modules can be found directly if the import is a
module otherwise *__module__* attribute is looked and the associated module is
either imported or looked from *sys.modules*. The latter is used e.g.
in *pickle.whichmodule* function.

Finally, the attributes in the module listed in *__deps__* are replaced with the
attributes from the importer imported modules instead of built-in.

This induced bundle of the modules can then be transferred anywhere and
re-imported using tailored *sys.meta_path* finder and loader. This
process is a bit more tricky because the meaning for especially non-package
relative imports is very specific to the original location of the module.
Therefore, the imports should be done one-by-one in the reverse dependency order.
Essentially, the finder should have the context of the currently imported
module. Using that, it can then map imports to modules imported previous import
steps.

Improved importer
-----------------

Instead of *__deps__* it is better to import all which are needed by the Python
object (i.e. function, class or module). We can exclude standard library
modules and not source file modules (like frozen or built-in). Instead of the
module level *__deps__* we could use global configuration for excluded and
included modules. This configuration could be a list of include and exclude
rule either for full tree or for specific objects. In conflicting case or in
overlapping case, always the later rule in the list will be in force. Also,
root level trees should be be supported. For example::

    recursive-exclude a
    recursive-include a.b
    exclude a.b.c

This means that no modules a.* are included but modules under a.b except a.b.c
(if they are needed by the object). If root level rules *include-all* or
*exclude-all* is added to the list of rules, then none of the rules before this
all rule has no effect.

We use importlib.util.find_spec (or imp.find_module in Python 2) for finding
source modules. The information from this find function can be used for
packaging module data.

Standard libraries can be found using *stdlib-list* library. This library
cannot be imported by this importer as it has data files. Therefore, the
library should be imported in the function which is only called if the standard
library collection is not yet generated. The standard library dictionary could
be transferred as part of the eval-package e.g in json-format.

Use importlib.util.find_spec (or imp.find_module in Python 2) for finding
modules which from which the source can be found (not e.g. built-in) and which
are not frozen. In Python 2 this is show as ret[3] != 1 and in python 3::

   >> from importlib.machinery import SourceFileLoader
   >> spec = importlib.util.find_spec('mymodule')
   >> isinstance(spec.loader, SourceFileLoader)

Moreover, standard libraries has to be used from::

   pip install stdlib-list
   >> from stdlib_list import short_versions, stdlib_list
   >> for v in short_versions:
   ...    d[v] = stdlib_list[v]

There is also a limited support for data files. Binary content can be
registered to importer.  There is no support for file system files (but that is
of course easy to implement using binary file support)::

    >> from stagecrew import Importer
    >> i = Importer()
    >> with open('some-data.txt', 'rb') as f:
    ...    i.register_data('some-data', f.read())

The __file__ attribute in when imported to remote system will point to
/current/working/directory/.stagecrew/full/path/to/module. Current
implementation does neither create .stagecrew directory nor create any
directories or files under it.  However, importer has *get_data* method which
can be used for retrieving registered data using identifier given in the data
registration. This *get_data* returns the content of the file as a binary
string.  The reasoning for limited support is that we need to support at least
importing stdlib dictionary content (e.g. in json format). There could be
as well *is_data* method, which checks whether the identifier is registered.

Importer requirements
---------------------

Importer is meant to package modules in Python system A to be extracted in
Python system B. The reasons for the transfer are the following:

    - make types defined in A picklable in B and vice versa
    - execute the code defined in A in B

Now, in ideal case this is easy if A and B are similar enough. However, this
becomes tricky when the systems A and B differ from each other.

There are two types of differences: system and module level. The system level
differences are typically differences in OS, Python version, software
libraries and tools. Module differences are always only differences in available
Python modules.

In this reason there is a need to provide interface for adding global
requirements (for both A and B). The requirements are added only to some of the
modules which cannot be imported in all types of the systems or requires
external Python modules.  These requirements are called system and module
requirements respectively. This is conceptually similar to setuptools
conditional install_requires requirements where conditionals are defined
programmatically e.g. by checking OS version etc.  In setuptools, there is also
PEP-508 style dependency logic which provides system requirement conditional
install for the module.  However, in our case these requirement types are
independent from each other.  Moreover, we are not going to follow fixed system
requirement markers but provide only programmatic conditional interface. In
practice we provide API taking callable argument for the system or module
requirement check.

Moreover, in some cases, if systems A and B are known to be very similar, it is
not useful to register and package modules which are in both systems. For this
reason, it is good to define API for excluding single module or recursively
exclude modules. There are two types of recursive exclusion of the modules:

  - depended recursively exclude - all depended modules are excluded.
  - sub-module recursively exclude - the module and all sub-modules are
    excluded.

Importer should be able to gather information about which modules it has
received together with information which requirements the modules satisfy. In
this fashion, if this data is shared between systems, the importer can then
tailor packages according to the real needs of the other system.

If the module does not satisfy system requirements it is not imported. However,
the code of it (if available) can be associated to it so that the module can be
added to the package.  This of cause requires that the associated package path
is correctly set so that the source module can be searched from the path
directory. In practice in the registration phase the modules not satisfying
requirements are registered as source (which can be found from the package
path) and replaced (by importer protocol, sys.meta_path modifications).

There should also be an API for defining module, source file path pairs so that
modules which do not satisfy the requirements in A can still be packaged in A
and send to the system B. The use case here is that sometimes the test code is
very specific to the target system (B) and it is not meaningful or even
possible to import the modules in the test execution host (A) but only in the
target (B).


.. _`issue-13`: https://github.com/petrieh/crl-interactivesessions/tree/issue-13
.. _`python imports`: https://blog.ffledgling.com/python-imports-i.html
.. _`importer protocol`: https://www.python.org/dev/peps/pep-0302/#specification-part-1-the-importer-protocol

