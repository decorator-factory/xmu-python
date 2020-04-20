from .. import ext
from ..util import namespace, splat, unique_identifier
import sass


@ext.register_extension
class InlineStyle(ext.EmuExtension):
    name = "tagf_style"
    rule = r'"style" tag_normal tag_normal'
    helpers = {}

    @namespace(fn=splat)
    def handlers():
        def tagf_style(style, element):
            # this handler creates a random html id
            # and defines a new style for it,
            # then attaches the id to the given element
            uid = unique_identifier()
            to_compile = f"#{uid} {{ {style} }}"
            css = sass.compile(string=to_compile)
            return f"<style>{css}</style>\n" \
                   f"<emu-styled id={uid}>{element}</emu-styled>"


@ext.register_extension
class InlineStyleLiterally(ext.EmuExtension):
    name = "tagf_lstyle"
    rule = r'"lstyle" "[" text "]" tag_normal'
    helpers = {}

    @namespace(fn=splat)
    def handlers():
        def tagf_lstyle(css, element):
            return f"<emu-styled style='{css}'>{element}</emu-styled>"
