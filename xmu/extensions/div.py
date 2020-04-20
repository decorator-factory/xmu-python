from ..ext import register_extension, XmuExtension
from ..util import namespace, splat

@register_extension
class ConfigurableDiv(XmuExtension):
    name = "tagf_configurable_div"
    rule = r'"div" maybe_div_id maybe_div_class_names tag_normal'
    helpers = {
        "maybe_div_id": r'["#" ID_NAME]',
        "maybe_div_class_names": r'["." CLASS_NAME*]'
    }

    @namespace()
    def handlers():
        @splat
        def tagf_configurable_div(maybe_id, maybe_classes, content):
            return f"<div{maybe_id}{maybe_classes}>{content}</div>"

        @splat
        def maybe_div_id(id_name):
            if id_name:
                return f" id='{id_name}' "
            else:
                return " "

        def maybe_div_class_names(class_names):
            if class_names:
                return f" class=\"{' '.join(class_names)}\" "
            else:
                return " "

        


