from . import (
    html_transformer,
    grammar,
    ext
)

def parse(text, *, context=None):
    if not isinstance(text, str):
        raise TypeError(f"Expected a string as the first argument (text), got {type(text)}: {text}")
    transformer = html_transformer.HtmlTransformer(
        extensions=ext.default_extensions,
        context=context
    )
    return transformer.transform(grammar.parser.parse(text))
