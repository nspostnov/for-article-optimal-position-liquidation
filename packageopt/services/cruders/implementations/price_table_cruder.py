from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.price import Price


__all__ = ['PriceTableCRUDer']


class PriceTableCRUDer(TableCRUDerDefault):
    def __init__(self, price_table, db_connection, modelclass=Price):
        self._db_connection = db_connection

        self._table_name = price_table.get_table_name()
        self._column_names = price_table.get_column_names()
        self._column_types = price_table.get_column_types()
        self._primary_key = price_table.get_primary_key()
        self._constraints = price_table.get_constraints()

        self._key = price_table.get_key()
        self._class = modelclass
