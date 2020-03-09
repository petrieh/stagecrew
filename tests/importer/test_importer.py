from stagecrew import IncrImporter


__copyright__ = 'Copyright (C) 2020, Nokia'


def test_incr_importer(importer_verify):
    i = IncrImporter()
    importer_verify(i)
