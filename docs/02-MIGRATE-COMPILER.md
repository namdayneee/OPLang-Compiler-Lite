# One-time compiler migration checklist

The new repository must become fully independent after migration.

## Copy

```text
src/grammar/
src/astgen/
src/semantics/
src/codegen/
src/utils/
src/runtime/io.java
oplang_specification.md
oplang-semantic_constraints_and_errors.md
```

## Do not copy

```text
.git/
venv/
build/
reports/
__pycache__/
.DS_Store
src/runtime/Main.j
src/runtime/Main.class
```

## Then

1. Install Python dependencies.
2. Install Java 17+ locally.
3. Run `bash scripts/build_antlr.sh`.
4. Restore/copy relevant compiler regression tests into this repository.
5. Run tests.
6. Refactor `Emitter` and `CodeGenerator` to accept an output directory.
7. Implement `compiler_core/OPLangCompiler.compile()`.
8. Delete any temporary migration scripts if you created them.
9. Verify `grep`/search finds no import path or URL to the old repository.
10. Commit the migrated sources into this repository.

After step 10, the old repository is no longer needed to build or run this project.
