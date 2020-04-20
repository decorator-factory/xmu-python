import re
from ..ext import simple_tag_extension, XmuExtension, register_extension
from ..util import namespace, splat

simple_tag_extension("bf", lambda e: f"<b>{e}</b>")
simple_tag_extension("it", lambda e: f"<i>{e}</i>")
simple_tag_extension("^", lambda e: f"<sup>{e}</sup>", "superscript")
simple_tag_extension("_", lambda e: f"<sub>{e}</sub>", "subscript")

# ?alpha -> &alpha;

CONSTANTS = {
    "--": "&mdash;",
    "alpha": "&alpha;",
    "beta": "&beta;",
    "pi": "&pi;",
    "forall": "&forall;",
    "exists": "&exist;",
    "not-exists": "&#x2204;",
    "in": "&isin;",
    "not-in": "&notin;",
    "set-or": "&cup;",
    "set-and": "&cap;",
    "<=": "&le;",
    ">=": "&ge;",
    "!=": "&ne;",
    "subset": "&sub;",
    "supset": "&sup;",
    "subset-e": "&sube;",
    "supset-e": "&supe;",
    "qed": "&#x25fc;",
}

CONSTANTS_REGEXP = "|".join(map(re.escape, CONSTANTS.keys()))

@register_extension
class Constant(XmuExtension):
    name = "tag_const"
    rule = rf'"?" /{CONSTANTS_REGEXP}/i'
    helpers = {}

    @namespace(fn=splat)
    def handlers():
        def tag_const(constant_name):
            return CONSTANTS[constant_name]