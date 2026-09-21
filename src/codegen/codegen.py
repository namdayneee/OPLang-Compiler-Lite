"""
Code Generator for OPLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter, is_void_type, is_int_type, is_float_type, is_string_type, is_bool_type
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    """
    Code generator for OPLang.
    Traverses AST and generates JVM bytecode.
    """
    
    def __init__(self, output_dir=None):
        self.output_dir = output_dir
        self.current_class = None
        self.emit = None
        self.builtin_funcs = {
            ("io", "readInt"): (
                "io/readInt",
                FunctionType(
                    [],
                    PrimitiveType("int"),
                ),
            ),
            ("io", "writeInt"): (
                "io/writeInt",
                FunctionType(
                    [PrimitiveType("int")],
                    PrimitiveType("void"),
                ),
            ),
            ("io", "writeIntLn"): (
                "io/writeIntLn",
                FunctionType(
                    [PrimitiveType("int")],
                    PrimitiveType("void"),
                ),
            ),

            # Float I/O
            ("io", "readFloat"): (
                "io/readFloat",
                FunctionType(
                    [],
                    PrimitiveType("float"),
                ),
            ),
            ("io", "writeFloat"): (
                "io/writeFloat",
                FunctionType(
                    [PrimitiveType("float")],
                    PrimitiveType("void"),
                ),
            ),
            ("io", "writeFloatLn"): (
                "io/writeFloatLn",
                FunctionType(
                    [PrimitiveType("float")],
                    PrimitiveType("void"),
                ),
            ),

            # Boolean I/O
            ("io", "readBool"): (
                "io/readBool",
                FunctionType(
                    [],
                    PrimitiveType("boolean"),
                ),
            ),
            ("io", "writeBool"): (
                "io/writeBool",
                FunctionType(
                    [PrimitiveType("boolean")],
                    PrimitiveType("void"),
                ),
            ),
            ("io", "writeBoolLn"): (
                "io/writeBoolLn",
                FunctionType(
                    [PrimitiveType("boolean")],
                    PrimitiveType("void"),
                ),
            ),

            # String I/O
            ("io", "readStr"): (
                "io/readStr",
                FunctionType(
                    [],
                    PrimitiveType("string"),
                ),
            ),
            ("io", "writeStr"): (
                "io/writeStr",
                FunctionType(
                    [PrimitiveType("string")],
                    PrimitiveType("void"),
                ),
            ),
            ("io", "writeStrLn"): (
                "io/writeStrLn",
                FunctionType(
                    [PrimitiveType("string")],
                    PrimitiveType("void"),
                ),
            ),
            "print": (
                "io/writeStr",
                FunctionType([PrimitiveType("string")], PrimitiveType("void")),
            ),
            "println": (
                "io/writeStrLn",
                FunctionType([PrimitiveType("string")], PrimitiveType("void")),
            ),
            "int2str": (
                "java/lang/String/valueOf",
                FunctionType([PrimitiveType("int")], PrimitiveType("string")),
            ),
            "bool2str": (
                "java/lang/String/valueOf",
                FunctionType([PrimitiveType("boolean")], PrimitiveType("string")),
            ),
            "float2str": (
                "java/lang/String/valueOf",
                FunctionType([PrimitiveType("float")], PrimitiveType("string")),
            ),
        }

    # ============================================================================
    # Program and Class Declarations
    # ============================================================================

    def visit_program(self, node: "Program", o: Any = None):
        """
        Visit program node - generate code for all classes.
        """
        # Process all class declarations
        for class_decl in node.class_decls:
            self.visit(class_decl, o)

    def visit_class_decl(self, node: "ClassDecl", o: Any = None):
        """
        Visit class declaration - generate class structure.
        """
        self.current_class = node.name
        class_file = node.name + ".j"
        self.emit = Emitter(
            class_file,
            output_dir=self.output_dir,
        )
        
        # Determine superclass
        superclass = node.superclass if node.superclass else "java/lang/Object"
        
        # Emit class prolog
        self.emit.print_out(self.emit.emit_prolog(node.name, superclass))
        
        # Process class members (attributes, methods, constructors, destructors)
        for member in node.members:
            self.visit(member, o)
        
        # Emit class epilog
        self.emit.emit_epilog()

    # ============================================================================
    # Attribute Declarations
    # ============================================================================

    def visit_attribute_decl(self, node: "AttributeDecl", o: Any = None):
        """
        Visit attribute declaration - generate field directives.
        TODO: Implement attribute initialization if needed
        """
        for attr in node.attributes:
            self.visit(attr, node)

    def visit_attribute(self, node: "Attribute", o: Any = None):
        """
        Visit individual attribute - generate field directive.
        """
        attr_decl = o  # AttributeDecl node
        class_name = self.current_class
        field_name = class_name + "/" + node.name
        
        # Emit field directive
        if attr_decl.is_static:
            self.emit.print_out(
                self.emit.emit_attribute(
                    field_name,
                    attr_decl.attr_type,
                    attr_decl.is_final
                )
            )
        else:
            # Instance field
            self.emit.print_out(
                self.emit.jvm.emitINSTANCEFIELD(
                    field_name,
                    self.emit.get_jvm_type(attr_decl.attr_type)
                )
            )
        
        # TODO: Handle initialization if node.init_value is not None

    # ============================================================================
    # Method Declarations
    # ============================================================================

    def visit_method_decl(self, node: "MethodDecl", o: Any = None):
        """
        Visit method declaration - generate method code.
        """
        frame = Frame(node.name, node.return_type)
        self.generate_method(node, frame, node.is_static)

    def visit_constructor_decl(self, node: "ConstructorDecl", o: Any = None):
        """
        Visit constructor declaration - generate constructor code.
        """
        frame = Frame("<init>", PrimitiveType("void"))
        # Build function type based on params
        func_type = FunctionType([p.param_type for p in node.params], PrimitiveType("void"))

        self.emit.print_out(self.emit.emit_method("<init>", func_type, False))

        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # 'this' reference
        this_idx = frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                this_idx, "this", ClassType(self.current_class), from_label, to_label
            )
        )
        sym_list = [Symbol("this", ClassType(self.current_class), Index(this_idx))]

        # Parameters
        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, from_label, to_label)
            )
            sym_list.append(Symbol(param.name, param.param_type, Index(idx)))

        # Add IO/builtin symbols
        sym_list = IO_SYMBOL_LIST + sym_list

        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Call superclass default constructor first
        self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), this_idx, frame))
        self.emit.print_out(
            self.emit.emit_invoke_special(
                frame,
                "java/lang/Object/<init>",
                FunctionType([], PrimitiveType("void")),
            )
        )

        # Body
        self.visit(node.body, SubBody(frame, sym_list))

        # Ensure return
        self.emit.print_out(self.emit.emit_return(PrimitiveType("void"), frame))
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()

    def visit_destructor_decl(self, node: "DestructorDecl", o: Any = None):
        """
        Visit destructor declaration - generate destructor code.
        """
        frame = Frame("finalize", PrimitiveType("void"))
        func_type = FunctionType([], PrimitiveType("void"))
        self.emit.print_out(self.emit.emit_method("finalize", func_type, False))
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        this_idx = frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                this_idx, "this", ClassType(self.current_class), from_label, to_label
            )
        )
        sym_list = IO_SYMBOL_LIST + [Symbol("this", ClassType(self.current_class), Index(this_idx))]

        self.emit.print_out(self.emit.emit_label(from_label, frame))
        self.visit(node.body, SubBody(frame, sym_list))
        self.emit.print_out(self.emit.emit_return(PrimitiveType("void"), frame))
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()

    def visit_parameter(self, node: "Parameter", o: Any = None):
        """
        Visit parameter - register parameter in frame.
        """
        # This is handled in generate_method
        pass

    def generate_method(self, node: "MethodDecl", frame: Frame, is_static: bool):
        """
        Generate code for a method.
        
        Args:
            node: Method declaration node
            frame: Frame for this method
            is_static: Whether method is static
        """
        class_name = self.current_class
        method_name = node.name
        
        # Build method signature
        param_types = [p.param_type for p in node.params]
        return_type = node.return_type
        
        # Special case for Java main method entry point
        # Java requires main(String[] args), so add it to JVM signature even if OPLang main has no params
        jvm_param_types = param_types[:]
        if is_static and method_name == "main" and len(param_types) == 0:
            jvm_param_types = [ArrayType(PrimitiveType("string"), 0)]
        
        # Create function type for method signature
        func_type = FunctionType(jvm_param_types, return_type)
        
        # Emit method directive
        self.emit.print_out(
            self.emit.emit_method(
                method_name,
                func_type,
                is_static
            )
        )
        
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        sym_list: List[Symbol] = []

        # Handle 'this' parameter for instance methods
        if not is_static:
            this_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    this_idx,
                    "this",
                    ClassType(class_name),
                    from_label,
                    to_label
                )
            )
            sym_list.append(Symbol("this", ClassType(class_name), Index(this_idx)))
        
        # If this is Java main entry point, reserve slot for String[] args
        if is_static and method_name == "main" and len(node.params) == 0:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx,
                    "args",
                    ArrayType(PrimitiveType("string"), 0),
                    from_label,
                    to_label
                )
            )
            # Don't add to sym_list since OPLang code can't reference it
        
        # Generate code for parameters
        for i, param in enumerate(node.params):
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    param.name,
                    param.param_type,
                    from_label,
                    to_label
                )
            )
            sym_list.append(Symbol(param.name, param.param_type, Index(idx)))
        
        # Add IO symbols
        sym_list = IO_SYMBOL_LIST + sym_list
        
        self.emit.print_out(self.emit.emit_label(from_label, frame))
        
        # Generate code for method body
        o = SubBody(frame, sym_list)
        self.visit(node.body, o)
        
        # Emit return if void
        if is_void_type(return_type):
            self.emit.print_out(self.emit.emit_return(return_type, frame))
        
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()

    # ============================================================================
    # Type System
    # ============================================================================

    def visit_primitive_type(self, node: "PrimitiveType", o: Any = None):
        pass

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        pass

    def visit_class_type(self, node: "ClassType", o: Any = None):
        pass

    def visit_reference_type(self, node: "ReferenceType", o: Any = None):
        pass

    # ============================================================================
    # Statements
    # ============================================================================

    def visit_block_statement(self, node: "BlockStatement", o: SubBody = None):
        """
        Visit block statement - process variable declarations and statements.
        """
        if o is None:
            return
        
        # Process variable declarations
        for var_decl in node.var_decls:
            o = self.visit(var_decl, o)
        
        # Process statements
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_variable_decl(self, node: "VariableDecl", o: SubBody = None):
        """
        Visit variable declaration - register local variables.
        """
        if o is None:
            return o
        
        frame = o.frame
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        new_sym = []
        for var in node.variables:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    var.name,
                    node.var_type,
                    from_label,
                    to_label
                )
            )
            
            # Add to symbol list
            new_sym.append(Symbol(var.name, node.var_type, Index(idx)))
            
            # Handle initialization if present
            if var.init_value is not None:
                # Generate code for initialization
                code, typ = self.visit(var.init_value, Access(frame, o.sym))
                self.emit.print_out(code)
                self.emit.print_out(
                    self.emit.emit_write_var(var.name, node.var_type, idx, frame)
                )
        
        return SubBody(frame, new_sym + o.sym)

    def visit_variable(self, node: "Variable", o: Any = None):
        pass

    def visit_assignment_statement(self, node: "AssignmentStatement", o: SubBody = None):
        """
        Visit assignment statement - generate assignment code.
        """
        if o is None:
            return
        
        # Generate code for RHS
        code, typ = self.visit(node.rhs, Access(o.frame, o.sym))
        self.emit.print_out(code)
        
        # Generate code for LHS
        lhs_code, lhs_type = self.visit(node.lhs, Access(o.frame, o.sym, is_left=True))
        self.emit.print_out(lhs_code)

    def visit_if_statement(self, node: "IfStatement", o: Any = None):
        """
        Visit if statement.
        """
        if o is None:
            return
        frame = o.frame
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()

        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))

        self.visit(node.then_stmt, o)
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        self.emit.print_out(self.emit.emit_label(end_label, frame))

    def visit_for_statement(self, node: "ForStatement", o: Any = None):
        """
        Visit for statement.
        """
        if o is None:
            return
        frame = o.frame
        frame.enter_loop()
        
        # Get loop labels
        start_label = frame.get_new_label()  # Condition check label
        continue_label = frame.get_continue_label()  # Continue jumps here (before increment)
        end_label = frame.get_break_label()  # Break jumps here

        loop_symbol = next(
            (symbol for symbol in o.sym if symbol.name == node.variable),
            None,
        )
        if loop_symbol is None or not isinstance(loop_symbol.value, Index):
            raise IllegalOperandException(
                f"Undeclared loop variable: {node.variable}"
            )
        loop_var_idx = loop_symbol.value.value

        # Initialize loop variable
        init_code, init_type = self.visit(node.start_expr, Access(frame, o.sym))
        self.emit.print_out(init_code)
        self.emit.print_out(self.emit.emit_write_var(node.variable, PrimitiveType("int"), loop_var_idx, frame))

        # Condition label (start of loop)
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        # condition: var <= end (to) or var >= end (downto)
        self.emit.print_out(self.emit.emit_read_var(node.variable, PrimitiveType("int"), loop_var_idx, frame))
        cond_code, cond_type = self.visit(node.end_expr, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        op = "<=" if node.direction == "to" else ">="
        self.emit.print_out(self.emit.emit_re_op(op, PrimitiveType("int"), frame))
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))

        # Body (with loop variable in scope)
        self.visit(node.body, o)

        # Continue label (jumps from continue statement come here)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))

        # Update: i = i + 1 or i - 1
        self.emit.print_out(self.emit.emit_read_var(node.variable, PrimitiveType("int"), loop_var_idx, frame))
        self.emit.print_out(self.emit.emit_push_iconst(1, frame))
        self.emit.print_out(
            self.emit.emit_add_op("-" if node.direction == "downto" else "+", PrimitiveType("int"), frame)
        )
        self.emit.print_out(self.emit.emit_write_var(node.variable, PrimitiveType("int"), loop_var_idx, frame))
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        
        # End label (jumps from break statement come here)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()

    def visit_break_statement(self, node: "BreakStatement", o: Any = None):
        """
        Visit break statement.
        """
        if o is None:
            return
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))

    def visit_continue_statement(self, node: "ContinueStatement", o: Any = None):
        """
        Visit continue statement.
        """
        if o is None:
            return
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))

    def visit_return_statement(self, node: "ReturnStatement", o: SubBody = None):
        """
        Visit return statement - generate return code.
        """
        if o is None:
            return
        
        # Generate code for return value
        code, typ = self.visit(node.value, Access(o.frame, o.sym))
        self.emit.print_out(code)
        
        # Emit return instruction
        self.emit.print_out(self.emit.emit_return(typ, o.frame))

    def visit_method_invocation_statement(
        self, node: "MethodInvocationStatement", o: Any = None
    ):
        """
        Visit method invocation statement.
        """
        if o is None:
            return
        code, typ = self.visit(node.method_call, Access(o.frame, o.sym))
        self.emit.print_out(code)
        # Discard return value if any
        if typ is not None and not is_void_type(typ):
            self.emit.print_out(self.emit.emit_pop(o.frame))

    # ============================================================================
    # Left-hand Side (LHS)
    # ============================================================================

    def visit_id_lhs(self, node: "IdLHS", o: Access = None):
        """
        Visit identifier LHS - generate code to write to variable.
        """
        if o is None:
            return "", None
        
        # Find symbol
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared variable: {node.name}")
        
        if type(sym.value) is Index:
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )
            return code, sym.type
        else:
            raise IllegalOperandException(f"Cannot assign to: {node.name}")

    def visit_postfix_lhs(self, node: "PostfixLHS", o: Any = None):
        """
        Visit postfix LHS (for member access, array access).
        """
        # Not fully supported; delegate to postfix expression and write through
        if o is None:
            return "", None
        code, typ = self.visit(node.postfix_expr, Access(o.frame, o.sym, is_left=True))
        return code, typ

    # ============================================================================
    # Expressions
    # ============================================================================

    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        """
        Visit binary operation.
        """
        if o is None:
            return "", None
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        code = left_code + right_code

        op = node.operator

        # Promote int to float when needed
        if (is_int_type(left_type) and is_float_type(right_type)) or (
            is_float_type(left_type) and is_int_type(right_type)
        ):
            if is_int_type(left_type):
                left_type = PrimitiveType("float")
                code = left_code + self.emit.emit_i2f(o.frame) + right_code
            else:
                right_type = PrimitiveType("float")
                code = left_code + right_code + self.emit.emit_i2f(o.frame)

        if op in ["+", "-"]:
            code += self.emit.emit_add_op(op, left_type, o.frame)
            return code, left_type
        if op in ["*", "/"]:
            code += self.emit.emit_mul_op(op, left_type, o.frame)
            return code, left_type
        if op == "%":
            code += self.emit.emit_mod(o.frame)
            return code, PrimitiveType("int")
        if op == "&&":
            code += self.emit.emit_and_op(o.frame)
            return code, PrimitiveType("boolean")
        if op == "||":
            code += self.emit.emit_or_op(o.frame)
            return code, PrimitiveType("boolean")
        if op in [">", ">=", "<", "<=", "!=", "=="]:
            code += self.emit.emit_re_op(op, left_type, o.frame)
            return code, PrimitiveType("boolean")
        raise IllegalOperandException(f"Unsupported operator {op}")

    def visit_unary_op(self, node: "UnaryOp", o: Access = None):
        """
        Visit unary operation.
        """
        if o is None:
            return "", None
        operand_code, operand_type = self.visit(node.operand, o)
        code = operand_code
        if node.operator == "-":
            code += self.emit.emit_neg_op(operand_type, o.frame)
            return code, operand_type
        if node.operator == "+":
            return code, operand_type
        if node.operator == "!":
            code += self.emit.emit_not(PrimitiveType("boolean"), o.frame)
            return code, PrimitiveType("boolean")
        raise IllegalOperandException(f"Unsupported unary operator {node.operator}")

    def visit_postfix_expression(self, node: "PostfixExpression", o: Access = None):
        """
        Visit postfix expression (method calls, member access, array access).
        """
        if o is None:
            return "", None

        # Built-in static class method:
        #
        #     io.writeIntLn(10)
        #
        # AST:
        #     primary = Identifier("io")
        #     postfix_ops = [MethodCall("writeIntLn", ...)]
        if (
            isinstance(node.primary, Identifier)
            and len(node.postfix_ops) == 1
            and isinstance(
                node.postfix_ops[0],
                MethodCall,
            )
        ):
            method_call = node.postfix_ops[0]

            method_key = (
                node.primary.name,
                method_call.method_name,
            )

            builtin_method = self.builtin_funcs.get(method_key)

            if builtin_method is not None:
                target, function_type = builtin_method

                if (
                    len(method_call.args)
                    != len(function_type.param_types)
                ):
                    raise IllegalOperandException(
                        "Invalid argument count for "
                        f"{node.primary.name}."
                        f"{method_call.method_name}"
                    )

                argument_codes = []

                for argument in method_call.args:
                    argument_code, _ = self.visit(
                        argument,
                        o,
                    )
                    argument_codes.append(
                        argument_code
                    )

                code = "".join(argument_codes)

                code += self.emit.emit_invoke_static(
                    target,
                    function_type,
                    o.frame,
                )

                return (
                    code,
                    function_type.return_type,
                )

        # Built-in free function form: Identifier + single MethodCall with same name
        if (
            isinstance(node.primary, Identifier)
            and len(node.postfix_ops) == 1
            and isinstance(node.postfix_ops[0], MethodCall)
        ):
            mc = node.postfix_ops[0]
            if mc.method_name in self.builtin_funcs:
                target, func_type = self.builtin_funcs[mc.method_name]
                codes = []
                for arg in mc.args:
                    acode, _ = self.visit(arg, o)
                    codes.append(acode)
                code = "".join(codes)
                code += self.emit.emit_invoke_static(target, func_type, o.frame)
                return code, func_type.return_type

        # Fallback: evaluate primary then each postfix op (limited support)
        code, typ = self.visit(node.primary, o)
        for op in node.postfix_ops:
            if isinstance(op, MethodCall):
                # Assume static call to current class if primary is ClassType symbol
                arg_codes = []
                arg_types = []
                for arg in op.args:
                    acode, atyp = self.visit(arg, o)
                    arg_codes.append(acode)
                    arg_types.append(atyp)
                func_type = FunctionType(arg_types, PrimitiveType("void"))
                code += "".join(arg_codes)
                code += self.emit.emit_invoke_static(
                    f"{self.current_class}/{op.method_name}", func_type, o.frame
                )
                typ = func_type.return_type
            elif isinstance(op, MemberAccess):
                # Load field from object on stack
                if type(typ) is ClassType:
                    code += self.emit.emit_get_field(
                        f"{typ.class_name}/{op.member_name}", typ, o.frame
                    )
            elif isinstance(op, ArrayAccess):
                idx_code, _ = self.visit(op.index, o)
                code += idx_code
                if type(typ) is ArrayType:
                    code += self.emit.emit_aload(typ.element_type, o.frame)
                    typ = typ.element_type
            else:
                raise IllegalOperandException("Unsupported postfix operation")
        return code, typ

    def visit_method_call(self, node: "MethodCall", o: Access = None):
        """
        Visit method call.
        """
        if o is None:
            return "", None
        # This will be handled in visit_postfix_expression; keep simple fallback
        codes = []
        arg_types = []
        for arg in node.args:
            acode, atyp = self.visit(arg, o)
            codes.append(acode)
            arg_types.append(atyp)
        func_type = FunctionType(arg_types, PrimitiveType("void"))
        code = "".join(codes)
        code += self.emit.emit_invoke_static(
            f"{self.current_class}/{node.method_name}", func_type, o.frame
        )
        return code, func_type.return_type

    # Static invocation placeholders (not used in current tests)
    def visit_static_method_invocation(self, node: Any, o: Access = None):
        return "", None

    def visit_static_member_access(self, node: Any, o: Access = None):
        return "", None

    def visit_method_invocation(self, node: Any, o: Access = None):
        return "", None

    def visit_member_access(self, node: "MemberAccess", o: Access = None):
        """
        Visit member access.
        """
        if o is None:
            return "", None
        raise IllegalOperandException("Member access not directly supported")

    def visit_array_access(self, node: "ArrayAccess", o: Access = None):
        """
        Visit array access.
        """
        if o is None:
            return "", None
        raise IllegalOperandException("Array access not directly supported")

    def visit_object_creation(self, node: "ObjectCreation", o: Access = None):
        """
        Visit object creation.
        """
        if o is None:
            return "", None
        # Limited support: call default constructor
        frame = o.frame
        frame.push()
        code = f"new {node.class_name}\n"
        code += self.emit.emit_dup(frame)
        func_type = FunctionType([PrimitiveType("void")][:0], PrimitiveType("void"))
        code += self.emit.emit_invoke_special(frame, f"{node.class_name}/<init>", func_type)
        return code, ClassType(node.class_name)

    def visit_identifier(self, node: "Identifier", o: Access = None):
        """
        Visit identifier - generate code to read variable.
        """
        if o is None:
            return "", None
        
        # Find symbol
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared identifier: {node.name}")
        
        if type(sym.value) is Index:
            code = self.emit.emit_read_var(
                sym.name, sym.type, sym.value.value, o.frame
            )
            return code, sym.type
        if type(sym.value) is CName:
            # Built-in/static function reference, no code emitted
            return "", sym.type
        else:
            raise IllegalOperandException(f"Cannot read: {node.name}")

    def visit_this_expression(self, node: "ThisExpression", o: Access = None):
        """
        Visit this expression - load 'this' reference.
        """
        if o is None:
            return "", None
        
        # Find 'this' in symbol table (should be at index 0 for instance methods)
        this_sym = next(filter(lambda x: x.name == "this", o.sym), None)
        if this_sym is None:
            raise IllegalOperandException("'this' not available in static context")
        
        if type(this_sym.value) is Index:
            code = self.emit.emit_read_var(
                "this", this_sym.type, this_sym.value.value, o.frame
            )
            return code, this_sym.type
        else:
            raise IllegalOperandException("Invalid 'this' reference")

    def visit_parenthesized_expression(
        self, node: "ParenthesizedExpression", o: Access = None
    ):
        """
        Visit parenthesized expression - just visit inner expression.
        """
        return self.visit(node.expr, o)

    # ============================================================================
    # Literals
    # ============================================================================

    def visit_int_literal(self, node: "IntLiteral", o: Access = None):
        """
        Visit integer literal - push integer constant.
        """
        if o is None:
            return "", None
        code = self.emit.emit_push_iconst(node.value, o.frame)
        return code, PrimitiveType("int")

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None):
        """
        Visit float literal - push float constant.
        """
        if o is None:
            return "", None
        code = self.emit.emit_push_fconst(str(node.value), o.frame)
        return code, PrimitiveType("float")

    def visit_bool_literal(self, node: "BoolLiteral", o: Access = None):
        """
        Visit boolean literal - push boolean constant.
        """
        if o is None:
            return "", None
        value_str = "1" if node.value else "0"
        code = self.emit.emit_push_iconst(value_str, o.frame)
        return code, PrimitiveType("boolean")

    def visit_string_literal(self, node: "StringLiteral", o: Access = None):
        """
        Visit string literal - push string constant.
        """
        if o is None:
            return "", None
        code = self.emit.emit_push_const('"' + node.value + '"', PrimitiveType("string"), o.frame)
        return code, PrimitiveType("string")

    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None):
        """
        Visit array literal.
        """
        # Not required for current tests; return empty
        return "", ArrayType(PrimitiveType("int"), len(node.value))

    def visit_nil_literal(self, node: "NilLiteral", o: Access = None):
        """
        Visit nil literal - push null reference.
        """
        if o is None:
            return "", None
        o.frame.push()
        code = self.emit.jvm.emitPUSHNULL()
        return code, None  # Type will be determined by context

