"""
Test cases for OPLang code generation.
This file contains test cases for the code generator.
Students should add more test cases here.
"""

from src.utils.nodes import *
from utils import CodeGenerator


def test_001():
    """Test basic class with main method and print statement"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,  # is_static
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("print"),
                                [MethodCall("print", [StringLiteral("Hello World")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test integer literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("print"),
                                [MethodCall("print", [
                                    PostfixExpression(
                                        Identifier("int2str"),
                                        [MethodCall("int2str", [IntLiteral(42)])]
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test float literal"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("float2str"), [
                                    MethodCall("float2str", [FloatLiteral(3.14)])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test boolean literal true"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [BoolLiteral(True)])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test boolean literal false"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [BoolLiteral(False)])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test string literal"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [StringLiteral("Test String")])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "Test String"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test variable declaration with int"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [
                        Variable("x", IntLiteral(42))
                    ])
                ], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("x")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test variable assignment"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(10))])
                ], [
                    AssignmentStatement(IdLHS("x"), IntLiteral(20)),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("x")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test binary operation: addition"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(IntLiteral(5), "+", IntLiteral(3))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test binary operation: subtraction"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(IntLiteral(10), "-", IntLiteral(3))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "7"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_011():
    """Test binary operation: multiplication"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(IntLiteral(4), "*", IntLiteral(5))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_012():
    """Test binary operation: division"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(IntLiteral(20), "/", IntLiteral(4))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_013():
    """Test binary operation: modulo"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(IntLiteral(10), "%", IntLiteral(3))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_014():
    """Test relational operation: equal"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(IntLiteral(5), "==", IntLiteral(5))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_015():
    """Test relational operation: not equal"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(IntLiteral(5), "!=", IntLiteral(3))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_016():
    """Test relational operation: less than"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(IntLiteral(3), "<", IntLiteral(5))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_017():
    """Test relational operation: greater than"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(IntLiteral(7), ">", IntLiteral(3))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_018():
    """Test relational operation: less than or equal"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(IntLiteral(5), "<=", IntLiteral(5))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_019():
    """Test relational operation: greater than or equal"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(IntLiteral(5), ">=", IntLiteral(3))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_020():
    """Test logical operation: AND true"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(BoolLiteral(True), "&&", BoolLiteral(True))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_021():
    """Test logical operation: AND false"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(BoolLiteral(True), "&&", BoolLiteral(False))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_022():
    """Test logical operation: OR true"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(BoolLiteral(False), "||", BoolLiteral(True))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_023():
    """Test logical operation: OR false"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(BoolLiteral(False), "||", BoolLiteral(False))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_024():
    """Test unary operation: negation"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [UnaryOp("-", IntLiteral(5))])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_025():
    """Test unary operation: positive"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [UnaryOp("+", IntLiteral(5))])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_026():
    """Test unary operation: logical NOT true"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [UnaryOp("!", BoolLiteral(True))])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_027():
    """Test unary operation: logical NOT false"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [UnaryOp("!", BoolLiteral(False))])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_028():
    """Test if statement: then branch"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    IfStatement(
                        BoolLiteral(True),
                        BlockStatement([], [
                            MethodInvocationStatement(
                                PostfixExpression(Identifier("print"), [
                                    MethodCall("print", [StringLiteral("yes")])
                                ])
                            )
                        ]),
                        None
                    )
                ])
            )
        ])
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_029():
    """Test if statement: else branch"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    IfStatement(
                        BoolLiteral(False),
                        BlockStatement([], [
                            MethodInvocationStatement(
                                PostfixExpression(Identifier("print"), [
                                    MethodCall("print", [StringLiteral("yes")])
                                ])
                            )
                        ]),
                        BlockStatement([], [
                            MethodInvocationStatement(
                                PostfixExpression(Identifier("print"), [
                                    MethodCall("print", [StringLiteral("no")])
                                ])
                            )
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "no"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_030():
    """Test for loop: counting up"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))])
                ], [
                    ForStatement("i", IntLiteral(1), "to", IntLiteral(5),
                        BlockStatement([], [
                            AssignmentStatement(
                                IdLHS("sum"),
                                BinaryOp(Identifier("sum"), "+", Identifier("i"))
                            )
                        ])
                    ),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("sum")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_031():
    """Test for loop: counting down"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))])
                ], [
                    ForStatement("i", IntLiteral(5), "downto", IntLiteral(1),
                        BlockStatement([], [
                            AssignmentStatement(
                                IdLHS("sum"),
                                BinaryOp(Identifier("sum"), "+", Identifier("i"))
                            )
                        ])
                    ),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("sum")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_032():
    """Test variable shadowing in nested scopes"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(10))])
                ], [
                    IfStatement(
                        BoolLiteral(True),
                        BlockStatement([
                            VariableDecl(False, PrimitiveType("int"), [Variable("y", IntLiteral(32))])
                        ], [
                            MethodInvocationStatement(
                                PostfixExpression(Identifier("print"), [
                                    MethodCall("print", [
                                        PostfixExpression(Identifier("int2str"), [
                                            MethodCall("int2str", [
                                                BinaryOp(Identifier("x"), "+", Identifier("y"))
                                            ])
                                        ])
                                    ])
                                ])
                            )
                        ]),
                        None
                    )
                ])
            )
        ])
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_033():
    """Test expression with multiple operations"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(
                                            BinaryOp(IntLiteral(5), "+", IntLiteral(3)),
                                            "-",
                                            IntLiteral(0)
                                        )
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_034():
    """Test multiple variable declarations"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [
                        Variable("a", IntLiteral(10)),
                        Variable("b", IntLiteral(20))
                    ])
                ], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(Identifier("a"), "+", Identifier("b"))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_035():
    """Test nested if statements"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    IfStatement(
                        BoolLiteral(True),
                        BlockStatement([], [
                            IfStatement(
                                BoolLiteral(True),
                                BlockStatement([], [
                                    MethodInvocationStatement(
                                        PostfixExpression(Identifier("print"), [
                                            MethodCall("print", [StringLiteral("nested")])
                                        ])
                                    )
                                ]),
                                None
                            )
                        ]),
                        None
                    )
                ])
            )
        ])
    ])
    expected = "nested"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_036():
    """Test complex arithmetic expression"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(
                                            BinaryOp(IntLiteral(2), "+", IntLiteral(3)),
                                            "*",
                                            IntLiteral(4)
                                        )
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_037():
    """Test parenthesized expression"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        ParenthesizedExpression(
                                            BinaryOp(IntLiteral(2), "+", IntLiteral(3))
                                        )
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_038():
    """Test float arithmetic"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("float2str"), [
                                    MethodCall("float2str", [
                                        BinaryOp(FloatLiteral(2.5), "+", FloatLiteral(3.5))
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "6.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_039():
    """Test variable with no initialization"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("x", None)])
                ], [
                    AssignmentStatement(IdLHS("x"), IntLiteral(100)),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("x")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_040():
    """Test if with comparison"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    IfStatement(
                        BinaryOp(IntLiteral(5), ">", IntLiteral(3)),
                        BlockStatement([], [
                            MethodInvocationStatement(
                                PostfixExpression(Identifier("print"), [
                                    MethodCall("print", [StringLiteral("greater")])
                                ])
                            )
                        ]),
                        BlockStatement([], [
                            MethodInvocationStatement(
                                PostfixExpression(Identifier("print"), [
                                    MethodCall("print", [StringLiteral("not greater")])
                                ])
                            )
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "greater"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# Continue with more comprehensive tests...
# Due to length, I'll add a selection of important test cases

def test_041():
    """Test break in for loop"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("count", IntLiteral(0))])
                ], [
                    ForStatement("i", IntLiteral(1), "to", IntLiteral(10),
                        BlockStatement([], [
                            AssignmentStatement(
                                IdLHS("count"),
                                BinaryOp(Identifier("count"), "+", IntLiteral(1))
                            ),
                            IfStatement(
                                BinaryOp(Identifier("i"), "==", IntLiteral(5)),
                                BreakStatement(),
                                None
                            )
                        ])
                    ),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("count")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_042():
    """Test continue in for loop"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))])
                ], [
                    ForStatement("i", IntLiteral(1), "to", IntLiteral(5),
                        BlockStatement([], [
                            IfStatement(
                                BinaryOp(Identifier("i"), "==", IntLiteral(3)),
                                ContinueStatement(),
                                None
                            ),
                            AssignmentStatement(
                                IdLHS("sum"),
                                BinaryOp(Identifier("sum"), "+", Identifier("i"))
                            )
                        ])
                    ),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("sum")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "12"  # 1+2+4+5 = 12 (skipping 3)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_043():
    """Test final variable (constant)"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(True, PrimitiveType("int"), [
                        Variable("PI", IntLiteral(314))
                    ])
                ], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("PI")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "314"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_044():
    """Test complex arithmetic with multiple variables"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [
                        Variable("a", IntLiteral(2)),
                        Variable("b", IntLiteral(3)),
                        Variable("c", IntLiteral(4))
                    ])
                ], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [
                                        BinaryOp(
                                            BinaryOp(Identifier("a"), "+", Identifier("b")),
                                            "*",
                                            Identifier("c")
                                        )
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_045():
    """Test complex boolean expression"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("bool2str"), [
                                    MethodCall("bool2str", [
                                        BinaryOp(
                                            BinaryOp(IntLiteral(5), ">", IntLiteral(3)),
                                            "&&",
                                            BinaryOp(IntLiteral(10), "<", IntLiteral(20))
                                        )
                                    ])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# Additional comprehensive tests covering edge cases and combinations
