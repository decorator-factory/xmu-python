from .. import parse
from . import XmuTestCase
import os
import re
import unittest



class TestParser(XmuTestCase):
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





if __name__ == '__main__':
    unittest.main()
