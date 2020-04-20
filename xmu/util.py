import ast
import inspect
import random
from attrdict import AttrDict
from textwrap import dedent
from typing import Callable


def splat(fn):
    """
    fn(x) -> fn(*x)
    """
    def splatted(arg_iterable):
        return fn(*arg_iterable)
    return splatted


def staticsplat(fn):
    return staticmethod(splat(fn))


def namespace(*, glob=None, fn=lambda x: x) -> Callable[[Callable], AttrDict]:
    frame = inspect.currentframe().f_back
    def _namespace(function_to_hack_open) -> AttrDict:
        nonlocal _namespace, glob
        _namespace.__name__ = f"namespace({function_to_hack_open.__name__}"
        source = dedent(inspect.getsource(function_to_hack_open))
        tree = ast.parse(source)
        glob = {**frame.f_globals, **(glob or {})}

        names_before = set(glob.keys())

        tree.body = tree.body[0].body
        """
        tree               tree
        before:            after:
        def fn():          a = 1
            a = 1          b = 2
            b = 2
        """

        

        exec(
            compile(
                tree,
                f"<namespace{function_to_hack_open.__name__}>",
                "exec"),
            glob
        )

        names_after = set(glob.keys())

        new_keys = names_after - names_before - {"local_names_before"}
        #
        # we have to subtract that set because `local_names_before`    ^
        # is defined after the collection of `locals()`:
        #      local_names_before = set(locals().keys())
        #

        return AttrDict({key: fn(glob[key]) for key in new_keys})
    
    return _namespace


def devour_namespace(obj, *nss: dict, fn=lambda x: x):
    for ns in nss:
        for name, value in ns.items():
            setattr(obj, name, fn(value))


def unique_identifier(length=16):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(alphabet) for _ in range(16))
