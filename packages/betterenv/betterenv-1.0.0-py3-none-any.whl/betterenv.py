"""
Better ENV - Custom Environment Library

Designed as a nice wrapper, inspired by how environmental variables work
in the linuxserver.io docker images.
"""

from os import environ as env
from pathlib import Path


def get(var, default=None):
    """
    Gets an environmental variable
    * First it tries FILE__VAR and gets the content of the file there
    * It returns the value of the environmental variable
    * Otherwise, it returns the default value
    """
    if f"FILE__{var}" in env:
        path = Path(env[f"FILE__{var}"])
        return path.read_text()

    if var in env:
        return env[var]

    return default


def keys():
    """Get a List of the environmental environmental variables"""
    return [f[6:] if f[:6] == "FILE__" else f for f in env.keys()]


def structured_keys(type):
    """
    Get the Structured Keys
    TYPE__SECTION__KEY=value will map to
    {
        "section":{
            "key":"value"
        }
    }
    """
    _env = keys()

    _keys = {
        e: get(f"{type}__{e}", "")
        for e in [e[len(type)+2:] for e in _env if e[:len(type)+2] == f"{type}__"]
    }

    out = {}

    for k, v in _keys.items():
        y = k.split("__")
        if y[0] not in out:
            out[y[0]] = dict()
        out[y[0]][y[1]] = v

    return out

