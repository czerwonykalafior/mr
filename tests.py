import unittest

from main import Morphy
import verbs


class TestMorphy(unittest.TestCase):
    def setUp(self) -> None:
        self.node = Morphy()

    def test_basic(self):
        self.assertEqual([], self.node.downstreams)
        self.assertEqual([None], self.node.upstreams)

    def test_arrow_register(self):
        self.assertTrue(hasattr(self.node, 'Map'))

    def test_connections(self):
        base_node = self.node
        map_node = base_node.Map()
        self.assertTrue(map_node.upstreams[0] is base_node)
        self.assertTrue(base_node.downstreams[0] is map_node)


if __name__ == '__main__':
    unittest.main()
