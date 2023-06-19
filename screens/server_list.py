from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from widgets.server_list import ServerList  # noqa: F401


class ServerListScreen(Screen):
    pass


Builder.load_file('screens/server_list.kv')
