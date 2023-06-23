import ctypes.wintypes
import os
import pathlib
import typing
from winreg import (
    HKEY_CURRENT_USER,
    HKEY_LOCAL_MACHINE,
    OpenKey,
    QueryValueEx,
    REG_SZ,
)

import trio
import pywintypes
from win32com.shell import shell, shellcon

GTASA_KEY = r'SOFTWARE\Rockstar Games\GTA San Andreas\Installation'
GTASA_EXE_SUBKEY = 'ExePath'
GTASA_EXE_NAME = 'gta_sa.exe'

SAMP_KEY = r'SOFTWARE\SAMP'
SAMP_EXE_SUBKEY = 'gta_sa_exe'
SAMP_NAME_SUBKEY = 'PlayerName'
SAMP_DLL_NAME = 'samp.dll'


def is_valid_gtasa_dir(dir: pathlib.Path) -> bool:
    gtasa_exe_path = dir / GTASA_EXE_NAME
    return gtasa_exe_path.exists()


def is_valid_samp_dir(dir: pathlib.Path) -> bool:
    samp_dll_path = dir / SAMP_DLL_NAME
    return is_valid_gtasa_dir(dir) and samp_dll_path.exists()


def find_gtasa_dir() -> pathlib.Path | None:
    for key, sub_key, value_name in (
        (HKEY_CURRENT_USER, SAMP_KEY, SAMP_EXE_SUBKEY),
        (HKEY_CURRENT_USER, GTASA_KEY, GTASA_EXE_SUBKEY),
        (HKEY_LOCAL_MACHINE, GTASA_KEY, GTASA_EXE_SUBKEY),
    ):
        try:
            with OpenKey(key, sub_key) as handle:
                value, type = QueryValueEx(handle, value_name)
                assert type == REG_SZ
                gtasa_dir = pathlib.Path(value).parent

                if is_valid_gtasa_dir(gtasa_dir):
                    return gtasa_dir

        except FileNotFoundError:
            pass

    return None


def find_samp_data_dir() -> pathlib.Path | None:
    buffer = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    shell.SHGetFolderPathW(
        None,
        shellcon.CSIDL_PERSONAL,
        None,
        shellcon.SHGFP_TYPE_CURRENT,
        buffer,
    )
    samp_dir = pathlib.Path(
        buffer.value,
        'GTA San Andreas User Files',
        'SAMP',
    )

    return samp_dir if samp_dir.exists() else None


def find_samp_user_data() -> pathlib.Path | None:
    samp_dir = find_samp_data_dir()

    if not samp_dir:
        return None

    user_data = samp_dir / 'USERDATA.DAT'
    return user_data if user_data.exists() else None


async def open_folder_chooser_dialog(
    title: str,
    start_path: os.PathLike,
    parent_window: int | None = None,
    callback: typing.Callable[[int, int, int, typing.Any], int] | None = None,
    flags: int = shellcon.BIF_RETURNONLYFSDIRS,
) -> pathlib.Path | None:
    pidl, *_ = await trio.to_thread.run_sync(
        shell.SHBrowseForFolder,
        parent_window,
        start_path,
        title,
        flags,
        callback,
    )

    if not pidl:
        return None

    try:
        return shell.SHGetPathFromIDList(pidl).decode('utf8')

    except pywintypes.com_error:
        return None
