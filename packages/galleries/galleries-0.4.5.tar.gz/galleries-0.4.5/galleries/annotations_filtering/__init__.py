import enum


class ComparisonType(enum.Enum):
    EQUAL = 0
    NOTEQUAL = 1
    LESS = 2
    GREATER = 3
    GREATER_EQUAL = 4
    LESS_EQUAL = 5
    CONTAINS = 6


data_type_to_comparison_type = {
    bool: [
        ComparisonType.EQUAL,
        ComparisonType.NOTEQUAL
    ],
    int: [
        ComparisonType.EQUAL,
        ComparisonType.NOTEQUAL,
        ComparisonType.LESS,
        ComparisonType.GREATER,
        ComparisonType.GREATER_EQUAL,
        ComparisonType.LESS_EQUAL
    ],
    float: [
        ComparisonType.EQUAL,
        ComparisonType.NOTEQUAL,
        ComparisonType.LESS,
        ComparisonType.GREATER,
        ComparisonType.GREATER_EQUAL,
        ComparisonType.LESS_EQUAL
    ],
    str: [
        ComparisonType.EQUAL,
        ComparisonType.NOTEQUAL,
        ComparisonType.CONTAINS,
    ],
    list: [
        ComparisonType.CONTAINS,
    ]
}


def equal_func(a, b) -> bool:
    return a == b


def not_equal_func(a, b) -> bool:
    return a != b


def less_func(a, b) -> bool:
    return a < b


def less_equal_func(a, b) -> bool:
    return a <= b


def greater_func(a, b) -> bool:
    return a > b


def greater_equal_func(a, b) -> bool:
    return a >= b


def contains_func(l: list, a) -> bool:
    return a in l


comparison_type_functions = {
    ComparisonType.EQUAL: equal_func,
    ComparisonType.NOTEQUAL: not_equal_func,
    ComparisonType.LESS: less_func,
    ComparisonType.GREATER: greater_func,
    ComparisonType.GREATER_EQUAL: greater_equal_func,
    ComparisonType.LESS_EQUAL: less_equal_func,
    ComparisonType.CONTAINS: contains_func,
}


comparison_type_to_sql_operator = {
    ComparisonType.EQUAL: "==",
    ComparisonType.NOTEQUAL: "==",
    ComparisonType.LESS: "<",
    ComparisonType.GREATER: ">",
    ComparisonType.GREATER_EQUAL: ">=",
    ComparisonType.LESS_EQUAL: "<=",
}
