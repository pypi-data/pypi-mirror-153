from .nearby import Nearby
from ..exceptions import ForsetiFunctionSyntaxError

import pytest


@pytest.mark.parametrize(
	"condition, text",
	[
		("|nearby", ""),
		(" |nearby ", ""),
		("", ""),
	]
)
def test_nearby_function_exceptions(condition, text):
	with pytest.raises(ForsetiFunctionSyntaxError):
		Nearby(condition, text)


@pytest.mark.parametrize(
	"condition, text, expected_result",
	[
		("Hugin, |nearby Munin", "Odin had two ravens Hugin, Munin", True),
		("Odin had son. And he was |nearby Tor | Vali | Vidar | Heimdall | Bragi | Tur", "Odin had son. And he was Tor", True),
		("Odin had son. And he was |nearby Tor | Vali | Vidar | Heimdall | Bragi | Tur", "Odin had son. And he was UNKNOWN", False),
		("elephant |nearby buy | well buy", "buy elephant", True),
		("elephant |nearby buy | well buy", "elephant buy", True),
		("elephant |nearby buy | well buy", "well buy elephant", True),
		("elephant |nearby buy | well buy", "elephant well buy", True),
	]
)
def test_nearby_function_results(condition, text, expected_result):
	assert Nearby(condition, text).res == expected_result
