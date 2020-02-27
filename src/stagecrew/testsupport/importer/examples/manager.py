from stagecrew import Importer

__copyright__ = 'Copyright (C) 2020, Nokia'
__deps__ = [Importer]


def import_and_call(dumps, *args, **kwargs):
    c = Importer().loads(dumps)
    return c(*args, **kwargs)
