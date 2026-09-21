from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from compiler_core import OPLangCompiler


compiler = OPLangCompiler()


VALID_PROGRAM = """
class Main {
    static void main() {
        io.writeIntLn(10);
    }
}
"""


def test_valid_compilation():
    result = compiler.compile(
        VALID_PROGRAM
    )

    assert result.success is True
    assert result.stage == "codegen"
    assert "Main.j" in result.jasmin_files


def test_parser_error():
    source = """
    class Main {
        static void main( {
        }
    }
    """

    result = compiler.compile(source)

    assert result.success is False
    assert result.stage == "parser"


def test_semantic_error():
    source = """
    class Main {
        static void main() {
            x := 1;
        }
    }
    """

    result = compiler.compile(source)

    assert result.success is False
    assert result.stage == "semantic"


def test_ast_can_be_disabled():
    result = compiler.compile(
        VALID_PROGRAM,
        include_ast=False,
    )

    assert result.success
    assert result.ast is None


def test_jasmin_can_be_hidden():
    result = compiler.compile(
        VALID_PROGRAM,
        include_jasmin=False,
    )

    assert result.success
    assert result.jasmin_files == {}


def test_parallel_compilation():
    def compile_once():
        return compiler.compile(
            VALID_PROGRAM
        )

    with ThreadPoolExecutor(
        max_workers=8
    ) as pool:

        results = list(
            pool.map(
                lambda _: compile_once(),
                range(8)
            )
        )

    assert all(
        result.success
        for result in results
    )

    assert all(
        "Main.j"
        in result.jasmin_files
        for result in results
    )


def test_compilation_does_not_depend_on_current_working_directory(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = compiler.compile(VALID_PROGRAM)

    assert result.success is True
    assert not (tmp_path / "Main.j").exists()

def test_builtin_io_compiles():
    source = """
    class Main {
        static void main() {
            io.writeIntLn(10);
        }
    }
    """

    result = compiler.compile(source)

    assert result.success is True, result.errors
    assert result.stage == "codegen"
    assert "Main.j" in result.jasmin_files

def test_unknown_receiver_is_rejected():
    source = """
    class Main {
        static void main() {
            unknown.writeIntLn(10);
        }
    }
    """

    result = compiler.compile(source)

    assert result.success is False
    assert result.stage == "semantic"
    assert result.errors[0].code == "UNDECLARED_IDENTIFIER"

def test_unknown_io_method_is_rejected():
    source = """
    class Main {
        static void main() {
            io.notExistingMethod(10);
        }
    }
    """

    result = compiler.compile(source)

    assert result.success is False
    assert result.stage == "semantic"
    assert result.errors[0].code == "UNDECLARED_METHOD"

def test_builtin_io_rejects_wrong_argument_type():
    source = """
    class Main {
        static void main() {
            io.writeIntLn("not an integer");
        }
    }
    """

    result = compiler.compile(source)

    assert result.success is False
    assert result.stage == "semantic"


def test_declared_integer_for_loop_compiles():
    source = """
    class Main {
        static void main() {
            int i := 0, sum := 0;
            for i := 1 to 3 do {
                sum := sum + i;
            }
            io.writeIntLn(sum);
        }
    }
    """

    result = compiler.compile(source)

    assert result.success is True, result.errors
    assert result.stage == "codegen"
