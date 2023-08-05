from __future__ import annotations

import pytest

from pyaerocom import Colocator, GriddedData, UngriddedData
from pyaerocom.aeroval import EvalSetup
from pyaerocom.aeroval._processing_base import DataImporter, HasColocator, HasConfig
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.exceptions import EntryNotAvailable

from .cfg_test_exp1 import CFG


@pytest.fixture(scope="module")
def setup() -> EvalSetup:
    obs_cfg = dict(
        obs1=dict(obs_id="obs1", obs_vars=["od550aer"], obs_vert_type="Column"),
        obs2=dict(obs_id="obs2", obs_vars=["od550aer"], obs_vert_type="Column", diurnal_only=True),
    )
    return EvalSetup("bla", "blub", obs_cfg=obs_cfg)


@pytest.fixture(scope="module")
def config(setup: EvalSetup) -> HasConfig:
    return HasConfig(setup)


def test_HasConfig_setup(config: HasConfig):
    assert isinstance(config.cfg, EvalSetup)
    assert isinstance(config.exp_output, ExperimentOutput)


def test_HasConfig_raise_exceptions(config: HasConfig):
    assert config.raise_exceptions == False


def test_HasConfig_reanalyse_existing(config: HasConfig):
    assert config.reanalyse_existing == True


@pytest.fixture(scope="module")
def collocator(setup: EvalSetup) -> HasColocator:
    return HasColocator(setup)


def test_HasColocator_get_diurnal_only(collocator: HasColocator):
    assert collocator._get_diurnal_only("obs1") == False
    assert collocator._get_diurnal_only("obs2") == True


@pytest.mark.parametrize("obs_name", [None, "obs1", "obs2"])
def test_HasColocator_get_colocator(collocator: HasColocator, obs_name: str | None):
    col = collocator.get_colocator(obs_name=obs_name)
    assert isinstance(col, Colocator)


def test_HasColocator_get_colocator_error(collocator: HasColocator):
    with pytest.raises(EntryNotAvailable) as e:
        collocator.get_colocator(model_name="mod2")
    assert str(e.value) == "'no such entry mod2'"


@pytest.fixture(scope="module")
def importer() -> DataImporter:
    setup = EvalSetup(**CFG)
    return DataImporter(setup)


def test_DataImporter_read_model_data(importer: DataImporter):
    data = importer.read_model_data("TM5-AP3-CTRL", "od550aer")
    assert isinstance(data, GriddedData)


def test_DataImporter_read_ungridded_obsdata(importer: DataImporter):
    data = importer.read_ungridded_obsdata("AERONET-Sun", "od550aer")
    assert isinstance(data, UngriddedData)
