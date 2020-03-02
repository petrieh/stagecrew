import pytest


__copyright__ = 'Copyright (C) 2020, Nokia'


pytest.register_assert_rewrite('runner', 'task', 'verifier')
