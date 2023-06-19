from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView


class ServerList(RecycleView):
    pass


Builder.load_file('widgets/server_list.kv')
