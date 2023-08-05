"""
A selection of useful function and classes
"""
import re

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    to
    '''
    def int_or_txt(text):
        return int(text) if text.isdigit() else text.lower()

    return [int_or_txt(c) for c in re.split(r'(\d+)', text)]

class HashableDict(dict):
    """
    A version of the dictionary class but has a hash method.
    """
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
