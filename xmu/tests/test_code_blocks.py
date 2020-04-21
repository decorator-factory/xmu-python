from . import XmuTestCase, without_ws
from .. import parse
import unittest

class TestPyEval(XmuTestCase):
    def test_py_eval_renders(self):
        parsed = parse("py-eval[2 + 2][4]")
        expected = """
            <div class='container ipy'>
                <pre  style="margin:0;padding:0;" class="shadow">
                    <code class="lang-python">
                        2 + 2
                    </code>
                </pre>
                <pre style="margin:0;padding:0;font-weight: 800; border-radius:0 0 1em 1em"
                     class="shadow border-top border-secondary">
                    <code class="lang-python">
                        >>> 4
                    </code>
                </pre>
            </div>
        """
        self.assertClose(parsed, expected)

    def test_py_eval_alerts_on_unexpected_output(self):
        parsed = parse("py-eval[2 + 2][5]")
        must_contain = """
            <table>
                <tr>
                    <td>
                        <div class="ex">Expected </div>
                    </td>
                    <td>
                        <tt> 5 </tt>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="ac"> Actual </div>
                    </td>
                    <td>
                        <tt> 4   </tt>
                    </td>
                </tr>
            </table>
        """
        self.assertIn(without_ws(must_contain), without_ws(parsed))


if __name__ == "__main__":
    unittest.main()