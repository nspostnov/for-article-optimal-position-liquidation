from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.vola import Vola


__all__ = ['VolaTableCRUDer']


class VolaTableCRUDer(TableCRUDerDefault):
    def __init__(self, vola_table, db_connection, 
            modelclass=Vola):
        self._db_connection = db_connection

        self._table_name = vola_table.get_table_name()
        self._column_names = vola_table.get_column_names()
        self._column_types = vola_table.get_column_types()
        self._primary_key = vola_table.get_primary_key()
        self._constraints = vola_table.get_constraints()

        self._key = vola_table.get_key()
        self._class = modelclass
