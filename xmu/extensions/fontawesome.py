from ..ext import simple_tag_extension

simple_tag_extension("fas", lambda icon: f"<i class='fas fa-{icon}'></i>")