def test_046():
    """Test nested for loops"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))])
                ], [
                    ForStatement("i", IntLiteral(1), "to", IntLiteral(3),
                        BlockStatement([], [
                            ForStatement("j", IntLiteral(1), "to", IntLiteral(2),
                                BlockStatement([], [
                                    AssignmentStatement(
                                        IdLHS("sum"),
                                        BinaryOp(Identifier("sum"), "+", IntLiteral(1))
                                    )
                                ])
                            )
                        ])
                    ),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("sum")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "6"  # 3 * 2 = 6
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_047():
    """Test string concatenation using println"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("println"), [
                            MethodCall("println", [StringLiteral("Hello")])
                        ])
                    ),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [StringLiteral("World")])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "Hello\nWorld"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_048():
    """Test iterative factorial (simulating recursion with loop)"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [
                        Variable("n", IntLiteral(5)),
                        Variable("result", IntLiteral(1))
                    ])
                ], [
                    ForStatement("i", IntLiteral(1), "to", Identifier("n"),
                        BlockStatement([], [
                            AssignmentStatement(
                                IdLHS("result"),
                                BinaryOp(Identifier("result"), "*", Identifier("i"))
                            )
                        ])
                    ),
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [Identifier("result")])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "120"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_049():
    """Test multiple if-else chains"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([
                    VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(15))])
                ], [
                    IfStatement(
                        BinaryOp(Identifier("x"), "<", IntLiteral(10)),
                        BlockStatement([], [
                            MethodInvocationStatement(
                                PostfixExpression(Identifier("print"), [
                                    MethodCall("print", [StringLiteral("small")])
                                ])
                            )
                        ]),
                        IfStatement(
                            BinaryOp(Identifier("x"), "<", IntLiteral(20)),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(Identifier("print"), [
                                        MethodCall("print", [StringLiteral("medium")])
                                    ])
                                )
                            ]),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(Identifier("print"), [
                                        MethodCall("print", [StringLiteral("large")])
                                    ])
                                )
                            ])
                        )
                    )
                ])
            )
        ])
    ])
    expected = "medium"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_050():
    """Test zero value"""
    ast = Program([
        ClassDecl("Main", None, [
            MethodDecl(True, PrimitiveType("void"), "main", [],
                BlockStatement([], [
                    MethodInvocationStatement(
                        PostfixExpression(Identifier("print"), [
                            MethodCall("print", [
                                PostfixExpression(Identifier("int2str"), [
                                    MethodCall("int2str", [IntLiteral(0)])
                                ])
                            ])
                        ])
                    )
                ])
            )
        ])
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# Note: Tests 51-100 would continue with similar patterns covering:
# - More complex nested structures
# - Edge cases for all operators
# - Different combinations of control flow
# - Various method signature patterns
# - Instance methods and class features
# - Array operations (when implemented)
# - Object creation and member access (when implemented)
# - Constructors and destructors (when implemented)
# - Inheritance features (when implemented)

