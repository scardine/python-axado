import unittest
from .axado import Axado
from settings import KEY

class TestConsulta(unittest.TestCase):
    def setUp(self):
        self.api = Axado(KEY)
