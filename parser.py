#! /usr/bin/python3


import re, sys, string

debug = False
dict = { }
tokens = [ ]


#  Expression class and its subclasses
class Expression( object ):
	def __str__(self):
		return ""

class BinaryExpr( Expression ):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right

	def __str__(self):
		return str(self.op) + " " + str(self.left) + " " + str(self.right)

class Number( Expression ):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return str(self.value)

class String( Expression ): #class for a string
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return str(self.value)

class VarRef( Expression ): #class for anything else I guess.
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return str(self.value)

##----------------------Identifier class and potential subclasses----------
class Statement( object ):
	def __str__(self):
		return ""

class StmtList( Statement ):#should create a list of statements
	def __init__(self):
		self.list = []

	def addStatement(self, statement):
		self.list.append(statement)

	def __str__(self):
		listed_statement = ""
		for i in range(0,len(self.list)):
			listed_statement = listed_statement + str(self.list[i])
		return listed_statement

class Assign( Statement ):
	def __init__(self, ident, expres):
		self.identifier = ident
		self.expression = expres

	def __str__(self):
		return "= {} {}\n".format(str(self.identifier), str(self.expression))

class IfStmt( Statement ):
	def __init__(self, ifexpr, if_statement, else_statement):
		self.expression = ifexpr
		self.ifstate = if_statement
		self.elsestate = else_statement

	def __str__(self):
		if (self.elsestate == 0):
			return "if {}\n".format(str(self.expression)) + "{}".format(str(self.ifstate)) + "endif\n"
		else:
			return "if {}\n".format(str(self.expression)) + "{}".format(str(self.ifstate)) + "else\n{}".format(str(self.elsestate)) + "endif\n"

class WhileStmt( Statement ):
	def __init__(self, while_ex, while_statement):
		self.w_hile = while_ex
		self.wstat = while_statement

	def __str__(self):
		return "while {}\n".format(str(self.w_hile)) + "{}".format(str(self.wstat)) + "endwhile\n"



def error( msg ):
	#print msg
	sys.exit(msg)

# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.

#-------------Not gonna touch match----------------------
def match(matchtok):
	tok = tokens.peek( )
	if (tok != matchtok): error("Expecting "+ matchtok)
	tokens.next( )
	return tok
#----------------Check these given functions-------------


def factor( ):
	"""factor     = number | string | ident |  '(' expression ')' """

	tok = tokens.peek( )
	if debug: print ("Factor: ", tok)
	if re.match(Lexer.number, tok):
		expr = Number(tok)
		tokens.next( )
		return expr
	#--------------Not given, added by me-------------
	if re.match(Lexer.identifier, tok):
		expr = VarRef(tok)
		tokens.next()
		#if debug:
		#	tok = tokens.peek()
		#	print("After factor ident: ", tok)
		return expr

	if re.match(Lexer.string, tok):
		expr = String()
		tokens.next()
		return expr
		
	#--------------------------------------------------
	if tok == "(":
		tokens.next( )  # or match( tok )
		expr = addExpr( )
		tokens.peek( )
		tok = match(")")
		return expr
	error("Invalid operand")
	return


