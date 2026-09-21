grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// ----------------------
// Parser rules
// ----------------------

program: classdecllist EOF;

classdecllist: classdecl classdecllisttail;

classdecllisttail: classdecl classdecllisttail | ;

classdecl: CLASS ID extendsclause LCB memberdecllistopt RCB;

extendsclause: EXTENDS ID | ;

memberdecl: attributedecl | methoddecl | constructordecl | destructordecl;

memberdecllistopt: memberdecllist | ;

memberdecllist: memberdecl memberdecllisttail;

memberdecllisttail: memberdecl memberdecllisttail | ;

attributedecl: attributemodsopt typ refmarkeropt attrlist SEMI;

attributemodsopt: attributemods | ;

attributemods: STATIC finalopt | FINAL staticopt | STATIC | FINAL;

refmarker: AMP;

refmarkeropt: refmarker | ;

attrlist: attrinit attrlisttail;

attrlisttail: COMMA attrinit attrlisttail | ;

attrinit: ID attrinitassignopt;

attrinitassignopt: ASSIGN expr | ;

// Methods (may be static). Return type can be void or a type optionally followed by '&'
methoddecl: staticopt returntyp ID LP paramlistopt RP blockstmt;

staticopt: STATIC | ;

returntyp: VOID | typ refmarkeropt;

// Constructors: same name as class (recognized syntactically as ID '(' ... ')')
constructordecl: ID LP paramlistopt RP blockstmt;

destructordecl: TILDE ID LP RP blockstmt;

paramlistopt: paramlist | ;

paramlist: paramdecl paramlisttail;

paramlisttail: SEMI paramdecl paramlisttail | ;

paramdecl: typ refmarkeropt idlist;

idlist: ID idlisttail;

idlisttail: COMMA ID idlisttail | ;

// ----------------------
// Statements
// ----------------------

blockstmt: LCB localvardecllistopt stmtlistopt RCB;

localvardecllistopt: localvardecllist | ;

localvardecllist: localvardecl localvardecllist | ;

stmtlistopt: stmtlist | ;

stmtlist: stmt stmtlist | ;

localvardecl: finalopt typ refmarkeropt localvarlist SEMI;

finalopt: FINAL | ;

localvarlist: localvarinit localvarlisttail;

localvarlisttail: COMMA localvarinit localvarlisttail | ;

localvarinit: ID localvarinitassignopt;

localvarinitassignopt: ASSIGN expr | ;

stmt: blockstmt | assignstmt | ifstmt | forstmt | breakstmt | continuestmt | returnstmt | callstmt;

assignstmt: lhs ASSIGN expr SEMI;

lhs: ID lhssuffix
   | THIS lhssuffixthis
   | LP expr RP lhssuffix
   | arrayliteral lhssuffix
   | newexpr lhssuffix
   | literal lhssuffix
   | NIL lhssuffix
   ;

lhssuffixopt: lhssuffix | ;

lhssuffix: lhsdotseqnoendinvoke lhsindexseqopt | lhsindexseq | ;

lhssuffixthis: lhsdotseqnoendinvoke lhsindexseqopt; 

lhsdotseq: lhsdotop lhsdotseq | ;

lhsdotseqnoendinvoke: memberaccess lhsdotseqtail | memberinvoke memberaccess lhsdotseqtail;

lhsdotseqtail: lhsdotop lhsdotseqtail | ;

lhsdotop: memberaccess | memberinvoke;

lhsindexseq: indexop lhsindexseq | ;

lhsindexseqopt: indexop lhsindexseq | ;

lhsbase: ID | THIS | LP expr RP;

ifstmt: IF expr THEN stmt ELSE stmt | IF expr THEN stmt;

forstmt: FOR ID ASSIGN expr fordirection expr DO stmt;

fordirection: TO | DOWNTO;

breakstmt: BREAK SEMI;

continuestmt: CONTINUE SEMI;

returnstmt: RETURN expropt SEMI;

expropt: expr | ;

// Only method invocations are allowed as standalone statements
// Allow only member access before first invocation; after each invocation, allow access/index before next
callstmt: primary callpreinvoke memberinvoke calltail SEMI;

callpreinvoke: memberaccess callpreinvoke | ;

calltail: memberinvokeseg calltail | ;

memberinvokeseg: callpostinvoke memberinvoke;

callpostinvoke: callpostinvoketok callpostinvoke | ;

callpostinvoketok: memberaccess | indexop;

// ----------------------
// Expressions and operators (with precedence)
// ----------------------

expr: exprrelational;

exprrelational: exprequality exprrelationalopt;

exprrelationalopt: relationalop exprequality | ;

relationalop: LT | GT | LE | GE;

exprequality: exprlogic exprequalityopt;

exprequalityopt: equalityop exprlogic | ;

equalityop: EQ | NEQ;

exprlogic: expradd exprlogictail;

exprlogictail: logicop expradd exprlogictail | ;

logicop: AND | OR;

