from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.strategy_optimal import StrategyOptimal


__all__ = ['StrategyOptimalTableCRUDer']


class StrategyOptimalTableCRUDer(TableCRUDerDefault):
    def __init__(self, strategy_optimal_table, db_connection, 
            modelclass=StrategyOptimal):
        self._db_connection = db_connection

        self._table_name = strategy_optimal_table.get_table_name()
        self._column_names = strategy_optimal_table.get_column_names()
        self._column_types = strategy_optimal_table.get_column_types()
        self._primary_key = strategy_optimal_table.get_primary_key()
        self._constraints = strategy_optimal_table.get_constraints()

        self._key = strategy_optimal_table.get_key()
        self._class = modelclass
