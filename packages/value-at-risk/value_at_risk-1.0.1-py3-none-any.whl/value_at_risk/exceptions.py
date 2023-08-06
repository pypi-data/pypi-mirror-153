class ValueAtRiskError(Exception):
    pass


class HistoricalVARMethodError(ValueAtRiskError):
    def __init__(self):
        super().__init__("No data kwargs given--only parametric VaR calculations method available")


class VARMethodsError(ValueAtRiskError):
    def __init__(self):
        super().__init__(
            "No data kwarg or mu and sigma kwargs specified--neither method of VaR calculations methods available")
