import os
from .parse_module import parse

class PyramidRendererFactory:
    def __init__(self, info):
        """ Constructor: info will be an object having the
        following attributes: name (the renderer name), package
        (the package that was 'current' at the time the
        renderer was registered), type (the renderer type
        name), registry (the current application registry) and
        settings (the deployment settings dictionary). """
        self.info = info

    def __call__(self, value, system):
        """ Call the renderer implementation with the value
        and the system value passed in as arguments and return
        the result (a string or unicode object).  The value is
        the return value of a view.  The system value is a
        dictionary containing available system values
        (e.g., view, context, and request). """
        # Obtain the absolute path of a template and render it:
        package = system['renderer_info'].package
        caller_dir = os.path.dirname(package.__file__)
        relative_template_path = system['renderer_name']
        template_path = os.path.join(caller_dir, relative_template_path)
        with open(template_path, 'r') as file:
            text = file.read()
        return parse(text, context=self.construct_context(value))

    def construct_context(self, value):
        """Convert the dict returned by a view to a context
        that will be passed to the template"""
        return value
