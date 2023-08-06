from .testcase import TestCase
from heaserver.service.testcase.mixin import GetOneMixin, GetAllMixin


class TestGet(TestCase, GetOneMixin):
    pass


class TestGetAll(TestCase, GetAllMixin):
    pass
