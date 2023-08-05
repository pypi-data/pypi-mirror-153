from pathlib import Path
from textwrap import dedent
from typing import List

from pytest import mark, param, raises

from pyaerocom.aeroval.aux_io_helpers import ReadAuxHandler, check_aux_info


def test_ReadAuxHandler(tmp_path: Path):
    path = tmp_path / "dummy.py"
    assert not path.exists()

    dummy = """
    def success() -> bool:
        return True
    
    FUNS = [success]
    """
    path.write_text(dedent(dummy))

    aux = ReadAuxHandler(str(path))
    success = aux.import_module().success
    assert success()

    funcs = aux.import_all()
    assert funcs[0] is success


def test_ReadAuxHandler_empty(tmp_path: Path):
    path = tmp_path / "empty.py"
    assert not path.exists()

    path.write_text("")

    with raises(Exception) as e:
        ReadAuxHandler(str(path)).import_all()

    assert str(e.value) == f"module '{path.stem}' has no attribute 'FUNS'"


@mark.parametrize(
    "fun,vars_required,funcs",
    [
        param(lambda: True, ["first"], {}, id="func as first arg"),
        param("func", ["last"], {"func": lambda: True}, id="func as last arg"),
    ],
)
def test_check_aux_info(fun, vars_required: List[str], funcs: dict):
    aux = check_aux_info(fun, vars_required, funcs)
    assert aux["fun"] is funcs.get(fun, fun)
    assert aux["vars_required"] == vars_required


@mark.parametrize(
    "fun,vars_required,funcs,error",
    [
        param(None, [], {}, "failed to retrieve aux func", id="no func"),
        param(
            None,
            [42],
            {},
            "not all items are str type in input list [42]",
            id="bad type vars_required",
        ),
    ],
)
def test_check_aux_info_error(fun, vars_required: List[str], funcs: dict, error: str):
    with raises(ValueError) as e:
        check_aux_info(fun, vars_required, funcs)

    assert str(e.value) == error
