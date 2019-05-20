#! /usr/bin/python3


import re, sys, string

debug = False
state = { }
tokens = [ ]
tm = { }


#  Expression class and its subclasses
class Expression( object ):
	def __str__(self):
		return ""

class BinaryExpr( Expression ):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right

	def meaning(self, state):
		if state.check_key(str(self.left)):#checks to see if self.left is a key
			left = state.most_terminal(self.left)
			if state.check_key(str(self.right)):
				right = state.most_terminal(self.right)#checks right
				return eval(str(left) + self.op + str(right))
			return eval(str(left) + self.op + str(self.right))#if left isn't a key but right is.
		elif state.check_key(self.right): #checks right to make sure it isn't a key
			return eval(str(str.left) + self.op + str(right))
		elif self.op == "or":
			if self.left.meaning(state) or self.right.meaning(state):
				return self.left.meaning(state) or self.right.meaning(state)
		elif self.op == "and":
			if self.left.meaning(state) and self.right.meaning(state):
				return self.left.meaning(state) and self.right.meaning(state)
		else:
			return eval(str(self.left) + self.op + str(self.right))

	def tipe(self, tm):

		if tm.check_key(str(self.left)):
			left = tm.fetch(str(self.left))
		elif re.match(Lexer.number, str(self.left)):
			left = "number"
		else:
			tm.ref_error(str(self.left))
			left = tm.fetch(str(self.left))

		if tm.check_key(str(self.right)):
			right = tm.fetch(str(self.right))
		elif re.match(Lexer.number, str(self.right)):
			right = "number"
		else:
			tm.ref_error(str(self.right))
			right = tm.fetch(str(self.right))

		if left == right and left != "boolean":
			if re.match(Lexer.relational, self.op):
				return "boolean"
			else:
				return "number"
		elif left == right and left == "boolean":
			if self.op == "or" or self.op == "and":
				return "boolean"
			else:
				return "TypeError: boolean " + self.op + "boolean"
		elif left != right:
			return "TypeError: Invalid Expression"



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

class Meaning( Expression ):# Dont actually need this, but can use stuff from it
	def __init__(self):
		self.dict = { }

	def add_key(self, Value):
		self.dict[Value] = "undef"

	def check_key(self, Value):
		if debug: print("Value: " + str(Value))
		if Value in self.dict:
			if debug: print("Returning True")
			return True
		else:
			if debug: print("Returning False")
			return False

	def update(self, Value, Wanted_term):
		term = self.most_terminal(Wanted_term)
		self.dict[Value] = term

	def most_terminal(self, term):
		referenced_val = True
		if str(term) in self.dict:
			referenced_val = False
		while referenced_val == False:
			term = self.dict[str(term)]
			if str(term) in self.dict:
				referenced_val = False
			else:
				referenced_val = True
		return term

	def __str__(self):
		meaningful_statment = "{"
		printed_terms = 0
		for d in self.dict:
			printed_terms = printed_terms + 1
			if printed_terms < len(self.dict):
				meaningful_statment = meaningful_statment + "<" + str(d) + ", " + str(self.dict[d]) + ">, "
			else:
				meaningful_statment = meaningful_statment + "<" + str(d) + ", " + str(self.dict[d]) + ">"
		meaningful_statment = meaningful_statment + "}"
		return meaningful_statment

class Typing( Expression ):
	def __init__(self):
		self.dict = { }
		self.dict_e = { }

	def typed(self, Value, Tipe):
		if debug: print("Tipe: " + str(Tipe))
		if (Tipe == "number" or Tipe == "boolean"):
			self.dict[Value] = Tipe
			if debug: print("Value of Key: " + str(Value) + "\nDict Value: " + self.dict[Value])
		elif str(Tipe) in self.dict:
			self.dict[Value] = self.dict[str(Tipe)]
			if debug: print("Value of Key: " + str(Value) + "\nDict Value: " + self.dict[Value])
		elif isinstance(Tipe, Number):
			self.dict[Value] = "number"
			if debug: print("Value of Key: " + str(Value) + "\nDict Value: " + self.dict[Value])
			#elif re.match(Lexer.identifier, Tipe):
			#	self.dict[Value] = "TypeError: " + Tipe + "is referenced before being defined!"
			#elif re.match(Lexer.string, Tipe):
			#	self.dict[Value] = "TypeError: " + Tipe + "is referenced before being defined!"
		else:
			self.dict[Value] = Tipe #"TypeError: Invalid assignment to " + str(Value)

	def ref_error(self, Value):
		if re.match(Lexer.identifier, str(Value)):
			self.dict[Value] = "TypeError: " + str(Value) + " is referenced before being defined!"
		elif re.match(Lexer.string, str(Value)):
			self.dict[Value] = "TypeError: " + str(Value) + " is referenced before being defined!"

	def check_key(self, Value):
		if debug: print("Value: " + str(Value))
		if Value in self.dict:
			if debug: print("Returning True")
			return True
		else:
			if debug: print("Returning False")
			return False

	def fetch(self, Value):
		if debug: print("Value: " + str(Value))
		return self.dict[Value]

		#def two_key(self, Value, Other_Value):
			#self.dict[Value] = self.dict[Other_Value]

	def p_error(self, Value, Maybe_error):
		#if (self.dict[Value] == "number" or self.dict[Value] == "boolean"):
		if str(Maybe_error) not in self.dict:
			if self.dict[Value] != Maybe_error:
				if debug: print("There was an error")
				if Value in self.dict_e:
					return
				else:
					self.dict_e[Value] = "TypeError: " + self.dict[Value] + " = " + Maybe_error + "!"
					if debug: print("Value: " + Value + "\nDict Value: " + self.dict_e[Value])


	def number(self, Value):
		self.dict[Value] = "number"


	def __str__(self):
		many_types = ""
		errors = ""
		for d in self.dict:
			if str(self.dict[d]) != "number" and str(self.dict[d]) != "boolean":
				errors = errors + self.dict[d] + "\n"
			else:
				many_types = many_types + str(d) + " " + self.dict[d] + "\n"
		for d in self.dict_e:
			errors = errors + self.dict_e[d] + "\n"
		return many_types + errors


