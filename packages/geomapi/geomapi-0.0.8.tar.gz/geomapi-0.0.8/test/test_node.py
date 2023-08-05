import unittest
from context import geomapi
from geomapi.node import Node

class TestNode(unittest.TestCase):

    def test_node_creation(self):
        graphPath = "./geomapi/test/testfiles/testNodeGraph.ttl"
        # Make a node from the graphPath
        newNode = Node(graphPath=graphPath)
        self.assertEqual(graphPath, newNode.graphPath)
        # Test if the variables are parsed correctly
        if (newNode.get_name() == "IMG_213"):
            self.assertEqual(newNode.label, "{b9c3f2e1-aea0-11ec-b2d9-a86daaa4a624}")
        elif (newNode.get_name() == "IMG_214"):
            self.assertEqual(newNode.label, "{b9da03dc-aea0-11ec-a4b1-a86daaa4a624}")
        
        


if __name__ == '__main__':
    unittest.main()