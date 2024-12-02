from lox.token import Token
from lox.token_type import TokenType


class ScannerException(Exception):
	def __init__(self, line: int, message: str):
		self.line = line
		self.message = message


class Scanner:
	keywords: dict[str, TokenType] = {
		"and": TokenType.AND,
		"class": TokenType.CLASS,
		"else": TokenType.ELSE,
		"false": TokenType.FALSE,
		"for": TokenType.FOR,
		"fun": TokenType.FUN,
		"if": TokenType.IF,
		"nil": TokenType.NIL,
		"or": TokenType.OR,
		"print": TokenType.PRINT,
		"return": TokenType.RETURN,
		"super": TokenType.SUPER,
		"this": TokenType.THIS,
		"true": TokenType.TRUE,
		"var": TokenType.VAR,
		"while": TokenType.WHILE,
	}

	def __init__(self, source: str):
		self.source = source
		self.tokens: list[Token] = list()
		self.start: int = 0
		self.current: int = 0
		self.line: int = 1

	def scan_tokens(self) -> list[Token]:
		while not self.is_at_end():
			self.start = self.current
			self.scan_token()

		self.tokens.append(Token(TokenType.EOF, "", None, self.line))
		return self.tokens

	def is_at_end(self) -> bool:
		return self.current >= len(self.source)

	def advance(self) -> str:
		c = self.source[self.current]
		self.current += 1
		return c

	def add_token(
		self, token_type: TokenType, literal: object | None = None
	) -> None:
		text = self.source[self.start : self.current]
		self.tokens.append(Token(token_type, text, literal, self.line))

	def match(self, expected: str):
		if self.is_at_end():
			return False
		if self.source[self.current] != expected:
			return False

		self.current += 1
		return True

	def peek(self):
		if self.is_at_end():
			return "\0"
		return self.source[self.current]

	def peek_next(self):
		if self.current + 1 >= len(self.source):
			return "\0"
		return self.source[self.current + 1]

	def string(self) -> None:
		while self.peek() != '"' and not self.is_at_end():
			if self.peek() == "\n":
				# multi-line string
				self.line += 1
			self.advance()

		if self.is_at_end():
			raise ScannerException(self.line, "Unterminated string")

		self.advance()  # the closing "

		# trim the surrounding quotes
		value: str = self.source[self.start + 1 : self.current - 1]
		self.add_token(TokenType.STRING, value)

	@staticmethod
	def is_digit(c: str) -> bool:
		return "0" <= c <= "9"

	@staticmethod
	def is_alpha(c: str) -> bool:
		return "a" <= c <= "z" or "A" <= c <= "Z" or c == "_"

	def is_alphanumeric(self, c: str) -> bool:
		return self.is_alpha(c) or self.is_digit(c)

	def number(self) -> None:
		while self.is_digit(self.peek()):
			self.advance()

		if self.peek() == "." and self.is_digit(self.peek_next()):
			# consume the '.'
			self.advance()
			while self.is_digit(self.peek()):
				self.advance()

			self.add_token(
				TokenType.NUMBER, float(self.source[self.start : self.current])
			)

	def identifier(self) -> None:
		while self.is_alphanumeric(self.peek()):
			self.advance()

		text: str = self.source[self.start : self.current]
		t_type: TokenType = self.keywords.get(text)
		if not t_type:
			t_type = TokenType.IDENTIFIER
		self.add_token(t_type)

	def scan_token(self):
		c = self.advance()
		match c:
			case "(":
				self.add_token(TokenType.LEFT_PAREN)
			case ")":
				self.add_token(TokenType.RIGHT_PAREN)
			case "{":
				self.add_token(TokenType.LEFT_BRACE)
			case "}":
				self.add_token(TokenType.RIGHT_BRACE)
			case ",":
				self.add_token(TokenType.COMMA)
			case ".":
				self.add_token(TokenType.DOT)
			case "-":
				self.add_token(TokenType.MINUS)
			case "+":
				self.add_token(TokenType.PLUS)
			case ";":
				self.add_token(TokenType.SEMICOLON)
			case "*":
				self.add_token(TokenType.STAR)
			case "!":
				self.add_token(
					TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
				)
			case "=":
				self.add_token(
					TokenType.EQUAL_EQUAL
					if self.match("=")
					else TokenType.EQUAL
				)
			case "<":
				self.add_token(
					TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
				)
			case ">":
				self.add_token(
					TokenType.GREATER_EQUAL
					if self.match("=")
					else TokenType.GREATER
				)
			case "/":
				if self.match("/"):
					while self.peek() != "\n" and not self.is_at_end():
						self.advance()
				else:
					self.add_token(TokenType.SLASH)
			case " " | "\r" | "\t":
				pass
			case "\n":
				self.line += 1
			case '"':
				self.string()
			case _:
				if self.is_digit(c):
					self.number()
				elif self.is_alpha(c):
					self.identifier()
				else:
					raise ScannerException(self.line, "Unexpected character")
		return
