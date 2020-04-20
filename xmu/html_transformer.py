import lark
from .util import devour_namespace
from . import parse_module
from . import base_namespaces

@lark.v_args(inline=True)
class HtmlTransformer(lark.Transformer):
    def __init__(self, *, extensions=None, context=None):
        super().__init__()
        self.context = {} if context is None else context
        self.extensions = {} if extensions is None else extensions

        devour_namespace(self, *base_namespaces.namespaces)
        
        for name, extension in self.extensions.items():
            devour_namespace(self, extension.handlers)

    @staticmethod
    def document(tags):
        return  "\n".join(map(str,tags))

    def tag_var(self, expr):
        return str(eval(expr, __builtins__, self.context))

    def tag_varxmu(self, code):
        return parse_module.parse(
            eval(code, __builtins__, self.context),
            context=self.lookup
        )
