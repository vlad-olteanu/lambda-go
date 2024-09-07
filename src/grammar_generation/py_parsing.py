from typing import List, Tuple
import re

def get_sections(src_text: str):
    """
    src_text => (import_section: str, map[function_name] function_text, final_commands: str)
    """
    if src_text=="":
        return "", {}, "" 

    sections = re.split("# ==Function==.*\n", src_text)
    sections[-1], final_commands = re.split("# ==Final Commands==.*\n",  sections[-1])

    import_section = sections[0]
    function_declarations = sections[1:]

    def get_function_name(src_text) -> str:
        try:
            return src_text.split("def ")[1].split("(")[0].strip()
        except Exception:
            raise Exception(
                "Function name could not be extracted:\n"+src_text+"\n")

    return import_section, {get_function_name(fn): fn for fn in sections[1:]}, final_commands
