import glob
import importlib
import types
from pathlib import Path
from typing import Dict, List, Tuple

from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent

PACKAGE_DIR_NAME = "ml6_kfp_components"

loader = importlib.machinery.SourceFileLoader(
    fullname="version",
    path=str(Path(PACKAGE_DIR_NAME) / "__init__.py"),
)
version = types.ModuleType(loader.name)
loader.exec_module(version)


def read_requirements(
    base_dir: Path, special_extras: List[str] = None
) -> Tuple[List[str], Dict[str, List[str]]]:
    """
    Extracts the packages install and extra requirements from `requirements.*` files in `base_dir`.

    Args:
        base_dir: the directory in which to look for `requirements.*` files
        special_extras: a list of special extras that are not included in the `all` extra

    Returns:
        install_requires: the list of requirements of the package,
        extras_require: a dictionary of extra requirements for the package

    Note:
        - the `requirements.txt` file is treated as the `install_requires` file.
        - the suffixes of the other `requirements.*` files determine the name of the extras.
        - the `dev` extra will contain **all** packages from all extra requirements
        - there is an additional `all` extra created, which contains all except the `special_extras`
    """
    req_files = [Path(req).name for req in glob.glob(f"{base_dir}/requirements.*")]
    reqs_map = dict((Path(req_file).suffix[1:], req_file) for req_file in req_files)
    for name, reqs_file in reqs_map.items():
        with open(f"{base_dir}/{reqs_file}") as fh:
            reqs_map[name] = [ln.strip() for ln in fh.readlines()]
    reqs = reqs_map.pop("txt")
    reqs_map["dev"] = [pkg for pkgs in reqs_map.values() for pkg in pkgs]
    if not special_extras:
        special_extras = []
    reqs_map["all"] = [
        pkg for extra, pkgs in reqs_map.items() if extra not in special_extras for pkg in pkgs
    ]
    return reqs, reqs_map


def read_package_data(package_dir):
    return {
        package_dir: [
            x.replace(package_dir, "")
            for x in glob.glob(package_dir + "/**/*.yaml", recursive=True)
        ]
    }


def read_long_description(base_dir: Path) -> str:
    return open(base_dir / "README.md", encoding="utf-8").read()


long_description = read_long_description(BASE_DIR)
install_requires, extras_require = read_requirements(
    BASE_DIR, special_extras=["dev", "test", "docs"]
)
package_data = read_package_data(PACKAGE_DIR_NAME)

setup(
    name="ml6-kfp-components",
    version=version.__version__,
    license="Apache License 2.0",
    description="A compilation of ML6 shared KFP components.",
    long_description=long_description,
    author="Maximilian Gartz",
    author_email="maximilian.gartz@ml6.eu",
    url="",
    keywords=["kfp", "vertex-ai-pipelines", "components"],
    classifiers=[],
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    include_package_data=True,
    package_data=package_data,
    install_requires=install_requires,
    extras_require=extras_require,
)
