from typing import Any

from galleries.annotations_filtering import ComparisonType


class FilterStatement:

    def __init__(self, annotation_key: str, comparison_type: ComparisonType, filter_value: Any, is_negated: bool):
        self._annotation_key = annotation_key
        self._comparison_type = comparison_type
        self._filter_value = filter_value
        self._is_negated = is_negated

    def __iter__(self):
        return iter([self._annotation_key, self._comparison_type, self._filter_value, self._is_negated])

    @property
    def annotation_key(self):
        return self._annotation_key

    @annotation_key.setter
    def annotation_key(self, value):
        self._annotation_key = value

    @property
    def filter_value(self):
        return self._filter_value

    @filter_value.setter
    def filter_value(self, value):
        self._filter_value = value

    @property
    def comparison_type(self):
        return self._comparison_type

    @comparison_type.setter
    def comparison_type(self, value):
        self._comparison_type = value

    @property
    def is_negated(self):
        return self._is_negated

    @is_negated.setter
    def is_negated(self, value):
        self._is_negated = value


if __name__ == '__main__':
    f = FilterStatement('asd', ComparisonType.EQUAL, 1, True)
    (a, b, c, d) = f
    print(a, b, c, d)
