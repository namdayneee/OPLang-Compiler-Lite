#!/usr/bin/env python3
"""One-time, read-only migration of OPLang compiler sources into this repository.

Usage:
    python scripts/migrate_compiler_from_path.py C:\\path\\to\\BTL-PPL
    python scripts/migrate_compiler_from_path.py ../BTL-PPL

The source directory is never modified. This script copies files only into the
current repository. After migration, the new repository has no runtime dependency
on the source path and this script may be deleted.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

COPY_DIRS = [
    "src/grammar",
    "src/astgen",
    "src/semantics",
    "src/codegen",
    "src/utils",
]

COPY_FILES = [
    "src/__init__.py",
    "src/runtime/io.java",
    "oplang_specification.md",
    "oplang-semantic_constraints_and_errors.md",
]

OPTIONAL_TESTS = [
    "tests/test_lexer.py",
    "tests/test_parser.py",
    "tests/test_ast_gen.py",
    "tests/test_checker.py",
    "tests/test_codegen.py",
    "tests/utils.py",
]

EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".class", ".j"}


def ignore(_directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in EXCLUDED_NAMES or Path(name).suffix in EXCLUDED_SUFFIXES:
            ignored.add(name)
    return ignored


def copy_file(source_root: Path, target_root: Path, relative: str, required: bool = True) -> None:
    src = source_root / relative
    dst = target_root / relative
    if not src.exists():
        if required:
            raise FileNotFoundError(f"Required source file not found: {src}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"copied {relative}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Local path to the old coursework repository")
    parser.add_argument("--with-tests", action="store_true", help="Also copy the existing regression tests")
    args = parser.parse_args()

    source_root = args.source.expanduser().resolve()
    target_root = Path(__file__).resolve().parents[1]

    if source_root == target_root:
        raise SystemExit("Source and target must be different repositories.")
    if not (source_root / "src" / "grammar" / "OPLang.g4").exists():
        raise SystemExit("The source directory does not look like the OPLang coursework repository.")

    for relative in COPY_DIRS:
        src = source_root / relative
        dst = target_root / relative
        if dst.exists():
            raise SystemExit(f"Target already exists: {dst}. Refusing to overwrite migrated compiler code.")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst, ignore=ignore)
        print(f"copied {relative}/")

    for relative in COPY_FILES:
        copy_file(source_root, target_root, relative)

    (target_root / "src" / "runtime").mkdir(parents=True, exist_ok=True)

    if args.with_tests:
        for relative in OPTIONAL_TESTS:
            copy_file(source_root, target_root, relative, required=False)

    print("\nMigration complete.")
    print("The source repository was read only and was not modified.")
    print("Next: build ANTLR, run tests, then refactor Emitter/CodeGenerator output_dir.")


if __name__ == "__main__":
    main()
