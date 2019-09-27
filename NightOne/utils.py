# multiplies 2 nums by one and returns them. used particulary with velocities on one line
def mult2by1(in1,in2,multi, tag = ""):
    out1 = in1 * multi
    out2 = in2 * multi
    return int(out1), int(out2)

# recursice algorithm to extract all values associated with a key in a multilevel dictionary
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

def collideDetect(sprite1,sprite2):
    return sprite1.col_rect.colliderect(sprite2.rect)