from ..ext import register_extension, EmuExtension
from ..util import namespace, splat

# @register_extension
# class Div(EmuExtension):
#     name = "tagf_jinja_block"
#     rule = r'"div" maybe_class_names maybe_div_id tag_normal'
#     helpers = {
#         "maybe_div_id": r'("#" ID_NAME)?',
#         "maybe_class_names": r'("." CLASS_NAME)*'
#     }

#     @namespace(fn=splat)
#     def handlers():
#         def tagf_jinja_block(block_name, element):
#             return '{% block ' + str(block_name) + ' %}\n' \
#                    + str(element) \
#                    + '\n{% endblock %}\n'
