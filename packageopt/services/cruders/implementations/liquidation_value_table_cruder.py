from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.liquidation_value import LiquidationValue


__all__ = ['LiquidationValueTableCRUDer']


class LiquidationValueTableCRUDer(TableCRUDerDefault):
    def __init__(self, liquidation_value_table, db_connection, 
            modelclass=LiquidationValue):
        self._db_connection = db_connection

        self._table_name = liquidation_value_table.get_table_name()
        self._column_names = liquidation_value_table.get_column_names()
        self._column_types = liquidation_value_table.get_column_types()
        self._primary_key = liquidation_value_table.get_primary_key()
        self._constraints = liquidation_value_table.get_constraints()

        self._key = liquidation_value_table.get_key()
        self._class = modelclass
