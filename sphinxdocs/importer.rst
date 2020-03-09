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

.. _`issue-13`: https://github.com/petrieh/crl-interactivesessions/tree/issue-13
.. _`python imports`: https://blog.ffledgling.com/python-imports-i.html
.. _`importer protocol`: https://www.python.org/dev/peps/pep-0302/#specification-part-1-the-importer-protocol

