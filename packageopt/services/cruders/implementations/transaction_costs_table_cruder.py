from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.transaction_costs import TransactionCosts


__all__ = ['TransactionCostsTableCRUDer']


class TransactionCostsTableCRUDer(TableCRUDerDefault):
    def __init__(self, transaction_costs_table, db_connection, 
            modelclass=TransactionCosts):
        self._db_connection = db_connection

        self._table_name = transaction_costs_table.get_table_name()
        self._column_names = transaction_costs_table.get_column_names()
        self._column_types = transaction_costs_table.get_column_types()
        self._primary_key = transaction_costs_table.get_primary_key()
        self._constraints = transaction_costs_table.get_constraints()

        self._key = transaction_costs_table.get_key()
        self._class = modelclass 
