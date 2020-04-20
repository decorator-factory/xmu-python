import typing
from .util import namespace, splat
default_extensions = {}
from .grammar import rebuild_parser

class XmuExtension:
    grammar_entry_point = "CUSTOM_TAGS"
    name = "default_extension"
    rule = '"example" MY_INTEGER'
    helpers = {} # rule_name|TERMINAL_NAME: definition

    @classmethod
    def apply_myself_to_grammar(cls, grammar):
        grammar = grammar.replace(
            f"//{cls.grammar_entry_point}:",

             f"    | {cls.name} // from extension {cls.__name__}\n"
            +f"//{cls.grammar_entry_point}:"
        ) + "\n" + f"{cls.name}: {cls.rule}\n"

        for name, rule in cls.helpers.items():
            grammar += f"\n{name}: {rule}  // from extension {cls.__name__}\n"

        return grammar

    @namespace(fn=splat)
    def handlers():
        def default_extension(a, b):
            """
            In:
                example 36 6
            Out:
                42
            """
            return f"<number>{int(a) + int(b)}</number>"


def register_extension(extension: typing.Type[XmuExtension]):
    if not isinstance(extension, type) or not issubclass(extension, XmuExtension):
        raise TypeError("An extension must be an XmuExtension subclass")
    global default_extensions
    default_extensions[extension.__name__] = extension
    rebuild_parser(extension.__name__)
    return extension


def simple_tag_extension(tag_name, handler, rule_name=None):

    if rule_name:
        rule_name = f"tag_{rule_name}"
    else:
        rule_name = f"tag_{tag_name}"
    class NewExtension(XmuExtension):
        name = rule_name
        rule = f'"{tag_name}" tag_normal'
        helpers = {}

        handlers = {rule_name: splat(handler)}

    NewExtension.__name__ = f"SimpleTagExtension {rule_name}"
    register_extension(NewExtension)

