import os.path
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional

from pip_requirements_parser import (
    RequirementsFile,
)
import subprocess
import sys

from poetry.inspection.info import PackageInfo


def _run_poetry(work_dir: Path, *args):
    result = subprocess.run(
        [sys.executable, "-m", "poetry", *args],
        cwd=work_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if result.returncode:
        print(result.stdout, file=sys.stderr)
        raise Exception("Poetry encountered an error")


def create_poetry_project(work_dir: Path, min_python_version: str):
    _run_poetry(
        work_dir,
        "init",
        f"--python=^{min_python_version}",
        "--no-interaction",
    )


def generate(
    work_dir: Path,
    requirements: List[str],
    existing_requirements: List[str],
    min_python_version: str,
    output_file: Path,
):
    relative_output_file = os.path.relpath(output_file)

    print(f"Populating project with {len(requirements)} top-level requirements")

    create_poetry_project(work_dir, min_python_version)
    _run_poetry(
        work_dir,
        "add",
        "--lock",
        *requirements,
    )

    if existing_requirements:
        print(
            f'Loading existing lockfile at "{relative_output_file}" containing '
            f"{len(existing_requirements)} requirements"
        )

        pyproject = work_dir / "pyproject.toml"
        pyproject_original = work_dir / "pyproject.toml.orig"
        pyproject.rename(pyproject_original)

        # Add all existing locked requirements to make poetry.lock match
        # the existing requirements.txt-format lockfile.
        create_poetry_project(work_dir, min_python_version)
        _run_poetry(
            work_dir,
            "add",
            "--lock",
            *existing_requirements,
        )

        # Revert pyproject.toml from the "existing lockfile" state to the "new
        # requirements" state.
        pyproject.unlink()
        pyproject_original.rename(pyproject)

    print("Generating fresh lockfile...")
    _run_poetry(
        work_dir,
        "lock",
        "--no-update",
    )

    print(f'Exporting pip-compatible lockfile to "{relative_output_file}"')
    _run_poetry(
        work_dir,
        "export",
        "-o",
        output_file.absolute(),
    )


def resolve_requirements(files: List[Path], work_dir: Path) -> List[str]:
    if not files:
        for p in ("requirements.in", "setup.py"):
            path = Path(p)
            if path.exists():
                files.append(path)
                break

    requirements = []
    for file in files:
        if file.name == "setup.py":
            info = PackageInfo.from_directory(file.parent)
            requirements.extend(info.requires_dist)

        raw_requirements = RequirementsFile.from_file(
            str(file), include_nested=True
        ).requirements
        for req in raw_requirements:
            if req.is_url and req.link and req.link.file_path:
                requirements.append(os.path.relpath(req.link.file_path, work_dir))
            elif req.req:
                requirements.append(str(req.req))
            else:
                raise Exception(f"[{file}] Unexpected kind of requirement: {req}")

    return requirements


def main(src_files: List[Path], output_file: Optional[Path], min_python_version: str):
    if not output_file:
        if len(src_files) == 1 and src_files[0].name.endswith(".in"):
            output_file = Path.cwd() / (src_files[0].stem + ".txt")
        else:
            output_file = Path("requirements.txt")

    td = TemporaryDirectory()
    with td as work_dir_str:
        work_dir = Path(work_dir_str) / Path.cwd().name
        work_dir.mkdir()

        requirements = resolve_requirements(src_files, work_dir)
        if output_file.exists():
            existing_requirements = resolve_requirements([output_file], work_dir)
        else:
            existing_requirements = []
        generate(
            work_dir,
            requirements,
            existing_requirements,
            min_python_version,
            output_file,
        )


def cli():
    parser = ArgumentParser(
        description="Compiles a cross-platform requirements.txt from requirements.in "
        "specs."
    )
    parser.add_argument(
        "src_files",
        metavar="src-file",
        nargs="*",
        help="requirements.in or setup.py file",
    )
    parser.add_argument(
        "-o --output-file",
        dest="output_file",
        help="Output file name. Will be derived from input file if only one provided, "
        'otherwise defaults to "requirements.txt".',
    )
    parser.add_argument(
        "--min-python-version",
        default="3.6",
        help="Minimum Python version to find supporting packages for.",
    )

    args = parser.parse_args()
    main(
        [Path(f) for f in args.src_files],
        Path(args.output_file) if args.output_file else None,
        args.min_python_version,
    )


if __name__ == "__main__":
    cli()
