# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Inner Join Node

This is a SQL Query Execution Plan Node.

This performs a INNER JOIN
"""
from typing import Iterable

import numpy
import pyarrow

from opteryx import config
from opteryx.engine.attribute_types import TOKEN_TYPES
from opteryx.engine.planner.operations.base_plan_node import BasePlanNode
from opteryx.engine.query_statistics import QueryStatistics
from opteryx.exceptions import SqlError
from opteryx.third_party import pyarrow_ops
from opteryx.utils.columns import Columns


class InnerJoinNode(BasePlanNode):
    def __init__(self, statistics: QueryStatistics, **config):
        self._right_table = config.get("right_table")
        self._join_type = config.get("join_type", "CrossJoin")
        self._on = config.get("join_on")
        self._using = config.get("join_using")

    @property
    def name(self):  # pragma: no cover
        return f"Inner Join"

    @property
    def config(self):  # pragma: no cover
        return ""

    def execute(self, data_pages: Iterable) -> Iterable:

        from opteryx.engine.planner.operations import DatasetReaderNode

        if isinstance(self._right_table, DatasetReaderNode):
            self._right_table = pyarrow.concat_tables(
                self._right_table.execute(None)
            )  # type:ignore

        if self._using:

            right_columns = Columns(self._right_table)
            left_columns = None
            right_join_columns = [
                right_columns.get_column_from_alias(col, only_one=True)
                for col in self._using
            ]

            for page in data_pages:

                if left_columns is None:
                    left_columns = Columns(page)
                    left_join_columns = [
                        left_columns.get_column_from_alias(col, only_one=True)
                        for col in self._using
                    ]
                    new_metadata = left_columns + right_columns

                new_page = pyarrow_ops.inner_join(
                    self._right_table, page, right_join_columns, left_join_columns
                )
                new_page = new_metadata.apply(new_page)
                yield new_page

        elif self._on:

            right_columns = Columns(self._right_table)
            left_columns = None

            for page in data_pages:

                if left_columns is None:
                    left_columns = Columns(page)
                    try:
                        right_join_column = right_columns.get_column_from_alias(
                            self._on[2][0], only_one=True
                        )
                        left_join_column = left_columns.get_column_from_alias(
                            self._on[0][0], only_one=True
                        )
                    except SqlError:
                        # the ON condition may not always be in the order of the tables
                        right_join_column = right_columns.get_column_from_alias(
                            self._on[0][0], only_one=True
                        )
                        left_join_column = left_columns.get_column_from_alias(
                            self._on[2][0], only_one=True
                        )

                    new_metadata = right_columns + left_columns

                # do the join
                new_page = page.join(
                    self._right_table,
                    keys=[left_join_column],
                    right_keys=[right_join_column],
                    join_type="inner",
                    coalesce_keys=False,
                )
                # update the metadata
                new_page = new_metadata.apply(new_page)
                yield new_page
