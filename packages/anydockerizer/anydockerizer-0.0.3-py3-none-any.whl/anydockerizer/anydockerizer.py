import ast
import fnmatch
import importlib.util
import logging
import os
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple

from distlib.database import (
    BaseInstalledDistribution,
    DistributionPath,
    make_graph,
)


IGNORE = [
    "__pycache__",
    "build",
    "develop-eggs",
    "dist",
    "eggs",
    ".eggs",
    "sdist",
    "wheels",
    "*.egg-info",
    "htmlcov",
    ".tox",
    ".nox",
    "cover",
    "_build",
    "__pypackages__",
    ".env",
    ".venv",
    "env",
    "venv",
    "ENV",
    ".idea",
    ".vscode",
]


DEFAULT_CONFIG = {
    'path': None,
    'exclude': None,
    'encoding': 'utf8',
    'follow_links': False,
}


def run(config: dict):
    config = dict(DEFAULT_CONFIG, **config)
    try:
        config['path'] = Path(config['path'])
    except Exception:
        raise
    mapping = get_local_package_distribution_mapping()
    print("--- Mapping ---")
    print("\n".join([str(d) for d in mapping.values()]))
    packages = get_imported_packages(
        path=config['path'],
        exclude=config['exclude'],
        encoding=config['encoding'],
        follow_links=config['follow_links'],
    )
    print("--- Import ---")
    print("\n".join(packages))
    dists, _ = extract_related_distributions(
        imported_packages=packages,
        package_distribution_mapping=mapping,
    )
    freeze_distributions(
        dists=sorted(dists, key=lambda d: d.name.lower()),
        path=config['path'],
    )


def get_local_python_env() -> str:
    pass


def get_local_package_distribution_mapping() -> Dict[str, BaseInstalledDistribution]:
    mapping = {}
    dists = DistributionPath(include_egg=True).get_distributions()
    for dist in dists:
        if dist.modules:
            for module_name in dist.modules:
                mapping[module_name] = dist
        else:
            mapping[dist.name] = dist
    return mapping


def get_imported_packages(
    path: Path,
    exclude: Optional[List[str]]=None,
    encoding: str='utf8',
    follow_links: bool=False,
) -> List[str]:
    visitor = ImportedPackagesVisitor()

    ignore = IGNORE
    if exclude:
        ignore.extend([e for e in exclude])
    ignore_pattern = r"|".join([fnmatch.translate(i) for i in ignore])

    walk = os.walk(path, followlinks=follow_links, topdown=True)
    for root, dirs, files in walk:
        # In-place update `dirs` to exclude ignored dirs
        dirs[:] = [d for d in dirs if not re.match(ignore_pattern, d)]
        files = [f for f in files if Path(f).suffix == ".py"]

        for file_name in files:
            file = Path(root) / file_name
            with file.open(mode="r", encoding=encoding) as f:
                contents = f.read()
            visitor.visit(ast.parse(contents))

    # Folders and files in code project's possible to be imported internally
    importable = set()
    for entry in Path(path).iterdir():
        if entry.is_dir():
            importable.add(entry.name)
        elif entry.is_file() and entry.suffix == ".py":
            importable.add(entry.stem)
    logging.debug(f"Internal importable pseudo-packages: {importable}")

    return list(visitor.imported_packages.difference(importable))


def extract_related_distributions(
    imported_packages: List[str],
    package_distribution_mapping: Dict[str, BaseInstalledDistribution],
) -> Tuple[List[BaseInstalledDistribution], List[str]]:
    # 1st stage: filter out directly imported packages' distributions
    filtered_distributions = set()
    bad_packages = set()
    for package in imported_packages:
        # Keep the root level of package ex. ruamel.yaml will become ruamel
        package, _, _ = package.partition(".")
        if package in package_distribution_mapping:
            # Package mapped with an installed distribution
            filtered_distributions.add(package_distribution_mapping[package])
        elif not importlib.util.find_spec(package):
            # Package is not part of installed builtin/stdlib/distributions
            bad_packages.add(package)
            logging.warning(f"[ANYD] `{package}` imported but not installed")

    # 2nd stage: populate indirect dependencies' distributions
    for dist in filtered_distributions.copy():
        deps = get_required_dists(package_distribution_mapping.values(), dist)
        for dep in deps:
            filtered_distributions.add(dep)
    return list(filtered_distributions), list(bad_packages)


def get_required_dists(
    dists: List[BaseInstalledDistribution],
    dist: BaseInstalledDistribution,
) -> List[BaseInstalledDistribution]:
    """
    Modified from ``distlib.dataset.get_required_dists``.

    Recursively generate a list of distributions from *dists* that are
    required by *dist*.

    :param dists: a list of distributions
    :param dist: a distribution, member of *dists* for which we are interested
    """
    if dist not in dists:
        raise Exception(
            f"Given distribution {dist.name} "
            "is not a member of the given list)"
        )
    graph = make_graph(dists)

    req = {d: False for d in dists}  # is each distribution required initialized with False
    todo = graph.adjacency_list[dist]  # list of nodes we should inspect

    while todo:
        d = todo.pop()[0]
        req[d] = True
        for pred in graph.adjacency_list[d]:
            if not req[d]:
                todo.append(pred)

    return [dist for dist, required in req.items() if required]


def freeze_distributions(
    dists: List[BaseInstalledDistribution],
    path: Path,
    requirements_filename="anyd_generated_requirements.txt",
) -> str:
    frozen = "\n".join([f"{d.name}=={d.version}" for d in dists])
    with open(Path(path) / requirements_filename, "w") as f:
        f.write(frozen)
    return frozen


class ImportedPackagesVisitor(ast.NodeVisitor):
    """
    An AST visitor to collect imported packages from all AST nodes.

    Attributes
    ----------
    imported_packages
        Set of all imported packages collected from all visited AST nodes.
    """

    def __init__(self):
        super().__init__()
        self.imported_packages = set()

    def visit_Import(self, node: ast.Import):
        # Possibly multiple packages imported in one statement
        for child in node.names:
            if child.name:
                package, _, _ = child.name.partition(".")
                self.imported_packages.add(package)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        # Discard any relative imports
        if node.module and node.level == 0:
            package, _, _ = node.module.partition(".")
            self.imported_packages.add(package)
        self.generic_visit(node)
