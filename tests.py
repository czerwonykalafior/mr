import unittest

from main import Morphy
import verbs


class TestMorphy(unittest.TestCase):
    def setUp(self) -> None:
        self.base_node = Morphy()

    def test_basic(self):
        self.assertEqual([], self.base_node.child_nodes)
        self.assertEqual([None], self.base_node.parent_nodes)


class TestMap(unittest.TestCase):
    def setUp(self) -> None:
        self.base_node = Morphy()

    def test_arrow_register(self):
        self.assertTrue(hasattr(self.base_node, 'map'))

    def test_one_to_one_connections(self):
        map_node = self.base_node.map()
        self.assertTrue(map_node.parent_nodes[0] is self.base_node)
        self.assertTrue(self.base_node.child_nodes[0] is map_node)

    def test_one_to_many(self):
        node_0 = self.base_node.map()
        node_1 = self.base_node.map()
        node_2 = self.base_node.map()

        self.assertTrue(self.base_node.child_nodes, [node_0, node_1, node_2])
        self.assertTrue(node_0.parent_nodes, [self.base_node])
        self.assertTrue(node_1.parent_nodes, [self.base_node])
        self.assertTrue(node_2.parent_nodes, [self.base_node])

    def test_data_flow(self):
        node_1 = self.base_node.map()
        node_2 = node_1.map()
        node_3 = node_2.map()

        self.base_node.emit(1)


class TestUnion(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Morphy()

    def test_many_to_one(self):
        node_0 = Morphy()
        node_1 = Morphy()
        node_2 = Morphy()
        node_3 = Morphy().union([node_0, node_1, node_2])

        self.assertEqual(node_0.child_nodes[0], node_3)
        self.assertEqual(node_1.child_nodes[0], node_3)
        self.assertEqual(node_2.child_nodes[0], node_3)
        self.assertEqual(node_3.parent_nodes, [node_0, node_1, node_2])


if __name__ == '__main__':
    unittest.main()
