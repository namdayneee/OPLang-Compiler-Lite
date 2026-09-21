import pytest

from compiler_core import OPLangCompiler


EXAMPLE_CASES = [
    (
        "hello-world",
        "class Main { static void main() { io.writeIntLn(10); } }",
        "codegen",
    ),
    ("syntax-error", "class Main {", "parser"),
    (
        "semantic-error",
        "class Main { static void main() { missing := 10; } }",
        "semantic",
    ),
]


@pytest.mark.parametrize(("example_id", "source", "expected_stage"), EXAMPLE_CASES)
def test_representative_frontend_example_stage(
    example_id: str,
    source: str,
    expected_stage: str,
) -> None:
    result = OPLangCompiler().compile(source)

    assert result.stage == expected_stage, example_id
    assert result.success is (expected_stage == "codegen"), example_id
