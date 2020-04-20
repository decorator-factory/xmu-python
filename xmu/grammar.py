import logging
import lark

default = r"""
%import common.WS
%ignore WS


?start: document
document: tag+
?element: document | text
?atom: tag | text

?tag: normal_tags | function_tags | custom_tags

// normal tag: tag[element]

tag_normal: "[" element "]"
tag_title: "title" tag_normal
tag_paragraph: "p" tag_normal
tag_pre: "pre" tag_normal
tag_comment: /comment|todo|bug|doc/ tag_normal
tag_unknown: "!" TAG_NAME tag_normal
tag_var: "$" tag_normal
tag_varemu: "$emu" tag_normal
TAG_NAME: /[-a-zA-Z]+/
?normal_tags: tag_comment
            | tag_title
            | tag_paragraph
            | tag_pre
            | tag_normal
            | tag_var
            | tag_varemu
            

// tag function: tag(a, b, c, ...)[element]

POSITIVE_INTEGER: /[1-9][0-9]*/
INT: POSITIVE_INTEGER
?tag_function: options tag_normal

tagf_fontsize: "fontsize" "(" OPTION ")" tag_normal
tagf_header: "header" "(" POSITIVE_INTEGER ")" tag_normal
tagf_div_id: "#" ID_NAME tag_normal
tagf_div_class: "." CLASS_NAME+ tag_normal
tagf_link: "a" tag_normal tag_normal
ID_NAME: /[a-zA-Z_]+/
CLASS_NAME: /[a-zA-Z-]+/

?function_tags: tagf_fontsize
              | tagf_header
              | tagf_div_id
              | tagf_div_class
              | tagf_link

options: "(" OPTION ("," OPTION)* ")" | "(" ")"
OPTION: /[-a-zA-Z0-9_=!?:.]+/

?text: raw_text | just_text
just_text: /(?!=:raw)[^\]]+/
raw_text: /\s*:raw(.|\n)+?rrr:/

?custom_tags: tag_unknown
//CUSTOM_TAGS:        

"""

parser = lark.Lark(default)
grammar = default

def rebuild_parser(source=""):
    global parser, grammar
    grammar = rebuild_grammar(default, source)
    parser = lark.Lark(grammar)

def rebuild_grammar(initial_grammar, source=""):
    from .ext import default_extensions
    logging.log(logging.INFO, "Rebuilding grammar...", f"from {source}" if source else "")
    new_grammar = initial_grammar

    for name, extension in default_extensions.items():
        new_grammar = extension.apply_myself_to_grammar(new_grammar)
    return new_grammar
