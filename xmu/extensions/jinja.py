from .. import ext
from ..util import namespace, splat


ext.simple_tag_extension("%", lambda expr: "{{" + expr + "}}", "jexpr")

ext.simple_tag_extension("%extends", lambda name: '{% extends "' + name + '" %}', "jextends")


@ext.register_extension
class JinjaBlock(ext.EmuExtension):
    name = "tagf_jinja_block"
    rule = r'"%block" "(" JINJA_BLOCK_NAME ")" tag_normal'
    helpers = {"JINJA_BLOCK_NAME": r"/[a-zA-Z_]+/"}

    @namespace(fn=splat)
    def handlers():
        def tagf_jinja_block(block_name, element):
            return '{% block ' + str(block_name) + ' %}\n' \
                   + str(element) \
                   + '\n{% endblock %}\n'
