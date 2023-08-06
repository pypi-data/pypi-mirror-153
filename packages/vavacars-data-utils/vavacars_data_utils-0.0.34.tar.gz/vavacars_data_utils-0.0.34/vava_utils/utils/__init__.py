from .comparisons import get_best_match, deep_get
from .callables import return_on_failure
from .strings import extract_json_objects
from .singleton import singleton

__all__ = [
    "get_best_match", "return_on_failure", "extract_json_objects", "deep_get", "singleton"
]
