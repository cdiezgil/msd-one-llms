from unittest.mock import MagicMock
from enum import Enum

class TrafficLight(str, Enum):
    YELLOW = "YELLOW"

m = MagicMock()
m("claude", TrafficLight.YELLOW)
try:
    m.assert_called_once_with("claude", "YELLOW")
    print("MATCHES!")
except Exception as e:
    print("ERROR:", e)
