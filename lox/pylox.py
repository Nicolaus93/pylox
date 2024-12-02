import sys

from lox.scanner import Scanner, ScannerException


class Lox:
	hadError: bool = False

	@staticmethod
	def error(line: int, message: str):
		Lox.report(line, "", message)

	@classmethod
	def report(cls, line: int, where: str, message: str):
		print(f"[line {line}] Error {where}: {message}")
		cls.hadError = True

	@classmethod
	def run(cls, source: str):
		scanner = Scanner(source)
		try:
			for token in scanner.scan_tokens():
				print(token)
		except ScannerException as err:
			cls.error(err.line, err.message)
		return

	@classmethod
	def runFile(cls, path):
		with open(path) as f:
			lines = f.readlines()

		cls.run("\n".join(lines))
		if cls.hadError:
			sys.exit(65)
		return

	@classmethod
	def runPrompt(cls):
		while True:
			print(">")
			line = input()
			if not line:
				break
			cls.run(line)
		return

	@classmethod
	def main(cls, args: list[str]):
		if len(args) > 1:
			print("Usage: pylox [script]")
			sys.exit(64)
		elif len(args) == 1:
			cls.runFile(args[0])
		else:
			cls.runPrompt()
