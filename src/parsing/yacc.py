import ply.yacc as yacc
from tokenization.tokens import tokens
from .statements import FunctionDefinition, FunctionTypeDeclaration
from generic_functions.functions.type_casts import TypeCast
from language import EnvVariable, Identifier, ListLiteral
from frozendict import frozendict

 # ==Function==
def p_STATEMENT_TYPE_DECLARATION(s):
   "STATEMENT : TYPE_DECLARATION"
   s[0] = s[1]


# ==Function==
def p_STATEMENT_FUNCTION_DEFINITIONS(s):
   "STATEMENT : FUNCTION_DEFINITIONS"
   s[0] = s[1]

# ==Function==
def p_STATEMENT(s):
   "STATEMENT : "
   pass

# ==Function==
def p_FUNCTION_DEFINITIONS_EXPRESSION_EQUAL_EXPRESSION(s):
   "FUNCTION_DEFINITIONS : EXPRESSION EQUAL EXPRESSION"
   s[0] = [FunctionDefinition(
      name=s[1][0], 
      parameters=s[1][1:], 
      condition=None, 
      expression=s[3]
   )]

# ==Function==
def p_FUNCTION_DEFINITIONS_EXPRESSION_CASE_LIST(s):
   "FUNCTION_DEFINITIONS : EXPRESSION CASE_LIST"
   signature = s[1]

   if len(signature) == 0:
      raise Exception("Function signature should not be empty")

   if not isinstance(signature[0], Identifier):
      raise Exception("Function name should be an identifier")

   name = signature[0]
   parameters = signature[1:]

   s[0] = [FunctionDefinition(name, parameters, c[0], c[1]) for c in s[2]]

# ==Function==
def p_TYPE_DECLARATION_IDENTIFIER_DOUBLE_DOTS_TYPE_LIST(s):
   "TYPE_DECLARATION : IDENTIFIER DOUBLE_DOTS TYPE_LIST"
   s[0] = FunctionTypeDeclaration(name=s[1], type=s[3])

# ==Function==
def p_TYPE_LIST_TYPE(s):
   "TYPE_LIST : TYPE"
   s[0] = [s[1]]

# ==Function==
def p_TYPE_LIST_TYPE_ARROW_TYPE_LIST(s):
   "TYPE_LIST : TYPE ARROW TYPE_LIST"
   s[0] = [s[1]] + s[3]

# ==Function==
def p_TYPE_IDENTIFIER(s):
   "TYPE : IDENTIFIER"
   s[0] = s[1]

# ==Function==
def p_TYPE_LBRACKET_TYPE_RBRACKET(s):
   "TYPE : LBRACKET TYPE RBRACKET"
   s[0] = [s[2]]

# ==Function==
def p_CASE_LIST_CASE(s):
   "CASE_LIST : CASE"
   s[0] = [s[1]]

# ==Function==
def p_CASE_LIST_CASE_CASE_LIST(s):
   "CASE_LIST : CASE CASE_LIST"
   s[0] = [s[1]] + s[2] 

# ==Function==
def p_CASE_PIPE_EXPRESSION_EQUAL_EXPRESSION(s):
   "CASE : PIPE EXPRESSION EQUAL EXPRESSION"
   s[0] = (s[2], s[4])

# ==Function==
def p_EXPRESSION_EXPRESSION_ELEM_EXPRESSION(s):
   "EXPRESSION : EXPRESSION_ELEM EXPRESSION"
   s[0] = [s[1]] + s[2]

# ==Function==
def p_EXPRESSION_EXPRESSION_ELEM(s):
   "EXPRESSION : EXPRESSION_ELEM"
   s[0] = [s[1]]

# ==Function==
def p_EXPRESSION_ELEM_LPARANTHESIS_EXPRESSION_RPARANTHESIS(s):
   "EXPRESSION_ELEM : LPARANTHESIS EXPRESSION RPARANTHESIS"
   s[0] = s[2]

