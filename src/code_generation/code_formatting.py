from utils import chain


def format_code(*lines) -> str:
    indent_level = 0
    ret = []
    lines = chain([l.split("\n") for l in lines])
    lines = [l.strip() for l in lines]
    for l in lines:
        if len(l) > 0 and l[0] == "}":
            indent_level -= 1
        ret.append(indent_level*"\t"+l)
        if len(l) > 0 and l[-1] == "{":
            indent_level += 1
    return "\n".join(ret)