import sys

from kivy.resources import resource_add_path

if getattr(sys, 'frozen', False):
    resource_add_path(sys._MEIPASS)
