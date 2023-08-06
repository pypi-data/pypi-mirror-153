# noqa: D100
from typing import List

import pandas as pd

from bambooapi_client.openapi.apis import PortfoliosApi as _PortfoliosApi
from bambooapi_client.openapi.models import PortfolioMarket, PortfolioSite


class PortfoliosApi(object):
    """Implementation for '/v1/portfolios endpoints."""

    def __init__(self, bambooapi_client):
        self._bambooapi_client = bambooapi_client
        self._api_instance = _PortfoliosApi(bambooapi_client.api_client)

    def list_portfolios_markets(
        self,
        portfolio_id: int,
    ) -> List[PortfolioMarket]:
        """List all markets of a portfolio."""
        return self._api_instance.list_portfolios_markets(portfolio_id)

    def list_portfolios_sites(self, portfolio_id: int) -> List[PortfolioSite]:
        """List all sites of a portfolio."""
        return self._api_instance.list_portfolios_sites(portfolio_id)

    def read_portfolio_energy_market_operations(
        self,
        portfolio_id: int,
        market_id: int,
    ) -> pd.DataFrame:
        """Get energy market operations of a portfolio and market."""
        response = self._api_instance.read_portfolio_energy_market_operations(
            portfolio_id=portfolio_id,
            market_id=market_id,
        )
        if response:
            return pd.DataFrame.from_records(
                [row.to_dict() for row in response],
                index='time',
            )
        else:
            return pd.DataFrame()

    def update_portfolio_energy_market_operations(
        self,
        portfolio_id: int,
        market_id: int,
        data_frame: pd.DataFrame,
    ):
        """Update portfolio operations."""
        datapoints = data_frame.reset_index().to_dict(orient='records')
        self._api_instance.update_portfolio_energy_market_operations(
            portfolio_id=portfolio_id,
            market_id=market_id,
            energy_market_operations=datapoints,
        )

    def read_portfolio_flexibility_market_operations(
        self,
        portfolio_id: int,
        market_id: int,
    ) -> pd.DataFrame:
        """Get flexibility market operations of a portfolio and market."""
        response = self._api_instance.read_portfolio_flexibility_market_operations(  # noqa: E501
            portfolio_id=portfolio_id,
            market_id=market_id,
        )
        if response:
            return pd.DataFrame.from_records(
                [row.to_dict() for row in response],
                index='time',
            )
        else:
            return pd.DataFrame()

    def update_portfolio_flexibility_market_operations(
        self,
        portfolio_id: int,
        market_id: int,
        data_frame: pd.DataFrame,
    ):
        """Update portfolio operations."""
        datapoints = data_frame.reset_index().to_dict(orient='records')
        self._api_instance.update_portfolio_flexibility_market_operations(
            portfolio_id=portfolio_id,
            market_id=market_id,
            flexibility_market_operations=datapoints,
        )
