from ..ext import XmuExtension, register_extension
from ..util import namespace, splat

@register_extension
class BasicTable(XmuExtension):
    name = "tagf_table"
    rule = ' "table" "(" POSITIVE_INTEGER "," POSITIVE_INTEGER ")" "[" tag_normal+ "]"'

    @namespace(fn=splat)
    def handlers():
        def tagf_table(width, height, *cells):
            if len(cells) != width * height:
                return f"[Error: expected {width * height} cells, got {len(cells)}]"
            output = "<table>"

            for j in range(height):
                output += "<tr>"
                for i in range(width):
                    output += "<td>" + cells[width * j + i] + "</td>"
                output += "</tr>"

            output += "</table>"

            return output

