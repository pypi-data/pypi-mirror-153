from .base import BaseFunction
from .distance import Distance
from ..exceptions import ForsetiFunctionSyntaxError

from re import search, split as re_split


class Nearby(BaseFunction):
	def __init__(self, command: str, text: str):
		self.arguments = []
		self.left_side_argument = ""
		super().__init__(command, text)

	def check_command(self):
		if "|nearby" not in self.command:
			raise ForsetiFunctionSyntaxError("Unsupported command syntax")

		command_parts = self.command.split(" |nearby ")

		if len(command_parts) != 2:
			raise ForsetiFunctionSyntaxError("Command doesn't support combined-condition")

		self.left_side_argument, self.arguments = command_parts
		self.arguments = self.arguments.split(" | ")

	def execute(self) -> bool:
		if not search(self.left_side_argument, self.text):
			return False

		results = []

		for i in self.arguments:
			condition = self.left_side_argument + " |w0 " + i
			results.append(Distance(condition, self.text).res)

		return any(results)

	def _word_in_left_side(self, left_side_part: str, word: str) -> bool:
		pass

	def _word_in_right_side(self, right_side_part: str, word: str) -> bool:
		pass
