# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/Client.ipynb (unless otherwise specified).

__all__ = ["Client", "DataBlob", "DataSource"]

# Cell

from typing import *
import types

import typer
import airt

from airt.constant import *

# Internal Cell


def _replace_env_var(s: str) -> str:
    return s.replace("AIRT_", "CAPTN_").replace("airt", "captn")


# Internal Cell


def _fix_doc_string(cls: Type):

    cls.__doc__ = _replace_env_var(cls.__doc__)  # type: ignore

    for i in dir(cls):

        attr = getattr(cls, i)

        if (attr) and (not i.startswith("_")):
            try:
                if attr.__class__ == types.MethodType:
                    attr.__func__.__doc__ = _replace_env_var(attr.__func__.__doc__)
                else:
                    attr.__doc__ = _replace_env_var(attr.__doc__)

            except:
                pass

            assert "AIRT_" not in attr.__doc__
            assert "airt" not in attr.__doc__


# Internal Cell


def _fix_cli_doc_string(app: typer.Typer, m_name: str):
    for c in app.registered_commands:
        name = c.callback.__name__.replace("-", "_")  # type: ignore

        getattr(getattr(airt.cli, m_name), name).__doc__ = _replace_env_var(
            getattr(getattr(airt.cli, m_name), name).__doc__
        )


# Internal Cell


def _set_global_env_vars(m: types.ModuleType):
    for v in dir(m):
        if not v.startswith("_"):
            setattr(m, v, _replace_env_var(getattr(m, v)))

            assert "AIRT_" not in getattr(m, v)


# Cell

_set_global_env_vars(airt.constant)

from airt.client import Client as _Client

Client = _Client

from airt.client import DataBlob as _DataBlob

DataBlob = _DataBlob

from airt.client import DataSource as _DataSource

DataSource = _DataSource

for cls in [Client, DataBlob, DataSource]:
    cls.__module__ = "captn.client"
    _fix_doc_string(cls)
