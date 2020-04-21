from .. import parse
from ..ext import XmuExtension, register_extension
from ..util import namespace, splat
from textwrap import dedent
import warnings
import html
import builtins

def format_code(language, code, style="", classes=""):
    lang_class = ("nohighlight"
                        if language == "nohighlight"
                  else f"lang-{language}")
    return  f'<pre  style="margin:0;padding:0;{style}" class="shadow {classes}">'\
               f'<code class="{lang_class}">' \
                    f'{dedent(code).strip()}' \
                '</code>'\
            '</pre>'


def sandbox(code, mode="exec"):
    if mode not in ("eval", "exec"):
        raise ValueError(f"Mode must be either 'eval' or 'exec', got: {mode}")

    try:

        if mode == "eval":
            glob = {**builtins.__dict__}
            output = repr(eval(code, glob))

        elif mode == "exec":
            output = ""
            def overridden_print(*args, end="\n", sep=" "):
                nonlocal output
                output += sep.join(map(str, args)) + end
            glob = {**builtins.__dict__, "print": overridden_print}
            exec(code, glob)

    except Exception as e:
        return f"{e.__class__.__name__}: {e}"
    else:
        return output


def render_test_fail_warning(expected_output, actual_output):
    return parse(
            f"""[
                    fas[exclamation-triangle]
                    [Test failed]
                    fas[arrow-up]

                    style[
                        table {{background: rgba(0, 0, 0, 0.25);}}
                        tt, * {{padding: 4px; margin: 4px}}
                        .ex {{margin: 4px; color: #00ff00; }}
                        .ac {{margin: 4px; color: #ff0000; }}

                    ][
                        table(2, 2)[
                            [.ex[ Expected ]] [!tt[:raw {html.escape(expected_output)} rrr:]]
                            [.ac[ Actual   ]] [!tt[:raw {html.escape(actual_output)}   rrr:]]   
                        ]
                    ]
                ]
            """
        )


def run_code(code, expected_output, mode, prefix=">>> "):
    code = dedent(code).strip()
    rendered_code = format_code("python", code)
    actual_output = sandbox(code, mode)
    if (
            dedent(actual_output).strip() == dedent(expected_output).strip()
            or "#!skip" in code
    ):
        warning = ""
    else:
        warning = render_test_fail_warning(expected_output, actual_output)
        warnings.warn(f"Expected: {expected_output}, got: {actual_output}")

    rendered_output = format_code(
        "python",
        prefix + html.escape(actual_output),
        style="font-weight: 800; border-radius:0 0 1em 1em",
        classes="border-top border-secondary"
    )
    return   "<div class='container ipy'>" \
                + rendered_code\
                + "\n"\
                + rendered_output\
            +f"</div>{warning}"


@register_extension
class CodeBlocks(XmuExtension):
    """
    Code block for `highlight.js`
    """
    name = "tagf_code_block"
    rule = r'"code" "(" LANGUAGE ")" tag_normal'
    helpers = {"LANGUAGE": r"/[-a-zA-Z_]+/"}

    handlers = {"tagf_code_block": splat(format_code)}


@register_extension
class PythonCodeBlockExec(XmuExtension):
    """
    Code block for `highlight.js` that takes
    a piece of python code and an expected
    output, then it checks whether the actual
    output matches the expected output.
    """
    name = "tagf_py_exec"
    rule = r'"py-exec" tag_normal tag_normal'

    @namespace(fn=splat)
    def handlers():
        def tagf_py_exec(code, expected_output):
            return run_code(code, expected_output, mode="exec", prefix="")


@register_extension
class PythonCodeBlockEval(XmuExtension):
    name = "tagf_py_eval"
    rule = r'"py-eval" tag_normal tag_normal'

    @namespace(fn=splat)
    def handlers():
        def tagf_py_eval(code, expected_output):
            return run_code(code, expected_output, mode="eval", prefix=">>> ")