def term( ):
	""" term    = factor { ('*' | '/') factor } """

	tok = tokens.peek( )
	if debug: print ("Term: ", tok)
	left = factor( )
	tok = tokens.peek( )
	while tok == "*" or tok == "/":
		tokens.next()
		right = factor( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

def addExpr( ):
	""" addExpr    = term { ('+' | '-') term } """

	tok = tokens.peek( )
	if debug: print ("addExpr: ", tok)
	left = term( )
	tok = tokens.peek( )
	while tok == "+" or tok == "-":
		tokens.next()
		right = term( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

#---------------------Nonterminal Expressions--------------------

def expression():
	""" expression = andExpr { "or" andExpr }"""
	tok = tokens.peek()
	if debug: print("expression: ", tok)
	left = andExpr()
	tok = tokens.peek()
	while(tok == "or"):
		tokens.next()
		right = andExpr()
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek()
	return left


def andExpr():
	""" andExpr = relationalExpr { "and" relationalExpr } """
	tok = tokens.peek()
	if debug: print("andExpr: ", tok)
	left = relationalExpr()
	tok = tokens.peek()
	while(tok == "and"):
		tokens.next()
		right = relationalExpr()
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek()
	return left

def relationalExpr():
	""" addExpr [ relation addExpr] """
	tok = tokens.peek()
	if debug: print("relationalExpr: ", tok)
	left = addExpr()
	tok = tokens.peek()
	if(re.match(Lexer.relational, tok)):
		tokens.next()
		right = andExpr()
		left = BinaryExpr(tok, left, right)
	return left

#---------------------Things I need to Fix------------------------
def parseStmtList( statment ):
	""" gee = { Statement } """
	tok = tokens.peek( )
	ast = StmtList()
	while tok is not None and tok is not "~":
        # need to store each statement in a list
		statement = parseStmt()
		ast.addStatement(statement) #stored each statment to a list
		tok = tokens.peek()
		if debug: print("Parsed Statement list: \n" + str(ast))
	return ast

def parse( text ) :
	global tokens
	tokens = Lexer( text )
	#expr = addExpr( )
	#print (str(expr))
	#     Or:
	stmtlist = parseStmtList( tokens )
	print(str(stmtlist))
	return

#---------------------Nonterimanl Statments----------------------
def parseStmt():
	""" statement = ifStatement | whileStatment | assign """
	tok = tokens.peek()
	if debug: print("Statement: ", tok)

	if (tok == "if"):
		statement = parseIf()
		return statement

	elif (tok == "while"):
		statement = parseWhile()
		return statement

	elif (re.match(Lexer.identifier, tok)):
		statement = parseAssign()
		return statement

	else:#everything has failed and should kill the program.
		error("Statement failed")
		return


def parseAssign():
	""" assign = ident "=" expression eoln """
	left = tokens.peek() #this should be the the variable being assigned
	if debug: print("Assign: ", left)
	tokens.next()
	tok = tokens.peek()
	if (tok != "="):
		error("No = when assigning expr to identifier")
		return
	else:
		tokens.next()
		right = expression() #assigns right to the expression to be parsed to left
		tok = tokens.peek()
	if (tok != ";"):
		error("No ; at the end of the assigning expression")
		return
	else:
		assign = Assign(left, right)
		tokens.next()
		return assign


def parseWhile():
	""" whileStatement = "while" expression block """
	tokens.next()#advances past the "while" token
	w_expr = expression()
	tok = tokens.peek()
	if (tok != ":"):
		error("While loop has no blocker")
		return
	else:
		w_block = parseBlock()
		#tokens.next()
		return WhileStmt(w_expr, w_block)

def parseBlock():
	""" block = ":" eoln indent stmtList undent """
	tokens.next()
	tok = tokens.peek()
	if debug: print("Block: ", tok)#should always be ";"

	if (tok != ";"):
		error("statment does not have ; after :")
		return

	tokens.next()
	tok = tokens.peek()
	if (tok != "@"):
		error("statment is not indented after eoln")
		return

	tokens.next()
	tok = tokens.peek()
	block_list = parseStmtList(tok)#parses the list of statments in while or if block
	if debug:
		tok = tokens.peek()
		print("Before block next: ", tok)
	#if (tok != "~"):
		#error("No undent after block")
		#return
	tokens.next()#iterates to the undent after the list
	if debug:
		tok = tokens.peek()
		print("After block next: ", tok)
	tok = tokens.peek()
	#if (tok != "~"): original location
		#error("No undent after block")
		#return

	return block_list


def parseIf():
	""" ifStatment = "if" expression block [ "else" block ] """
	tokens.next()
	tok = tokens.peek()
	if debug: print("If: ", tok)

	if_expr = expression()
	tok = tokens.peek()
	if (tok !=":"):
		error("Expression does not have a block")
		return
	if_block =  parseBlock()
	tok = tokens.peek()
	if (tok != "else"): #checks for else block
		#tokens.next()
		return IfStmt(if_expr, if_block, 0)
	else:
		tokens.next()
		else_block = parseBlock()
		return IfStmt(if_expr, if_block, else_block)



#-----------------------------------------------------------------




# Lexer, a private class that represents lists of tokens from a Gee
# statement. This class provides the following to its clients:
#
#   o A constructor that takes a string representing a statement
#       as its only parameter, and that initializes a sequence with
#       the tokens from that string.
#
#   o peek, a parameterless message that returns the next token
#       from a token sequence. This returns the token as a string.
#       If there are no more tokens in the sequence, this message
#       returns None.
#
#   o removeToken, a parameterless message that removes the next
#       token from a token sequence.
#
#   o __str__, a parameterless message that returns a string representation
#       of a token sequence, so that token sequences can print nicely

class Lexer :


	# The constructor with some regular expressions that define Gee's lexical rules.
	# The constructor uses these expressions to split the input expression into
	# a list of substrings that match Gee tokens, and saves that list to be
	# doled out in response to future "peek" messages. The position in the
	# list at which to dole next is also saved for "nextToken" to use.

	special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"
	relational = "<=?|>=?|==?|!="
	arithmetic = "\+|\-|\*|/"
	#char = r"'."
	string = r"'[^']*'" + "|" + r'"[^"]*"'
	number = r"\-?\d+(?:\.\d+)?"
	literal = string + "|" + number
	#idStart = r"a-zA-Z"
	#idChar = idStart + r"0-9"
	#identifier = "[" + idStart + "][" + idChar + "]*"
	identifier = "[a-zA-Z]\w*"
	lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier

	def __init__( self, text ) :
		self.tokens = re.findall( Lexer.lexRules, text )
		self.position = 0
		self.indent = [ 0 ]


	# The peek method. This just returns the token at the current position in the
	# list, or None if the current position is past the end of the list.

	def peek( self ) :
		if self.position < len(self.tokens) :
			return self.tokens[ self.position ]
		else :
			return None


	# The removeToken method. All this has to do is increment the token sequence's
	# position counter.

	def next( self ) :
		self.position = self.position + 1
		return self.peek( )


	# An "__str__" method, so that token sequences print in a useful form.

	def __str__( self ) :
		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"



def chkIndent(line):
	ct = 0
	for ch in line:
		if ch != " ": return ct
		ct += 1
	return ct


def delComment(line):
	pos = line.find("#")
	if pos > -1:
		line = line[0:pos]
		line = line.rstrip()
	return line

def mklines(filename):
	inn = open(filename, "r")
	lines = [ ]
	pos = [0]
	ct = 0
	for line in inn:
		ct += 1
		line = line.rstrip( )+";"
		line = delComment(line)
		if len(line) == 0 or line == ";": continue
		indent = chkIndent(line)
		line = line.lstrip( )
		if indent > pos[-1]:
			pos.append(indent)
			line = '@' + line
		elif indent < pos[-1]:
			while indent < pos[-1]:
				del(pos[-1])
				line = '~' + line
		print (ct, "\t", line)
		lines.append(line)
	# print len(pos)
	undent = ""
	for i in pos[1:]:
		undent += "~"
	lines.append(undent)
	# print undent
	return lines



def main():
	"""main program for testing"""
	global debug
	ct = 0
	for opt in sys.argv[1:]:
		if opt[0] != "-": break
		ct = ct + 1
		if opt == "-d": debug = True
	if len(sys.argv) < 2+ct:
		print ("Usage:  %s filename" % sys.argv[0])
		return
	parse("".join(mklines(sys.argv[1+ct])))
	return

#execute program: python parser.py testfilename.txt

main()
