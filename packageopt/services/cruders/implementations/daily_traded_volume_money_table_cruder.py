from ..abstract_base_classes.table_cruder_default import TableCRUDerDefault
from ....models.daily_traded_volume_money import DailyTradedVolumeMoney


__all__ = ['DailyTradedVolumeMoneyTableCRUDer']


class DailyTradedVolumeMoneyTableCRUDer(TableCRUDerDefault):
    def __init__(self, daily_traded_volume_money_table, db_connection):
        self._db_connection = db_connection

        self._table_name = daily_traded_volume_money_table.get_table_name()
        self._column_names = daily_traded_volume_money_table.get_column_names()
        self._column_types = daily_traded_volume_money_table.get_column_types()
        self._primary_key = daily_traded_volume_money_table.get_primary_key()
        self._constraints = daily_traded_volume_money_table.get_constraints()

        self._key = daily_traded_volume_money_table.get_key()
        self._class = DailyTradedVolumeMoney