# ==Function==
def p_EXPRESSION_ELEM_VALUE(s):
   "EXPRESSION_ELEM : VALUE"
   s[0] = s[1]

# ==Function==
def p_EXPRESSION_ELEM_OPERATOR(s):
   "EXPRESSION_ELEM : OPERATOR"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_PLUS(s):
   "OPERATOR : PLUS"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_MUL(s):
   "OPERATOR : MUL"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_DIV(s):
   "OPERATOR : DIV"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_MOD(s):
   "OPERATOR : MOD"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_CONCAT(s):
   "OPERATOR : CONCAT"
   s[0] = s[1]

# ==Function==
def p_VALUE_IDENTIFIER(s):
   "VALUE : IDENTIFIER"
   s[0] = s[1]

# ==Function==
def p_VALUE_INTEGER(s):
   "VALUE : INTEGER"
   s[0] = s[1]

# ==Function==
def p_VALUE_FLOAT(s):
   "VALUE : FLOAT"
   s[0] = s[1]

# ==Function==
def p_VALUE_STRING(s):
   "VALUE : STRING"
   s[0] = s[1]

# ==Function==
def p_VALUE_ENV_VAR(s):
   "VALUE : ENV_VAR"
   s[0] = s[1]

# ==Function==
def p_VALUE_JSON(s):
   "VALUE : JSON"
   s[0] = s[1]

# ==Function==
def p_VALUE_LIST_LBRACKET_RBRACKET(s):
   "VALUE_LIST : LBRACKET RBRACKET"
   s[0] = ListLiteral([])

# ==Function==
def p_JSON_LCURLYBRACES_JSON_KV_LIST_RCURLYBRACES(s):
   "JSON : LCURLYBRACES JSON_KV_LIST RCURLYBRACES"
   s[0] = s[2]

# ==Function==
def p_JSON_KV_LIST_JSON_KV(s):
   "JSON_KV_LIST : JSON_KV"
   s[0] = s[1]

# ==Function==
def p_JSON_KV_IDENTIFIER_DOTS_JSON(s):
   "JSON_KV : IDENTIFIER DOTS JSON"
   s[0] = {s[1]: s[3]}

# ==Function==
def p_JSON_VALUE_LIST_LBRACKET_RBRACKET(s):
   "JSON_VALUE_LIST : LBRACKET RBRACKET"
   s[0] = []

# ==Function==
def p_JSON_VALUE_JSON_VALUE_LIST(s):
   "JSON_VALUE : JSON_VALUE_LIST"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_JSON(s):
   "JSON_VALUE : JSON"
   s[0] = s[1]

# ==Function==
def p_ENV_VAR_DOLLLAR_IDENTIFIER(s):
   "ENV_VAR : DOLLLAR IDENTIFIER"
   s[0] = EnvVariable(s[2].name)

# ==Function==
def p_JSON_KV_IDENTIFIER_DOTS_JSON_VALUE_LIST(s):
   "JSON_KV : IDENTIFIER DOTS JSON_VALUE_LIST"
   s[0] = {s[1].name : s[3]}

# ==Function==
def p_VALUE_VALUE_LIST(s):
   "VALUE : VALUE_LIST"
   s[0] = s[1]

# ==Function==
def p_VALUE_LIST_R(s):
   "VALUE_LIST_R : "
   s[0] = []

# ==Function==
def p_JSON_VALUE_LIST_R(s):
   "JSON_VALUE_LIST_R : "
   s[0] = []

# ==Function==
def p_OPERATOR_AND(s):
   "OPERATOR : AND"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_OR(s):
   "OPERATOR : OR"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_GREATER_THAN(s):
   "OPERATOR : GREATER_THAN"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_LESS_THAN(s):
   "OPERATOR : LESS_THAN"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_GREATER_OR_EQUAL_THAN(s):
   "OPERATOR : GREATER_OR_EQUAL_THAN"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_LESS_OR_EQUAL_THAN(s):
   "OPERATOR : LESS_OR_EQUAL_THAN"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_EQUALITY(s):
   "OPERATOR : EQUALITY"
   s[0] = s[1]

