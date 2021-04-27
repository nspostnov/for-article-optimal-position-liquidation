from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.traded_volume_from_to import TradedVolumeFromTo


__all__ = ['TradedVolumeFromToTableCRUDer']


class TradedVolumeFromToTableCRUDer(TableCRUDerDefault):
    def __init__(self, tradedvolumefromtotable, db_connection):
        self._db_connection = db_connection

        self._table_name = tradedvolumefromtotable.get_table_name()
        self._column_names = tradedvolumefromtotable.get_column_names()
        self._column_types = tradedvolumefromtotable.get_column_types()
        self._primary_key = tradedvolumefromtotable.get_primary_key()
        self._constraints = tradedvolumefromtotable.get_constraints()

        self._key = tradedvolumefromtotable.get_key()
        self._class = TradedVolumeFromTo
