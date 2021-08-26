# -*- coding: utf-8 -*-
"""
Path handling
"""

import pathlib
from pathlib import Path
import simplejson as json

customdir = Path.home() / ".komoog"

def _prepare():

    customdir.mkdir(exist_ok=True)
    cred_file = customdir / "komoot.json"
    if not cred_file.exists():
        data = {
                    "email" : "",
                    "password" : "",
                    "clientid" : "",
               }
        with open(cred_file,'w') as f:
            credentials = json.dump(data,f)


def get_credentials():
    """
    Returns credentials for komoot login in structure

    .. code:: python

        {
            "email" : "",
            "password" : "",
            "clientid" : ""
        }

    from the file ``~/.komoog/komoot.json``
    """

    _prepare()

    cred_file = customdir / "komoot.json"

    with open(cred_file,'r') as f:
        credentials = json.load(f)

    assert(all([ k in credentials.keys() for k in ["email", "password", "clientid"]]))
    assert(not any([ credentials[k] == '' for k in ["email", "password", "clientid"]]))

    return credentials

if __name__ == "__main__":
    get_credentials()
