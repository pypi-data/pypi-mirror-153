from typing import List

from galleries.annotations_filtering import comparison_type_functions
from galleries.annotations_filtering.filter import FilterStatement


def does_annotations_meets_filter(annotations: dict, filters: List[List[FilterStatement]]):
    met_any = False or len(filters) == 0
    for and_conditions in filters:
        met_all = True
        for statement in and_conditions:
            annotation_key, comparison_type, value, is_negated = statement
            annotation_value = annotations[annotation_key]
            comparison_function = comparison_type_functions[comparison_type]
            met_condition = comparison_function(annotation_value, value)
            met_condition ^= is_negated
            met_all &= met_condition
        met_any |= met_all
    return met_any
