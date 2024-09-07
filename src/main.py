from tokenization.lex import lexer
from parsing import parse
from utils import flatten
import sys
from program_factory import build_program
from code_generation.function_expansion import expand_functions
from code_generation.hard_fn_expansion import expand_hard_fns
from code_generation.go_src import copy_go_src
import argparse
import os
import re


def split_statements(src_text):
    lines = src_text.split("\n")
    lines = [l.rstrip() for l in lines]
    src_text = "\n".join(lines)
    statements = re.split(r"\.\n|\.$", src_text)
    return [s+"\n\n" for s in statements]


def parse_statements(statements):
    return flatten([parse(s) for s in statements if s is not None])


def write_fns_file(output_dir, program, package_name=None):
    if package_name is None:
        package_name = os.path.basename(output_dir)
    file_path = os.path.join(output_dir, "functions.go")
    with open(file_path, "w") as f:
        def print_file(*args, **kwargs): print(*args, **kwargs, file=f)
        print_file(f"package {package_name}")
        print_file("")
        print_file(expand_functions(program))


def write_hard_fns_file(output_dir, program, package_name=None):
    if package_name is None:
        package_name = os.path.basename(output_dir)
    file_path = os.path.join(output_dir, "hardFunctions.go")
    with open(file_path, "w") as f:
        def print_file(*args, **kwargs): print(*args, **kwargs, file=f)
        print_file(f"package {package_name}")
        print_file("")
        print_file(expand_hard_fns(program))


def write_program_representation(output_dir, program):
    """
    Only used for debugging
    """
    file_path = os.path.join(output_dir, "program")
    with open(file_path, "w") as f:
        print(program, file=f)


def main():
    parser = argparse.ArgumentParser("compiler")
    parser.add_argument("src_path")
    parser.add_argument("output_dir")
    parser.add_argument("-pkg", "--package-name", type=str,
                        help="Package name of the generated code")
    args = parser.parse_args()

    src_path, output_dir = args.src_path, args.output_dir

    with open(src_path, "r") as f:
        src = f.read()
    statements = split_statements(src)
    statements = parse_statements(statements)
    program = build_program(statements)

    # source generation
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    write_program_representation(output_dir, program)
    write_fns_file(output_dir, program, package_name=args.package_name)
    write_hard_fns_file(output_dir, program, package_name=args.package_name)
    copy_go_src(output_dir, package_name=args.package_name)


if __name__ == "__main__":
    main()
