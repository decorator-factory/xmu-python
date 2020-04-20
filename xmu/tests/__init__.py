from .. import parse
import difflib
import os
import re
import unittest

def are_strings_close(a, b, *, threshold: "higher = stricter; 1..0", ignore_ws):
    if ignore_ws:
        a = re.sub(r"\s+", "", a)
        b = re.sub(r"\s+", "", b)
    sm = difflib.SequenceMatcher(a=a, b=b)
    return sm.ratio() >= threshold

class TestParser(unittest.TestCase):

    def test_sample_from_readme_works(self):
        reference_html = """
            <h1> Hello, world! </h1>
            <style>#lwunnaxwqbgasdhs {
                color: red;
                border-color: #cc0000; }
            </style>
            <emu-styled id=lwunnaxwqbgasdhs>
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
            </emu-styled>
        """
        with open(os.path.join(os.path.dirname(__file__), "../../README.md")) as readme_file:
            markdown = readme_file.read()
        xmu_sample = re.findall(r"```xmu((?:(?!```).|\n)+)```", markdown)[0]
        html = parse(xmu_sample)
        self.assertTrue(are_strings_close(html, reference_html, threshold=0.7, ignore_ws=True))

if __name__ == '__main__':
    unittest.main()
