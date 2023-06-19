import os
import sys

from kivy.resources import resource_add_path

if not sys.stderr:
    # https://github.com/pyinstaller/pyinstaller/issues/3503
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

if getattr(sys, 'frozen', False):
    resource_add_path(sys._MEIPASS)
