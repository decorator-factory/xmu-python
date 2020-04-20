# The imported modules are unused later on, but
# importing a module executes everything inside
# of it, therefore connecting the extensions
# to a host
from .extensions import(
    inline_style,
    jinja,
    tables,
    fontawesome,
    code_blocks,
    text_formatting,
    div
)
