import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        n = HTMLNode()
        self.assertEqual(n.props_to_html(), "")

    def test_props_empty(self):
        n = HTMLNode(props={})
        self.assertEqual(n.props_to_html(), "")

    def test_props_single(self):
        n = HTMLNode(props={"a": "b"})
        self.assertEqual(n.props_to_html(), ' a="b"')

    def test_props_double(self):
        n = HTMLNode(props={"a": "b", "c": "d"})
        self.assertEqual(n.props_to_html(), ' a="b" c="d"')

    def test_repr(self):
        n = HTMLNode(
            tag="a",
            value="val",
            children=[HTMLNode()],
            props={"a": "b", "c": "d"})
        self.assertEqual(f"{n}", "HTMLNode(a, val, [HTMLNode(None, None, None, None)], {'a': 'b', 'c': 'd'})")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", {"a": "b"})
        self.assertEqual(node.to_html(), '<p a="b">Hello, world!</p>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!", {"a": "b"})
        self.assertEqual(node.to_html(), 'Hello, world!')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None, {"a": "b"})
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_with_attrs(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"a": "b"})
        self.assertEqual(parent_node.to_html(), '<div a="b"><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as ve:
            parent_node.to_html()
        self.assertEqual(str(ve.exception), "No children")

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError) as ve:
            parent_node.to_html()
        self.assertEqual(str(ve.exception), "No tag")