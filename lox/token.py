from dataclasses import dataclass

from lox.token_type import TokenType


@dataclass
class Token:
	type: TokenType
	lexeme: str
	literal: object
	line: int

	def __repr__(self):
		string_token = f"{self.lexeme} \n\ttype = {self.type}"
		if self.literal:
			string_token += f"\n\tliteral: {self.literal}"
		return string_token
