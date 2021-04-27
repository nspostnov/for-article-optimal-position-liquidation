from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.lob import LOB


__all__ = ['LOBTableCRUDer']


class LOBTableCRUDer(TableCRUDerDefault):
    def __init__(self, lob_table, db_connection, modelclass=LOB):
        self._db_connection = db_connection

        self._table_name = lob_table.get_table_name()
        self._column_names = lob_table.get_column_names()
        self._column_types = lob_table.get_column_types()
        self._primary_key = lob_table.get_primary_key()
        self._constraints = lob_table.get_constraints()

        self._key = lob_table.get_key()
        self._class = modelclass
