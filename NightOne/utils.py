def cleanDuplicates(structure):
    clean = []
    for item in structure:
        if item not in clean:
            clean.append(item)
    return(clean)
# recursiVe algorithm to extract all values associated with a key in a multilevel dictionary
def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

def vec2int(v):
    return (int(v.x), int(v.y))