expradd: exprmul expraddtail;

expraddtail: addop exprmul expraddtail | ;

addop: ADD | SUB;

exprmul: exprconcat exprmultail;

exprmultail: mulop exprconcat exprmultail | ;

mulop: MUL | DIV | IDIV | MOD;

exprconcat: exprunary exprconcattail;

exprconcattail: CONCAT exprunary exprconcattail |;

exprunary: notseq signseq exprpostfix | notseq exprpostfix;

notseq: NOT notseq | ;

signseq: sign signseq | sign;

sign: ADD | SUB;

exprpostfix: primary postfixtailopt;

postfixtailopt: postfixtail | ;

postfixtail: dotseq indexseq;

dotseq: dotop dotseq | ;

dotop: memberinvoke | memberaccess;

indexseq: indexop indexseq | ;

indexop: LSB expr RSB;

memberaccess: DOT ID;

memberinvoke: DOT ID LP arglistopt RP;

arglistopt: arglist | ;

arglist: expr arglisttail;

arglisttail: COMMA expr arglisttail | ;

primary: THIS | NIL | literal | ID | LP expr RP | arrayliteral | newexpr;

newexpr: NEW ID LP arglistopt RP;

arrayliteral: LCB arrayelement arrayliteraltailopt RCB;

arrayliteraltailopt: arrayliteraltail | ;

arrayliteraltail: COMMA arrayelement arrayliteraltail | ;

arrayelement: literal | NIL;

literal: INTLIT | FLOATLIT | STRINGLIT | TRUE | FALSE;

// ----------------------
// Types
// ----------------------

typ: primtyp | arraytyp | classtyp;

primtyp: INT | FLOAT | BOOLEAN | STRING;

arraytyp: arrayelementtyp LSB INTLIT RSB;

arrayelementtyp: primtyp | classtyp;

classtyp: ID;

// ----------------------
// Lexer rules
// ----------------------

WS : [ \t\r\n\f]+ -> skip ;

// Comments
LINE_CMT: '#' ~[\r\n]* -> skip ;
BLOCK_CMT: '/*' .*? '*/' -> skip ;

// Separators
LSB : '[' ; 
RSB : ']' ;
LCB : '{' ; 
RCB : '}' ;
LP  : '(' ; 
RP  : ')' ;
SEMI: ';' ; 
COLON: ':' ; 
DOT: '.' ; 
COMMA: ',' ;

// Operators and special symbols
ASSIGN : ':=' ;
ADD: '+' ; 
SUB: '-' ; 
MUL: '*' ; 
DIV: '/' ; 
IDIV: '\\' ; 
MOD: '%' ;
NEQ: '!=' ; 
EQ: '==' ;
LT: '<' ; 
GT: '>' ; 
LE: '<=' ; 
GE: '>=' ;
OR: '||' ; 
AND: '&&' ; 
NOT: '!' ;
CONCAT: '^' ;
TILDE: '~' ;
AMP: '&' ;

// Keywords
CLASS: 'class' ;
EXTENDS: 'extends' ;
FINAL: 'final' ;
STATIC: 'static' ;
IF: 'if' ; 
THEN: 'then' ; 
ELSE: 'else' ;
FOR: 'for' ; 
TO: 'to' ; 
DOWNTO: 'downto' ; 
DO: 'do' ;
RETURN: 'return' ;
BREAK: 'break' ; 
CONTINUE: 'continue' ;
NEW: 'new' ;
THIS: 'this' ;
NIL: 'nil' ;
BOOLEAN: 'boolean' ;
INT: 'int' ; 
FLOAT: 'float' ; 
STRING: 'string' ; 
VOID: 'void' ;
TRUE: 'true' ; 
FALSE: 'false' ;

// Identifiers
ID: [a-zA-Z_][a-zA-Z_0-9]* ;

// Integer and floating-point literals
INTLIT: DIGIT+ ;

FLOATLIT
    : DIGIT+ FRAC_DOT DIGIT* EXP?    
    | DIGIT+ EXP                 
    ;

fragment DIGIT: [0-9] ;
fragment FRAC_DOT: '.' ;
fragment EXP: [eE][+-]? DIGIT+ ;

// String literals and error handling
STRINGLIT
    : '"' STR_CHAR* '"' { self.text = self.text[1:-1] }
    ;

ILLEGAL_ESCAPE
    : '"' STR_CHAR* '\\' ~[btnfr"\\] { self.text = self.text[1:] }
    ;

UNCLOSE_STRING
    : '"' STR_CHAR* ('\r'? '\n' | EOF)
      {
        s = self.text
        if s[-1] == '\n' or s[-1] == '\r':
            self.text = s[1:]
        else:
            self.text = s[1:]
      }
    ;

fragment STR_CHAR
    : ~["\\\r\n]
    | ESC_SEQ
    ;

fragment ESC_SEQ
    : '\\' [btnfr"\\]
    ;

// Fallback for any other unexpected character
ERROR_CHAR: .;