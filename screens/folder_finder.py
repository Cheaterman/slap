import pathlib

import pywintypes
import win32api
import win32gui
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen
from win32com.shell import shell, shellcon

from samp import (
    find_gtasa_dir,
    is_valid_gtasa_dir,
    is_valid_samp_dir,
    open_folder_chooser_dialog,
)


class FolderFinder(Screen):
    __events__ = ['on_folder_found']

    folder_path = StringProperty()
    is_valid_gtasa_dir = BooleanProperty(False)
    is_valid_samp_dir = BooleanProperty(False)

    def open_finder_dialog(self):
        self.nursery.start_soon(self.find_gtasa_folder)

    async def find_gtasa_folder(self) -> None:
        gtasa_dir = find_gtasa_dir()

        if gtasa_dir:
            Logger.info(
                'FolderFinder: Valid GTA:SA dir found at "%s"',
                gtasa_dir,
            )
            self.dispatch('on_folder_found', gtasa_dir)
            return

        gtasa_dir = await open_folder_chooser_dialog(
            'Please locate your GTA: San Andreas installation.',
            gtasa_dir,
            self.hwnd,
            self.samp_dialog_callback,
        )

        if gtasa_dir:
            self.dispatch('on_folder_found', pathlib.Path(gtasa_dir))

    def samp_dialog_callback(self, hwnd, event, param, data):
        if event == shellcon.BFFM_INITIALIZED:
            win32gui.SetWindowText(hwnd, 'GTA: San Andreas installation')

        elif event == shellcon.BFFM_SELCHANGED:
            pidl = shell.AddressAsPIDL(param)
            param_value = None

            try:
                param_value = shell.SHGetPathFromIDList(pidl)
            except pywintypes.com_error:
                pass

            enable_ok = is_valid_gtasa_dir(
                pathlib.Path(param_value.decode('utf8'))
            ) if param_value else False

            win32api.SendMessage(
                hwnd,
                shellcon.BFFM_ENABLEOK,
                None,
                enable_ok,
            )

    def on_folder_found(self, folder: pathlib.Path):
        self.folder_path = str(folder)
        self.is_valid_gtasa_dir = is_valid_gtasa_dir(folder)
        self.is_valid_samp_dir = is_valid_samp_dir(folder)


Builder.load_file('screens/folder_finder.kv')
