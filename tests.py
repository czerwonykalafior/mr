import unittest

from main import Morphy
import verbs


class TestMorphy(unittest.TestCase):
    def setUp(self) -> None:
        self.base_node = Morphy()

    def test_basic(self):
        self.assertEqual([], self.base_node.child_nodes)
        self.assertEqual([None], self.base_node.parent_nodes)

    def test_catch(self):
        error_node = self.base_node.map(lambda x: x / 0)

        self.base_node.emit(1)

    def test_connect(self):
        next_node = Morphy()
        next_node.connect(self.base_node)
        self.assertEqual([], self.base_node.child_nodes)
        self.assertEqual([None, next_node], self.base_node.parent_nodes)


class TestMap(unittest.TestCase):
    def setUp(self) -> None:
        self.base_node = Morphy()

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
        result = []
        node_3 = node_2.sink(result.append)

        self.base_node.emit(1)
        self.assertEqual([4], result)


class TestFilter(unittest.TestCase):
    def test_basic(self):
        base_node = Morphy()
        result = []
        next_node = base_node.filter(lambda x: x % 2 == 0, result.append)

        base_node.emit(1)
        base_node.emit(2)
        self.assertEqual([2], result)


class TestUnion(unittest.TestCase):
    def test_many_to_one(self):
        node_0, node_1, node_2 = Morphy(), Morphy(), Morphy()
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
        result = []
        node_3 = Morphy().union_map([node_0, node_1, node_2], func=lambda x: x + 1)
        node_4 = node_3.sink(result.append)

        base.emit(1)
        self.assertEqual([3, 1, 11], result)


class TestUnpack(unittest.TestCase):
    def test_basic(self):
        node_0 = Morphy()
        node_1 = node_0.unpack()
        node_2 = node_1.map(lambda x: x * 2)
        result = []
        node_3 = node_2.sink(result.append)

        node_0.emit([1, 2, 3])
        self.assertEqual([2, 4, 6], result)


if __name__ == '__main__':
    unittest.main()
