import abc
import numpy as np
from typing import List, Any, Dict, Optional, Callable

from galleries.annotations_filtering import ComparisonType, comparison_type_to_sql_operator
from galleries.annotations_filtering.filter import FilterStatement


class SqlDataRetriever:

    @abc.abstractmethod
    def get_indices(self, cursor, filters: List[List[FilterStatement]] = None):
        pass

    @abc.abstractmethod
    def get_annotations_by_index(self, cursor, index: Any) -> dict:
        pass

    @abc.abstractmethod
    def get_image_by_index(self, cursor, index: Any) -> np.ndarray:
        pass

    @abc.abstractmethod
    def get_annotations_types(self) -> Optional[Dict[str, type]]:
        pass

    @abc.abstractmethod
    def get_discrete_annotations_values(self) -> Dict[str, list]:
        pass

    @staticmethod
    def get_where_statement_from_filters(
            filters: List[List[FilterStatement]],
            annotations_keys_to_sql_keys: dict,
            annotations_types: dict,
            annotation_list_subquery: Callable
    ):
        arguments = []
        sql_and_statements = [
            SqlDataRetriever.list_of_filter_statements_to_sql_statement(
                and_statements,
                annotations_keys_to_sql_keys,
                annotations_types,
                annotation_list_subquery
            ) for and_statements in filters
        ]
        complete_sql_statement = " OR ".join(sql_and_statements)
        for and_statements in filters:
            values = [value for _, _, value, _ in and_statements]
            arguments += values
        where_statement = f"WHERE {complete_sql_statement}"
        return where_statement, arguments

    @staticmethod
    def list_of_filter_statements_to_sql_statement(
            statements: List[FilterStatement],
            annotations_keys_to_sql_keys: dict,
            annotations_types: dict,
            annotation_list_subquery: Callable
    ):
        sql_statements = [
            SqlDataRetriever.filter_statement_to_sql_statement(
                statement,
                alias_index,
                annotations_keys_to_sql_keys,
                annotations_types,
                annotation_list_subquery
            )
            for alias_index, statement in enumerate(statements)
        ]
        complete_sql_statement = " AND ".join(sql_statements)
        return f"({complete_sql_statement})"

    @staticmethod
    def filter_statement_to_sql_statement(
            statement: FilterStatement,
            alias_index: int,
            annotations_keys_to_sql_keys: dict,
            annotations_types: dict,
            annotation_list_subquery: Callable
    ):
        key, comparison_type, value, is_negated = statement
        sql_key = annotations_keys_to_sql_keys[key]
        key_type = annotations_types[key] if key in annotations_types else str
        if comparison_type != ComparisonType.CONTAINS:
            operator = comparison_type_to_sql_operator[comparison_type]
            sql_condition = f"{sql_key}{operator}?"
        elif key_type == str:
            statement.filter_value = f"%{value}%"
            sql_condition = f"{sql_key} LIKE ?"
        elif key_type == list:
            subquery = annotation_list_subquery(key, alias_index)
            sql_condition = f"? IN {subquery}"
        else:
            raise ValueError(f"Wrong filter statement {statement}")

        if is_negated:
            sql_condition = f"NOT {sql_condition}"
        return sql_condition
