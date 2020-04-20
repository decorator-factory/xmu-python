from .. import parse
import difflib
import os
import re
import unittest

def are_strings_close(
        a, b, *,
        threshold: "higher = stricter; 1..0",
        ignore_ws
        ):
    if ignore_ws:
        a = re.sub(r"\s+", "", a)
        b = re.sub(r"\s+", "", b)
    sm = difflib.SequenceMatcher(a=a, b=b)
    return sm.ratio() >= threshold

class TestParser(unittest.TestCase):
    def assertClose(self, a, b, threshold=0.8, ignore_ws=True):
        if not are_strings_close(a, b, threshold=threshold, ignore_ws=ignore_ws):
            print("\nString a:")
            print(a)
            print("String b:")
            print(b)
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_sample_from_readme_works(self):
        # The single most important test!
        reference_html = """
            <h1> Hello, world! </h1>
            <style>#lwunnaxwqbgasdhs {
                color: red;
                border-color: #cc0000; }
            </style>
            <xmu-styled id=lwunnaxwqbgasdhs>
                <table>
                    <tr>
                        <td> Lorem </td>
                        <td> Ipsum </td>
                        <td> Dolor </td>
                    </tr>
                    <tr>
                        <td> Sit </td>
                        <td> Amet </td>
                        <td> \_/__^[.]w[.]^__\_/ </td>
                    </tr>
                </table>
            </xmu-styled>
        """
        with open(os.path.join(os.path.dirname(__file__), "../../README.md")) as readme_file:
            markdown = readme_file.read()
        xmu_sample = re.findall(r"```xmu((?:(?!```).|\n)+)```", markdown)[0]
        html = parse(xmu_sample)
        self.assertClose(html, reference_html)


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
        self.assertClose(parsed,expected,threshold=0.9,)


if __name__ == '__main__':
    unittest.main()
