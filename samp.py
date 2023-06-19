import ctypes.wintypes
import pathlib
from winreg import (
    HKEY_CURRENT_USER,
    HKEY_LOCAL_MACHINE,
    OpenKey,
    QueryValueEx,
    REG_SZ,
)

GTASA_KEY = r'SOFTWARE\Rockstar Games\GTA San Andreas\Installation'
GTASA_EXE_SUBKEY = 'ExePath'
GTASA_EXE_NAME = 'gta_sa.exe'

SAMP_KEY = r'SOFTWARE\SAMP'
SAMP_EXE_SUBKEY = 'gta_sa_exe'
SAMP_NAME_SUBKEY = 'PlayerName'
SAMP_DLL_NAME = 'samp.dll'

CSIDL_PERSONAL = 5
SHGFP_TYPE_CURRENT = 0


def is_valid_gtasa_dir(gtasa_dir: pathlib.Path) -> bool:
    gtasa_exe_path = gtasa_dir / GTASA_EXE_NAME
    samp_dll_path = gtasa_dir / SAMP_DLL_NAME
    return gtasa_exe_path.exists() and samp_dll_path.exists()


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


def find_samp_dir() -> pathlib.Path | None:
    buffer = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    shell32 = ctypes.OleDLL('shell32')
    shell32.SHGetFolderPathW(
        None,
        CSIDL_PERSONAL,
        None,
        SHGFP_TYPE_CURRENT,
        buffer,
    )
    samp_dir = pathlib.Path(
        buffer.value,
        'GTA San Andreas User Files',
        'SAMP',
    )

    return samp_dir if samp_dir.exists() else None


def find_user_data() -> pathlib.Path | None:
    samp_dir = find_samp_dir()

    if not samp_dir:
        return

    user_data = samp_dir / 'USERDATA.DAT'
    return user_data if user_data.exists() else None
