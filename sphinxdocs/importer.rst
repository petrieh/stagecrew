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

.. _`issue-13`: https://github.com/petrieh/crl-interactivesessions/tree/issue-13
.. _`python imports`: https://blog.ffledgling.com/python-imports-i.html
.. _`importer protocol`: https://www.python.org/dev/peps/pep-0302/#specification-part-1-the-importer-protocol

