# multiplies 2 nums by one and returns them. used particulary with velocities on one line
def mult2by1(in1,in2,multi, tag = ""):
    out1 = in1 * multi
    out2 = in2 * multi
    return int(out1), int(out2)

def cleanDuplicates(structure):
    clean = []
    for item in structure:
        if item not in clean:
            clean.append(item)
    return(clean)
