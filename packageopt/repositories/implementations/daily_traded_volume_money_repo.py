from ..abstract_base_classes import RepoABC
from ...models.daily_traded_volume_money import DailyTradedVolumeMoney


__all__ = ['DailyTradedVolumeMoneyRepo']


class DailyTradedVolumeMoneyRepo(RepoABC):
    def __init__(self, dailytradedvolumemoneytablecruder):
        self._dailytradedvolumemoneytablecruder = dailytradedvolumemoneytablecruder

    def get(self, key):
        dailytradedvolumemoney = DailyTradedVolumeMoney()
        dailytradedvolumemoney.set_key(key)

        return self._dailytradedvolumemoneytablecruder.get(dailytradedvolumemoney)

    def set(self, dailytradedvolumemoney):
        self._dailytradedvolumemoneytablecruder.update(dailytradedvolumemoney)
