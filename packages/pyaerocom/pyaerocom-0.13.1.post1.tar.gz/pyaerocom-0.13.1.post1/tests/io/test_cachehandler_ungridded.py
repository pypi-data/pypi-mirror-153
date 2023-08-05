import os

import pytest

from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded

from ..conftest import data_unavail


@pytest.fixture(scope="module")
def cache_handler():
    return CacheHandlerUngridded()


def test_cache_dir(cache_handler):
    cd = cache_handler.cache_dir
    comps = cd.split(os.path.sep)
    assert comps[-2] == "_cache"
    assert comps[-3] == "MyPyaerocom"


@data_unavail
@pytest.mark.dependency
def test_write_custom(cache_handler, aeronetsunv3lev2_subset, tempdir):
    ch = cache_handler
    outfile = "test_manual_caching.pkl"
    ch.write(aeronetsunv3lev2_subset, var_or_file_name=outfile, cache_dir=tempdir)

    fp = os.path.join(tempdir, outfile)
    assert os.path.exists(fp)


@data_unavail
@pytest.mark.dependency(depends=["test_write_custom"])
def test_check_and_load_custom(cache_handler, aeronetsunv3lev2_subset, tempdir):
    ch = cache_handler

    filename = "test_manual_caching.pkl"
    ch.check_and_load(var_or_file_name=filename, cache_dir=tempdir)
    assert ch.loaded_data[filename].shape == aeronetsunv3lev2_subset.shape


@data_unavail
@pytest.mark.dependency
def test_write(cache_handler, aeronetsunv3lev2_subset, aeronet_sun_subset_reader):
    reader = aeronet_sun_subset_reader
    ch = cache_handler
    ch.reader = reader
    ch.write(aeronetsunv3lev2_subset, var_or_file_name="od550aer")

    assert os.path.exists(ch.file_path("od550aer"))


@data_unavail
@pytest.mark.dependency(depends=["test_write"])
def test_check_and_load(cache_handler, aeronetsunv3lev2_subset, aeronet_sun_subset_reader):
    ch = cache_handler

    ch.check_and_load(var_or_file_name="od550aer")
    subset = aeronetsunv3lev2_subset.extract_var("od550aer")
    assert "od550aer" in ch.loaded_data
    reloaded = ch.loaded_data["od550aer"]
    from pyaerocom import UngriddedData

    assert isinstance(reloaded, UngriddedData)
    assert reloaded.shape == subset.shape
