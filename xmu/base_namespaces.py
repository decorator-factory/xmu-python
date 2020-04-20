import re
from . import parse_module
from .util import splat, namespace

def simple_tag(tag_name):
    def tag_handler(element):
        return f"<{tag_name}>{element}</{tag_name}>"
    return splat(tag_handler)


@namespace(fn=splat)
def ParseText():
    def just_text(text):
        return re.sub(r"\s+", " ", str(text))

    def raw_text(text):
        return re.sub(r":raw|rrr:", "", str(text))


@namespace()
def ParseLiterals():
    POSITIVE_INTEGER = int


@namespace()
def ParseSimpleTags():
    tag_paragraph = simple_tag("p")
    tag_pre = simple_tag("pre")
    tag_normal = splat(lambda e: e)

    @splat
    def tag_unknown(tag_name, element, *args):
        return simple_tag(tag_name)([element])

    @splat
    def tag_comment(comment_type, comment_text):
        return f"<!--{comment_type}: {comment_text}-->"


@namespace(fn=splat)
def ParseTagFunctions():

    def tagf_header(h_level, element):
        return f"<h{h_level}>{element}</h{h_level}>"

    def tagf_fontsize(size, element):
        return f"<span style='font-size: {size}'>{element}</span>"

    def tagf_div_id(id_name, element):
        return f'<div id="{id_name}">{element}</div>'

    def tagf_div_class(*args):
        *class_names, element = args
        class_string = " ".join(class_names)
        return f'<div class="{class_string}">{element}</div>'

    def tagf_link(href, element):
        # if re.match(r"^\s*http[s]?://", href):
        #     prefix = parse_module.parse("fas[external-link-alt]") + " "
        # else:
        #     prefix = ""
        prefix = ""
        return f'<a href="{href}">{prefix}{element}</a>'

namespaces = [ParseText, ParseLiterals, ParseSimpleTags, ParseTagFunctions]