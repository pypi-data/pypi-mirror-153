import yaml
import typing


def extract_json_objects(text) -> typing.Generator[typing.Dict, None, None]:
    """
    Find JSON objects in text, and yield the decoded JSON data.
    Does not attempt to look for JSON arrays, text, or other JSON types outside a parent JSON object.
    Args:
        text: the text where the function will look for the jsons
    Returns: Dicts found in text
    """
    pos = 0
    start_pos = text.find('{', 0)
    while start_pos >= 0:
        for pos in range(start_pos, len(text)):
            try:
                yield yaml.full_load(text[start_pos:pos + 1].replace(':"', ': "'))
                break
            except Exception:
                pass

        start_pos = text.find('{', pos + 1)
