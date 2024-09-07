from .types import expand_type


def get_fn_header(fn_name: str, fn_type: list) -> str:
    ret = []
    for i in range(0, len(fn_type)-1):
        if i==0:
            prefix =  f"func {fn_name} "
        else:
            prefix = "return func"
        arg_type = fn_type[i]
        if len(fn_type[i+1:])==1:
            ret_type = fn_type[i+1]
        else:
            ret_type = fn_type[i+1:]
        ret.append(
            f"{prefix}(arg{i} {expand_type(arg_type)}) {expand_type(ret_type)}"+"{")
    return "\n".join(ret)


def get_fn_footer(fn_type: list) -> str:
    return "}\n" * (len(fn_type)-1)
