# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).
import sys

import ipywidgets as widgets
from threading import Thread

from bamboolib.helper import notification, safe_cast
from bamboolib.plugins import LoaderPlugin, DF_NEW, Text, BamboolibError
from bamboolib.widgets.selectize import Singleselect

try:
    # We expect this to fail in testing & outside databricks
    from pyspark.sql import SparkSession
except ModuleNotFoundError:
    _spark = None
else:
    _spark = SparkSession.getActiveSession()

DATABASE_DOES_NOT_EXIST = "DATABASE_DOES_NOT_EXIST"
ROW_LIMIT_DEFAULT = 100_000


class DatabricksDatabaseTableLoader(LoaderPlugin):
    """
    Allows the user to load data from a databricks database table
    """

    name = "Databricks: Load database table"
    new_df_name_placeholder = "df"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._database_description = self._description("Database")
        self.database = Singleselect(
            placeholder="Database - leave empty for default database",
            width="xl",
            execute=self,
            on_change=lambda _: self._update_tables(),
        )
        self.database_error_outlet = widgets.VBox()
        self._table_description = self._description("Table")
        self.table = Singleselect(placeholder="Table", width="xl", execute=self)
        self.row_limit = Text(
            description="Row limit: read the first N rows - leave empty for no limit",
            placeholder="E.g. 1000",
            value=str(ROW_LIMIT_DEFAULT),
            width="xl",
            execute=self,
        )
        for target in (self._update_databases, self._update_tables):
            thread = Thread(target=target)
            thread.start()

    @staticmethod
    def _description(description):
        widget = widgets.HTML(description)
        widget.add_class("bamboolib-text-label")
        return widget

    def _update_databases(self):
        self.database.options = self._list_databases()

    def _update_tables(self):
        try:
            options = self._list_tables(self.database.value)
            if options is DATABASE_DOES_NOT_EXIST:
                self.table.options = []
                msg = f"Database '{self.database.value}' does not exist. Most likely the database<br>" \
                      "was recently deleted. Please select a different database."
                self.database_error_outlet.children = [notification(msg, type="error")]
            else:
                self.database_error_outlet.children = []
                self.table.options = options
        except BaseException as e:
            print(repr(e), sys.stderr)

    def _list_databases(self):
        if _spark is None:
            return []
        else:
            return [tuple.__getitem__(i, 0) for i in _spark.sql("show databases").collect()]

    def _list_tables(self, database):
        if _spark is None:
            return []
        else:
            if database is None:
                cmd = "show tables"
            elif _spark.catalog.databaseExists(database):
                cmd = f"show tables from {database}"
            else:
                return DATABASE_DOES_NOT_EXIST
            tables = _spark.sql(cmd)
            index = tables.schema.fieldNames().index("tableName")
            return [tuple.__getitem__(i, index) for i in tables.collect()]

    def is_valid_loader(self):
        if self.table.value is None:
            raise BamboolibError("No Table selected.")
        return True

    def get_exception_message(self, exception):

        if "Table or view not found" in str(exception):
            database_name = (
                self.database.value if self.database.value is not None else "default"
            )
            return notification(
                f"""We were not able to find the table <b>{self.table.value}</b> in the database <b>{database_name}</b>.<br>
                Most likely the table or database were recently deleted.<br> 
                """,
                type="error",
            )
        return None

    def render(self):
        self.set_title("Databricks: Load database table")
        if _spark is None:
            self.set_content(notification(
                f"""This feature only works within the Databricks platform but it seems like you are currently outside of Databricks.<br>
                Please only run this feature from within Databricks.""",
                type="error",
            ))
        else:
            self.set_content(
                self._database_description,
                self.database,
                self.database_error_outlet,
                self._table_description,
                self.table,
                self.spacer,
                self.row_limit,
                self.new_df_name_group,
                self.execute_button,
            )

    def get_code(self):
        database_prefix = f"{self.database.value}." if self.database.value is not None else ""

        if self.row_limit.value == "":
            row_limit_code = ""
        else:
            row_limit_code = (
                f".limit({safe_cast(self.row_limit.value, int, ROW_LIMIT_DEFAULT)})"
            )

        return f'{DF_NEW} = spark.table("{database_prefix}{self.table.value}"){row_limit_code}.toPandas()'