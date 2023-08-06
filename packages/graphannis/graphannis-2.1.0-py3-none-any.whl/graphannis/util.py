import re

def node_name_from_match(match):
    """ Takes a match identifier (which includes the matched annotation name) and returns the node name. This can take a single string or a list of strings as argument. 
    
    >>> m = node_name_from_match("tiger::cat::topcorpus/subcorpus/doc1#n2")
    >>> m == "topcorpus/subcorpus/doc1#n2"
    True

    """
    if isinstance(match, str):
        elements = re.split('::', match, 3)
        if len(elements) == 3:
            return elements[2]
        elif len(elements) == 2:
            return elements[1]
        else:
            return elements[0]
    elif isinstance(match, list):
        result = []
        for m in match:
            result.append(node_name_from_match(m))
        return result
    else:
        return None