##----------------------Identifier class and potential subclasses----------
class Statement( object ):
	def __str__(self):
		return ""

class StmtList( Statement ):#should create a list of statements
	def __init__(self):
		self.list = []

	def addStatement(self, statement):
		self.list.append(statement)

	def meaning(self, state):#p3
		for i in range(0,len(self.list)):
			self.list[i].meaning(state)

	def tipe(self, tm):#p4
		for i in range(0,len(self.list)):
			self.list[i].tipe(tm)

	def __str__(self):
		listed_statement = ""
		for i in range(0,len(self.list)):
			listed_statement = listed_statement + str(self.list[i])
		return listed_statement

class Assign( Statement ):
	def __init__(self, ident, expres):
		self.identifier = ident
		self.expression = expres

	def meaning(self, state):#p3
		equation = self.expression
		if isinstance(self.expression, BinaryExpr):
			equation = self.expression.meaning(state)
		if state.check_key(self.identifier):
			state.update(self.identifier, equation)
		else:
			state.add_key(self.identifier)
			state.update(self.identifier, equation)

	def tipe(self, tm):#p4
		equation = self.expression
		if isinstance(self.expression, BinaryExpr):
			equation = self.expression.tipe(tm)
		if tm.check_key(self.identifier):
			if debug: print("Equation: " + str(equation))
			tm.p_error(self.identifier, equation)#checks to make sure the key and equation are the same
		else:
			if debug: print("Checking for Error: " + str(self.identifier))
			tm.typed(self.identifier, equation)#assigns a type to the key


	def __str__(self):
		return "= {} {}\n".format(str(self.identifier), str(self.expression))

class IfStmt( Statement ):
	def __init__(self, ifexpr, if_statement, else_statement):
		self.expression = ifexpr
		self.ifstate = if_statement
		self.elsestate = else_statement

	def meaning(self, state):#p3
		if self.expression.meaning(state):
			self.ifstate.meaning(state)
		else:
			if self.elsestate != 0:
				self.elsestate.meaning(state)

	def tipe(self, tm):#p4
		if isinstance(self.expression, BinaryExpr):
			self.expression.tipe(tm)
		elif tm.check_key(str(self.expression)) == False:
			tm.ref_error(str(self.expression))

		self.ifstate.tipe(tm)
		if self.elsestate != 0:
			self.elsestate.tipe(tm)

	def __str__(self):
		if (self.elsestate == 0):
			return "if {}\n".format(str(self.expression)) + "{}".format(str(self.ifstate)) + "endif\n"
		else:
			return "if {}\n".format(str(self.expression)) + "{}".format(str(self.ifstate)) + "else\n{}".format(str(self.elsestate)) + "endif\n"

class WhileStmt( Statement ):
	def __init__(self, while_ex, while_statement):
		self.w_hile = while_ex
		self.wstat = while_statement

	def meaning(self, state):#p3
		while self.w_hile.meaning(state):
			self.wstat.meaning(state)

	def tipe(self, tm):#4
		if isinstance(self.w_hile, BinaryExpr):
			self.w_hile.tipe(tm)
		elif tm.check_key(str(self.w_hile)) == False:
			tm.ref_error(str(self.w_hile))
		self.wstat.tipe(tm)

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

#----------------Block Meaning Function------------------------

#def block_meaning():#p3

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
	global state
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
	while(re.match(Lexer.relational, tok)):
		tokens.next()
		right = addExpr()
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek()#just added
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

def parse( text ) : #Everything starts here
	global tokens
	global state
	global type
	tokens = Lexer( text )
	type = Typing()
	#state = Meaning()
	#expr = addExpr( )
	#print (str(expr))
	#     Or:
	stmtlist = parseStmtList( tokens )
	#print(str(stmtlist))
	#print(str(state))
	print(type)
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
		#assign.meaning(state)#p3
		assign.tipe(type)
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
		w_statement = WhileStmt(w_expr, w_block)
		#w_statement.meaning(state)#p3
		w_statement.tipe(type)
		return w_statement

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
		if_statement = IfStmt(if_expr, if_block, 0)
		#if_statement.meaning(state)#p3
		if_statement.tipe(type)#p4
		return if_statement
	else:
		tokens.next()
		else_block = parseBlock()
		if_statement = IfStmt(if_expr, if_block, else_block)
		#if_statement.meaning(state)#p3
		if_statement.tipe(type)#p4
		return if_statement



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
