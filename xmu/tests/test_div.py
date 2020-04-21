import unittest
from . import XmuTestCase
from .. import parse


class TestDiv(XmuTestCase):
    def test_div_works(self):
        parsed = parse("""
            [
                div #myId [
                    Div with just an id
                ]
                div .class [
                    Div with a single class
                ]
                div .class1 class2 class3 [
                    Div with multiple classes
                ]
                div #myId .class1 class2 [
                    Div with an id and multiple classes
                ]
            ]
            """)
        expected = """
            <div class="class">
                Div with a single class
            </div>
            <div class="class1 class2 class3">
                Div with multiple classes
            </div>
            <div id='myId' class="class1 class2">
                Div with an id and multiple classes
            </div>
        """
        self.assertClose(parsed, expected, threshold=0.9)


if __name__ == "__main__":
    unittest.main()