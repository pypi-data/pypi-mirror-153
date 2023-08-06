import logging

import pytest

from snelstart import SnelStart


@pytest.mark.parametrize("module", ["grootboekmutaties", "kostenplaatsen", "dagboeken", "grootboeken", "relaties"])
def test_request_data(module):
    """General test to check if functionality works"""
    logging.info(f"start test request data {module}")
    if module == "grootboekmutaties":
        years = [2022]
        SnelStart().request_data(module=module, years=years)
    else:
        SnelStart().request_data(module=module)
    logging.info(f"test {module} finished")


@pytest.mark.parametrize("module,normalise", [("dagboeken", False), ("dagboeken", False), ("grootboeken", True)])
def test_get_data(module, normalise):
    """General test to check if get data works"""
    logging.info(f"start test get data {module}...")
    df = SnelStart().request_data(module=module, dataframe=True)
    logging.info(f"test {module} finished! {df.shape}")


def test_allowed_modules():
    with pytest.raises(ValueError):
        SnelStart().request_data(module="does not exist")
