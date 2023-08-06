import pandas as pd

from typing import Union

from value_at_risk.support import ParametricValueAtRisk, HistoricalValueAtRisk


class ValueAtRisk(ParametricValueAtRisk, HistoricalValueAtRisk):
    """
    Calculate Value at Risk through historical and parametric methods
    """

    def __init__(self, data: Union[pd.Series, str] = None,
                 mu: Union[int, float] = None,
                 sigma: Union[int, float] = None,
                 mkt_val: Union[int, float] = None,
                 alpha: Union[int, float] = .01,
                 smooth_factor: Union[int, float] = 1,
                 pct: bool = True):
        """
        :param data: pd.Series, str -> n x 1 dataframe with price data and datetime as an index
        :param mu: int, float -> Given expected mean of portfolio returns to calculate the VaR using
        the parametric VaR method
        :param sigma: int, float -> Given expected standard deviation of portfolio returns to calculate the VaR using
        the parametric VaR method
        :param mkt_val: int, float -> The specified notional value of the portfolio (Default is 1)
        :param alpha: float -> Confidence level which translates to the return threshold above the inverse CDF assuming
        our return distribution is normal or Gaussian (Default cutoff at .01)
        :param smooth_factor: float -> Alpha or smoothing factor to exponentially adjust weights in moving frame.
        Note that if the class's sigma and mean were given then the smoothing factor will not be available
        (default is 1)
        :param pct: bool -> Set to False if notional value of asset is to be returned  (default is True)

        :return NoneType (Sets historical_var and parametric_var attrs)
        """

        self.alpha, self.smooth_factor, self.pct = alpha, smooth_factor, pct

        ParametricValueAtRisk.__init__(self, data=data, mu=mu, sigma=sigma, mkt_val=mkt_val)
        HistoricalValueAtRisk.__init__(self, data=data, mu=mu, sigma=sigma, mkt_val=mkt_val)

    @property
    def historical_var(self):
        return self.calculate_historical_var(alpha=self.alpha, pct=self.pct)

    @property
    def parametric_var(self):
        return self.calculate_parametric_var(alpha=self.alpha, smooth_factor=self.smooth_factor, pct=self.pct)


class VAR(ValueAtRisk):
    """
    Calculate Value at Risk through historical and parametric methods
    """

    def __init__(self, data: Union[pd.Series, str] = None,
                 mu: Union[int, float] = None,
                 sigma: Union[int, float] = None,
                 mkt_val: Union[int, float] = None,
                 alpha: Union[int, float] = .01,
                 smooth_factor: Union[int, float] = 1,
                 pct: bool = True):
        """
        :param data: pd.Series, str -> n x 1 dataframe with price data and datetime as an index
        :param mu: int, float -> Given expected mean of portfolio returns to calculate the VaR using
        the parametric VaR method
        :param sigma: int, float -> Given expected standard deviation of portfolio returns to calculate the VaR using
        the parametric VaR method
        :param mkt_val: int, float -> The specified notional value of the portfolio (Default is 1)
        :param alpha: float -> Confidence level which translates to the return threshold above the inverse CDF assuming
        our return distribution is normal or Gaussian (Default cutoff at .01)
        :param smooth_factor: float -> Alpha or smoothing factor to exponentially adjust weights in moving frame.
        Note that if the class's sigma and mean were given then the smoothing factor will not be available
        (default is 1)
        :param pct: bool -> Set to False if notional value of asset is to be returned  (default is True)

        :return NoneType (Sets historical_var and parametric_var attrs)
        """

        ValueAtRisk.__init__(**locals())
