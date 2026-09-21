"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *

class ASTGeneration(OPLangVisitor):
    # program: classdecllist EOF;
    def visitProgram(self, ctx: OPLangParser.ProgramContext):
        return Program(self.visit(ctx.classdecllist()))

    # classdecllist: classdecl classdecllisttail;
    def visitClassdecllist(self, ctx: OPLangParser.ClassdecllistContext):
        return [self.visit(ctx.classdecl())] + self.visit(ctx.classdecllisttail())

    # classdecllisttail: classdecl classdecllisttail | ;
    def visitClassdecllisttail(self, ctx: OPLangParser.ClassdecllisttailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.classdecl())] + self.visit(ctx.classdecllisttail())

    # classdecl: CLASS ID extendsclause LCB memberdecllistopt RCB;
    def visitClassdecl(self, ctx: OPLangParser.ClassdeclContext):
        name = ctx.ID().getText()
        superclass = None
        if ctx.extendsclause() and ctx.extendsclause().ID():
            superclass = ctx.extendsclause().ID().getText()
        members = self.visit(ctx.memberdecllistopt()) or []
        flat_members = reduce(lambda acc, x: acc + (x if isinstance(x, list) else [x]) if x is not None else acc, members, [])
        return ClassDecl(name, superclass, flat_members)

    # extendsclause: EXTENDS ID | ;
    def visitExtendsclause(self, ctx: OPLangParser.ExtendsclauseContext):
        if ctx.getChildCount() == 0:
            return None
        return ctx.ID().getText()

    # memberdecl: attributedecl | methoddecl | constructordecl | destructordecl;
    def visitMemberdecl(self, ctx: OPLangParser.MemberdeclContext):
        if ctx.attributedecl():
            return self.visit(ctx.attributedecl())
        if ctx.methoddecl():
            return self.visit(ctx.methoddecl())
        if ctx.constructordecl():
            return self.visit(ctx.constructordecl())
        if ctx.destructordecl():
            return self.visit(ctx.destructordecl())
        return None

    # memberdecllistopt: memberdecllist | ;
    def visitMemberdecllistopt(self, ctx: OPLangParser.MemberdecllistoptContext):
        if ctx.memberdecllist():
            return self.visit(ctx.memberdecllist())
        return []

    # memberdecllist: memberdecl memberdecllisttail;
    def visitMemberdecllist(self, ctx: OPLangParser.MemberdecllistContext):
        return [self.visit(ctx.memberdecl())] + self.visit(ctx.memberdecllisttail())

    # memberdecllisttail: memberdecl memberdecllisttail | ;
    def visitMemberdecllisttail(self, ctx: OPLangParser.MemberdecllisttailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.memberdecl())] + self.visit(ctx.memberdecllisttail())

    # ---------------- attributes ----------------

    # attributedecl: attributemodsopt typ refmarkeropt attrlist SEMI;
    def visitAttributedecl(self, ctx: OPLangParser.AttributedeclContext):
        mods = self.visit(ctx.attributemodsopt()) or {}
        attr_type = self.visit(ctx.typ())
        if ctx.refmarkeropt() and ctx.refmarkeropt().getText():
            attr_type = ReferenceType(attr_type)
        attrs = self.visit(ctx.attrlist()) or []
        attr_objs = [Attribute(name, init) for (name, init) in attrs]
        return AttributeDecl(mods.get("static", False), mods.get("final", False), attr_type, attr_objs)

    # attributemodsopt: attributemods | ;
    def visitAttributemodsopt(self, ctx: OPLangParser.AttributemodsoptContext):
        if ctx.attributemods():
            return self.visit(ctx.attributemods())
        return {}

    # attributemods: STATIC finalopt | FINAL staticopt | STATIC | FINAL;
    def visitAttributemods(self, ctx: OPLangParser.AttributemodsContext):
        text = ctx.getText()
        result = {"static": False, "final": False}
        if "static" in text:
            result["static"] = True
        if "final" in text:
            result["final"] = True
        return result

    # refmarker: AMP;
    def visitRefmarker(self, ctx: OPLangParser.RefmarkerContext):
        return "&"

    # refmarkeropt: refmarker | ;
    def visitRefmarkeropt(self, ctx: OPLangParser.RefmarkeroptContext):
        if ctx.refmarker():
            return self.visit(ctx.refmarker())
        return None

    # attrlist: attrinit attrlisttail;
    def visitAttrlist(self, ctx: OPLangParser.AttrlistContext):
        return [self.visit(ctx.attrinit())] + self.visit(ctx.attrlisttail())

    # attrlisttail: COMMA attrinit attrlisttail | ;
    def visitAttrlisttail(self, ctx: OPLangParser.AttrlisttailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.attrinit())] + self.visit(ctx.attrlisttail())

    # attrinit: ID attrinitassignopt;
    def visitAttrinit(self, ctx: OPLangParser.AttrinitContext):
        name = ctx.ID().getText()
        init = None
        if ctx.attrinitassignopt() and ctx.attrinitassignopt().expr():
            init = self.visit(ctx.attrinitassignopt().expr())
        return (name, init)

    # attrinitassignopt: ASSIGN expr | ;
    def visitAttrinitassignopt(self, ctx: OPLangParser.AttrinitassignoptContext):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.expr())

    # ---------------- methods / constructors / destructors ----------------

    # methoddecl: staticopt returntyp ID LP paramlistopt RP blockstmt;
    def visitMethoddecl(self, ctx: OPLangParser.MethoddeclContext):
        is_static = bool(ctx.staticopt() and ctx.staticopt().getText())
        return_type = self.visit(ctx.returntyp())
        name = ctx.ID().getText()
        params_raw = self.visit(ctx.paramlistopt()) or []
        params = reduce(lambda acc, p: acc + (p if isinstance(p, list) else [p]), params_raw, []) if params_raw else []
        body = self.visit(ctx.blockstmt())
        return MethodDecl(is_static, return_type, name, params, body)

    # staticopt: STATIC | ;
    def visitStaticopt(self, ctx: OPLangParser.StaticoptContext):
        return True if ctx.getChildCount() > 0 else False

    # returntyp: VOID | typ refmarkeropt;
    def visitReturntyp(self, ctx: OPLangParser.ReturntypContext):
        if ctx.VOID():
            return PrimitiveType("void")
        base_type = self.visit(ctx.typ())
        if ctx.refmarkeropt() and ctx.refmarkeropt().getText():
            return ReferenceType(base_type)
        return base_type

    # constructordecl: ID LP paramlistopt RP blockstmt;
    def visitConstructordecl(self, ctx: OPLangParser.ConstructordeclContext):
        name = ctx.ID().getText()
        params_raw = self.visit(ctx.paramlistopt()) or []
        params = reduce(lambda acc, p: acc + (p if isinstance(p, list) else [p]), params_raw, []) if params_raw else []
        body = self.visit(ctx.blockstmt())
        return ConstructorDecl(name, params, body)

    # destructordecl: TILDE ID LP RP blockstmt;
    def visitDestructordecl(self, ctx: OPLangParser.DestructordeclContext):
        return DestructorDecl(ctx.ID().getText(), self.visit(ctx.blockstmt()))

    # paramlistopt: paramlist | ;
    def visitParamlistopt(self, ctx: OPLangParser.ParamlistoptContext):
        if ctx.paramlist():
            return self.visit(ctx.paramlist())
        return []

    # paramlist: paramdecl paramlisttail;
    def visitParamlist(self, ctx: OPLangParser.ParamlistContext):
        return [self.visit(ctx.paramdecl())] + self.visit(ctx.paramlisttail())

    # paramlisttail: SEMI paramdecl paramlisttail | ;
    def visitParamlisttail(self, ctx: OPLangParser.ParamlisttailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.paramdecl())] + self.visit(ctx.paramlisttail())

    # paramdecl: typ refmarkeropt idlist;
    def visitParamdecl(self, ctx: OPLangParser.ParamdeclContext):
        typ = self.visit(ctx.typ())
        if ctx.refmarkeropt() and ctx.refmarkeropt().getText():
            typ = ReferenceType(typ)
        id_names = self.visit(ctx.idlist())  # list of names
        params = [Parameter(typ, name) for name in id_names]
        if len(params) == 1:
            return params[0]
        return params

    # idlist: ID idlisttail;
    def visitIdlist(self, ctx: OPLangParser.IdlistContext):
        return [ctx.ID().getText()] + self.visit(ctx.idlisttail())

    # idlisttail: COMMA ID idlisttail | ;
    def visitIdlisttail(self, ctx: OPLangParser.IdlisttailContext):
        if ctx.getChildCount() == 0:
            return []
        return [ctx.ID().getText()] + self.visit(ctx.idlisttail())

    # ---------------- block / local vars / statements ----------------

    # blockstmt: LCB localvardecllistopt stmtlistopt RCB;
    def visitBlockstmt(self, ctx: OPLangParser.BlockstmtContext):
        var_decls_raw = self.visit(ctx.localvardecllistopt()) or []
        
        var_decls = []
        for x in var_decls_raw:
            if x is None:
                continue
            if isinstance(x, list):
                var_decls.extend(x)
            else:
                var_decls.append(x)
        stmts_raw = self.visit(ctx.stmtlistopt()) or []

        stmts = []
        for x in stmts_raw:
            if x is None:
                continue
            if isinstance(x, list):
                stmts.extend(x)
            else:
                stmts.append(x)
        return BlockStatement(var_decls, stmts)

    # localvardecllistopt: localvardecllist | ;
    def visitLocalvardecllistopt(self, ctx: OPLangParser.LocalvardecllistoptContext):
        if ctx.localvardecllist():
            return self.visit(ctx.localvardecllist())
        return []

    # localvardecllist: localvardecl localvardecllist | ;
    def visitLocalvardecllist(self, ctx: OPLangParser.LocalvardecllistContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.localvardecl())] + self.visit(ctx.localvardecllist())

    # stmtlistopt: stmtlist | ;
    def visitStmtlistopt(self, ctx: OPLangParser.StmtlistoptContext):
        if ctx.stmtlist():
            return self.visit(ctx.stmtlist())
        return []

    # stmtlist: stmt stmtlist | ;
    def visitStmtlist(self, ctx: OPLangParser.StmtlistContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.stmt())] + self.visit(ctx.stmtlist())

    # localvardecl: finalopt typ refmarkeropt localvarlist SEMI;
    def visitLocalvardecl(self, ctx: OPLangParser.LocalvardeclContext):
        is_final = bool(ctx.finalopt() and ctx.finalopt().getText())
        typ = self.visit(ctx.typ())
        if ctx.refmarkeropt() and ctx.refmarkeropt().getText():
            typ = ReferenceType(typ)
        vars_list = self.visit(ctx.localvarlist()) or []
        variables = [Variable(name, init) for (name, init) in vars_list]
        return VariableDecl(is_final, typ, variables)

    # finalopt: FINAL | ;
    def visitFinalopt(self, ctx: OPLangParser.FinaloptContext):
        return True if ctx.getChildCount() > 0 else False

    # localvarlist: localvarinit localvarlisttail;
    def visitLocalvarlist(self, ctx: OPLangParser.LocalvarlistContext):
        return [self.visit(ctx.localvarinit())] + self.visit(ctx.localvarlisttail())

    # localvarlisttail: COMMA localvarinit localvarlisttail | ;
    def visitLocalvarlisttail(self, ctx: OPLangParser.LocalvarlisttailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.localvarinit())] + self.visit(ctx.localvarlisttail())

    # localvarinit: ID localvarinitassignopt;
    def visitLocalvarinit(self, ctx: OPLangParser.LocalvarinitContext):
        name = ctx.ID().getText()
        init = None
        if ctx.localvarinitassignopt() and ctx.localvarinitassignopt().expr():
            init = self.visit(ctx.localvarinitassignopt().expr())
        return (name, init)

    # localvarinitassignopt: ASSIGN expr | ;
    def visitLocalvarinitassignopt(self, ctx: OPLangParser.LocalvarinitassignoptContext):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.expr())

    # stmt: blockstmt | assignstmt | ifstmt | forstmt | breakstmt | continuestmt | returnstmt | callstmt;
    def visitStmt(self, ctx: OPLangParser.StmtContext):
        if ctx.blockstmt():
            return self.visit(ctx.blockstmt())
        if ctx.assignstmt():
            return self.visit(ctx.assignstmt())
        if ctx.ifstmt():
            return self.visit(ctx.ifstmt())
        if ctx.forstmt():
            return self.visit(ctx.forstmt())
        if ctx.breakstmt():
            return self.visit(ctx.breakstmt())
        if ctx.continuestmt():
            return self.visit(ctx.continuestmt())
        if ctx.returnstmt():
            return self.visit(ctx.returnstmt())
        if ctx.callstmt():
            return self.visit(ctx.callstmt())
        return None

    # assignstmt: lhs ASSIGN expr SEMI;
    def visitAssignstmt(self, ctx: OPLangParser.AssignstmtContext):
        return AssignmentStatement(self.visit(ctx.lhs()), self.visit(ctx.expr()))

    # lhs: ID lhssuffix | THIS lhssuffixthis | LP expr RP lhssuffix | arrayliteral lhssuffix | newexpr lhssuffix | literal lhssuffix | NIL lhssuffix;
    def visitLhs(self, ctx: OPLangParser.LhsContext):
        if ctx.ID():
            base = Identifier(ctx.ID().getText())
            suffix = self.visit(ctx.lhssuffix())
            if suffix:
                ops_list = suffix if isinstance(suffix, list) else [suffix]
                postfix_ops = []
                for item in ops_list:
                    if isinstance(item, list):
                        postfix_ops.extend(item)
                    else:
                        postfix_ops.append(item)
                while any(isinstance(x, list) for x in postfix_ops):
                    tmp = []
                    for x in postfix_ops:
                        if isinstance(x, list):
                            tmp.extend(x)
                        else:
                            tmp.append(x)
                    postfix_ops = tmp
                return PostfixLHS(PostfixExpression(base, postfix_ops))
            return IdLHS(ctx.ID().getText())
        if ctx.THIS():
            base = ThisExpression()
            suffix = self.visit(ctx.lhssuffixthis())
            if suffix:
                if isinstance(suffix, list):
                    flat = []
                    for item in suffix:
                        if isinstance(item, list):
                            flat.extend(item)
                        else:
                            flat.append(item)
                    return PostfixLHS(PostfixExpression(base, flat))
                else:
                    return PostfixLHS(PostfixExpression(base, [suffix]))
            return PostfixLHS(PostfixExpression(base, []))
        if ctx.arrayliteral():
            base = self.visit(ctx.arrayliteral())
            suffix = self.visit(ctx.lhssuffix())
            if suffix:
                ops_list = suffix if isinstance(suffix, list) else [suffix]
                postfix_ops = []
                for item in ops_list:
                    if isinstance(item, list):
                        postfix_ops.extend(item)
                    else:
                        postfix_ops.append(item)
                while any(isinstance(x, list) for x in postfix_ops):
                    tmp = []
                    for x in postfix_ops:
                        if isinstance(x, list):
                            tmp.extend(x)
                        else:
                            tmp.append(x)
                    postfix_ops = tmp
                return PostfixLHS(PostfixExpression(base, postfix_ops))
            return PostfixLHS(PostfixExpression(base, []))
        if ctx.newexpr():
            base = self.visit(ctx.newexpr())
            suffix = self.visit(ctx.lhssuffix())
            if suffix:
                ops_list = suffix if isinstance(suffix, list) else [suffix]
                postfix_ops = []
                for item in ops_list:
                    if isinstance(item, list):
                        postfix_ops.extend(item)
                    else:
                        postfix_ops.append(item)
                while any(isinstance(x, list) for x in postfix_ops):
                    tmp = []
                    for x in postfix_ops:
                        if isinstance(x, list):
                            tmp.extend(x)
                        else:
                            tmp.append(x)
                    postfix_ops = tmp
                return PostfixLHS(PostfixExpression(base, postfix_ops))
            return PostfixLHS(PostfixExpression(base, []))
        if ctx.literal():
            base = self.visit(ctx.literal())
            suffix = self.visit(ctx.lhssuffix())
            if suffix:
                ops_list = suffix if isinstance(suffix, list) else [suffix]
                postfix_ops = []
                for item in ops_list:
                    if isinstance(item, list):
                        postfix_ops.extend(item)
                    else:
                        postfix_ops.append(item)
                while any(isinstance(x, list) for x in postfix_ops):
                    tmp = []
                    for x in postfix_ops:
                        if isinstance(x, list):
                            tmp.extend(x)
                        else:
                            tmp.append(x)
                    postfix_ops = tmp
                return PostfixLHS(PostfixExpression(base, postfix_ops))
            return PostfixLHS(PostfixExpression(base, []))
        if ctx.NIL():
            base = NilLiteral()
            suffix = self.visit(ctx.lhssuffix())
            if suffix:
                ops_list = suffix if isinstance(suffix, list) else [suffix]
                postfix_ops = []
                for item in ops_list:
                    if isinstance(item, list):
                        postfix_ops.extend(item)
                    else:
                        postfix_ops.append(item)
                while any(isinstance(x, list) for x in postfix_ops):
                    tmp = []
                    for x in postfix_ops:
                        if isinstance(x, list):
                            tmp.extend(x)
                        else:
                            tmp.append(x)
                    postfix_ops = tmp
                return PostfixLHS(PostfixExpression(base, postfix_ops))
            return PostfixLHS(PostfixExpression(base, []))
        if ctx.getChildCount() >= 4:
            base = self.visit(ctx.expr())
            suffix = self.visit(ctx.lhssuffix())
            if suffix:
                ops_list = suffix if isinstance(suffix, list) else [suffix]
                postfix_ops = []
                for item in ops_list:
                    if isinstance(item, list):
                        postfix_ops.extend(item)
                    else:
                        postfix_ops.append(item)
                while any(isinstance(x, list) for x in postfix_ops):
                    tmp = []
                    for x in postfix_ops:
                        if isinstance(x, list):
                            tmp.extend(x)
                        else:
                            tmp.append(x)
                    postfix_ops = tmp
                ops = postfix_ops[0] if len(postfix_ops) == 1 else postfix_ops
                return PostfixLHS(PostfixExpression(base, ops))
            return PostfixLHS(PostfixExpression(base, []))
        return None

    # lhssuffixopt: lhssuffix | ;
    def visitLhssuffixopt(self, ctx: OPLangParser.LhssuffixoptContext):
        if ctx.lhssuffix():
            return self.visit(ctx.lhssuffix())
        return []

    # lhssuffix: lhsdotseqnoendinvoke lhsindexseqopt | lhsindexseq | ;
    def visitLhssuffix(self, ctx: OPLangParser.LhssuffixContext):
        if ctx.getChildCount() == 0:
            return []
        if ctx.lhsdotseqnoendinvoke():
            seq = self.visit(ctx.lhsdotseqnoendinvoke()) or []
            idxs = self.visit(ctx.lhsindexseqopt()) or []
            combined = seq + idxs
            flat = []
            for item in (combined if isinstance(combined, list) else [combined]):
                if isinstance(item, list):
                    flat.extend(item)
                else:
                    flat.append(item)
            while any(isinstance(x, list) for x in flat):
                tmp = []
                for x in flat:
                    if isinstance(x, list):
                        tmp.extend(x)
                    else:
                        tmp.append(x)
                flat = tmp
            return flat
        if ctx.lhsindexseq():
            return self.visit(ctx.lhsindexseq())
        return []

    # lhssuffixthis: lhsdotseqnoendinvoke lhsindexseqopt;
    def visitLhssuffixthis(self, ctx: OPLangParser.LhssuffixthisContext):
        seq = self.visit(ctx.lhsdotseqnoendinvoke()) or []
        idxs = self.visit(ctx.lhsindexseqopt()) or []
        combined = seq + idxs
        flat = []
        for item in (combined if isinstance(combined, list) else [combined]):
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)
        while any(isinstance(x, list) for x in flat):
            tmp = []
            for x in flat:
                if isinstance(x, list):
                    tmp.extend(x)
                else:
                    tmp.append(x)
            flat = tmp
        return flat

    # lhsdotseq: lhsdotop lhsdotseq | ;
    def visitLhsdotseq(self, ctx: OPLangParser.LhsdotseqContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.lhsdotop())] + self.visit(ctx.lhsdotseq())

    # lhsdotseqnoendinvoke: memberaccess lhsdotseqtail | memberinvoke memberaccess lhsdotseqtail;
    def visitLhsdotseqnoendinvoke(self, ctx: OPLangParser.LhsdotseqnoendinvokeContext):
        res = []
        if ctx.memberinvoke() and ctx.memberaccess():
            res.append(self.visit(ctx.memberinvoke()))
            res.append(self.visit(ctx.memberaccess()))
            tail = self.visit(ctx.lhsdotseqtail()) or []
            res.extend(tail)
            return res
        if ctx.memberaccess():
            res.append(self.visit(ctx.memberaccess()))
            tail = self.visit(ctx.lhsdotseqtail()) or []
            res.extend(tail)
            return res
        return []

    # lhsdotseqtail: lhsdotop lhsdotseqtail | ;
    def visitLhsdotseqtail(self, ctx: OPLangParser.LhsdotseqtailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.lhsdotop())] + self.visit(ctx.lhsdotseqtail())

    # lhsdotop: memberaccess | memberinvoke;
    def visitLhsdotop(self, ctx: OPLangParser.LhsdotopContext):
        if ctx.memberaccess():
            return self.visit(ctx.memberaccess())
        if ctx.memberinvoke():
            return self.visit(ctx.memberinvoke())
        return None

    # lhsindexseq: indexop lhsindexseq | ;
    def visitLhsindexseq(self, ctx: OPLangParser.LhsindexseqContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.indexop())] + self.visit(ctx.lhsindexseq())

    # lhsindexseqopt: indexop lhsindexseq | ;
    def visitLhsindexseqopt(self, ctx: OPLangParser.LhsindexseqoptContext):
        if ctx.getChildCount() == 0:
            return []
        # Grammar: lhsindexseqopt: indexop lhsindexseq | ;
        # Must include the first indexop, then the rest
        return [self.visit(ctx.indexop())] + self.visit(ctx.lhsindexseq())

    # lhsbase: ID | THIS | LP expr RP;
    def visitLhsbase(self, ctx: OPLangParser.LhsbaseContext):
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        if ctx.THIS():
            return ThisExpression()
        if ctx.getChildCount() == 3:
            return self.visit(ctx.expr())

    # ---------------- simple statements ----------------

    # ifstmt: IF expr THEN stmt ELSE stmt | IF expr THEN stmt;
    def visitIfstmt(self, ctx: OPLangParser.IfstmtContext):
        cond = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.stmt(0))
        else_stmt = self.visit(ctx.stmt(1)) if ctx.getChildCount() > 4 else None
        return IfStatement(cond, then_stmt, else_stmt)

    # forstmt: FOR ID ASSIGN expr fordirection expr DO stmt;
    def visitForstmt(self, ctx: OPLangParser.ForstmtContext):
        varname = ctx.ID().getText()
        start_expr = self.visit(ctx.expr(0))
        direction = ctx.fordirection().getText()
        end_expr = self.visit(ctx.expr(1))
        body = self.visit(ctx.stmt())
        return ForStatement(varname, start_expr, direction, end_expr, body)

    # fordirection: TO | DOWNTO;
    def visitFordirection(self, ctx: OPLangParser.FordirectionContext):
        return ctx.getText()

    # breakstmt: BREAK SEMI;
    def visitBreakstmt(self, ctx: OPLangParser.BreakstmtContext):
        return BreakStatement()

    # continuestmt: CONTINUE SEMI;
    def visitContinuestmt(self, ctx: OPLangParser.ContinuestmtContext):
        return ContinueStatement()

    # returnstmt: RETURN expropt SEMI;
    def visitReturnstmt(self, ctx: OPLangParser.ReturnstmtContext):
        value = self.visit(ctx.expropt()) if ctx.expropt() else None
        return ReturnStatement(value)

    # expropt: expr | ;
    def visitExpropt(self, ctx: OPLangParser.ExproptContext):
        if ctx.expr():
            return self.visit(ctx.expr())
        return NilLiteral()

    # callstmt: primary callpreinvoke memberinvoke calltail SEMI;
    def visitCallstmt(self, ctx: OPLangParser.CallstmtContext):
        primary = self.visit(ctx.primary())
        pre = self.visit(ctx.callpreinvoke()) or []
        invoke = self.visit(ctx.memberinvoke())
        tail = self.visit(ctx.calltail()) or []

        postfix_ops = pre + [invoke]
        for seg in tail:
            if isinstance(seg, tuple) and len(seg) == 2:
                post, inv = seg
                postfix_ops.extend(post if isinstance(post, list) else [post])
                postfix_ops.append(inv)
            else:
                postfix_ops.append(seg)

        postfix_expr = PostfixExpression(primary, postfix_ops) if postfix_ops else primary
        return MethodInvocationStatement(postfix_expr)

    # expr: exprrelational;
    def visitExpr(self, ctx: OPLangParser.ExprContext):
        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':  
            inner = self.visit(ctx.getChild(1))
            return ParenthesizedExpression(inner)
        return self.visit(ctx.exprrelational())

    # ---------------- expressions hierarchy ----------------

    # exprrelational: exprequality exprrelationalopt;
    def visitExprrelational(self, ctx: OPLangParser.ExprrelationalContext):
        left = self.visit(ctx.exprequality())
        opt = ctx.exprrelationalopt()
        if opt and opt.getChildCount() > 0:
            op = opt.getChild(0).getText()
            right = self.visit(opt.exprequality())
            return BinaryOp(left, op, right)
        return left

    # exprequality: exprlogic exprequalityopt;
    def visitExprequality(self, ctx: OPLangParser.ExprequalityContext):
        left = self.visit(ctx.exprlogic())
        opt = ctx.exprequalityopt()
        if opt and opt.getChildCount() > 0:
            op = opt.getChild(0).getText()
            right = self.visit(opt.exprlogic())
            return BinaryOp(left, op, right)
        return left

    # exprlogic: expradd exprlogictail;
    def visitExprlogic(self, ctx: OPLangParser.ExprlogicContext):
        left = self.visit(ctx.expradd())
        tail = ctx.exprlogictail()
        while tail and tail.getChildCount() > 0:
            op = tail.getChild(0).getText()
            right = self.visit(tail.expradd())
            left = BinaryOp(left, op, right)
            tail = tail.exprlogictail()
        return left

    # expradd: exprmul expraddtail;
    def visitExpradd(self, ctx: OPLangParser.ExpraddContext):
        left = self.visit(ctx.exprmul())
        tail = ctx.expraddtail()
        while tail and tail.getChildCount() > 0:
            op = tail.getChild(0).getText()
            right = self.visit(tail.exprmul())
            left = BinaryOp(left, op, right)
            tail = tail.expraddtail()
        return left

    # exprmul: exprconcat exprmultail;
    def visitExprmul(self, ctx: OPLangParser.ExprmulContext):
        left = self.visit(ctx.exprconcat())
        tail = ctx.exprmultail()
        while tail and tail.getChildCount() > 0:
            op = tail.getChild(0).getText()
            right = self.visit(tail.exprconcat())
            left = BinaryOp(left, op, right)
            tail = tail.exprmultail()
        return left

    # exprconcat: exprunary exprconcattail;
    def visitExprconcat(self, ctx: OPLangParser.ExprconcatContext):
        left = self.visit(ctx.exprunary())
        tail = ctx.exprconcattail()
        while tail and tail.getChildCount() > 0:
            right = self.visit(tail.exprunary())
            left = BinaryOp(left, '^', right)
            tail = tail.exprconcattail()
        return left

    # exprunary: notseq signseq exprpostfix | notseq exprpostfix;
    def visitExprunary(self, ctx: OPLangParser.ExprunaryContext):
        nots = self.visit(ctx.notseq()) if ctx.notseq() else []
        signs = self.visit(ctx.signseq()) if ctx.signseq() else []
        operand = self.visit(ctx.exprpostfix())
        for s in reversed(signs):
            operand = UnaryOp(s, operand)
        for _ in reversed(nots):
            operand = UnaryOp('!', operand)
        return operand

    # notseq: NOT notseq | ;
    def visitNotseq(self, ctx: OPLangParser.NotseqContext):
        if ctx.getChildCount() == 0:
            return []
        return ['!'] + self.visit(ctx.notseq())

    # signseq: sign signseq | sign;
    def visitSignseq(self, ctx: OPLangParser.SignseqContext):
        head = self.visit(ctx.sign())
        if ctx.signseq():
            return [head] + self.visit(ctx.signseq())
        return [head]

    # sign: ADD | SUB;
    def visitSign(self, ctx: OPLangParser.SignContext):
        return ctx.getChild(0).getText()

    # exprpostfix: primary postfixtailopt;
    def visitExprpostfix(self, ctx: OPLangParser.ExprpostfixContext):
        primary = self.visit(ctx.primary())
        tail = self.visit(ctx.postfixtailopt()) or []
        if not tail:
            return primary
        ops = tail if isinstance(tail, list) else [tail]
        return PostfixExpression(primary, ops)

    # postfixtailopt: postfixtail | ;
    def visitPostfixtailopt(self, ctx: OPLangParser.PostfixtailoptContext):
        if ctx.postfixtail():
            return self.visit(ctx.postfixtail())
        return []

    # postfixtail: dotseq indexseq;
    def visitPostfixtail(self, ctx: OPLangParser.PostfixtailContext):
        dot_ops = self.visit(ctx.dotseq()) or []
        idx_ops = self.visit(ctx.indexseq()) or []
        return dot_ops + idx_ops

    # dotseq: dotop dotseq | ;
    def visitDotseq(self, ctx: OPLangParser.DotseqContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.dotop())] + self.visit(ctx.dotseq())

    # dotop: memberinvoke | memberaccess;
    def visitDotop(self, ctx: OPLangParser.DotopContext):
        if ctx.memberinvoke():
            return self.visit(ctx.memberinvoke())
        if ctx.memberaccess():
            return self.visit(ctx.memberaccess())
        return None

    # indexseq: indexop indexseq | ;
    def visitIndexseq(self, ctx: OPLangParser.IndexseqContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.indexop())] + self.visit(ctx.indexseq())

    # indexop: LSB expr RSB;
    def visitIndexop(self, ctx: OPLangParser.IndexopContext):
        return ArrayAccess(self.visit(ctx.expr()))

    # memberaccess: DOT ID;
    def visitMemberaccess(self, ctx: OPLangParser.MemberaccessContext):
        return MemberAccess(ctx.ID().getText())

    # memberinvoke: DOT ID LP arglistopt RP;
    def visitMemberinvoke(self, ctx: OPLangParser.MemberinvokeContext):
        name = ctx.ID().getText()
        args = self.visit(ctx.arglistopt()) or []
        return MethodCall(name, args)

    # arglistopt: arglist | ;
    def visitArglistopt(self, ctx: OPLangParser.ArglistoptContext):
        if ctx.arglist():
            return self.visit(ctx.arglist())
        return []

    # arglist: expr arglisttail;
    def visitArglist(self, ctx: OPLangParser.ArglistContext):
        return [self.visit(ctx.expr())] + self.visit(ctx.arglisttail())

    # arglisttail: COMMA expr arglisttail | ;
    def visitArglisttail(self, ctx: OPLangParser.ArglisttailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.arglisttail())

    # callpreinvoke: memberaccess callpreinvoke | ;
    def visitCallpreinvoke(self, ctx: OPLangParser.CallpreinvokeContext):
        if ctx.getChildCount() == 0:
            return []
        result = [self.visit(ctx.memberaccess())]
        tail = self.visit(ctx.callpreinvoke()) or []
        result.extend(tail)
        return result

    # calltail: memberinvokeseg calltail | ;
    def visitCalltail(self, ctx: OPLangParser.CalltailContext):
        if ctx.getChildCount() == 0:
            return []
        result = [self.visit(ctx.memberinvokeseg())]
        tail = self.visit(ctx.calltail()) or []
        result.extend(tail)
        return result

    # memberinvokeseg: callpostinvoke memberinvoke;
    def visitMemberinvokeseg(self, ctx: OPLangParser.MemberinvokesegContext):
        post = self.visit(ctx.callpostinvoke()) or []
        invoke = self.visit(ctx.memberinvoke())
        return (post, invoke)

    # callpostinvoke: callpostinvoketok callpostinvoke | ;
    def visitCallpostinvoke(self, ctx: OPLangParser.CallpostinvokeContext):
        if ctx.getChildCount() == 0:
            return []
        result = [self.visit(ctx.callpostinvoketok())]
        tail = self.visit(ctx.callpostinvoke()) or []
        result.extend(tail)
        return result

    # callpostinvoketok: memberaccess | indexop;
    def visitCallpostinvoketok(self, ctx: OPLangParser.CallpostinvoketokContext):
        if ctx.memberaccess():
            return self.visit(ctx.memberaccess())
        if ctx.indexop():
            return self.visit(ctx.indexop())
        return None

    # primary: THIS | NIL | literal | ID | LP expr RP | arrayliteral | newexpr;
    def visitPrimary(self, ctx: OPLangParser.PrimaryContext):
        if ctx.THIS():
            return ThisExpression()
        if ctx.NIL():
            return NilLiteral()
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        if ctx.getChildCount() == 3 and ctx.expr():
            return ParenthesizedExpression(self.visit(ctx.expr()))
        if ctx.arrayliteral():
            return self.visit(ctx.arrayliteral())
        if ctx.newexpr():
            return self.visit(ctx.newexpr())
        return None

    # newexpr: NEW ID LP arglistopt RP;
    def visitNewexpr(self, ctx: OPLangParser.NewexprContext):
        class_name = ctx.ID().getText()
        args = self.visit(ctx.arglistopt()) or []
        return ObjectCreation(class_name, args)

    # arrayliteral: LCB arrayelement arrayliteraltailopt RCB;
    def visitArrayliteral(self, ctx: OPLangParser.ArrayliteralContext):
        first = self.visit(ctx.arrayelement())
        tail = self.visit(ctx.arrayliteraltailopt()) or []
        elements = [first] + tail
        return ArrayLiteral(elements)

    # arrayliteraltailopt: arrayliteraltail | ;
    def visitArrayliteraltailopt(self, ctx: OPLangParser.ArrayliteraltailoptContext):
        if ctx.arrayliteraltail():
            return self.visit(ctx.arrayliteraltail())
        return []

    # arrayliteraltail: COMMA arrayelement arrayliteraltail | ;
    def visitArrayliteraltail(self, ctx: OPLangParser.ArrayliteraltailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.arrayelement())] + self.visit(ctx.arrayliteraltail())

    # arrayelement: literal | NIL;
    def visitArrayelement(self, ctx: OPLangParser.ArrayelementContext):
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.NIL():
            return NilLiteral()
        return None

    # literal: INTLIT | FLOATLIT | STRINGLIT | TRUE | FALSE;
    def visitLiteral(self, ctx: OPLangParser.LiteralContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        if ctx.STRINGLIT():
            txt = ctx.STRINGLIT().getText()
            if len(txt) >= 2 and txt[0] == '"' and txt[-1] == '"':
                txt = txt[1:-1]
            return StringLiteral(txt)
        if ctx.TRUE():
            return BoolLiteral(True)
        if ctx.FALSE():
            return BoolLiteral(False)
        return None

    # ---------------- types ----------------

    # typ: primtyp | arraytyp | classtyp;
    def visitTyp(self, ctx: OPLangParser.TypContext):
        if ctx.primtyp():
            return self.visit(ctx.primtyp())
        if ctx.arraytyp():
            return self.visit(ctx.arraytyp())
        if ctx.classtyp():
            return self.visit(ctx.classtyp())
        return None

    # primtyp: INT | FLOAT | BOOLEAN | STRING;
    def visitPrimtyp(self, ctx: OPLangParser.PrimtypContext):
        if ctx.INT():
            return PrimitiveType("int")
        if ctx.FLOAT():
            return PrimitiveType("float")
        if ctx.BOOLEAN():
            return PrimitiveType("boolean")
        if ctx.STRING():
            return PrimitiveType("string")
        return None

    # arraytyp: arrayelementtyp LSB INTLIT RSB;
    def visitArraytyp(self, ctx: OPLangParser.ArraytypContext):
        return ArrayType(self.visit(ctx.arrayelementtyp()), int(ctx.INTLIT().getText()))

    # arrayelementtyp: primtyp | classtyp;
    def visitArrayelementtyp(self, ctx: OPLangParser.ArrayelementtypContext):
        if ctx.primtyp():
            return self.visit(ctx.primtyp())
        if ctx.classtyp():
            return self.visit(ctx.classtyp())
        return None

    # classtyp: ID;
    def visitClasstyp(self, ctx: OPLangParser.ClasstypContext):
        return ClassType(ctx.ID().getText())