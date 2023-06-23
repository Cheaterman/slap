import config  # noqa: F401

import trio
from kivy.app import App

import screens  # noqa: F401
import widgets  # noqa: F401
from translation import TranslatedApp


class Slap(
    TranslatedApp,
    App,
):
    async def async_run(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery
            await super().async_run('trio')
            nursery.cancel_scope.cancel()

    def load_kv(self, filename):
        from kivy.core.window import Window
        self.hwnd = Window.get_window_info().window
        return super().load_kv(filename)

    def build(self):
        self.icon = 'assets/icon.png'


if __name__ == '__main__':
    app = Slap()
    trio.run(app.async_run)
