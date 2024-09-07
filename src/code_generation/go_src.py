import os
import shutil

DEFAULT_GO_SRC_DIR = os.path.join(
    os.path.dirname(__file__),
    "go_sources"
)


def copy_go_src(out_dir: str, go_src_dir: str = DEFAULT_GO_SRC_DIR, package_name = None):
    if package_name is None:
        package_name = os.path.basename(out_dir)
    for f in os.listdir(go_src_dir):
        fpath = os.path.join(go_src_dir, f)
        if os.path.isfile(fpath):
            dst_path = os.path.join(out_dir, f)
            with open(fpath, "r") as f:
                content = f.read()
            with open(dst_path, "w") as f:
                f.write(f"package {package_name}\n\n")
                f.write(content)
