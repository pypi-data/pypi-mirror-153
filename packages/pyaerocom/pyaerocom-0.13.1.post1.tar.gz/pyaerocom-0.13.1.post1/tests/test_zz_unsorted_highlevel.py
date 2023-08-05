import numpy as np
from numpy.testing import assert_allclose

from .conftest import data_unavail


@data_unavail
def test_meta_blocks_ungridded(aeronetsunv3lev2_subset):
    assert len(aeronetsunv3lev2_subset.metadata) == 22
    assert len(aeronetsunv3lev2_subset.unique_station_names) == 22

    names = [
        "AAOT",
        "ARIAKE_TOWER",
        "Agoufou",
        "Alta_Floresta",
        "American_Samoa",
        "Amsterdam_Island",
        "Anmyon",
        "Avignon",
        "Azores",
        "BORDEAUX",
        "Barbados",
        "Blyth_NOAH",
        "La_Paz",
        "Mauna_Loa",
        "Tahiti",
        "Taihu",
        "Taipei_CWB",
        "Tamanrasset_INM",
        "The_Hague",
        "Thessaloniki",
        "Thornton_C-power",
        "Trelew",
    ]
    assert aeronetsunv3lev2_subset.unique_station_names == names


@data_unavail
def test_od550aer_meanval_stats(aeronetsunv3lev2_subset):
    no_odcount = 0
    mean_vals = []
    std_vals = []
    for stat in aeronetsunv3lev2_subset.to_station_data_all()["stats"]:
        if not "od550aer" in stat:
            no_odcount += 1
            continue
        td = stat.od550aer[:100]
        mean = np.mean(td)
        if np.isnan(mean):
            no_odcount += 1
            continue
        mean_vals.append(mean)
        std_vals.append(np.std(td))
    assert no_odcount == 4
    should_be = [0.2097, 0.1397]
    assert_allclose(actual=[np.mean(mean_vals), np.mean(std_vals)], desired=should_be, atol=1e-2)


@data_unavail
def test_ang4487aer_meanval_stats(aeronetsunv3lev2_subset):
    no_odcount = 0
    mean_vals = []
    std_vals = []
    for stat in aeronetsunv3lev2_subset.to_station_data_all()["stats"]:
        if not "ang4487aer" in stat:
            no_odcount += 1
            continue
        td = stat.ang4487aer[:100]
        mean = np.mean(td)
        if np.isnan(mean):
            no_odcount += 1
            continue
        mean_vals.append(mean)
        std_vals.append(np.std(td))
    assert no_odcount == 0
    got = [np.mean(mean_vals), np.mean(std_vals)]
    should_be = [0.9196, 0.325]
    assert_allclose(actual=got, desired=should_be, atol=1e-2)
