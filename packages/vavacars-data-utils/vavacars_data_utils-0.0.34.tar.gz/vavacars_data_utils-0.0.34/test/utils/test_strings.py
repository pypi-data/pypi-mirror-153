from unittest import TestCase
import vava_utils.utils.strings as strings


class Test(TestCase):
    def test_extract_json_objects(self):
        test_cases = {
            'hello 123 {"a":123}': [{"a": 123}],
            '{"a":123}': [{"a": 123}],
            '1223 {"a":123} ada': [{"a": 123}],
            '1223 {"a":123} a123\n' * 10: [{"a": 123}] * 10,
            'hello 123 {"a":123}, {\'1\':1}': [{"a": 123}, {"1": 1}],
            '{a:"a"}': [{"a": "a"}],
            '{a: "a"}': [{"a": "a"}],
            '{"a":"a"}': [{"a": "a"}],
            '{"a":"a"\n,"c":"c"}': [{"a": "a", "c": "c"}],
            '123 {} {a:"a"} {': [{}, {"a": "a"}],
            '{': [],
            '{}': [{}],
            '': [],

        }

        for text, expected in test_cases.items():
            objs = list(strings.extract_json_objects(text))
            self.assertEqual(expected, objs)

    def test_extract_json_objects_exit_iterator(self):
        """
        This test force break the iteration
        Returns:

        """

        for o in strings.extract_json_objects('{"a":123} {"a":123}'):
            self.assertEqual(o, {"a": 123})
            return
