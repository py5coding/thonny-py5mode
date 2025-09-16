'''thonny-py5mode backend
   interacts with thonny-py5mode frontend (thonny-py5mode > __init__.py)'''

from os import environ as env
from sys import path

from typing import Optional, TypedDict, TypeAlias

from thonny.common import InlineCommand, InlineResponse, CompletionInfo
from thonny.plugins.cpython_backend import MainCPythonBackend
from thonny import jedi_utils, get_sys_path_directory_containg_plugins

path.append( get_sys_path_directory_containg_plugins() )

AutoComplete: TypeAlias = dict[str, list[CompletionInfo] | str | None]

class Command(TypedDict):
    source: str
    row: int
    column: int
    filename: str
    sys_path: Optional[list[str]]

def patched_editor_autocomplete(self: MainCPythonBackend, cmd: Command) -> AutoComplete:
    '''Add py5 to autocompletion'''

    prefix = 'from py5 import *\n'

    cmd['source'] = prefix + cmd['source']
    cmd['row'] += 1

    result: Command = dict(
        source=cmd.source,
        row=cmd.row,
        column=cmd.column,
        filename=cmd.filename
    )

    result['completions'] = jedi_utils.get_script_completions(
        **result, sys_path=[get_sys_path_directory_containg_plugins()])

    result['row'] -= 1
    result['source'] = result['source'][len(prefix):]

    return result


def load_plugin() -> None:
    '''Every Thonny plug-in uses this function to load'''
    if env.get('PY5_IMPORTED_MODE', 'False').lower() == 'false': return

    # Note that _cmd_editor_autocomplete() is not a public API
    # May need to treat different Thonny versions differently:
    # https://groups.Google.com/g/thonny/c/wWCeXWpKy8c
    c_e_a = MainCPythonBackend._cmd_editor_autocomplete
    setattr(MainCPythonBackend, '_original_editor_autocomplete', c_e_a)
    # MainCPythonBackend._original_editor_autocomplete = c_e_a
    MainCPythonBackend._cmd_editor_autocomplete = patched_editor_autocomplete
