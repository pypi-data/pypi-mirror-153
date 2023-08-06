from .base import BaseFunction
from ..exceptions import ForsetiFunctionSyntaxError

from typing import Tuple
from re import search, split as re_split, finditer


class Distance(BaseFunction):
	COMMAND_FORMAT = r'\s\|[cw]?\d+\s'

	def __init__(self, command: str, text: str):
		self.left_argument = ""
		self.right_argument = ""
		self.distance = -1
		self.f_exclude_right_argument = False

		super().__init__(command, text)

	def check_command(self):
		if bool(search(self.COMMAND_FORMAT, self.command)):
			parts = re_split(self.COMMAND_FORMAT, self.command)

			if len(parts) != 2:
				raise ForsetiFunctionSyntaxError("Command doesn't support combined-condition")

			command_to_exec = search(self.COMMAND_FORMAT, self.command).group(0).strip()

			if 'c' in command_to_exec or 'w' in command_to_exec:
				_p = 2
			else:
				_p = 1

			self.distance = int(command_to_exec[_p:])
			self.left_argument, self.right_argument = parts

			if self.right_argument[0] == '-':
				self.right_argument = self.right_argument[1:]
				self.f_exclude_right_argument = True

		else:
			raise ForsetiFunctionSyntaxError("Unsupported command format. You must use: {word1} [|c{number} or |w{number}] {word2}")

	def execute(self) -> bool:
		if "|w" in self.command:
			return self._by_words()

		elif "|c" in self.command:
			return self._by_characters()

		else:
			return self._by_words()

	def _by_words(self) -> bool:
		if not self._parts_in_text():
			return False

		text_by_words = self.text.split()
		words_number = len(text_by_words)
		words_in_arguments = len(self.left_argument.split()) + len(self.right_argument.split())
		words_in_arguments += self.left_argument.count('\s') + self.right_argument.count('\s')

		for i in range(words_number):
			text_part = ' '.join(text_by_words[i:i+words_in_arguments+self.distance])

			if search(self.left_argument, text_part) and search(self.right_argument, text_part):
				return True

		return False

	def _by_characters(self) -> bool:
		if not self._parts_in_text():
			return False

		def check_pair_distance(pair_1: Tuple[int, int], pair_2: Tuple[int, int]) -> bool:
			pairs = ((pair_1[0], pair_2[1]), (pair_1[1], pair_2[0]))

			if max(pairs[0]) - min(pairs[0]) <= self.distance or max(pairs[1]) - min(pairs[1]) <= self.distance:
				return True

			return False

		left_argument_positions = list(map(lambda x: (x.start(), x.end()), finditer(self.left_argument, self.text)))
		right_argument_positions = list(map(lambda x: (x.start(), x.end()), finditer(self.right_argument, self.text)))

		for i in left_argument_positions:
			if any(map(lambda x: check_pair_distance(i, x), right_argument_positions)):
				return True

		return False

	def _parts_in_text(self) -> bool:
		return bool(search(self.left_argument, self.text) and search(self.right_argument, self.text))
