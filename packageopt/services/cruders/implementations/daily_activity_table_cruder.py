from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.daily_activity import DailyActivity


__all__ = ['DailyActivityTableCRUDer']


class DailyActivityTableCRUDer(TableCRUDerDefault):
    def __init__(self, daily_activity_table, db_connection):
        self._db_connection = db_connection

        self._table_name = daily_activity_table.get_table_name()
        self._column_names = daily_activity_table.get_column_names()
        self._column_types = daily_activity_table.get_column_types()
        self._primary_key = daily_activity_table.get_primary_key()
        self._constraints = daily_activity_table.get_constraints()

        self._key = daily_activity_table.get_key()
        self._class = DailyActivity
