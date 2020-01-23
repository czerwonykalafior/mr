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
        self.dummy_func = lambda x: x

    def test_arrow_register(self):
        self.assertTrue(hasattr(self.base_node, 'map'))

    def test_one_to_one_connections(self):
        map_node = self.base_node.map(lambda x: x)
        self.assertTrue(map_node.parent_nodes[0] is self.base_node)
        self.assertTrue(self.base_node.child_nodes[0] is map_node)

    def test_one_to_many(self):
        node_0 = self.base_node.map(lambda x: x)
        node_1 = self.base_node.map(lambda x: x)
        node_2 = self.base_node.map(lambda x: x)

        self.assertTrue(self.base_node.child_nodes, [node_0, node_1, node_2])
        self.assertTrue(node_0.parent_nodes, [self.base_node])
        self.assertTrue(node_1.parent_nodes, [self.base_node])
        self.assertTrue(node_2.parent_nodes, [self.base_node])

    def test_data_flow(self):
        node_1 = self.base_node.map(lambda x: x + 1)
        node_2 = node_1.map(lambda x: x * 2)
        node_3 = node_2.map(lambda x: print(x))

        self.base_node.emit(1)


class TestFilter(unittest.TestCase):
    def test_basic(self):
        base_node = Morphy()
        next = base_node.filter(lambda x: x % 2 == 0, lambda z: print(z))

        base_node.emit(1)
        base_node.emit(2)


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

    def test_union_map(self):
        base = Morphy()
        node_0 = base.map(lambda x: x + 1)
        node_1 = base.map(lambda x: x - 1)
        node_2 = base.map(lambda x: x * 10)
        node_3 = Morphy().union_map([node_0, node_1, node_2], func=lambda x: print(x))

        base.emit(1)


if __name__ == '__main__':
    unittest.main()
