import unittest
import re
import difflib


def without_ws(string):
    return re.sub(r"\s+", "", string)

def are_strings_close(
        a, b, *,
        threshold: "higher = stricter; 1..0",
        ignore_ws
        ):
    if ignore_ws:
        a = without_ws(a)
        b = without_ws(b)
    sm = difflib.SequenceMatcher(a=a, b=b)
    return sm.ratio() >= threshold


class XmuTestCase(unittest.TestCase):
    def assertClose(self, a, b, threshold=0.8, ignore_ws=True):
        if not are_strings_close(a, b, threshold=threshold, ignore_ws=ignore_ws):
            print("\nString a:")
            print(a)
            print("String b:")
            print(b)
            self.assertTrue(False)
        else:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()