# ==Function==
def p_OPERATOR_MINUS(s):
   "OPERATOR : MINUS"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_LIST_R_COMMA_JSON_VALUE_JSON_VALUE_LIST_R(s):
   "JSON_VALUE_LIST_R : COMMA JSON_VALUE JSON_VALUE_LIST_R"
   s[0] = [s[2]]+s[3]

# ==Function==
def p_JSON_VALUE_LIST_LBRACKET_JSON_VALUE_JSON_VALUE_LIST_R_RBRACKET(s):
   "JSON_VALUE_LIST : LBRACKET JSON_VALUE JSON_VALUE_LIST_R RBRACKET"
   s[0] = [s[2]] + s[3]

# ==Function==
def p_error(t):
   raise Exception(f"Parse error at: {t}")

# ==Function==
def p_JSON_KV_LIST_JSON_KV_COMMA_JSON_KV_LIST(s):
   "JSON_KV_LIST : JSON_KV COMMA JSON_KV_LIST"
   s[0] = {**s[1], **s[3]}

# ==Function==
def p_JSON_VALUE_IDENTIFIER(s):
   "JSON_VALUE : IDENTIFIER"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_INTEGER(s):
   "JSON_VALUE : INTEGER"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_FLOAT(s):
   "JSON_VALUE : FLOAT"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_STRING(s):
   "JSON_VALUE : STRING"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_ENV_VAR(s):
   "JSON_VALUE : ENV_VAR"
   s[0] = s[1]

# ==Function==
def p_JSON_KV_IDENTIFIER_DOTS_JSON_VALUE(s):
   "JSON_KV : IDENTIFIER DOTS JSON_VALUE"
   s[0] = {s[1]: s[3]}

# ==Function==
def p_VALUE_BOOL(s):
   "VALUE : BOOL"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_BOOL(s):
   "JSON_VALUE : BOOL"
   s[0] = s[1]

# ==Function==
def p_TYPE_LPARANTHESIS_TYPE_LIST_RPARANTHESIS(s):
   "TYPE : LPARANTHESIS TYPE_LIST RPARANTHESIS"
   s[0] = s[2]

# ==Function==
def p_OPERATOR_INEQUALITY(s):
   "OPERATOR : INEQUALITY"
   s[0] = s[1]

# ==Function==
def p_JSON_VALUE_LPARANTHESIS_EXPRESSION_RPARANTHESIS(s):
   "JSON_VALUE : LPARANTHESIS EXPRESSION RPARANTHESIS"
   s[0] = s[2]

# ==Function==
def p_VALUE_TYPE_CAST(s):
   "VALUE : TYPE_CAST"
   s[0] = s[1]

# ==Function==
def p_TYPE_CAST_LESS_THAN_TYPE_LIST_GREATER_THAN(s):
   "TYPE_CAST : LESS_THAN TYPE_LIST GREATER_THAN"
   s[0] = Identifier("type_cast", metadata=frozendict({"target_type": tuple(s[2])}))

# ==Function==
def p_VALUE_LIST_LBRACKET_EXPRESSION_ELEM_VALUE_LIST_R_RBRACKET(s):
   "VALUE_LIST : LBRACKET EXPRESSION_ELEM VALUE_LIST_R RBRACKET"
   s[0] = ListLiteral([s[2]] + s[3])

# ==Function==
def p_VALUE_LIST_R_COMMA_EXPRESSION_ELEM_VALUE_LIST_R(s):
   "VALUE_LIST_R : COMMA EXPRESSION_ELEM VALUE_LIST_R"
   s[0] = [s[2]] + s[3]

# ==Final Commands==
parser = yacc.yacc()