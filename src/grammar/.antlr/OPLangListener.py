# Generated from d:/Project/OPLang-Compiler-Lite/src/grammar/OPLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .OPLangParser import OPLangParser
else:
    from OPLangParser import OPLangParser

# This class defines a complete listener for a parse tree produced by OPLangParser.
class OPLangListener(ParseTreeListener):

    # Enter a parse tree produced by OPLangParser#program.
    def enterProgram(self, ctx:OPLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by OPLangParser#program.
    def exitProgram(self, ctx:OPLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by OPLangParser#classdecllist.
    def enterClassdecllist(self, ctx:OPLangParser.ClassdecllistContext):
        pass

    # Exit a parse tree produced by OPLangParser#classdecllist.
    def exitClassdecllist(self, ctx:OPLangParser.ClassdecllistContext):
        pass


    # Enter a parse tree produced by OPLangParser#classdecllisttail.
    def enterClassdecllisttail(self, ctx:OPLangParser.ClassdecllisttailContext):
        pass

    # Exit a parse tree produced by OPLangParser#classdecllisttail.
    def exitClassdecllisttail(self, ctx:OPLangParser.ClassdecllisttailContext):
        pass


    # Enter a parse tree produced by OPLangParser#classdecl.
    def enterClassdecl(self, ctx:OPLangParser.ClassdeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#classdecl.
    def exitClassdecl(self, ctx:OPLangParser.ClassdeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#extendsclause.
    def enterExtendsclause(self, ctx:OPLangParser.ExtendsclauseContext):
        pass

    # Exit a parse tree produced by OPLangParser#extendsclause.
    def exitExtendsclause(self, ctx:OPLangParser.ExtendsclauseContext):
        pass


    # Enter a parse tree produced by OPLangParser#memberdecl.
    def enterMemberdecl(self, ctx:OPLangParser.MemberdeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#memberdecl.
    def exitMemberdecl(self, ctx:OPLangParser.MemberdeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#memberdecllistopt.
    def enterMemberdecllistopt(self, ctx:OPLangParser.MemberdecllistoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#memberdecllistopt.
    def exitMemberdecllistopt(self, ctx:OPLangParser.MemberdecllistoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#memberdecllist.
    def enterMemberdecllist(self, ctx:OPLangParser.MemberdecllistContext):
        pass

    # Exit a parse tree produced by OPLangParser#memberdecllist.
    def exitMemberdecllist(self, ctx:OPLangParser.MemberdecllistContext):
        pass


    # Enter a parse tree produced by OPLangParser#memberdecllisttail.
    def enterMemberdecllisttail(self, ctx:OPLangParser.MemberdecllisttailContext):
        pass

    # Exit a parse tree produced by OPLangParser#memberdecllisttail.
    def exitMemberdecllisttail(self, ctx:OPLangParser.MemberdecllisttailContext):
        pass


    # Enter a parse tree produced by OPLangParser#attributedecl.
    def enterAttributedecl(self, ctx:OPLangParser.AttributedeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#attributedecl.
    def exitAttributedecl(self, ctx:OPLangParser.AttributedeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#attributemodsopt.
    def enterAttributemodsopt(self, ctx:OPLangParser.AttributemodsoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#attributemodsopt.
    def exitAttributemodsopt(self, ctx:OPLangParser.AttributemodsoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#attributemods.
    def enterAttributemods(self, ctx:OPLangParser.AttributemodsContext):
        pass

    # Exit a parse tree produced by OPLangParser#attributemods.
    def exitAttributemods(self, ctx:OPLangParser.AttributemodsContext):
        pass


    # Enter a parse tree produced by OPLangParser#refmarker.
    def enterRefmarker(self, ctx:OPLangParser.RefmarkerContext):
        pass

    # Exit a parse tree produced by OPLangParser#refmarker.
    def exitRefmarker(self, ctx:OPLangParser.RefmarkerContext):
        pass


    # Enter a parse tree produced by OPLangParser#refmarkeropt.
    def enterRefmarkeropt(self, ctx:OPLangParser.RefmarkeroptContext):
        pass

    # Exit a parse tree produced by OPLangParser#refmarkeropt.
    def exitRefmarkeropt(self, ctx:OPLangParser.RefmarkeroptContext):
        pass


    # Enter a parse tree produced by OPLangParser#attrlist.
    def enterAttrlist(self, ctx:OPLangParser.AttrlistContext):
        pass

    # Exit a parse tree produced by OPLangParser#attrlist.
    def exitAttrlist(self, ctx:OPLangParser.AttrlistContext):
        pass


    # Enter a parse tree produced by OPLangParser#attrlisttail.
    def enterAttrlisttail(self, ctx:OPLangParser.AttrlisttailContext):
        pass

    # Exit a parse tree produced by OPLangParser#attrlisttail.
    def exitAttrlisttail(self, ctx:OPLangParser.AttrlisttailContext):
        pass


    # Enter a parse tree produced by OPLangParser#attrinit.
    def enterAttrinit(self, ctx:OPLangParser.AttrinitContext):
        pass

    # Exit a parse tree produced by OPLangParser#attrinit.
    def exitAttrinit(self, ctx:OPLangParser.AttrinitContext):
        pass


    # Enter a parse tree produced by OPLangParser#attrinitassignopt.
    def enterAttrinitassignopt(self, ctx:OPLangParser.AttrinitassignoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#attrinitassignopt.
    def exitAttrinitassignopt(self, ctx:OPLangParser.AttrinitassignoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#methoddecl.
    def enterMethoddecl(self, ctx:OPLangParser.MethoddeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#methoddecl.
    def exitMethoddecl(self, ctx:OPLangParser.MethoddeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#staticopt.
    def enterStaticopt(self, ctx:OPLangParser.StaticoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#staticopt.
    def exitStaticopt(self, ctx:OPLangParser.StaticoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#returntyp.
    def enterReturntyp(self, ctx:OPLangParser.ReturntypContext):
        pass

    # Exit a parse tree produced by OPLangParser#returntyp.
    def exitReturntyp(self, ctx:OPLangParser.ReturntypContext):
        pass


    # Enter a parse tree produced by OPLangParser#constructordecl.
    def enterConstructordecl(self, ctx:OPLangParser.ConstructordeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#constructordecl.
    def exitConstructordecl(self, ctx:OPLangParser.ConstructordeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#destructordecl.
    def enterDestructordecl(self, ctx:OPLangParser.DestructordeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#destructordecl.
    def exitDestructordecl(self, ctx:OPLangParser.DestructordeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#paramlistopt.
    def enterParamlistopt(self, ctx:OPLangParser.ParamlistoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#paramlistopt.
    def exitParamlistopt(self, ctx:OPLangParser.ParamlistoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#paramlist.
    def enterParamlist(self, ctx:OPLangParser.ParamlistContext):
        pass

    # Exit a parse tree produced by OPLangParser#paramlist.
    def exitParamlist(self, ctx:OPLangParser.ParamlistContext):
        pass


    # Enter a parse tree produced by OPLangParser#paramlisttail.
    def enterParamlisttail(self, ctx:OPLangParser.ParamlisttailContext):
        pass

    # Exit a parse tree produced by OPLangParser#paramlisttail.
    def exitParamlisttail(self, ctx:OPLangParser.ParamlisttailContext):
        pass


    # Enter a parse tree produced by OPLangParser#paramdecl.
    def enterParamdecl(self, ctx:OPLangParser.ParamdeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#paramdecl.
    def exitParamdecl(self, ctx:OPLangParser.ParamdeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#idlist.
    def enterIdlist(self, ctx:OPLangParser.IdlistContext):
        pass

    # Exit a parse tree produced by OPLangParser#idlist.
    def exitIdlist(self, ctx:OPLangParser.IdlistContext):
        pass


    # Enter a parse tree produced by OPLangParser#idlisttail.
    def enterIdlisttail(self, ctx:OPLangParser.IdlisttailContext):
        pass

    # Exit a parse tree produced by OPLangParser#idlisttail.
    def exitIdlisttail(self, ctx:OPLangParser.IdlisttailContext):
        pass


    # Enter a parse tree produced by OPLangParser#blockstmt.
    def enterBlockstmt(self, ctx:OPLangParser.BlockstmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#blockstmt.
    def exitBlockstmt(self, ctx:OPLangParser.BlockstmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#localvardecllistopt.
    def enterLocalvardecllistopt(self, ctx:OPLangParser.LocalvardecllistoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#localvardecllistopt.
    def exitLocalvardecllistopt(self, ctx:OPLangParser.LocalvardecllistoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#localvardecllist.
    def enterLocalvardecllist(self, ctx:OPLangParser.LocalvardecllistContext):
        pass

    # Exit a parse tree produced by OPLangParser#localvardecllist.
    def exitLocalvardecllist(self, ctx:OPLangParser.LocalvardecllistContext):
        pass


    # Enter a parse tree produced by OPLangParser#stmtlistopt.
    def enterStmtlistopt(self, ctx:OPLangParser.StmtlistoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#stmtlistopt.
    def exitStmtlistopt(self, ctx:OPLangParser.StmtlistoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#stmtlist.
    def enterStmtlist(self, ctx:OPLangParser.StmtlistContext):
        pass

    # Exit a parse tree produced by OPLangParser#stmtlist.
    def exitStmtlist(self, ctx:OPLangParser.StmtlistContext):
        pass


    # Enter a parse tree produced by OPLangParser#localvardecl.
    def enterLocalvardecl(self, ctx:OPLangParser.LocalvardeclContext):
        pass

    # Exit a parse tree produced by OPLangParser#localvardecl.
    def exitLocalvardecl(self, ctx:OPLangParser.LocalvardeclContext):
        pass


    # Enter a parse tree produced by OPLangParser#finalopt.
    def enterFinalopt(self, ctx:OPLangParser.FinaloptContext):
        pass

    # Exit a parse tree produced by OPLangParser#finalopt.
    def exitFinalopt(self, ctx:OPLangParser.FinaloptContext):
        pass


    # Enter a parse tree produced by OPLangParser#localvarlist.
    def enterLocalvarlist(self, ctx:OPLangParser.LocalvarlistContext):
        pass

    # Exit a parse tree produced by OPLangParser#localvarlist.
    def exitLocalvarlist(self, ctx:OPLangParser.LocalvarlistContext):
        pass


    # Enter a parse tree produced by OPLangParser#localvarlisttail.
    def enterLocalvarlisttail(self, ctx:OPLangParser.LocalvarlisttailContext):
        pass

    # Exit a parse tree produced by OPLangParser#localvarlisttail.
    def exitLocalvarlisttail(self, ctx:OPLangParser.LocalvarlisttailContext):
        pass


    # Enter a parse tree produced by OPLangParser#localvarinit.
    def enterLocalvarinit(self, ctx:OPLangParser.LocalvarinitContext):
        pass

    # Exit a parse tree produced by OPLangParser#localvarinit.
    def exitLocalvarinit(self, ctx:OPLangParser.LocalvarinitContext):
        pass


    # Enter a parse tree produced by OPLangParser#localvarinitassignopt.
    def enterLocalvarinitassignopt(self, ctx:OPLangParser.LocalvarinitassignoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#localvarinitassignopt.
    def exitLocalvarinitassignopt(self, ctx:OPLangParser.LocalvarinitassignoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#stmt.
    def enterStmt(self, ctx:OPLangParser.StmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#stmt.
    def exitStmt(self, ctx:OPLangParser.StmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#assignstmt.
    def enterAssignstmt(self, ctx:OPLangParser.AssignstmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#assignstmt.
    def exitAssignstmt(self, ctx:OPLangParser.AssignstmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhs.
    def enterLhs(self, ctx:OPLangParser.LhsContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhs.
    def exitLhs(self, ctx:OPLangParser.LhsContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhssuffixopt.
    def enterLhssuffixopt(self, ctx:OPLangParser.LhssuffixoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhssuffixopt.
    def exitLhssuffixopt(self, ctx:OPLangParser.LhssuffixoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhssuffix.
    def enterLhssuffix(self, ctx:OPLangParser.LhssuffixContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhssuffix.
    def exitLhssuffix(self, ctx:OPLangParser.LhssuffixContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhssuffixthis.
    def enterLhssuffixthis(self, ctx:OPLangParser.LhssuffixthisContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhssuffixthis.
    def exitLhssuffixthis(self, ctx:OPLangParser.LhssuffixthisContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhsdotseq.
    def enterLhsdotseq(self, ctx:OPLangParser.LhsdotseqContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhsdotseq.
    def exitLhsdotseq(self, ctx:OPLangParser.LhsdotseqContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhsdotseqnoendinvoke.
    def enterLhsdotseqnoendinvoke(self, ctx:OPLangParser.LhsdotseqnoendinvokeContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhsdotseqnoendinvoke.
    def exitLhsdotseqnoendinvoke(self, ctx:OPLangParser.LhsdotseqnoendinvokeContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhsdotseqtail.
    def enterLhsdotseqtail(self, ctx:OPLangParser.LhsdotseqtailContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhsdotseqtail.
    def exitLhsdotseqtail(self, ctx:OPLangParser.LhsdotseqtailContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhsdotop.
    def enterLhsdotop(self, ctx:OPLangParser.LhsdotopContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhsdotop.
    def exitLhsdotop(self, ctx:OPLangParser.LhsdotopContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhsindexseq.
    def enterLhsindexseq(self, ctx:OPLangParser.LhsindexseqContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhsindexseq.
    def exitLhsindexseq(self, ctx:OPLangParser.LhsindexseqContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhsindexseqopt.
    def enterLhsindexseqopt(self, ctx:OPLangParser.LhsindexseqoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhsindexseqopt.
    def exitLhsindexseqopt(self, ctx:OPLangParser.LhsindexseqoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#lhsbase.
    def enterLhsbase(self, ctx:OPLangParser.LhsbaseContext):
        pass

    # Exit a parse tree produced by OPLangParser#lhsbase.
    def exitLhsbase(self, ctx:OPLangParser.LhsbaseContext):
        pass


    # Enter a parse tree produced by OPLangParser#ifstmt.
    def enterIfstmt(self, ctx:OPLangParser.IfstmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#ifstmt.
    def exitIfstmt(self, ctx:OPLangParser.IfstmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#forstmt.
    def enterForstmt(self, ctx:OPLangParser.ForstmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#forstmt.
    def exitForstmt(self, ctx:OPLangParser.ForstmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#fordirection.
    def enterFordirection(self, ctx:OPLangParser.FordirectionContext):
        pass

    # Exit a parse tree produced by OPLangParser#fordirection.
    def exitFordirection(self, ctx:OPLangParser.FordirectionContext):
        pass


    # Enter a parse tree produced by OPLangParser#breakstmt.
    def enterBreakstmt(self, ctx:OPLangParser.BreakstmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#breakstmt.
    def exitBreakstmt(self, ctx:OPLangParser.BreakstmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#continuestmt.
    def enterContinuestmt(self, ctx:OPLangParser.ContinuestmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#continuestmt.
    def exitContinuestmt(self, ctx:OPLangParser.ContinuestmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#returnstmt.
    def enterReturnstmt(self, ctx:OPLangParser.ReturnstmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#returnstmt.
    def exitReturnstmt(self, ctx:OPLangParser.ReturnstmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#expropt.
    def enterExpropt(self, ctx:OPLangParser.ExproptContext):
        pass

    # Exit a parse tree produced by OPLangParser#expropt.
    def exitExpropt(self, ctx:OPLangParser.ExproptContext):
        pass


    # Enter a parse tree produced by OPLangParser#callstmt.
    def enterCallstmt(self, ctx:OPLangParser.CallstmtContext):
        pass

    # Exit a parse tree produced by OPLangParser#callstmt.
    def exitCallstmt(self, ctx:OPLangParser.CallstmtContext):
        pass


    # Enter a parse tree produced by OPLangParser#callpreinvoke.
    def enterCallpreinvoke(self, ctx:OPLangParser.CallpreinvokeContext):
        pass

    # Exit a parse tree produced by OPLangParser#callpreinvoke.
    def exitCallpreinvoke(self, ctx:OPLangParser.CallpreinvokeContext):
        pass


    # Enter a parse tree produced by OPLangParser#calltail.
    def enterCalltail(self, ctx:OPLangParser.CalltailContext):
        pass

    # Exit a parse tree produced by OPLangParser#calltail.
    def exitCalltail(self, ctx:OPLangParser.CalltailContext):
        pass


    # Enter a parse tree produced by OPLangParser#memberinvokeseg.
    def enterMemberinvokeseg(self, ctx:OPLangParser.MemberinvokesegContext):
        pass

    # Exit a parse tree produced by OPLangParser#memberinvokeseg.
    def exitMemberinvokeseg(self, ctx:OPLangParser.MemberinvokesegContext):
        pass


    # Enter a parse tree produced by OPLangParser#callpostinvoke.
    def enterCallpostinvoke(self, ctx:OPLangParser.CallpostinvokeContext):
        pass

    # Exit a parse tree produced by OPLangParser#callpostinvoke.
    def exitCallpostinvoke(self, ctx:OPLangParser.CallpostinvokeContext):
        pass


    # Enter a parse tree produced by OPLangParser#callpostinvoketok.
    def enterCallpostinvoketok(self, ctx:OPLangParser.CallpostinvoketokContext):
        pass

    # Exit a parse tree produced by OPLangParser#callpostinvoketok.
    def exitCallpostinvoketok(self, ctx:OPLangParser.CallpostinvoketokContext):
        pass


    # Enter a parse tree produced by OPLangParser#expr.
    def enterExpr(self, ctx:OPLangParser.ExprContext):
        pass

    # Exit a parse tree produced by OPLangParser#expr.
    def exitExpr(self, ctx:OPLangParser.ExprContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprrelational.
    def enterExprrelational(self, ctx:OPLangParser.ExprrelationalContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprrelational.
    def exitExprrelational(self, ctx:OPLangParser.ExprrelationalContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprrelationalopt.
    def enterExprrelationalopt(self, ctx:OPLangParser.ExprrelationaloptContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprrelationalopt.
    def exitExprrelationalopt(self, ctx:OPLangParser.ExprrelationaloptContext):
        pass


    # Enter a parse tree produced by OPLangParser#relationalop.
    def enterRelationalop(self, ctx:OPLangParser.RelationalopContext):
        pass

    # Exit a parse tree produced by OPLangParser#relationalop.
    def exitRelationalop(self, ctx:OPLangParser.RelationalopContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprequality.
    def enterExprequality(self, ctx:OPLangParser.ExprequalityContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprequality.
    def exitExprequality(self, ctx:OPLangParser.ExprequalityContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprequalityopt.
    def enterExprequalityopt(self, ctx:OPLangParser.ExprequalityoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprequalityopt.
    def exitExprequalityopt(self, ctx:OPLangParser.ExprequalityoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#equalityop.
    def enterEqualityop(self, ctx:OPLangParser.EqualityopContext):
        pass

    # Exit a parse tree produced by OPLangParser#equalityop.
    def exitEqualityop(self, ctx:OPLangParser.EqualityopContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprlogic.
    def enterExprlogic(self, ctx:OPLangParser.ExprlogicContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprlogic.
    def exitExprlogic(self, ctx:OPLangParser.ExprlogicContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprlogictail.
    def enterExprlogictail(self, ctx:OPLangParser.ExprlogictailContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprlogictail.
    def exitExprlogictail(self, ctx:OPLangParser.ExprlogictailContext):
        pass


    # Enter a parse tree produced by OPLangParser#logicop.
    def enterLogicop(self, ctx:OPLangParser.LogicopContext):
        pass

    # Exit a parse tree produced by OPLangParser#logicop.
    def exitLogicop(self, ctx:OPLangParser.LogicopContext):
        pass


    # Enter a parse tree produced by OPLangParser#expradd.
    def enterExpradd(self, ctx:OPLangParser.ExpraddContext):
        pass

    # Exit a parse tree produced by OPLangParser#expradd.
    def exitExpradd(self, ctx:OPLangParser.ExpraddContext):
        pass


    # Enter a parse tree produced by OPLangParser#expraddtail.
    def enterExpraddtail(self, ctx:OPLangParser.ExpraddtailContext):
        pass

    # Exit a parse tree produced by OPLangParser#expraddtail.
    def exitExpraddtail(self, ctx:OPLangParser.ExpraddtailContext):
        pass


    # Enter a parse tree produced by OPLangParser#addop.
    def enterAddop(self, ctx:OPLangParser.AddopContext):
        pass

    # Exit a parse tree produced by OPLangParser#addop.
    def exitAddop(self, ctx:OPLangParser.AddopContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprmul.
    def enterExprmul(self, ctx:OPLangParser.ExprmulContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprmul.
    def exitExprmul(self, ctx:OPLangParser.ExprmulContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprmultail.
    def enterExprmultail(self, ctx:OPLangParser.ExprmultailContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprmultail.
    def exitExprmultail(self, ctx:OPLangParser.ExprmultailContext):
        pass


    # Enter a parse tree produced by OPLangParser#mulop.
    def enterMulop(self, ctx:OPLangParser.MulopContext):
        pass

    # Exit a parse tree produced by OPLangParser#mulop.
    def exitMulop(self, ctx:OPLangParser.MulopContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprconcat.
    def enterExprconcat(self, ctx:OPLangParser.ExprconcatContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprconcat.
    def exitExprconcat(self, ctx:OPLangParser.ExprconcatContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprconcattail.
    def enterExprconcattail(self, ctx:OPLangParser.ExprconcattailContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprconcattail.
    def exitExprconcattail(self, ctx:OPLangParser.ExprconcattailContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprunary.
    def enterExprunary(self, ctx:OPLangParser.ExprunaryContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprunary.
    def exitExprunary(self, ctx:OPLangParser.ExprunaryContext):
        pass


    # Enter a parse tree produced by OPLangParser#notseq.
    def enterNotseq(self, ctx:OPLangParser.NotseqContext):
        pass

    # Exit a parse tree produced by OPLangParser#notseq.
    def exitNotseq(self, ctx:OPLangParser.NotseqContext):
        pass


    # Enter a parse tree produced by OPLangParser#signseq.
    def enterSignseq(self, ctx:OPLangParser.SignseqContext):
        pass

    # Exit a parse tree produced by OPLangParser#signseq.
    def exitSignseq(self, ctx:OPLangParser.SignseqContext):
        pass


    # Enter a parse tree produced by OPLangParser#sign.
    def enterSign(self, ctx:OPLangParser.SignContext):
        pass

    # Exit a parse tree produced by OPLangParser#sign.
    def exitSign(self, ctx:OPLangParser.SignContext):
        pass


    # Enter a parse tree produced by OPLangParser#exprpostfix.
    def enterExprpostfix(self, ctx:OPLangParser.ExprpostfixContext):
        pass

    # Exit a parse tree produced by OPLangParser#exprpostfix.
    def exitExprpostfix(self, ctx:OPLangParser.ExprpostfixContext):
        pass


    # Enter a parse tree produced by OPLangParser#postfixtailopt.
    def enterPostfixtailopt(self, ctx:OPLangParser.PostfixtailoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#postfixtailopt.
    def exitPostfixtailopt(self, ctx:OPLangParser.PostfixtailoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#postfixtail.
    def enterPostfixtail(self, ctx:OPLangParser.PostfixtailContext):
        pass

    # Exit a parse tree produced by OPLangParser#postfixtail.
    def exitPostfixtail(self, ctx:OPLangParser.PostfixtailContext):
        pass


    # Enter a parse tree produced by OPLangParser#dotseq.
    def enterDotseq(self, ctx:OPLangParser.DotseqContext):
        pass

    # Exit a parse tree produced by OPLangParser#dotseq.
    def exitDotseq(self, ctx:OPLangParser.DotseqContext):
        pass


    # Enter a parse tree produced by OPLangParser#dotop.
    def enterDotop(self, ctx:OPLangParser.DotopContext):
        pass

    # Exit a parse tree produced by OPLangParser#dotop.
    def exitDotop(self, ctx:OPLangParser.DotopContext):
        pass


    # Enter a parse tree produced by OPLangParser#indexseq.
    def enterIndexseq(self, ctx:OPLangParser.IndexseqContext):
        pass

    # Exit a parse tree produced by OPLangParser#indexseq.
    def exitIndexseq(self, ctx:OPLangParser.IndexseqContext):
        pass


    # Enter a parse tree produced by OPLangParser#indexop.
    def enterIndexop(self, ctx:OPLangParser.IndexopContext):
        pass

    # Exit a parse tree produced by OPLangParser#indexop.
    def exitIndexop(self, ctx:OPLangParser.IndexopContext):
        pass


    # Enter a parse tree produced by OPLangParser#memberaccess.
    def enterMemberaccess(self, ctx:OPLangParser.MemberaccessContext):
        pass

    # Exit a parse tree produced by OPLangParser#memberaccess.
    def exitMemberaccess(self, ctx:OPLangParser.MemberaccessContext):
        pass


    # Enter a parse tree produced by OPLangParser#memberinvoke.
    def enterMemberinvoke(self, ctx:OPLangParser.MemberinvokeContext):
        pass

    # Exit a parse tree produced by OPLangParser#memberinvoke.
    def exitMemberinvoke(self, ctx:OPLangParser.MemberinvokeContext):
        pass


    # Enter a parse tree produced by OPLangParser#arglistopt.
    def enterArglistopt(self, ctx:OPLangParser.ArglistoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#arglistopt.
    def exitArglistopt(self, ctx:OPLangParser.ArglistoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#arglist.
    def enterArglist(self, ctx:OPLangParser.ArglistContext):
        pass

    # Exit a parse tree produced by OPLangParser#arglist.
    def exitArglist(self, ctx:OPLangParser.ArglistContext):
        pass


    # Enter a parse tree produced by OPLangParser#arglisttail.
    def enterArglisttail(self, ctx:OPLangParser.ArglisttailContext):
        pass

    # Exit a parse tree produced by OPLangParser#arglisttail.
    def exitArglisttail(self, ctx:OPLangParser.ArglisttailContext):
        pass


    # Enter a parse tree produced by OPLangParser#primary.
    def enterPrimary(self, ctx:OPLangParser.PrimaryContext):
        pass

    # Exit a parse tree produced by OPLangParser#primary.
    def exitPrimary(self, ctx:OPLangParser.PrimaryContext):
        pass


    # Enter a parse tree produced by OPLangParser#newexpr.
    def enterNewexpr(self, ctx:OPLangParser.NewexprContext):
        pass

    # Exit a parse tree produced by OPLangParser#newexpr.
    def exitNewexpr(self, ctx:OPLangParser.NewexprContext):
        pass


    # Enter a parse tree produced by OPLangParser#arrayliteral.
    def enterArrayliteral(self, ctx:OPLangParser.ArrayliteralContext):
        pass

    # Exit a parse tree produced by OPLangParser#arrayliteral.
    def exitArrayliteral(self, ctx:OPLangParser.ArrayliteralContext):
        pass


    # Enter a parse tree produced by OPLangParser#arrayliteraltailopt.
    def enterArrayliteraltailopt(self, ctx:OPLangParser.ArrayliteraltailoptContext):
        pass

    # Exit a parse tree produced by OPLangParser#arrayliteraltailopt.
    def exitArrayliteraltailopt(self, ctx:OPLangParser.ArrayliteraltailoptContext):
        pass


    # Enter a parse tree produced by OPLangParser#arrayliteraltail.
    def enterArrayliteraltail(self, ctx:OPLangParser.ArrayliteraltailContext):
        pass

    # Exit a parse tree produced by OPLangParser#arrayliteraltail.
    def exitArrayliteraltail(self, ctx:OPLangParser.ArrayliteraltailContext):
        pass


    # Enter a parse tree produced by OPLangParser#arrayelement.
    def enterArrayelement(self, ctx:OPLangParser.ArrayelementContext):
        pass

    # Exit a parse tree produced by OPLangParser#arrayelement.
    def exitArrayelement(self, ctx:OPLangParser.ArrayelementContext):
        pass


    # Enter a parse tree produced by OPLangParser#literal.
    def enterLiteral(self, ctx:OPLangParser.LiteralContext):
        pass

    # Exit a parse tree produced by OPLangParser#literal.
    def exitLiteral(self, ctx:OPLangParser.LiteralContext):
        pass


    # Enter a parse tree produced by OPLangParser#typ.
    def enterTyp(self, ctx:OPLangParser.TypContext):
        pass

    # Exit a parse tree produced by OPLangParser#typ.
    def exitTyp(self, ctx:OPLangParser.TypContext):
        pass


    # Enter a parse tree produced by OPLangParser#primtyp.
    def enterPrimtyp(self, ctx:OPLangParser.PrimtypContext):
        pass

    # Exit a parse tree produced by OPLangParser#primtyp.
    def exitPrimtyp(self, ctx:OPLangParser.PrimtypContext):
        pass


    # Enter a parse tree produced by OPLangParser#arraytyp.
    def enterArraytyp(self, ctx:OPLangParser.ArraytypContext):
        pass

    # Exit a parse tree produced by OPLangParser#arraytyp.
    def exitArraytyp(self, ctx:OPLangParser.ArraytypContext):
        pass


    # Enter a parse tree produced by OPLangParser#arrayelementtyp.
    def enterArrayelementtyp(self, ctx:OPLangParser.ArrayelementtypContext):
        pass

    # Exit a parse tree produced by OPLangParser#arrayelementtyp.
    def exitArrayelementtyp(self, ctx:OPLangParser.ArrayelementtypContext):
        pass


    # Enter a parse tree produced by OPLangParser#classtyp.
    def enterClasstyp(self, ctx:OPLangParser.ClasstypContext):
        pass

    # Exit a parse tree produced by OPLangParser#classtyp.
    def exitClasstyp(self, ctx:OPLangParser.ClasstypContext):
        pass



del OPLangParser