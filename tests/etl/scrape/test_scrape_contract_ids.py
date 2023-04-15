import httpx
import pytest

from mndot_bid_api.etl.scrape import scrape_contract_ids

def test_scrape_contract_ids():
    contract_ids = scrape_contract_ids(2020)
    assert len(contract_ids) == 172

    with pytest.raises(httpx.HTTPStatusError):
        scrape_contract_ids(999)