import pandas as pd
import numpy as np

from typing import Union, NoReturn
from scipy.stats import norm

from value_at_risk.exceptions import VARMethodsError, HistoricalVARMethodError


class ValueAtRiskBase:

    def __init__(self, data: Union[pd.Series, str] = None,
                 mu: Union[int, float] = None,
                 sigma: Union[int, float] = None,
                 mkt_val: Union[int, float] = None):

        self.trading_days = 252

        if isinstance(mkt_val, (int, float)):
            self.mkt_val = mkt_val
        else:
            self.mkt_val = 1

        if not isinstance(data, pd.Series):
            self._mu = mu
            self._sigma = sigma
        else:
            self._returns = data.sort_index().reset_index(drop=True).pct_change().dropna()

    @property
    def returns(self) -> Union[pd.Series, NoReturn]:
        if hasattr(self, '_returns'):
            return self._returns
        else:
            if not isinstance(self._mu, (int, float)) or not isinstance(self._sigma, (int, float)):
                return VARMethodsError()
            else:
                return HistoricalVARMethodError()

    @property
    def roll_len(self) -> int:
        if hasattr(self, '_returns'):
            return len(self.returns) if len(self.returns) < self.trading_days else self.trading_days
        else:
            return 1

    @property
    def ann_factor(self) -> Union[float, int]:
        return np.sqrt(self.trading_days / self.roll_len)

    @property
    def mu(self) -> Union[float, int]:
        if hasattr(self, '_mu'):
            return self._mu
        else:
            return self.returns.rolling(window=self.roll_len).mean().dropna().iloc[-1]

    @property
    def sigma(self) -> Union[float, int]:
        if hasattr(self, '_sigma'):
            return self._sigma
        else:
            return self.returns.rolling(window=self.roll_len).std().dropna().iloc[-1]


class ParametricValueAtRisk(ValueAtRiskBase):

    def __init__(self, data: Union[pd.Series, str] = None,
                 mu: Union[int, float] = None,
                 sigma: Union[int, float] = None,
                 mkt_val: Union[int, float] = None):

        ValueAtRiskBase.__init__(self, data=data, mu=mu, sigma=sigma, mkt_val=mkt_val)

    def calculate_parametric_var(self, alpha: float = .01, smooth_factor: float = 1.0, pct: bool = True) -> Union[
        float, int, VARMethodsError]:
        """
        Calculate the value at risk (VaR) from
        :param alpha: float -> Confidence level which translates to the return threshold above the inverse CDF assuming
        our return distribution is normal or Gaussian (Default cutoff at .01)
        :param smooth_factor: float -> Alpha or smoothing factor to exponentially adjust weights in moving frame.
        (Default is 1)
        :param pct: bool -> Set to False if notional value of asset is to be returned  (default is True)

        :return: float, int -> Notional value of asset at risk (VaR) or percentage based if param percent is True
        """

        if not isinstance(self.returns, pd.Series) and (
                not isinstance(self._mu, (int, float)) or not isinstance(self._sigma, (int, float))):
            return VARMethodsError()

        if smooth_factor == 1 or not isinstance(self.returns, type(None)):
            sigma = self.sigma
        else:
            sigma = self.returns.ewm(alpha=smooth_factor, min_periods=self.roll_len).std().iloc[
                        -1] * self.ann_factor

        var = sigma * norm.ppf(1 - alpha)

        if pct:
            return var * 100
        else:
            return var * self.mkt_val


class HistoricalValueAtRisk(ValueAtRiskBase):

    def __init__(self, data: Union[pd.Series, str] = None,
                 mu: Union[int, float] = None,
                 sigma: Union[int, float] = None,
                 mkt_val: Union[int, float] = None):

        ValueAtRiskBase.__init__(self, data=data, mu=mu, sigma=sigma, mkt_val=mkt_val)

    def calculate_historical_var(self, alpha: float = .01, iter_: int = 1000, pct: bool = True) -> Union[
        float, int, HistoricalVARMethodError, VARMethodsError]:
        """
        Calculate the value at risk (VaR) from random samples (default sample number set to 10000) of historical returns
        :param alpha: float -> Confidence level which translates to the quantile of returns corresponding to the highest
        available datapoint within the interval of data points that the specified quantile lies between
        :param iter_: int -> Number of iterations to draw random samples from historical data (default at 1000)
        :param pct: bool -> Set to False if notional value of asset is to be returned (default is True)

        :return: float, int -> Notional value of asset at risk (VaR) or percentage based if param percent is True
        """

        returns = self.returns

        if not isinstance(returns, pd.Series) and (
                not isinstance(self._mu, (int, float)) or not isinstance(self._sigma, (int, float))):
            return VARMethodsError()
        elif not isinstance(returns, pd.Series):
            return HistoricalVARMethodError()

        func_vec = np.vectorize(
            lambda: np.array([np.random.choice(returns, self.trading_days) for _ in range(iter_)]),
            otypes=[int, float])

        simulations = np.apply_along_axis(lambda x: np.quantile(x, 1 - alpha, interpolation='higher'), 0, func_vec())

        var = np.mean(simulations)

        if pct:
            return var * 100
        else:
            return var * self.mkt_val
